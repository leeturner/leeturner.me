---
title: Outputting the result of a mockMvc call
date: 2021-09-12T10:20:08Z
description: How to output the result of a mockmvc call to help with debugging
slug: outputting-result-of-mockmvc
toc: true
featured: board-2450236_640.jpg
featuredalt: Outputting the result of a mockMvc call
featuredpath: /images/blog/common
type: post
author: Lee Turner
tags:
- spring
- spring boot 
- mockmvc 
- testing 
- junit
- reference
---

This post falls into the category of something I always forget and need to Google.  

When running spring integration tests and using mockMvc, it can often be useful to see the output of the call in the console to help with debugging.  This can be done by adding a `MockMvcResultsHandlers.print()` call to the chain like in the following example.

This:

```java
@Test  
void getStatementsThrowABadRequestWhenCookiesNotPresent() throws Exception {  
   mockMvc.perform(get("/statements")  
	 .headers(getHeaders())  
	 .cookie(getCookies())  
	 .contentType(MediaType.APPLICATION_JSON));
	 .andExpect(status().isBadRequest())  
	 .andExpect(jsonPath("$.status", is(400)))  
	 .andExpect(jsonPath("$.type", is("BAD_REQUEST")))  
	 .andExpect(jsonPath("$.errors.length()", is(0)));
}
```

Becomes this:

```java
@Test  
void getStatementsThrowABadRequestWhenCookiesNotPresent() throws Exception {  
   mockMvc.perform(get("/statements")  
	 .headers(getHeaders())  
	 .cookie(getCookies())  
	 .contentType(MediaType.APPLICATION_JSON));
	 .andExpect(status().isBadRequest())  
	 .andExpect(jsonPath("$.status", is(400)))  
	 .andExpect(jsonPath("$.type", is("BAD_REQUEST")))  
	 .andExpect(jsonPath("$.errors.length()", is(0)))
	 .andDo(MockMvcResultHandlers.print());
}
```

Along with all the other output from the test, there will be the `json` response from the call to the endpoint.
