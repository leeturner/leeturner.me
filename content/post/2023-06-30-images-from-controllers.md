---
title: Returning Images From Micronaut Controllers
subTitle: How to load an image from the classpath and return it from a Micronaut controller
description: This week I was browsing the Micronaut Gitter channel and instantly got nerd snipped
date: 2023-06-29T18:00:00Z
slug: returning-images-from-micronaut-controllers
layout: post
author: Lee Turner
showtoc: false
comments: true
tags:
  - Micronaut
  - Controllers
  - Nerd Snipped
---

This week I was browsing the [Micronaut Gitter channel](https://matrix.to/#/#micronautfw_questions:gitter.im) and saw a
question about how to return a BufferedImage from a Micronaut controller. This isn't something I've done before and it
instantly [nerd snipped](https://xkcd.com/356/) me:

> I am looking for help on how to make a controller method respond with a BufferedImage. Any ideas ?

I had a quick google, and it turns out you don't need a buffered image at all. I found a few references to returning a
byte array from a controller, so I quickly span up a new service from [Micronaut Launch](https://micronaut.io/launch/), 
added a controller with an endpoint that loaded an image from the classpath returned it as a byte array:

```kotlin
import io.micronaut.http.MediaType
import io.micronaut.http.annotation.Controller
import io.micronaut.http.annotation.Get
import io.micronaut.http.annotation.Produces

@Controller("/buffered-image")
class BufferedImageController {

  // create a controller method that will return a byte array, turns out we don't need to return a
  // BufferedImage after all
  @Get
  @Produces(MediaType.IMAGE_JPEG) // Adjust the media type based on the image format
  fun loadImage(): ByteArray {
    val imageStream =
        javaClass.getResourceAsStream("/images/astronaut.jpeg")
            ?: error("Image could not be found") // Replace with your image path
    return imageStream.readBytes()
  }
}

```

Specifying the `@Produces(MediaType.IMAGE_JPEG)` allows the client to undertand what type of data is being returned and
render the image correctly.

That was all I needed to do, and I was able to hit the endpoint and see the image rendered in postman:

![Postman screenshot showing the image returned from the controller](/img/blog/2023-06-30-images-from-controllers/micronaut-astro.png)

The repo with all the source code is [here](https://github.com/leeturner/micronaut-bufferedimage) if you want to take a
look
