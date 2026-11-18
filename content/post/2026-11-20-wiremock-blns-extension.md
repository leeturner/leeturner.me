---
title: wiremock-blns-extension - Naughty Strings for WireMock
subTitle: Putting the Big List of Naughty Strings into your templated responses
description: Introducing wiremock-blns-extension, a WireMock extension that adds a naughtyString Handlebars helper backed by the Big List of Naughty Strings
date: 2026-11-20T10:00:00Z
slug: wiremock-blns-extension
layout: post
author: Lee Turner
showtoc: true
comments: true
tags:
  - wiremock
  - testing
  - appsec
  - java
---

Most of the time when we mock an API we send back nice, well-behaved data. A name like "Alice", an email that's actually an email, a description with nothing weirder in it than a full stop. That's fine for the happy path, but real APIs don't always play nice, and plenty of bugs only show up when some unexpected string comes back from a downstream service.

If you haven't come across it, the [Big List of Naughty Strings](https://github.com/minimaxir/big-list-of-naughty-strings) (BLNS) is a collection of strings that are very likely to cause problems when used as input: SQL injection, RTL text, zero-width characters, emoji, Zalgo text and more.

So I built [wiremock-blns-extension](/projects/wiremock-blns-extension/) :) Every client test that hits the stub then exercises those cases for free.

## What it does

The extension adds a `naughtyString` Handlebars helper to WireMock's response templating. Drop it into a templated response and WireMock fills in a string from BLNS, so your client code has to cope with the kind of input that tends to break things.

A few things worth knowing:

- The list has **516 strings** across **30 categories**
- It is **bundled in the JAR**, so nothing is downloaded at runtime
- It targets **WireMock 4.0.0-beta.41** and runs on **Java 17 or later**

Here is a stub that returns a SQL injection string as the user's name:

```json
{
  "request": { "method": "GET", "url": "/user" },
  "response": {
    "status": 200,
    "headers": { "Content-Type": "application/json" },
    "body": "{ \"name\": {{{toJson (naughtyString category='sql-injection')}}} }",
    "transformers": ["response-template"]
  }
}
```

## Picking your strings

The helper takes two optional parameters, `category` and `index`:

```handlebars
{{naughtyString}}                                  {{!-- random, from the whole list --}}
{{naughtyString category='Emoji'}}                 {{!-- random, from one category --}}
{{naughtyString category='sql-injection'}}         {{!-- category given as a slug --}}
{{naughtyString index=42}}                         {{!-- fixed entry from the whole list --}}
{{naughtyString category='Emoji' index=0}}         {{!-- fixed entry within a category --}}
```

- **`category`** limits the choice to one category, matched case-insensitively by heading (`SQL Injection`) or slug (`sql-injection`)
- **`index`** returns a fixed entry instead of a random one, counted from 0 within the whole list or the category, which is handy when you want the same string every time

An unknown category or an out-of-range index gives you an error string rather than quietly returning the wrong thing. The full category list is on the [project page](/projects/wiremock-blns-extension/).

If you want to see it working end to end, my [WireMock standalone Docker example](https://github.com/leeturner/wiremock-standalone-docker-example#big-list-of-naughty-strings-example) project has it wired up: `docker compose up`, then `GET /blns` returns a random naughty string from every category.

## Which artifact to use?

There are **two artifacts**, and each only works in its own setting:

| Artifact | For |
|---|---|
| `io.github.leeturner:wiremock-blns-extension` | Embedded WireMock (`org.wiremock:wiremock`, JUnit) |
| `io.github.leeturner:wiremock-blns-extension-standalone` | The `wiremock-standalone` JAR and the Docker image |

`wiremock-standalone` relocates Handlebars, so the standalone artifact is built against the relocated packages. Use the wrong one and it fails at runtime: the plain JAR in standalone WireMock throws an `AbstractMethodError`. If you see that, check which artifact you picked.

For embedded WireMock in JUnit, add the dependency (at the time of writing, the latest release is 0.1.0):

```kotlin
testImplementation("io.github.leeturner:wiremock-blns-extension:0.1.0")
```

Then register the extension:

```java
@RegisterExtension
static WireMockExtension wm =
    WireMockExtension.newInstance()
        .options(wireMockConfig().dynamicPort().extensions(new BlnsExtension()))
        .build();
```

The standalone JAR and Docker setups are in the [README](https://github.com/leeturner/wiremock-blns-extension) too. For Docker, you mount the standalone JAR into `/var/wiremock/extensions/`.

## Tip: JSON bodies

WireMock doesn't escape helper output, so a naughty string dropped straight into JSON will often break it. Wrap the helper in WireMock's `toJson` helper, which adds the quotes and escaping, and leave the value unquoted, as in the stub above. It is tested against every entry in the list: all 516 come back as valid JSON that parses to the original string.

Use `body`, not `jsonBody`. Inside a `jsonBody` string value the quotes double up and you get invalid JSON.

## A word of warning

These are real payloads. The XSS, SQL and command-injection strings reach whatever consumes the mock, including logs, databases and browsers. That's the whole point, but only point clients at these stubs in environments where that is safe. You have been warned :)

## What's next

This is version 0.1.0, so I'd much rather hear how people actually use it than guess. If it finds a bug in your code, I'd love to hear about it.

There is more on the [project page](/projects/wiremock-blns-extension/), and the code is on [GitHub](https://github.com/leeturner/wiremock-blns-extension). Issues and PRs are very welcome.
