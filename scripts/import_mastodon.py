#!/usr/bin/env python3
"""Import Lee's public Mastodon posts into the microblog.

Each new post becomes content/microblog/<year>/<YYYY-MM-DDTHH-MM>.md, with any
images and videos saved under static/img/mastodon/. Posts already imported are
recognised by the `mastodon_id` in their front matter, so it is safe to run
this as often as you like.

What gets imported: public and unlisted posts, including replies to yourself
(threads). Skipped: boosts, replies to other people, followers-only and direct
posts, and anything tagged #nosite.

    scripts/import_mastodon.py --since 2026-10-21
    scripts/import_mastodon.py --since 2026-01-01 --dry-run
"""

import argparse
import html
import json
import mimetypes
import os
import re
import sys
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CONTENT = ROOT / "content" / "microblog"
MEDIA = ROOT / "static" / "img" / "mastodon"
OPT_OUT_TAG = "nosite"
USER_AGENT = "leeturner.me microblog importer (+https://leeturner.me)"


def get(url):
    request = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(request, timeout=30) as response:
        return response.read()


def get_json(url):
    return json.loads(get(url))


def fetch_statuses(instance, account_id, since):
    """Yield the account's statuses newest first, stopping at `since`."""
    max_id = None
    while True:
        params = {"limit": 40, "exclude_reblogs": "true"}
        if max_id:
            params["max_id"] = max_id
        url = f"https://{instance}/api/v1/accounts/{account_id}/statuses?{urllib.parse.urlencode(params)}"
        page = get_json(url)
        if not page:
            return
        for status in page:
            if parse_date(status["created_at"]) < since:
                return
            yield status
        max_id = page[-1]["id"]


def parse_date(value):
    return datetime.fromisoformat(value.replace("Z", "+00:00")).astimezone(timezone.utc)


class MastodonHTML(HTMLParser):
    """Turn Mastodon's status HTML into the plain Markdown the microblog uses.

    Hashtags become plain #tags, links become bare URLs (Hugo linkifies them),
    and mentions become Markdown links to the person's profile.
    """

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.out = []
        self.link = None  # (href, classes, text parts) while inside <a>
        self.hidden = 0  # depth inside Mastodon's "invisible" spans

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == "br":
            self.out.append("\\\n")  # Markdown hard line break
        elif tag == "p" and self.out:
            self.out.append("\n\n")
        elif tag == "a":
            self.link = (attrs.get("href", ""), attrs.get("class", "") or "", [])
        elif tag == "span" and "invisible" in (attrs.get("class") or "").split():
            self.hidden += 1
        elif tag == "span" and self.hidden:
            self.hidden += 1

    def handle_endtag(self, tag):
        if tag == "span" and self.hidden:
            self.hidden -= 1
        elif tag == "a" and self.link:
            href, classes, parts = self.link
            text = "".join(parts).strip()
            self.link = None
            classes = classes.split()
            if "hashtag" in classes:
                self.out.append(escape(text))
            elif "mention" in classes:
                self.out.append(f"[{escape(text)}]({href})")
            elif text.startswith(("http", "www.")) or text.rstrip("…") in href:
                self.out.append(href)
            else:
                self.out.append(f"[{escape(text)}]({href})")

    def handle_data(self, data):
        if self.link:
            # Mastodon hides part of long URLs in invisible spans; keep the text
            # for matching but always print the real href.
            self.link[2].append(data)
        elif not self.hidden:
            self.out.append(escape(data))

    def markdown(self):
        return "".join(self.out).strip()


def escape(text):
    return re.sub(r"([\\`*_\[\]<>])", r"\\\1", text)


def to_markdown(content):
    parser = MastodonHTML()
    parser.feed(content)
    parser.close()
    return parser.markdown()


