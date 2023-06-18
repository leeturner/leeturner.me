---
title: Do You Bake or Fry
date: 2018-01-20T22:09:08Z
description: A quick discussion on the pros and cons of a static versus dynamic website.  I also give a little bit of an insight as to why I am using a static site and what I am using to bake it with.
slug: do-you-bake-or-fry
layout: post
author: Lee Turner 
tags:
- static-sites
- jbake
- jekyll
- wordpress
- b2evolution   
aliases:
- /blog/2018/01/do-you-bake-or-fry.html
- /posts/do-you-bake-or-fry/
---
Before I go much further, I thought it was probably worth me putting down a few notes about my technology choices for this site.  

In term of website development, I have had experience of quite a few different content management systems such as [b2Evolution](http://b2evolution.net) and more recently [Wordpress](http://wordpress.org).  I have developed plugins and templates for b2Evolution as well as contributing code to the core product back in the day.  I have put more sites together in Wordpress than I care to remember - most of my clients used Wordpress in some form or other while I was working in the paid traffic/SEO industry.

Content management systems like b2Evolution and Wordpress have become commonly know as '_frying_' your site - all of your content is hidden away in a database somewhere and the CMS code takes a request from a browser, translates that into a request on the database to pull out the content and wrap it up with your chosen theme to produce your site.  There is absolutely nothing wrong with this.... in fact it works very well.  You can get a good looking site up and running very quickly and it is probably going to be able to do everything you need it to do.

On the flip side of '_frying_' is '_baking_'.  This is where your content is stored in text files using a simple markup like [Markdown](https://daringfireball.net/projects/markdown/) or [AsciiDoc](http://asciidoctor.org).  You run your content through an application that bakes it together with a template to produce a static site.  By static site I mean a pure html based website that can be run from any web server or hard drive.

I have dabbled with blog aware static site generators since reading an article on [Blogging Like a Hacker](http://tom.preston-werner.com/2008/11/17/blogging-like-a-hacker.html) using [Jekyll](https://jekyllrb.com) and [Octopress](https://octopress.org) to put a few sites together.  The problem I have always had is that I needed the sites to serve a purpose and I didn't have the time to devote to understanding everything I needed to know to get the best out of the static site.

## Why Bake ?

There are many pro's and con's to static site generators and they aren't suitable for everyone or every use case.  There has been plenty written about the benefits of static sites but the ones that appeal to me the most are:

* *Flexibility* - the content I write is stored in plain text files.  This means I can write it in a [text editor](http://www.vim.org) of [my choosing](http://sublimetext.com).
* *Security* - the output of running a static site generator is a static site - html, css, javascript etc.  There isn't a whole lot you can hack with a static site.  If you have ever had to clean up a hacked Wordpress site you will know that it is no easy job - content inserted into the database, rogue code inserted into the php files, additional files added to your hosting account.... the list goes on.
* *Performance* - as discussed above, a '_frying_' based content management system has multiple resources that it is managing all of which are limited.  There are only a limited number of database requests that the CMS can make at any one time and therefore, if your site is getting a reasonable amount of traffic you will have to consider some kind of caching solution.  A '_baked_' site doesn't have these limitations..... it is just a static site which can be cached by your browsers standard browser cache.
* *Reliability* - Similar to the performance point above, with all the moving parts of a a '_frying_' based CMS there are so many things that can go wrong - problems connecting to the database, issues with conflicting plugins, problems when upgrading the CMS or the plugins.  Static sites have none of these problems.
* *Version Control* - even though some content management systems try to provide some level of version control for your content, that content is still stored in a database which is inherently harder to version control in its entirety.  With a static site you can store all of your content in a version control system such as git, which not only provides you with first class version control but serves as an effective backup as well.  It makes sense that developers who use these tools on a daily basis are drawn to static sites.

## Why Bake Now ?

So I guess the question has to be why am I now choosing to put this site together using static site generation instead of a standard CMS that I am more familiar with?  I think the main difference this time round is that for me, the website is a project in and of itself, which was never the case before.  I plan to use it to learn a few things I have had on my radar for a little while and also to get involved in an open source project or two.

This site will be the perfect outlet for all of those things and doesn't have to serve any other purpose than for me to document what I am playing with.

## What Do You Bake With ?

This leaves just one thing to discuss.  What am I going to use to generate this site?  There are many more static site generators available now than when I first played with Jekyl and Octopress.  You only have to look at [StaticGen](https://www.staticgen.com) to see that Jekyll is still the granddaddy of them all, but there are now others out there that are gaining traction.

As I am primarily a Java developer I was looking for a good solid open source static site generator written in Java so I could get involved in driving the project forward.  There are a few Java based site generators out there but by far the most complete is [jBake](http://www.jbake.org).  This is the tool I have chosen to build my site with.  This site isn't yet up and running, even as I type this post.  This is mostly due to the fact that I am looking into converting a new template to use with my site (more on this in future posts), but I am playing around with it as I type so hopefully I will have something up and running soon.

Jbake is by no means perfect.  One of the big things it is missing is a plugin system which would allow people to extend the functionality of jBake while the site is being baked.  I am hoping that this is something that will be worked on soon and something I am looking forward to getting involved with.

So that is it.  This post lays the foundation of what I am using to build the site and I am sure there will be many more related posts as I dig deeper and get more involved in the project.                
