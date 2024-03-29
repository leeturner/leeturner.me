---
title: Building a Camel Case @DisplayNameGenerator For JUnit 5
date: 2019-02-10T22:09:08Z
description: I am loving the new JUnit 5 features and the @DisplayName annotation seemed like a great idea.  However, it was a lot of work to write and keep updated - especially when you like to write descriptive test method names.  It just seemed like unnecessary duplication.  With the latest JUnit 5.4 release and the new @DisplayNameGenerator API all of that will change.
slug: building-a-camel-case-junit5-displaynamegenerator
layout: post
author: Lee Turner 
tags:
- tdd
- testing
- junit
aliases:
- /blog/2019/02/building-a-camel-case-junit5-displaynamegenerator.html
- /posts/building-a-camel-case-junit5-displaynamegenerator/
---
I think it is fair to say that [JUnit](https://junit.org) has been my go to unit testing framework for quite a while.  I have used [TestNG](https://testng.org/) on some pretty major projects where it was already in use (and it has some awesome features) but if I am building something from scratch, I will most likely reach for the JUnit maven dependencies.

This was solidified even further with the release of JUnit 5.  I won't go into any detail here of what the major differences are between version 4 and 5 because there are loads of great articles on the web about this already.  However, some of my favourites are:

* New asserts - especially assertThrows()
* Assumptions
* More readable test descriptions with the @DisplayName annotation
* Tags
* Parameterised Tests
* Dynamic Tests (although I need to delve into this one a little more)

## The @DisplayName Annotation

The `@DisplayName` annotation seemed like a great idea - you add the annotation with a more readable description to your test class or methods and that gets displayed instead of the default class or method name in your test runner.  Something like this:

```java
@DisplayName("Tests that when updating your password, the two passwords submitted must match")
@Test
public void testWhenAnUpdatePasswordRequestIsSubmittedTheTwoPasswordsMustMatch{} {
	// test goes here
}
```

It was fun for a while but it quickly became a lot of work to write and keep updated - especially when you like to write descriptive test method names.  It just seemed like unnecessary duplication.  However, all of this might change with the latest JUnit 5.4 release and the new `@DisplayNameGenerator` API.

If you follow along on Twitter, you will have heard of the new `@DisplayNameGenerator` API before the 5.4 release.  Basically it would allow JUnit to determine a nice display name for your classes and tests from your class and method names without having to add the `@DisplayName` annotation.  Seemed like the best of both worlds to me.

When the [5.4 release announcement was made on twitter](https://twitter.com/junitteam/status/1093621376978747393) I setup a quick project and dived right in, but there was one big problem.  The only `@DisplayNameGenerator` provided in release 5.4 is a [ReplaceUnderscores](https://junit.org/junit5/docs/5.4.0/api/org/junit/jupiter/api/DisplayNameGenerator.ReplaceUnderscores.html) Generator which as you can imagine replaces the underscores in your class and method names with a space.  For example, the following:

```java
@DisplayNameGeneration(DisplayNameGenerator.ReplaceUnderscores.class)
public class Password_Reset_Tests {
    @Test
    public void test_When_An_Update_Password_Request_Is_Submitted_The_Two_Passwords_Must_Match{} {
      // test goes here
    }
}
```

Will output:

```
+-- Password Reset Test
	+-- test When An Update Password Request Is Submitted The Two Passwords Must Match
```

All well and good if you use underscores in your class and method names.  I tend to be more of a camel case kind of guy.  Underscores never really did it for me so this wasn't going to work out of the box.  The nice thing here is that the JUnit team give a [really good example](https://junit.org/junit5/docs/5.4.0/user-guide/index.html#writing-tests-display-name-generator) of implementing a new `DisplayNameGenerator` so I borrowed the code from their user guide and has a play with a new camel case generator.

All of the code discussed here can be found in [this github repo](https://github.com/leeturner/junit5-camel-case-emoji-display-name-generator).

## A Camel Case @DisplayNameGenerator

On the face of it putting a space before every capital letter in a class or method name isn't that hard.  It can all be achieved with a simple `replaceAll` regex.  Something like this which extends the `DisplayNameGenerator.Standard` built into JUnit 5.4:

```java
static class ReplaceCamelCase extends DisplayNameGenerator.Standard {
    public ReplaceCamelCase() {
    }

    public String generateDisplayNameForClass(Class<?> testClass) {
        return this.replaceCapitals(super.generateDisplayNameForClass(testClass));
    }

    public String generateDisplayNameForNestedClass(Class<?> nestedClass) {
        return this.replaceCapitals(super.generateDisplayNameForNestedClass(nestedClass));
    }

    public String generateDisplayNameForMethod(Class<?> testClass, Method testMethod) {
        return this.replaceCapitals(testMethod.getName());
    }

    private String replaceCapitals(String name) {
        name = name.replaceAll("([A-Z])", " $1");
        return name;
    }
}
```

This works for the most part but you very quickly see the benefit of having a single character that you need to replace like in the `ReplaceUnderscores`.  For example, the above implementation doesn't take into account numbers and will fail to put a space where you would expect one.  For example, this:

```java
@Test
void ifItIsDivisibleBy4ButNotBy100() {
	/// test goes here
}
```

Would render:

```
+-- if It Is Divisible By4 But Not By100
```

Not particularly ideal.  We also need to cater for numbers and not just individual numbers, we have to look for sequences of numbers and assume they are intended to be together.  Simple enough with another regex:

```java
static class ReplaceCamelCase extends DisplayNameGenerator.Standard {
    public ReplaceCamelCase() {
    }

    public String generateDisplayNameForClass(Class<?> testClass) {
        return this.replaceCapitals(super.generateDisplayNameForClass(testClass));
    }

    public String generateDisplayNameForNestedClass(Class<?> nestedClass) {
        return this.replaceCapitals(super.generateDisplayNameForNestedClass(nestedClass));
    }

    public String generateDisplayNameForMethod(Class<?> testClass, Method testMethod) {
        return this.replaceCapitals(testMethod.getName());
    }

    private String replaceCapitals(String name) {
        name = name.replaceAll("([A-Z])", " $1");
        name = name.replaceAll("([0-9]+)", " $1");
        return name;
    }
}
```

All in all this simple camel case `DisplayNameGenerator` works pretty well and generates something like this:

![Replace Camel Case Junit 5 Display Name Generator](/img/blog/2019-02-10-building-a-camel-case-junit5-displaynamegenerator/junit5-ReplaceCamelCase.png)

I will be playing around with this further to see if there are any other scenarios It doesn't cater for and updating accordingly.

## One Step Too Far......

I am going to leave this here for posterity's sake.  I am not proud of it but once I thought of it I couldn't help myself :)

One of the new things JUnit 5 allows is [emoji in your test names](https://twitter.com/sam_brannen/status/660595585288970240?lang=en).  This also applies to the `@DisplayName` annotation.  All I will say is that it doesn't take a great leap to extend the `ReplaceUnderscores` or `ReplaceCamelCase` Generators with one that replaces certain words with emoji.  Here is a little proof of concept using the example from the JUnit user guide:

```java
static class ReplaceCamelCaseEmojis extends ReplaceCamelCase {
    public ReplaceCamelCaseEmojis() {
    }

    public String generateDisplayNameForClass(Class<?> testClass) {
        return this.replaceWithEmojis(super.generateDisplayNameForClass(testClass));
    }

    public String generateDisplayNameForNestedClass(Class<?> nestedClass) {
        return this.replaceWithEmojis(super.generateDisplayNameForNestedClass(nestedClass));
    }

    public String generateDisplayNameForMethod(Class<?> testClass, Method testMethod) {
        return this.replaceWithEmojis(super.generateDisplayNameForMethod(testClass, testMethod));
    }

    private String replaceWithEmojis(String name) {
        name = name.replaceAll("Camel|camel", "\uD83D\uDC2B");
        name = name.replaceAll("Case|case", "\uD83D\uDCBC");
        name = name.replaceAll("Display|display", "\uD83D\uDCBB");
        name = name.replaceAll("Divisible|divisible", "\u2797");
        name = name.replaceAll("Year|year", "\uD83D\uDCC5");
        name = name.replaceAll("100", "\uD83D\uDCAF");
        return name;
    }
}
```

This generates something like this:

![Replace Camel Case Junit 5 Display Name Generator](/img/blog/2019-02-10-building-a-camel-case-junit5-displaynamegenerator/junit5-ReplaceCamelCaseEmoji.png)

You are very welcome :)

