---
title: "Introducing wiremock-micronaut"
subTitle: WireMock for your Micronaut 5 tests
description: Introducing wiremock-micronaut, a small library that starts WireMock servers per test class, binds their URLs into your Micronaut config and injects them into your tests
date: 2026-11-18T15:00:00Z
slug: wiremock-micronaut
layout: post
author: Lee Turner
showtoc: true
comments: true
tags:
  - wiremock
  - micronaut
  - kotlin
  - java
  - testing
---

WireMock and Micronaut are two things I really like, so it was only a matter of time before the two came together :)

Say hello to [wiremock-micronaut](/projects/wiremock-micronaut/), a small library that makes testing HTTP clients in Micronaut 5 apps a whole lot nicer.

## The problem

Testing an HTTP client properly means standing up a WireMock server, getting its URL into your Micronaut config before the beans that need it are created, and then getting hold of the server in your test so you can stub things. None of that is hard on its own, but it is the same plumbing every time, and it is easy to get the ordering wrong.

I wanted that bit to just go away. WireMock has an official Spring Boot integration that does all of this for you, and I wanted the same for Micronaut, including the most recent versions.

## What it does

wiremock-micronaut takes care of the plumbing for you:

- It starts WireMock servers per test class
- It binds their URLs into your Micronaut configuration *before* any beans are created
- It injects the servers into your tests so you can stub away

The annotations and attributes deliberately mirror [wiremock-spring-boot](https://github.com/wiremock/wiremock-spring-boot), so if you have used that one it should feel very familiar.

## Already using the nahuel92 library?

If you have come across `io.github.nahuel92:wiremock-micronaut`, this is its replacement, and moving over is mostly a find and replace:

| Before | After |
|---|---|
| `@MicronautWireMockTest(...)` | `@MicronautTest` + `@EnableWireMock(...)` |
| `@ConfigureWireMock(properties = "x")` | `@ConfigureWireMock(baseUrlProperties = "x")` |
| `portProperty = "x"` | `portProperties = "x"` |
| package `io.github.nahuel92.wiremock.micronaut` | `com.leeturner.wiremock.micronaut` |
| gRPC (`WireMockGrpcService`) | Not supported |

If you need gRPC support you should definitely stick with `io.github.nahuel92:wiremock-micronaut` for now, until I look at adding gRPC support.

## Getting started

You will need Java 25 and Micronaut 5.2.1 or later (5.x) with `micronaut-test-junit5`. Then add the dependency (at the time of writing, the latest release is 0.2.0):

```kotlin
testImplementation("io.github.leeturner:wiremock-micronaut:0.2.0")
```

The library brings `wiremock-standalone` (a shaded jar) with it, so WireMock's own dependencies never clash with Micronaut's.

## A quick example

Annotate your test with `@EnableWireMock`, inject the server with `@InjectWireMock`, and you are good to go. Here is the Java version:

```java
@MicronautTest
@EnableWireMock(@ConfigureWireMock(name = "users", baseUrlProperties = "users.url"))
class UsersClientTest {
  @Inject UsersClient client;           // @Client("${users.url}")
  @InjectWireMock("users") WireMockServer users;

  @Test
  void fetchesAUser() {
    users.stubFor(get("/users/1").willReturn(ok("alice")));
    assertThat(client.user("1")).isEqualTo("alice");
  }
}
```

And for the Kotlin folks (the test body is the same as the Java one):

```kotlin
@MicronautTest
@EnableWireMock(ConfigureWireMock(name = "users", baseUrlProperties = ["users.url"]))
class UsersClientTest {
    @Inject lateinit var client: UsersClient
    @InjectWireMock("users") lateinit var users: WireMockServer

    @Test
    fun fetchesAUser() {
        users.stubFor(get("/users/1").willReturn(ok("alice")))
        assertThat(client.user("1")).isEqualTo("alice")
    }
}
```

No manual server lifecycle, no fiddling with property ordering, just stubs and assertions. Servers are reset before each test and stopped after the test class.

## There's more

Once the basics were in place I added a few more things:

- **Multiple servers**, for when your app talks to more than one service. Give each server its own property names.
- **SSE and message stubs**, using WireMock's message stubs and Server-Sent Events support, with no extra configuration.
- **Pyronaut support**: [Pyronaut](https://pyronaut.io) apps are Micronaut apps written in Python, and the extension works in their JUnit 5 tests, whether those are written in Java or as Python test modules. pytest tests don't run through JUnit, so it does nothing there.

The [README](https://github.com/leeturner/wiremock-micronaut) has examples for all of these.

## Good to know

One limitation up front:

- `@EnableWireMock` and `@ConfigureWireMock` belong on the top-level test class, not on `@Nested` classes

It is also versioned as `0.x` while WireMock 4 is in beta, with `1.0.0` to follow WireMock 4 GA, so expect things to settle as WireMock 4 does.

## Give it a try

If you give it a go, I would love to know how it goes. Bug reports and ideas are very welcome in the [issues on GitHub](https://github.com/leeturner/wiremock-micronaut/issues), and there is more on the [project page](/projects/wiremock-micronaut/).
