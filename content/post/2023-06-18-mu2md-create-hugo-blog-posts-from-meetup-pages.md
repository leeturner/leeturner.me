---
title: Creating Hugo Blog Posts from Meetup Pages using Kotlin Script and JSoup
subTitle: Automating workflows by scraping Meetup pages using Kotlin Script and JSoup
date: 2023-06-30:09:36+0100
description: There is a lot of admin involved in running a meetup group.  One of the things I wanted to automate was the creation of blog posts for our meetup blogs.  This post describes how I used Kotlin Script and JSoup to scrape the meetup page and create the blog posts.
slug: creating-hugo-blog-posts-from-meetup-pages-using-kotlin-script-and-j-soup
layout: post
author: Lee Turner
showtoc: true
comments: true
tags:
- kotlin
- hugo
- jsoup
---

```shell
./mu2md.main.kts -s "Michele Sollecito" -t Apache,Pulsar,Corutines,Flows https://www.meetup.com/brighton-kotlin/events/294227622/ > 2023-06-17-apache-pulsar-with-kotlin-couroutines-and-flows.md
```

```kotlin
#!/usr/bin/env kotlin
@file:Repository("https://jcenter.bintray.com")
@file:DependsOn("org.jetbrains.kotlinx:kotlinx-cli-jvm:0.3.5")
@file:DependsOn("org.jsoup:jsoup:1.16.1")
@file:DependsOn("io.github.furstenheim:copy_down:1.1")

import io.github.furstenheim.CopyDown
import io.github.furstenheim.HeadingStyle
import io.github.furstenheim.OptionsBuilder
import java.net.SocketTimeoutException
import java.time.LocalDateTime
import java.time.format.DateTimeFormatter.ISO_LOCAL_DATE_TIME
import kotlinx.cli.ArgParser
import kotlinx.cli.ArgType
import kotlinx.cli.default
import org.jsoup.Jsoup

object Constants {
  const val DEFAULT_USER_AGENT =
      "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:109.0) Gecko/20100101 Firefox/114.0"
}

// Handle all the required command line arguments for the script
val parser = ArgParser("mu2md.main.kts")
val url by
    parser.argument(
        ArgType.String, description = "URL of the meetup page we are converting to markdown")
val speaker by
    parser
        .option(
            ArgType.String,
            shortName = "s",
            fullName = "speaker",
            description = "Name of the speaker")
        .default("")
val tags by
    parser
        .option(
            ArgType.String,
            shortName = "t",
            fullName = "tags",
            description = "List of comma separated tags")
        .default("")

parser.parse(args)

try {
  val meetUpPage =
      Jsoup.connect(url).userAgent(Constants.DEFAULT_USER_AGENT).get()
          ?: error("Could not connect to $url")
  val eventTitle = meetUpPage.select("h1").text() ?: error("Could not find event title")
  val eventDescription =
      meetUpPage.select("div#event-details div.break-words")
          ?: error("Could not find event description")
  val now = LocalDateTime.now()
  val markdownOptions = OptionsBuilder.anOptions().withHeadingStyle(HeadingStyle.ATX).build()
  val converter = CopyDown(markdownOptions)
  val eventTitleWithSpeaker = "$eventTitle ${if (speaker.isNotEmpty()){"with $speaker"} else ""}"
  val tagsList = tags.split(",").map { it.trim() }.filter { it.isNotEmpty() }
  val blogPostTemplate =
      """
        |---
        |title: $eventTitleWithSpeaker
        |description: $eventTitleWithSpeaker
        |date: ${now.format(ISO_LOCAL_DATE_TIME)}
        |author: Lee Turner
        |type: post
        |featured: ${if (speaker.isEmpty()){"replace-me.png"} else "${speaker.lowercase().replace(" ", "-")}.png"}
        |featuredalt: $eventTitleWithSpeaker
        |featuredpath: /images/blog/${now.year}/${String.format("%02d", now.monthValue)}/
        |slug: ${eventTitle.lowercase().replace(" ", "-")}
        |categories:
        |- Meetups
        |tags:
        |${tagsList.joinToString("\n") { "- $it" }}
        |---
        |Come and join us by signing up on our meetup page: [$url]($url)
        |
        |${converter.convert(eventDescription.toString())}
  """
          .trimMargin("|")
  println(blogPostTemplate)
} catch (e: SocketTimeoutException) {
  println("Could not connect to $url.  Connection timed out.")
}
```