def known_ids():
    ids = set()
    for path in CONTENT.rglob("*.md"):
        with path.open(encoding="utf-8") as f:
            for number, line in enumerate(f):
                if line.startswith("mastodon_id:"):
                    ids.add(line.split(":", 1)[1].strip().strip('"'))
                    break
                if number > 0 and line.strip() == "---":  # end of front matter
                    break
    return ids


def wanted(status, account_id):
    if status.get("reblog"):
        return False
    if status["visibility"] not in ("public", "unlisted"):
        return False
    reply_to = status.get("in_reply_to_account_id")
    if reply_to and reply_to != account_id:
        return False
    tags = {t["name"].lower() for t in status.get("tags", [])}
    return OPT_OUT_TAG not in tags


def media_markdown(status, dry_run):
    lines = []
    for index, media in enumerate(status.get("media_attachments", []), start=1):
        url = media.get("url")
        if not url or media["type"] not in ("image", "gifv", "video"):
            continue
        ext = Path(urllib.parse.urlparse(url).path).suffix or mimetypes.guess_extension(media["type"]) or ""
        name = f"{status['id']}-{index}{ext}"
        if not dry_run:
            MEDIA.mkdir(parents=True, exist_ok=True)
            (MEDIA / name).write_bytes(get(url))
        src = f"/img/mastodon/{name}"
        alt = (media.get("description") or "").replace("\n", " ").strip()
        if media["type"] == "image":
            lines.append(f"![{escape(alt)}]({src})")
        else:
            loop = " autoplay loop muted playsinline" if media["type"] == "gifv" else " controls"
            label = f' aria-label="{html.escape(alt)}"' if alt else ""
            lines.append(f'<video src="{src}"{loop}{label}></video>')
    return lines


def post_path(created):
    stamp = created.strftime("%Y-%m-%dT%H-%M")
    folder = CONTENT / created.strftime("%Y")
    path = folder / f"{stamp}.md"
    n = 2
    while path.exists():
        path = folder / f"{stamp}-{n}.md"
        n += 1
    return path


def render(status, path, body):
    created = parse_date(status["created_at"])
    front_matter = [
        "---",
        f"title: {path.stem}",
        f"date: {created.strftime('%Y-%m-%dT%H:%M:%SZ')}",
        "author: Lee Turner",
        "showtoc: false",
        "comments: true",
        f'mastodon_id: "{status["id"]}"',
        f"mastodon_url: {status['url']}",
        "---",
    ]
    return "\n".join(front_matter) + "\n\n" + body + "\n"


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--account", default=os.environ.get("MASTODON_ACCOUNT", "leeturner@hachyderm.io"))
    parser.add_argument("--since", required=True, help="only import posts on or after this date (YYYY-MM-DD)")
    parser.add_argument("--dry-run", action="store_true", help="print what would be imported without writing files")
    args = parser.parse_args()

    username, instance = args.account.lstrip("@").split("@")
    since = datetime.fromisoformat(args.since).replace(tzinfo=timezone.utc)
    account_id = get_json(f"https://{instance}/api/v1/accounts/lookup?acct={username}")["id"]
    seen = known_ids()

    imported = []
    # Oldest first, so a thread's posts get filenames in order.
    for status in reversed(list(fetch_statuses(instance, account_id, since))):
        if status["id"] in seen or not wanted(status, account_id):
            continue
        parts = [to_markdown(status["content"])] + media_markdown(status, args.dry_run)
        body = "\n\n".join(p for p in parts if p)
        if not body:
            continue
        path = post_path(parse_date(status["created_at"]))
        if args.dry_run:
            print(f"--- would write {path.relative_to(ROOT)}\n{render(status, path, body)}")
        else:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(render(status, path, body), encoding="utf-8")
        imported.append(path)

    print(f"{'Would import' if args.dry_run else 'Imported'} {len(imported)} post(s) from {args.account}", file=sys.stderr)
    if "GITHUB_OUTPUT" in os.environ:
        with open(os.environ["GITHUB_OUTPUT"], "a") as out:
            out.write(f"count={len(imported)}\n")


if __name__ == "__main__":
    main()
