---
title: arrow-detekt-rules - Catching Arrow Mistakes with detekt
subTitle: A detekt 2 rule set for Either and Raise code
description: Introducing arrow-detekt-rules, a set of detekt 2 rules that catch common mistakes when working with Arrow's Either and Raise
date: 2026-11-23T10:00:00Z
slug: arrow-detekt-rules
layout: post
author: Lee Turner
showtoc: true
comments: true
tags:
  - kotlin
  - arrow
  - detekt
  - static-analysis
---

[Arrow](https://arrow-kt.io/) makes typed errors with `Either` and `Raise` a joy to work with, and a lot clearer than throwing exceptions around. There is more than one way to write it, though, and I have a style I want to stick to, like using `ensure` rather than an `if` statement with a `raise`.

As more and more code is written by agents, I wanted them to get early, automated feedback on that style, rather than me spotting it in review. So I built [arrow-detekt-rules](/projects/arrow-detekt-rules/), a [detekt](https://detekt.dev/) 2 rule set for Arrow code. It flags places where a standard construct, like an `if` statement, has been used instead of the Arrow one, like `ensure`, along with a few mistakes the compiler is perfectly happy with that are quietly wrong.

## Getting started

Add it to your `build.gradle.kts`. It's on Maven Central, so `mavenCentral()` in `repositories` is enough (the latest `<version>` is on the Maven Central badge in the README):

```kotlin
dependencies {
    detektPlugins("io.github.leeturner:arrow-detekt-rules:<version>")
}
```

A few things worth knowing up front:

- **Type resolution is required.** The rules run in `detektMain` and `detektTest`, not plain `detekt`.
- **Every rule is active by default**, so you are good to go once the plugin is added.
- **Each release is built for one detekt version**, because a rule set built against one detekt API may not load in another. Releases 0.1.0 to 0.3.0 are all built for detekt `2.0.0-alpha.6`, with Kotlin 2.4.21 for Java 17 and later, and tested against Arrow 2.2 and 2.3.

To turn a rule off, add it to your detekt config:

```yaml
arrow:
  UseEnsure:
    active: false
```

## What it catches

There are seven rules. Here are the ones I'd point at first, each with a flagged and a fine version.

### `NoCatchAllInRaiseScope`

A `runCatching`, or a `catch` of `Exception`, `Throwable` and friends, around a call that raises into an outer Raise scope swallows Arrow's `RaiseCancellationException`, so the error never reaches the scope.

```kotlin
// Flagged: runCatching catches the raise, so it never reaches either { }
either {
    val user = runCatching { findUser(id).bind() }.getOrNull()
    ensureNotNull(user) { UserMissing }
}

// Fine: turn exceptions into errors at the edge, then bind
either {
    val user = Either.catch { repository.find(id) }.mapLeft(::LookupFailed).bind()
    ensureNotNull(user) { UserMissing }
}
```

### `NoUnboundEither`

Flags an `Either`, `Option`, `Ior` or `Effect` used as a statement while a Raise is in scope. The `bind()` is missing, so the error is silently dropped.

```kotlin
// Flagged: the Either from findUser(id) is never bound, so its error is dropped
either {
    findUser(id)
    save(user)
}

// Fine
either {
    findUser(id).bind()
    save(user)
}
```

### `NoFoldBackIntoEither`

Flags a `fold` on an `Either` where one lambda builds a `Left` and the other a `Right`, and suggests `mapLeft` and `map`.

```kotlin
// Flagged
findUser(id).fold({ Left(LookupFailed(it)) }, { Right(it.name) })

// Fine
findUser(id).mapLeft { LookupFailed(it) }.map { it.name }
```

### `NoNestedEither`

Flags an `Either` inside an `Either`, which usually means a `map` that should be a `flatMap` or a missing `bind()`.

```kotlin
// Flagged: Either<E, Either<E, String>>
val user = findId(name).map { findUser(it) }

// Fine
val user = findId(name).flatMap { findUser(it) }
```

Sometimes the nesting is deliberate, and you can suppress the finding there with `@Suppress("NoNestedEither")`.

### `PreferEitherCatch`

Flags Arrow's `catch({ ... }) { ... }` when the handler only raises, and suggests `Either.catch` with `mapLeft`.

```kotlin
// Flagged
either {
    catch({ repository.find(id) }) { raise(LookupFailed(it)) }
}

// Fine
either {
    Either.catch { repository.find(id) }.mapLeft { LookupFailed(it) }.bind()
}
```

### `UseEnsure` and `UseEnsureNotNull`

These replace hand-rolled `if (...) raise(...)` checks with the built-in `ensure` and `ensureNotNull`, which read a lot better. `UseEnsureNotNull` also smart-casts for you.

```kotlin
// Flagged
either {
    if (amount > limit) raise(OverLimit)
    if (user == null) raise(UserMissing)
}

// Fine
either {
    ensure(amount <= limit) { OverLimit }
    ensureNotNull(user) { UserMissing }
}
```

The [README](https://github.com/leeturner/arrow-detekt-rules) covers what each rule deliberately doesn't flag, and the options, like `reportCompoundConditions` for `UseEnsure`.

## Releases

There have been three releases so far, 0.1.0 to 0.3.0, and detekt 2 is still in alpha, so expect things to move as it heads to a stable release.

## Try it

If you have an Arrow pattern that keeps tripping you or your team up, or a false positive in one of these rules, please tell me. There is more on the [project page](/projects/arrow-detekt-rules/), and the code is on [GitHub](https://github.com/leeturner/arrow-detekt-rules), where issues, rule ideas and PRs are all welcome. Point it at your Arrow code and see what it finds :)
