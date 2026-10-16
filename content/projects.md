---
title: Projects
description: A collection of side projects I have built for myself or others.  Hopefully you will find them useful
layout: page
author: Lee Turner
comments: false
---
Here you can find a collection of side projects I have built for myself or others.  Your mileage might vary, but you are welcome to dig in and have a play if they are useful to you.

## Micronaut Launch TUI
[mtui](https://github.com/leeturner/micronaut-launch-tui) is a terminal UI for creating [Micronaut](https://micronaut.io) projects through [Micronaut Launch](https://launch.micronaut.io), written in [Kotlin](https://kotlinlang.org) and built with [TamboUI](https://tamboui.dev).  The hardest part of creating a Micronaut project is finding the right features from the hundreds available, so mtui puts them all in one searchable list.  Pick your options, preview the generated files and unzip the project straight into the current directory without ever leaving the terminal.  It was inspired by Dan Vega's [spring-initializr-tui](https://github.com/danvega/spring-initializr-tui)

<a class="github-button" href="https://github.com/leeturner/micronaut-launch-tui" data-color-scheme="no-preference: dark; light: dark; dark: dark;" data-size="large" aria-label="View leeturner/micronaut-launch-tui on GitHub">View the project on GitHub</a>

## wiremock-micronaut
[wiremock-micronaut](https://github.com/leeturner/wiremock-micronaut) simplifies testing HTTP clients in [Micronaut](https://micronaut.io) 5 and above.  It starts [WireMock](https://wiremock.org) servers per test class, binds their URLs into Micronaut configuration before your beans are created and injects them into your tests.  The annotations mirror [wiremock-spring-boot](https://github.com/wiremock/wiremock-spring-boot) so it should feel familiar if you have used that.  It is available on [Maven Central](https://central.sonatype.com/artifact/io.github.leeturner/wiremock-micronaut)

<a class="github-button" href="https://github.com/leeturner/wiremock-micronaut" data-color-scheme="no-preference: dark; light: dark; dark: dark;" data-size="large" aria-label="View leeturner/wiremock-micronaut on GitHub">View the project on GitHub</a>

## wiremock-blns-extension
[wiremock-blns-extension](https://github.com/leeturner/wiremock-blns-extension) is a [WireMock](https://wiremock.org) extension that adds a `naughtyString` Handlebars helper, so templated responses can return strings from the [Big List of Naughty Strings](https://github.com/minimaxir/big-list-of-naughty-strings) - SQL injection, RTL text, zero-width characters, emoji, Zalgo text and more.  Every client test that hits the stub then exercises those cases for free.  It works with both embedded WireMock and the standalone JAR / Docker image and is available on [Maven Central](https://central.sonatype.com/artifact/io.github.leeturner/wiremock-blns-extension)

<a class="github-button" href="https://github.com/leeturner/wiremock-blns-extension" data-color-scheme="no-preference: dark; light: dark; dark: dark;" data-size="large" aria-label="View leeturner/wiremock-blns-extension on GitHub">View the project on GitHub</a>

## Xport
[Xport](https://github.com/leeturner/xport) is a command line tool written in [Kotlin](https://kotlinlang.org) and [Micronaut](https://micronaut.io) that converts an X/Twitter data export into [Hugo](https://gohugo.io/) compatible markdown files, preserving the original timestamps and media.  I used it to bring my old tweets over to my own [microblog](/microblog/) on this site

<a class="github-button" href="https://github.com/leeturner/xport" data-color-scheme="no-preference: dark; light: dark; dark: dark;" data-size="large" aria-label="View leeturner/xport on GitHub">View the project on GitHub</a>

## Conway's Game of Life
A terminal based implementation of [Conway's Game of Life](https://en.wikipedia.org/wiki/Conway%27s_Game_of_Life) written in [Kotlin](https://kotlinlang.org) using [Micronaut](https://micronaut.io) and functional programming with [Arrow](https://arrow-kt.io).  The universe wraps around like a torus and can be rendered in the terminal with ANSI colours or in a [KorGE](https://korge.org/) 2D window

<a class="github-button" href="https://github.com/leeturner/conways-game-of-life-kotlin" data-color-scheme="no-preference: dark; light: dark; dark: dark;" data-size="large" aria-label="View leeturner/conways-game-of-life-kotlin on GitHub">View the project on GitHub</a>

## Spektrum
[Spektrum](https://github.com/leeturner/spektrum) is a work in progress Sinclair ZX Spectrum emulator written in [Kotlin](https://kotlinlang.org) and [Micronaut](https://micronaut.io), starting with an emulation of the Z80 CPU

<a class="github-button" href="https://github.com/leeturner/spektrum" data-color-scheme="no-preference: dark; light: dark; dark: dark;" data-size="large" aria-label="View leeturner/spektrum on GitHub">View the project on GitHub</a>

## Micronaut CLI Template
[Micronaut CLI Template](https://github.com/leeturner/micronaut-cli-template) is a ready to go [Kotlin](https://kotlinlang.org) [Micronaut](https://micronaut.io) command line application template with all the tooling I like already set up - a Gradle version catalogue, Kotlinter and Detekt for linting, [Arrow](https://arrow-kt.io) for functional programming, [Strikt](https://strikt.io) for assertions and GitHub Actions and Dependabot for CI.  Click "Use this template" on GitHub to start a new project from it

<a class="github-button" href="https://github.com/leeturner/micronaut-cli-template" data-color-scheme="no-preference: dark; light: dark; dark: dark;" data-size="large" aria-label="View leeturner/micronaut-cli-template on GitHub">View the project on GitHub</a>

## callback-logger
[callback-logger](https://github.com/leeturner/callback-logger) is a simple [Kotlin](https://kotlinlang.org) and [Micronaut](https://micronaut.io) service to receive callbacks, which is useful when testing APIs locally that send them.  Point the API you are testing at it and it will log every `POST` or `PUT` it receives, with a simple web UI to see what has arrived.  You can also define custom callback endpoints and configure the response code and payload it returns

<a class="github-button" href="https://github.com/leeturner/callback-logger" data-color-scheme="no-preference: dark; light: dark; dark: dark;" data-size="large" aria-label="View leeturner/callback-logger on GitHub">View the project on GitHub</a>

## image-term
[image-term](https://github.com/leeturner/image-term) is a terminal based image viewer written in [V](https://vlang.io/) that renders images as colourful ASCII mosaics.  It scales the image to fit your terminal, corrects for the aspect ratio of terminal characters and averages the colours within each block of pixels.  It is based on the blog post [Convert an Image into Colourful Ascii Art](https://linyunliu.com/blogs/convert-an-image-into-colourful-ascii-art/)

<a class="github-button" href="https://github.com/leeturner/image-term" data-color-scheme="no-preference: dark; light: dark; dark: dark;" data-size="large" aria-label="View leeturner/image-term on GitHub">View the project on GitHub</a>

## Hugo Progression Framework
Hugo Progression is a [Hugo](https://gohugo.io/) template that can render progression frameworks using the same data format as the [Monzo progression framework](https://github.com/monzo/progression-framework) - find out more information in this [blog post](/posts/hugo-progression-framework/)

<a class="github-button" href="https://github.com/leeturner/hugo-progression" data-color-scheme="no-preference: dark; light: dark; dark: dark;" data-size="large" aria-label="View leeturner/hugo-progression on GitHub">View the project on GitHub</a>

## BlinkyTapeTestWatcher
[BlinkyTapeTestWatcher](https://github.com/leeturner/BlinkyTapeTestWatcher) is a [Kotlin](https://kotlinlang.org) based implementation of the [Junit 5](https://junit.org/junit5/) [TestWatcher API](https://junit.org/junit5/docs/5.5.1/api/org/junit/jupiter/api/extension/TestWatcher.html) that hooks up your tests to a BlinkyTape LED strip - find out more information in this [blog post](/posts/blinkytape-junit-testwatcher/)

<a class="github-button" href="https://github.com/leeturner/BlinkyTapeTestWatcher" data-color-scheme="no-preference: dark; light: dark; dark: dark;" data-size="large" aria-label="View leeturner/BlinkyTapeTestWatcher on GitHub">View the project on GitHub</a>

## pinboard2markdown
[pinboard2markdown](https://github.com/leeturner/pinboard2markdown) is a command line tool written in [Kotlin](https://kotlinlang.org) and [Spring Boot](https://start.spring.io) that communicates with the [pinboard.in api](https://pinboard.in/api/) to retrieve a selection of bookmarks that are tagged with a specified tag.  It then converts those bookmarks to markdown and outputs them to the terminal.

Because I built this for myself it isn't yet packaged up as a command line tool that can be easily downloaded and used.  If you are a developer familiar with Kotlin or Java technologies that you can clone the github repo and build the project.  If there is any interest I will release a formal version of the project and make it so it can be run just like any other command line tool.

I use this tool to build regular newsletters for the backend developers at [Crunch](https://medium.com/@crunchtech) and to generate my [Geek Reads](/tags/bookmarks/) posts

<a class="github-button" href="https://github.com/leeturner/pinboard2markdown/" data-color-scheme="no-preference: dark; light: dark; dark: dark;" data-size="large" aria-label="View leeturner/pinboard2markdown on GitHub">View the project on GitHub</a>

