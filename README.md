# Hugo project for leeturner.me

This is the [Hugo](https://gohugo.io) used to generate [leeturner.me](https://leeturner.me).  The site is served from Github Pages and built using Github Actions.

## Theme

The site uses its own theme in `themes/leeturner`, kept in this repo. Layouts live in `themes/leeturner/layouts`,
styles in `themes/leeturner/assets/css/main.css` and the small amount of JavaScript (theme toggle, giscus and the
projects filter) in `themes/leeturner/assets/js/site.js`.

The projects page is generated from `data/projects.yaml`. Add a project there and give it tags; any tag used by
two or more projects becomes a filter button.

Run it locally with `hugo server` (Hugo 0.146 or newer).

## Posting to the microblog

Microblog posts live in `content/microblog/<year>/`. Anything pushed to `master` is deployed, so there's no need for a branch or PR for a post.

- **From Mastodon (automatic):** the `import mastodon posts` workflow runs hourly and copies new public posts from [@leeturner@hachyderm.io](https://hachyderm.io/@leeturner) into the microblog, with their images. Boosts, replies to other people and posts tagged `#nosite` are skipped. To backfill older posts, run the workflow by hand from the Actions tab with a `since` date (tick "dry run" first to preview).
- **From the laptop:** on `master`, run `scripts/mb "Some text"` (add image paths after the text to attach them, or run it with no arguments to write in `$EDITOR`). It creates the post, commits and pushes.
