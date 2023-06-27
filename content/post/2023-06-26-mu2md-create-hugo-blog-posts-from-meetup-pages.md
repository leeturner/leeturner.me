---
title: Creating Hugo Blog Posts from Meetup Pages using Kotlin Script and JSoup
subTitle: Automating workflows by scraping Meetup pages using Kotlin Script and JSoup
date: 2023-06-26T10:20:08Z
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

## The Dark Side of Running a Meetup Group

I really enjoy running the [Brighton Kotlin](https://brightonkotlin.com) and [Brighton JUG](https://brightonjug.com)
meetup groups. It is purely selfish to be honest, I get to meet lots of interesting people and learn a lot from the
speakers and attendees and generally geek out with like-minded people.

However, there is a lot of admin involved in running a meetup group, let alone two - especially when you decide to set
up a dedicated blog for each of the meetup groups. Add that to a full time job and family commitments and it makes an
interesting juggling act. So, inspired by [Yannick](https://twitter.com/osteel), one of the organisers of the
local [PHP meetup](https://phpsussex.uk/), and the way he [automates](https://github.com/PHPSussex/phpsussex.github.io)
the updating of the website homepage, I decided that it was time for me to look at my setup.

## Automating the Creation of Blog Posts

I started by looking at the creation of blog posts for the meetup blogs. This was the one task that I always
left till the last minute or very often didn't get round to at all. It is actually pretty simple - just copy the
content I had already added to the meetup page and create a blog post from it. Each of the meetup blogs are created
using [hugo](https://gohugo.io) and hosted on GitHub pages (just like this blog) so I just needed to create a markdown
file with the correct front matter and content.

The basic idea was to create a script that would scrape a meetup page and create the markdown file in the format
of a hugo blog post. If I made it generic enough, I could use it for both the Kotlin and Java meetup groups.

Essentially, something where I could point it
to [this meetup page](https://www.meetup.com/brighton-kotlin/events/294227622/) and
generate this [blog post](https://brightonkotlin.com/blog/apache-pulsar-with-kotlin-couroutines-and-flows/):

```markdown
---
title: Apache Pulsar with Kotlin coroutines and flows with Michele Sollecito
description: Apache Pulsar with Kotlin coroutines and flows with Michele Sollecito
date: 2023-06-17T14:23:23.550313
author: Lee Turner
type: post
featured: michele-sollecito.png
featuredalt: Apache Pulsar with Kotlin coroutines and flows with Michele Sollecito
featuredpath: /images/blog/2023/06/
slug: apache-pulsar-with-kotlin-coroutines-and-flows
categories:
- Meetups
tags:
- Apache
- Pulsar
- Coroutines
- Flows
---

Come and join us by signing up on our meetup
page: [https://www.meetup.com/brighton-kotlin/events/294227622/](https://www.meetup.com/brighton-kotlin/events/294227622/)

We are very excited to welcome **Michele Sollecito** to our July meetup. He will be giving a talk on **Apache Pulsar
with Kotlin couroutines and flows**

**Event Format: Hybrid**

* Join us in-person: 6:00pm @ [Pizza Pilgrims, Brighton](https://goo.gl/maps/ZPuDh6w8vz3H7KbQ9)
* Join us online: 6:30pm on
	YouTube - [https://www.youtube.com/watch?v=JbeK486FTyU](https://www.youtube.com/watch?v=JbeK486FTyU)

We'll explore how Kotlin makes consuming and producing messages from/to Apache Pulsar easy. We'll look at some tests,
and discuss how coroutines and flows work great with this kind of reactive and event-driven use cases.

Apache Pulsar is an open-source, distributed messaging and streaming platform built for the cloud. Its features include
multi-tenancy with resource separation and access control, geo-replication across regions, and tiered storage.

**Bio**

Connect with Michele:  
Twitter: [https://twitter.com/sollecitom](https://twitter.com/sollecitom)  
LinkedIn: [https://www.linkedin.com/in/michelesollecito/](https://www.linkedin.com/in/michelesollecito/)
```

### Kotlin Script and JSoup FTW

For me, Kotlin is the obvious choice for the script and I had already used [JSoup](https://jsoup.org/) for a previous
project, and it was really easy to use, so I decided to use it again.

Below is the script I came up with. It is pretty self-explanatory, but I will go through it in more detail below. The
script is hosted on GitHub [here](https://github.com/leeturner/mu2md) so make sure you check there for any updates.

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
	ArgType.String, description = "URL of the meetup page we are converting to markdown"
)
val speaker by
parser
	.option(
		ArgType.String,
		shortName = "s",
		fullName = "speaker",
		description = "Name of the speaker"
	)
	.default("")
val tags by
parser
	.option(
		ArgType.String,
		shortName = "t",
		fullName = "tags",
		description = "List of comma separated tags"
	)
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
	val eventTitleWithSpeaker = "$eventTitle ${
		if (speaker.isNotEmpty()) {
			"with $speaker"
		} else ""
	}"
	val tagsList = tags.split(",").map { it.trim() }.filter { it.isNotEmpty() }
	val blogPostTemplate =
		"""
        |---
        |title: $eventTitleWithSpeaker
        |description: $eventTitleWithSpeaker
        |date: ${now.format(ISO_LOCAL_DATE_TIME)}
        |author: Lee Turner
        |type: post
        |featured: ${
			if (speaker.isEmpty()) {
				"replace-me.png"
			} else "${speaker.lowercase().replace(" ", "-")}.png"
		}
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

The script is called `mu2md` (Meetup 2 Markdown) and it starts off by using the `kotlinx-cli` library from JetBrains to
handle the command line arguments. The script requires a single argument which is the URL of the meetup page we want
to convert to markdown. There are also two optional arguments, the speaker and the tags. The speaker is used to
generate the image name for the blog post, along with some of the blog post metadata and the tags are used to generate
the tags for the blog post.

We then parse the meetup page using JSoup and extract the event title and description by referencing the HTML elements.
I then use a library I called [copy_down](https://github.com/furstenheim/copy-down) to take the html from the meetup
description and convert it to markdown. (I had never used this library before, and it worked really well)

When we have everything we need, we then print the blog post to the console using standard kotlin string interpolation.

### Running the Script

To run the script, you need to have the Kotlin compiler installed and make the script executable. Once you have that,
you can run the script on the command line just like any shell script and pipe the results into a markdown file. For
example:

```shell
./mu2md.main.kts -s "Michele Sollecito" -t Apache,Pulsar,Coroutines,Flows https://www.meetup.com/brighton-kotlin/events/294227622/ > 2023-06-17-apache-pulsar-with-kotlin-couroutines-and-flows.md
```

As a nice bonus, `kotlinx-cli` generates a help page for the script, so if you run the script with the `-h` flag,
you will see the following:

```shell
./mu2md.main.kts -h
Usage: mu2md.main.kts options_list
Arguments:
    url -> URL of the meetup page we are converting to markdown { String }
Options:
    --speaker, -s [] -> Name of the speaker { String }
    --tags, -t [] -> List of comma separated tags { String }
    --help, -h -> Usage info
```

Let me know if you find this script useful or if you have any suggestions for improvements. I am going to take a look
at other repetitive tasks I do as part of my meetup workflow and see if I can automate those as well. I will write those
up as well if I do. I am also going to look at whether I can use GitHub actions along with a variation of this script
to automate the whole flow of blog post creation and publishing but I will need to figure out how to handle the speaker
name and tags. That requires a bit more thought.

