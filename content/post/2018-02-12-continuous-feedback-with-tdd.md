---
title: Continuous Feedback With TDD & Auto Running Tests
date: 2018-02-12T22:09:08Z
description: Listen to your code and evolve your design using TDD and auto running tests.
slug: continuous-feedback-with-tdd
layout: post
author: Lee Turner 
tags:
- tdd
- intellij
- reference
aliases:
- /blog/2018/02/continuous-feedback-with-tdd.html
- /posts/continuous-feedback-with-tdd/
---
This is the first of my 'reference' posts which pretty much means I am writing about it here so I don't forget about it in the future.

This post it about configuring your dev environment to provide you with continuous feedback while writing your code.  All of this came about after a conversation with another developer on my team about how to setup IntelliJ to run tests automatically.  We were looking at plugins such as [Infinitest](https://infinitest.github.io) but it all seemed a little clunky and crashed every so often.

The classic [3 laws of TDD](http://butunclebob.com/ArticleS.UncleBob.TheThreeRulesOfTdd) are pretty well known:

* Write production code only to make a failing unit test pass.
* Write only enough of a unit test to fail.
* Write only enough production code to make the failing unit test pass.

However, in all of the above, it is implicit that you are running your tests regularly enough to get feedback on the different stages.  Don't get me wrong, this is easy enough in IntelliJ, with a quick keyboard command but I was interested to see if there was a different way of working.

I went home that evening and dug a little deeper.  I eventually came across a feature of IntelliJ that I am amazed that I haven't seen before and it fit the bill nicely.

## Enter 'Toggle Auto-Test'

Toggle auto-test basically runs your test suite for you when it recognised a change in your code.  This is exactly what we were looking for and it was there in IntelliJ all this time.  Toggle auto-test is one of those little buttons tucked away down the side of the 'Run' or 'Debug' panels - click this and magical things start to happen :)

![Toggle Auto-Test In IntelliJ](/img/blog/2018-02-12-continuous-feedback-with-tdd/toggle-auto-test-intellij.png)

## Setting Up Toggle Auto-Test

There are just a few small things that you need to do to get this up and running:

* Firstly you need to make sure you have Intellij setup to automatically build your project.  To do this open up the preferences dialog and search for 'Build Project Automatically'.  Once found, tick the option.
* Then you need to setup and run a test suite.  This can be done via the 'Edit Configurations' dialog or simply by running a test or tests via the shortcut keys or project sidebar.
* Once you have run the test suite all you then need to do is click the toggle auto-test button and everytime IntelliJ detects a change to your code, it will build your project and execute your test suite.

It is important to remember that all this is doing is running the same test suite over and over again so make sure you are executing the right tests or you won't get the feedback you are looking for.  At the moment I have all my unit tests running on every change I make.  Unit tests are quick enough to make this easy to do but you might want to be careful about running things like integration tests where they can take longer.  You certainly don't want to slow down your development/test cycle by doing this.

## Summary

All in all this has been a positive change to my development cycle and I will be trialing this for a little longer.  It will be interesting to see at what point this becomes impractical based on the number/type of tests run on every change.

I think one of the reasons I might not have spotted this button before is because unfortunately it isn't accessible via keyboard only shortcuts.  I don't use the mouse much while developing as it slows me down but the toggle auto-test feature isn't accessible via a keyboard shortcut or and Action command.

Hopefully they will add this in a future release.  I have logged an [feature improvement](https://youtrack.jetbrains.com/issue/IDEA-186112) in the IntelliJ tracker so who knows.
