---
title: Tooling Up - Implementing test && commit || revert (TCR) In IntelliJ
date: 2019-01-17T22:09:08Z
description: This post shows how I implemented a minimal test && commit || revert inside InelliJ - and when I say minimal I mean minimal.
slug: tooling-up-tcr-intellij
toc: true
author: Lee Turner 
tags:
- tooling
- tcr
- intellij
aliases:
- /blog/2019/01/tooling-up-tcr-intellij.html
---
Like many others, I have been reading about the new programming workflow introduced by [Kent Beck](https://twitter.com/KentBeck) called [test && commit || revert](https://medium.com/@kentbeck_7670/test-commit-revert-870bbd756864) (TCR)

When I first heard about it I had much the same response as Kent - why the hell would you want to do something like that?  That can't possibly work, my tests don't always pass when I am experimenting - I would lose my code if I did this.

## So what is test && commit || revert anyway?

The concept is extremely simple.  When your tests run successfully your code is committed, if your tests fail for any reason, your code is automatically reverted back to the state where the tests last passed.  Yes, this means that you can (and probably will) lose code - especially in the beginning when you are still playing around with this.

The easiest way to get your head around it is to watch it in action.  Take a look at this video by Kent Beck [demonstrating TCR](https://www.youtube.com/watch?v=ZrHBVTCbcE0)

So, what's the point ?  The idea is to make everything smaller - the amount of code you write between green test runs, your iterations around the test/dev/commit cycle and bigger problems broken down into smaller parts.  Of course, writing tests is a given here because it is what the whole workflow is based on but they don't always have to come first.

Most of the TCR implementations I have seen so far have been like in the video linked above, a single file implementation where the tests and the code are in the same file.  The problem I had is that I don't work like that.  I am a Java developer so most of my projects are based on Maven where the 'code' and the tests are kept in separate directories.  I also use IntelliJ as my main IDE so I wanted something that worked in that environment and not have to use a different editor and/or keep switching to the commandline.

On the flip side I didn't want to invest too much time in tooling up while I was still only playing with the workflow.  I effectively wanted as little as I could get away with so I could get up and running.  I then found another video by Kent Beck where he walks you through his [minimal TCR setup in VS Code](https://www.youtube.com/watch?v=IIKndRX5qHw).  That video ultimately gave me all I needed to set this up in IntelliJ.

## My minimal TCR implementation in IntelliJ

The first step was to find a way to get feedback on the success or failure of a test run.  As I said above, most of my day to day coding is done using Java and maven.  I can easily run my test suite using mavan on the command line so this is where I started looking first.  Well, it turns out that the maven command line (mvn) returns different status codes based on the success or failure of your tests.  This means I can run _mvn test_ on a project where the tests all pass and see the following:

```bash
[INFO] Tests run: 42, Failures: 0, Errors: 0, Skipped: 0
[INFO]
[INFO] ------------------------------------------------------------------------
[INFO] BUILD SUCCESS
[INFO] ------------------------------------------------------------------------
[INFO] Total time: 2.509 s
[INFO] Finished at: 2019-01-17T21:54:57Z
[INFO] Final Memory: 11M/309M
[INFO] ------------------------------------------------------------------------
>  night-fever git:(master) echo $?
0
```

And on a project where there are failing tests and see this:

```bash
[ERROR] Tests run: 42, Failures: 1, Errors: 0, Skipped: 0
[INFO]
[INFO] ------------------------------------------------------------------------
[INFO] BUILD FAILURE
[INFO] ------------------------------------------------------------------------
[INFO] Total time: 3.085 s
[INFO] Finished at: 2019-01-17T22:03:32Z
[INFO] Final Memory: 11M/309M
[INFO] ------------------------------------------------------------------------
[ERROR] Failed to execute goal org.apache.maven.plugins:maven-surefire-plugin:2.22.0:test (default-test) on project nightfever: There are test failures.

>  night-fever git:(master) echo $?
1
```

This means I can now use that status code to chain together a command much like the one Kent Beck uses in his VS Code video:
```bash
mvn test && git commit -am working || git reset --hard
```

OK, good start, I now have a command line TCR implementation working with maven.  Next step, how do I execute this from within IntelliJ?

My first try at this was to setup an *external tool* within IntelliJ.  This wasn't as easy as it sounds due to IntelliJ only accepting one command along with parameters.  There was also no way to chain multiple external tools together.  After a little bit of Googling I found an IntelliJ support article that talked about calling bash directly and passing the commands you want to call as a parameter.  The external tool edit window looks like this:

![IntelliJ External Tool Edit Screen](/images/blog/2019-01-17-tooling-up-tcr-intellij/intellij-external-tool-edit.png)

This worked pretty well, as you can see from the screen shot you can even set it to synchronise the files after execution of the tool so IntelliJ picks up any reverts that might have happened.

That in and of itself would probably be enough for a minimal TCR implementation inside IntelliJ.  However, there are other options along the same theme which might work better for you depending on how you prefer to code.  There is a plugin written by Jet Brains called [File Watchers](https://www.jetbrains.com/help/idea/using-file-watchers.html) that allows you to automatically run a command when you change or save a file. This is how I ultimately had this setup:

![IntelliJ File Watcher Edit Screen](/images/blog/2019-01-17-tooling-up-tcr-intellij/intellij-file-watcher-edit.png)

You will notice that I un-ticked the option *Auto-save edited files to trigger the watcher*.  I turned that off so the File Watcher starts upon save (File | Save All) or when you move the focus from IntelliJ IDEA (on frame deactivation).  The main reason being that I didn't want the File Watcher to kick in when I was part way through a change and IntelliJ decided to auto-save the file.

## What Next ?

All of the above works really well but it obviously has some downsides.  I am effectively running the whole test suite via maven and although this ran pretty fast on my machine with a relatively small project, it would really slow things down when the project grew to any reasonable size.  That would make this solution effectively unusable at that point.  Thankfully IntelliJ was quite quick at syncing with the file system when a revert happened so hopefully that won't be a problem moving forwards.

My ultimate solution would be to have this type of functionality integrated with the Run/Debug test runner inside IntelliJ.  I could then use my standard keyboard shortcuts to run individual test methods, a whole test class or a whole test suite and it would trigger the test && commit || revert workflow based on the results in a much more integrated way.  I imagine this would require a plugin to make this happen.

I'll be continuing to play with TCR to see how far I can stretch it and whether is it applicable to all types of projects.  That is the topic for another article though.
