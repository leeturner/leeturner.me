---
title: WireMock 3.6.0 - New Array Helpers
subTitle: How to use the new array helpers in WireMock 3.6.0
description: WireMock 3.6.0 has been released with new array helpers. This post shows how to use them.
date: 2024-05-24T10:00:00Z
slug: wiremock-3-6-0-array-helpers
layout: post
author: Lee Turner
showtoc: true
comments: true
tags:
  - wiremock
  - response-templating
---

WireMock version 3.6.0 has [just been released](https://www.wiremock.io/post/wiremock-3-6-0-released) containing a
number of new features, bug fixes and dependency updates. Version 3.6.0 has a number of new template helpers to make
working with arrays much easier when using Response Templating.

In this post we are going to explore the new array helpers and how to use them.

## arrayAdd - add elements to an array

The `arrayAdd` helper can be used to add elements to an array based on a position value or the start or end keywords. If
no position is specified, the element will be added to end of the array.

```handlebars
{{arrayAdd (array 1 'three') 2 position=1}} // [1, 2, three]
{{arrayAdd (array 1 'three') 2 position='start'}} // [2, 1, three]
{{arrayAdd (array 1 'three') 2 position='end'}} // [1, three, 2]
{{arrayAdd (array 1 'three') 2}} // [1, three, 2]
```

## arrayRemove - remove elements from an array

The `arrayRemove` helper can be used to remove elements from an array based on a position value or the start or end
keywords. If no position is specified, the last element will be removed.

```handlebars
{{arrayRemove (array 1 2 'three') position=1}} // [1, three]
{{arrayRemove (array 1 2 'three') position='start'}} // [2, three]
{{arrayRemove (array 1 2 'three') position='end'}} // [1, 2]
{{arrayRemove (array 1 2 'three')}} // [1, 2]
```

## arrayJoin - join elements of an array

The `arrayJoin` helper will concatenate the values passed to it with the separator specified

```handlebars
{{arrayJoin ',' (array 'One' 'Two' 'Three')}} // One,Two,Three
{{arrayJoin ' - ' 'a' 'b' 'c'}} // a - b - c
{{arrayJoin ' , ' (range 1 5)}} // 1, 2, 3, 4, 5
{{arrayJoin ':' (array 'One' 'Two' 'Three')}} // One:Two:Three
```

`arrayJoin` will allow you to specify a prefix and suffix to be added to the start and end of the result

```handlebars
{{arrayJoin ',' (array '1' '2' '3') prefix='[' suffix=']'}} // [1,2,3]
{{arrayJoin ' * ' (array 1 2 3) prefix='(' suffix=')'}} // (1 * 2 * 3)
```

`arrayJoin` can also be used as a block helper

```handlebars
// first parse some json
{{#parseJson 'myThings'}}
    [ { "id": 1,
    "name": "One" },
    { "id": 2,
    "name": "Two" },
    { "id": 3,
    "name": "Three" }]
{{/parseJson}}
[{{#arrayJoin ', ' myThings as |item|}}
    {
    "name{{item.id}}": "{{item.name}}"
    }
{{/arrayJoin}}] // [{ "name1": "One" }, { "name2": "Two" }, { "name3": "Three" }]
```

The last example shows how you can use `arrayJoin` as a block helper to iterate over an array of objects and output
valid JSON. Before the `arrayJoin` helper was released outputting JSON from an array of objects was a little more
clunky because you had to use the `#each` helper and then check if you were on the last item to avoid adding a comma:

```handlebars
{{#each myThings as |item|}}
    {
    "name{{item.id}}": "{{item.name}}"
    }{{#not @last}},{{/not}}
{{/each}} 
```

The new `arrayJoin` helper makes this much cleaner and easier to read. You can download and get started with WireMock
3.6.0 from the [WireMock website](https://wiremock.org/docs/download-and-installation/). The full list of new features
and bug fixes can be found in the [release notes](https://www.wiremock.io/post/wiremock-3-6-0-released). If you have
any questions or need help with the new array helpers, join us in
the [WireMock Community Slack](https://slack.wiremock.org/).

## Download the PDF

You can download the content of this post in PDF format below:

[![WireMock 3.6.0 - New Array Helpers](/img/blog/2024-05-27-wiremock-3-6-0-array-helpers/wiremock-3-6-0-array-helpers.png)](/pdf/2024-05-27-wiremock-3-6-0-array-helpers/wiremock-3-6-0-array-helpers.pdf)

