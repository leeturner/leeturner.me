---
title: mtui - A Terminal UI for Micronaut Launch
subTitle: Creating Micronaut projects without leaving the terminal
description: Introducing mtui, a Kotlin TUI built with TamboUI for generating Micronaut projects via Micronaut Launch
date: 2026-11-21T10:00:00Z
slug: micronaut-launch-tui
layout: post
author: Lee Turner
showtoc: true
comments: true
tags:
  - micronaut
  - kotlin
  - tui
  - tamboui
---

The hardest part of creating a Micronaut project is finding the right features: there are hundreds of them. Starting one usually means opening the browser, heading to Micronaut Launch, clicking through the options, downloading the zip, unzipping it and moving it to where you actually wanted it...

You can skip the browser altogether with the [Micronaut CLI](https://docs.micronaut.io/latest/guide/#cli) and `mn create-app`, but then you need to know the feature names up front. I wanted something in between: the browsing and searching you get on the website, without leaving the terminal.

Dan Vega's [spring-initializr-tui](https://github.com/danvega/spring-initializr-tui) does the same job for Spring Boot, and it inspired me to build one for Micronaut :)

Say hello to [mtui](/projects/micronaut-launch-tui/), a terminal UI for creating Micronaut projects through [Micronaut Launch](https://launch.micronaut.io).

![Creating a project with mtui](https://raw.githubusercontent.com/leeturner/micronaut-launch-tui/main/docs/images/demo.gif)

## What it does

mtui puts every feature in one searchable list, so you type a few letters, press Space and move on, without leaving the terminal or unzipping a download:

- Choose the application type, language, build tool, test framework and JDK
- Switch between the latest Micronaut release and the current snapshot
- Search every feature by name, title or description, and see what you have selected at all times
- Preview the generated files before creating anything
- Unzip the project straight into the current directory
- Open the project with your editor or IDE once it is created
- Press `?` on any screen to see its keys

Press `/` to search and Space to select. In the preview, `p` browses the files Launch would generate and `f` jumps to a file by name. Lists move with the arrow keys or `j`/`k`.

## Built with Kotlin and TamboUI

It is written in Kotlin, and the UI is built with [TamboUI](https://tamboui.dev). TamboUI is a great TUI library to use if you are on the JVM.

It ships as a GraalVM native binary, so there is nothing to install on the JVM side to run it.

## Getting it

With the [GitHub CLI](https://cli.github.com), this installs or updates `mtui` in `~/.local/bin` (make sure that is on your `PATH`). This is the macOS Apple Silicon version; on Linux, use `'*linux-x86_64*'` as the pattern:

```bash
mkdir -p ~/.local/bin
gh release download -R leeturner/micronaut-launch-tui -p '*macos-aarch64*' -O - | tar -xz -C ~/.local/bin
```

A download made by `gh` isn't quarantined, so macOS doesn't block it.

If you'd rather not use `gh`, grab the archive for your platform from the [latest release](https://github.com/leeturner/micronaut-launch-tui/releases/latest): macOS (Apple Silicon), Linux (x86_64) or Windows (x86_64). Unpack it and move `mtui` somewhere on your `PATH`:

```bash
tar -xzf mtui-*-macos-aarch64.tar.gz
mv mtui /usr/local/bin/
```

Two things to know. The binary isn't signed, so if macOS blocks it, clear the quarantine flag:

```bash
xattr -d com.apple.quarantine /usr/local/bin/mtui
```

And the Windows binary is built but hasn't been tested on Windows yet, so if you try it, I'd love to hear how it goes.

## Using it

Run `mtui` in the directory where you want your project, pick your options, search for the features you need, have a quick look at the preview and generate. The project is unzipped right where you are.

If you want to jump straight into your editor afterwards, give `mtui` the command that opens a project. It runs it with the new project's path once the project is created:

```bash
mtui --open idea
```

Or set it once in your shell profile (`--open` wins if both are set):

```bash
export MTUI_OPEN=idea
```

## What's next

What's planned is on the [roadmap](https://github.com/leeturner/micronaut-launch-tui/blob/main/docs/roadmap.md), and there is more on the [project page](/projects/micronaut-launch-tui/). If you try it and something doesn't behave on your setup, an [issue](https://github.com/leeturner/micronaut-launch-tui/issues) would be great. Ideas and PRs are welcome too.
