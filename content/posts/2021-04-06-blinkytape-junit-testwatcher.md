---
title: BlinkyTape JUnit Testwatcher API Implementation
date: 2021-04-06T10:20:08Z
description: This implementation demonstrates a Junit 5 TestWatcher API implementation that hooks up your tests to a BlinkyTape LED strip.
slug: blinkytape-junit-testwatcher
type: post
author: Lee Turner
tags:
- kotlin 
- junit 
- blinkytape 
- blinky 
- junit5 
- testwatcher
---

[Every so often](/posts/building-a-camel-case-junit5-displaynamegenerator/) I like to have a play around with a part of [ Junit ](https://junit.org) that I haven't used before, and I recently decided to look into the [TestWatcher API](https://junit.org/junit5/docs/5.5.1/api/org/junit/jupiter/api/extension/TestWatcher.html).

I have to admit that I have been meaning to play with this for quite a while now.... I just haven't really found a good use-case for it. Given that I decided to quit trying to find a good use-case and implement something nerdy instead.  

Stretched across the back of the desk in front of me is a [ BlinkyTape ](https://shop.blinkinlabs.com/collections/frontpage/products/blinkytape-basic_) attached to my usb hub.  Most of the time the BlinkyTape is just used for a bit of subtle lighting behind my monitor but while looking into the Junit TestWatcher API, it suddenly hit me.... maybe I could combine the two.

I already had a [bit of code](https://github.com/leeturner/night-fever) to interact directly with the BlinkyTape so all I needed to do was figure out how to tracks the success, failure or whether a test is disabled.  If I could do that I could then turn the BlinkyTape green, red or orange.

I put together a simple Kotlin implementation of the TestWatcher API that adds a test result status to a list:

```kotlin
class BlinkyTapeTestWatcher : TestWatcher, AfterAllCallback {

    private val testResultsStatus = mutableListOf<TestResultStatus>()

    override fun testDisabled(context: ExtensionContext, reason: Optional<String>) {
        this.testResultsStatus.add(TestResultStatus.DISABLED)
    }

    override fun testSuccessful(context: ExtensionContext) {
        this.testResultsStatus.add(TestResultStatus.SUCCESS)
    }

    override fun testAborted(context: ExtensionContext, cause: Throwable?) {
        this.testResultsStatus.add(TestResultStatus.ABORTED)
    }

    override fun testFailed(context: ExtensionContext, cause: Throwable?) {
        this.testResultsStatus.add(TestResultStatus.FAILED)
    }

    override fun afterAll(extensionContext: ExtensionContext) {
        // first lets check to see if we have any test failures so we can leave the blinky tape as red
        if (this.testResultsStatus.any { it == TestResultStatus.FAILED }) {
            this.renderFrame(RED_BLINKY_TAPE_FRAME)
            return
        }

        // if no test failures then we can take a look to see if there are any disabled tests.  If there are then
        // we can set the blinky tape to orange
        if (this.testResultsStatus.any { it == TestResultStatus.DISABLED }) {
            this.renderFrame(ORANGE_BLINKY_TAPE_FRAME)
            return
        }

        // if no failures or disabled tests then we can set the blinky tape to green
        if (this.testResultsStatus.any { it == TestResultStatus.SUCCESS }) {
            this.renderFrame(GREEN_BLINKY_TAPE_FRAME)
            return
        }
    }

    private fun renderFrame(frame: BlinkyTapeFrame) {
        val controller = BlinkyTapeController()
        controller.renderFrame(frame)
        controller.close()
    }

    companion object {
        val ORANGE_BLINKY_TAPE_FRAME = BlinkyTapeFrame(defaultColour = Color.ORANGE)
        val RED_BLINKY_TAPE_FRAME = BlinkyTapeFrame(defaultColour = Color.RED)
        val GREEN_BLINKY_TAPE_FRAME = BlinkyTapeFrame(defaultColour = Color.GREEN)
    }

    private enum class TestResultStatus {
        SUCCESS, ABORTED, FAILED, DISABLED
    }
}
```

The `BlinkyTapeTestWatcher` class also implements the `AfterAllCallback` interface allows us to override a method called `afterAll` that is executed when all the tests have finished.

The `afterAll` method performs 3 checks:

1. If any of the tests have failed it renders the BlinkyTape as all red
1. If non of the tests have failed but there were disabled tests it renders the BlinkyTape as all orange
1. If all of the tests pass then it renders the BlinkyTape as all green

All in all it seemed to work out pretty well.  I uploaded the repo to github if you wanted to play around with this yourself - https://github.com/leeturner/BlinkyTapeTestWatcher

I uploaded a short video of this in action:

<iframe width="560" height="315" src="https://www.youtube.com/embed/xzw-NS8ua_c" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>
