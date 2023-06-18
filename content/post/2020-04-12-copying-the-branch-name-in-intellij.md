---
title: Copying A Branch Name In Intellij
date: 2020-04-12T18:09:08Z
description: How many times do you need to use the name of the branch you are currently working on?  Up until now I didn't know an easy way to copy the name into the clipboard
slug: copying-the-branch-name-in-intellij
layout: post
showtoc: false
author: Lee Turner 
tags:
- intellij
- reference
aliases:
  - /posts/copying-the-branch-name-in-intellij/
---
How many times do you need to use the name of the branch you are currently working on ?  Entering the name of the branch into your CI/CD system to deploy your feature branch into a staging environment, sending the name over email or internal messaging app to a co-worker who you are pair-programming with...

I seem to need to do this quite frequently over the course of a working week, and the place I always go to get the branch name is Intellij.  Up until a couple of days ago I longed for an easy way to simply copy the name of the current branch from the git branch list in the status bar.  It just seemed to make sense when there are already options like `remane`.  So, to achieve this I would select the `rename` option on the branch name I would like to copy and then just `Ctrl/Cmd+C` in the rename branch dialog.  Quite a few mouse clicks and keyboard presses, but it achieved the desired result in the end.

Fast forward to a couple of days ago when I heard that the new [2020.1 version of IntelliJ had been released](https://www.jetbrains.com/idea/whatsnew/#v20201-apr-9), and I thought I would look into this again - maybe with the aim of submitting a feature request. I did a quick bit of googling only to find this [issue had been submitted 5 years ago](https://youtrack.jetbrains.com/issue/IDEA-145798).  The interesting thing about that issue is that it was marked fixed with this comment added 6 months ago:

> Select current branch item in the Git | Branches popup menu (available from the status bar as well) and press Ctrl/Cmd+C.

I instantly tried it out, and it worked perfectly.  I wish I had known this over the past few years.  It would have saved me a few mouse clicks and keystrokes :)

Here is how it works:

![Copying The Branch Name In IntelliJ](/img/blog/2020-04-12-copying-the-branch-name-in-intellij/copy-branch-name.gif)
