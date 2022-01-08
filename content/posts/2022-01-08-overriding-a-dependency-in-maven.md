---
title: Overriding a Parent Dependency in Maven
date: 2022-01-08T10:20:08Z
description: How to override a parent dependency in maven
slug: overriding-a-dependency-in-maven.md
toc: true
type: post
author: Lee Turner
tags:
- mvn
- maven
- spring
- spring boot
- dependency 
- snyk
---

This weekend I am spending some time taking a look at my [Snyk Dashboard](https://snyk.io) and upgrading a few dependencies in old projects

The main thing I wanted to take a look at was the recent RCE (Remote Code Execution) vulnerability that was disclosed in the h2 database.  This is a similar `JNDI` exploit to the one that impacted Log4j in December last year (called Log4Shell).  You can read more about Log4Shell on the [Snyk resources page](https://snyk.io/log4j-vulnerability-resources/) and find details of the recent h2 RCE on the [Snyk Vulnerability Database](https://security.snyk.io/vuln/SNYK-JAVA-COMH2DATABASE-2331071)

As you can see from the dependency scan, I am using version `1.4.200` and this dependency is introduced via the `spring-boot-starter-parent` version `2.5.4`

![Snyk H2 CVE](/img/blog/2022-01-08-overriding-a-dependency-in-maven/snyk-cwe-h2.png "Snyk H2 CWE")


## 1. Update the Parent Dependencies

The first thing to do is to make sure we are using the latest version of the parent.  This won't actually fix the h2 issue given Spring Boot `2.6.2` was released before the h2 vulnerability was disclosed but using the latest parent will [update](https://github.com/spring-projects/spring-boot/releases/tag/v2.6.2) a load of other dependencies as well.

```xml
  <parent>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-parent</artifactId>
    <version>2.6.2</version>
    <relativePath/>
  </parent>
```

## 2. Override the H2 dependency

The next step is to override the h2 dependency provided by Sprint Boot and upgrade it to the version that fixes RCE vulnerability - `2.0.206`.

To do this we simply add the version of h2 we want to the `<properties>` element in the `pom.xml`:

```xml
<properties>
    <h2.version>2.0.206</h2.version>
</properties>
```

If you use an IDE like IntelliJ you should now be able to see the updated dependency in your dependencies' manager:

![IntelliJ Dependencies](/img/blog/2022-01-08-overriding-a-dependency-in-maven/intellij-deps.png "IntelliJ Dependencies")

Or, if you want to do it on the command line `mvn dependency:tree` is your friend:

```shell
mvn dependency:tree                                                  
[INFO] Scanning for projects...
[INFO] 
[INFO] ------------------------------------------------------------------------
[INFO] Building spring-boot-graphql-example 0.0.1-SNAPSHOT
[INFO] ------------------------------------------------------------------------
[INFO] 
[INFO] --- maven-dependency-plugin:3.2.0:tree (default-cli) @ spring-boot-graphql-example ---
[INFO] com.leeturner.graphql:spring-boot-graphql-example:jar:0.0.1-SNAPSHOT
[INFO] +- com.graphql-java-kickstart:graphql-spring-boot-starter:jar:12.0.0:compile
[INFO] |  \- com.graphql-java-kickstart:graphql-spring-boot-autoconfigure:jar:12.0.0:compile
[INFO] |     +- com.graphql-java-kickstart:graphql-java-tools:jar:11.1.2:compile
[INFO] |     |  +- org.jetbrains.kotlin:kotlin-stdlib:jar:1.6.10:compile
[INFO] |     |  |  +- org.jetbrains:annotations:jar:13.0:compile
[INFO] |     |  |  \- org.jetbrains.kotlin:kotlin-stdlib-common:jar:1.6.10:compile
[INFO] |     |  +- org.jetbrains.kotlin:kotlin-reflect:jar:1.6.10:compile
[INFO] |     |  +- org.jetbrains.kotlinx:kotlinx-coroutines-jdk8:jar:1.5.2:compile
[INFO] |     |  |  +- org.jetbrains.kotlinx:kotlinx-coroutines-core-jvm:jar:1.5.2:compile
[INFO] |     |  |  \- org.jetbrains.kotlin:kotlin-stdlib-jdk8:jar:1.6.10:compile
[INFO] |     |  |     \- org.jetbrains.kotlin:kotlin-stdlib-jdk7:jar:1.6.10:compile
[INFO] |     |  +- org.jetbrains.kotlinx:kotlinx-coroutines-core:jar:1.5.2:compile
[INFO] |     |  +- org.jetbrains.kotlinx:kotlinx-coroutines-reactive:jar:1.5.2:compile
[INFO] |     |  +- com.fasterxml.jackson.core:jackson-core:jar:2.13.1:compile
[INFO] |     |  +- com.fasterxml.jackson.module:jackson-module-kotlin:jar:2.13.1:compile
[INFO] |     |  \- org.apache.commons:commons-lang3:jar:3.12.0:compile
[INFO] |     +- com.graphql-java-kickstart:graphql-kickstart-spring-support:jar:12.0.0:compile
[INFO] |     +- com.graphql-java-kickstart:graphql-kickstart-spring-webflux:jar:12.0.0:compile
[INFO] |     +- com.graphql-java:graphql-java-extended-scalars:jar:17.0:compile
[INFO] |     +- com.graphql-java-kickstart:graphql-java-kickstart:jar:12.0.0:compile
[INFO] |     |  \- com.fasterxml.jackson.core:jackson-annotations:jar:2.13.1:compile
[INFO] |     +- com.graphql-java-kickstart:graphql-java-servlet:jar:12.0.0:compile
[INFO] |     |  +- javax.servlet:javax.servlet-api:jar:4.0.1:compile
[INFO] |     |  \- javax.websocket:javax.websocket-api:jar:1.1:compile
[INFO] |     +- com.graphql-java:graphql-java:jar:17.3:compile
[INFO] |     |  +- com.graphql-java:java-dataloader:jar:3.1.0:compile
[INFO] |     |  +- org.reactivestreams:reactive-streams:jar:1.0.3:compile
[INFO] |     |  \- org.antlr:antlr4-runtime:jar:4.9.2:runtime
[INFO] |     +- io.github.graphql-java:graphql-java-annotations:jar:9.1:compile
[INFO] |     |  \- javax.validation:validation-api:jar:2.0.1.Final:compile
[INFO] |     +- org.reflections:reflections:jar:0.9.11:runtime
[INFO] |     |  +- com.google.guava:guava:jar:20.0:runtime
[INFO] |     |  \- org.javassist:javassist:jar:3.21.0-GA:runtime
[INFO] |     +- org.springframework.boot:spring-boot-starter-validation:jar:2.6.2:runtime
[INFO] |     |  \- org.hibernate.validator:hibernate-validator:jar:6.2.0.Final:runtime
[INFO] |     |     \- jakarta.validation:jakarta.validation-api:jar:2.0.2:runtime
[INFO] |     +- org.apache.commons:commons-text:jar:1.9:runtime
[INFO] |     \- org.springframework:spring-webflux:jar:5.3.14:runtime
[INFO] |        \- io.projectreactor:reactor-core:jar:3.4.13:runtime
[INFO] +- com.graphql-java-kickstart:graphiql-spring-boot-starter:jar:11.1.0:runtime
[INFO] |  \- com.graphql-java-kickstart:graphiql-spring-boot-autoconfigure:jar:11.1.0:runtime
[INFO] |     \- com.graphql-java-kickstart:graphql-kickstart-starter-utils:jar:11.1.0:runtime
[INFO] +- org.springframework.boot:spring-boot-starter-data-jpa:jar:2.6.2:compile
[INFO] |  +- org.springframework.boot:spring-boot-starter-aop:jar:2.6.2:compile
[INFO] |  |  +- org.springframework:spring-aop:jar:5.3.14:compile
[INFO] |  |  \- org.aspectj:aspectjweaver:jar:1.9.7:compile
[INFO] |  +- org.springframework.boot:spring-boot-starter-jdbc:jar:2.6.2:compile
[INFO] |  |  +- com.zaxxer:HikariCP:jar:4.0.3:compile
[INFO] |  |  \- org.springframework:spring-jdbc:jar:5.3.14:compile
[INFO] |  +- jakarta.transaction:jakarta.transaction-api:jar:1.3.3:compile
[INFO] |  +- jakarta.persistence:jakarta.persistence-api:jar:2.2.3:compile
[INFO] |  +- org.hibernate:hibernate-core:jar:5.6.3.Final:compile
[INFO] |  |  +- org.jboss.logging:jboss-logging:jar:3.4.2.Final:compile
[INFO] |  |  +- net.bytebuddy:byte-buddy:jar:1.11.22:compile
[INFO] |  |  +- antlr:antlr:jar:2.7.7:compile
[INFO] |  |  +- org.jboss:jandex:jar:2.2.3.Final:compile
[INFO] |  |  +- com.fasterxml:classmate:jar:1.5.1:compile
[INFO] |  |  +- org.hibernate.common:hibernate-commons-annotations:jar:5.1.2.Final:compile
[INFO] |  |  \- org.glassfish.jaxb:jaxb-runtime:jar:2.3.5:compile
[INFO] |  |     +- org.glassfish.jaxb:txw2:jar:2.3.5:compile
[INFO] |  |     +- com.sun.istack:istack-commons-runtime:jar:3.0.12:compile
[INFO] |  |     \- com.sun.activation:jakarta.activation:jar:1.2.2:runtime
[INFO] |  +- org.springframework.data:spring-data-jpa:jar:2.6.0:compile
[INFO] |  |  +- org.springframework.data:spring-data-commons:jar:2.6.0:compile
[INFO] |  |  +- org.springframework:spring-orm:jar:5.3.14:compile
[INFO] |  |  +- org.springframework:spring-context:jar:5.3.14:compile
[INFO] |  |  +- org.springframework:spring-tx:jar:5.3.14:compile
[INFO] |  |  +- org.springframework:spring-beans:jar:5.3.14:compile
[INFO] |  |  \- org.slf4j:slf4j-api:jar:1.7.32:compile
[INFO] |  \- org.springframework:spring-aspects:jar:5.3.14:compile
[INFO] +- org.springframework.boot:spring-boot-starter-web:jar:2.6.2:compile
[INFO] |  +- org.springframework.boot:spring-boot-starter:jar:2.6.2:compile
[INFO] |  |  +- org.springframework.boot:spring-boot-starter-logging:jar:2.6.2:compile
[INFO] |  |  |  +- ch.qos.logback:logback-classic:jar:1.2.9:compile
[INFO] |  |  |  |  \- ch.qos.logback:logback-core:jar:1.2.9:compile
[INFO] |  |  |  +- org.apache.logging.log4j:log4j-to-slf4j:jar:2.17.0:compile
[INFO] |  |  |  |  \- org.apache.logging.log4j:log4j-api:jar:2.17.0:compile
[INFO] |  |  |  \- org.slf4j:jul-to-slf4j:jar:1.7.32:compile
[INFO] |  |  +- jakarta.annotation:jakarta.annotation-api:jar:1.3.5:compile
[INFO] |  |  \- org.yaml:snakeyaml:jar:1.29:compile
[INFO] |  +- org.springframework.boot:spring-boot-starter-json:jar:2.6.2:compile
[INFO] |  |  +- com.fasterxml.jackson.core:jackson-databind:jar:2.13.1:compile
[INFO] |  |  +- com.fasterxml.jackson.datatype:jackson-datatype-jdk8:jar:2.13.1:compile
[INFO] |  |  +- com.fasterxml.jackson.datatype:jackson-datatype-jsr310:jar:2.13.1:compile
[INFO] |  |  \- com.fasterxml.jackson.module:jackson-module-parameter-names:jar:2.13.1:compile
[INFO] |  +- org.springframework.boot:spring-boot-starter-tomcat:jar:2.6.2:compile
[INFO] |  |  +- org.apache.tomcat.embed:tomcat-embed-core:jar:9.0.56:compile
[INFO] |  |  +- org.apache.tomcat.embed:tomcat-embed-el:jar:9.0.56:compile
[INFO] |  |  \- org.apache.tomcat.embed:tomcat-embed-websocket:jar:9.0.56:compile
[INFO] |  +- org.springframework:spring-web:jar:5.3.14:compile
[INFO] |  \- org.springframework:spring-webmvc:jar:5.3.14:compile
[INFO] |     \- org.springframework:spring-expression:jar:5.3.14:compile
[INFO] +- org.springframework.boot:spring-boot-devtools:jar:2.6.2:runtime (optional) 
[INFO] |  +- org.springframework.boot:spring-boot:jar:2.6.2:compile
[INFO] |  \- org.springframework.boot:spring-boot-autoconfigure:jar:2.6.2:compile
[INFO] +- com.h2database:h2:jar:2.0.206:runtime
[INFO] +- org.springframework.boot:spring-boot-starter-test:jar:2.6.2:test
[INFO] |  +- org.springframework.boot:spring-boot-test:jar:2.6.2:test
[INFO] |  +- org.springframework.boot:spring-boot-test-autoconfigure:jar:2.6.2:test
[INFO] |  +- com.jayway.jsonpath:json-path:jar:2.6.0:test
[INFO] |  |  \- net.minidev:json-smart:jar:2.4.7:test
[INFO] |  |     \- net.minidev:accessors-smart:jar:2.4.7:test
[INFO] |  |        \- org.ow2.asm:asm:jar:9.1:test
[INFO] |  +- jakarta.xml.bind:jakarta.xml.bind-api:jar:2.3.3:compile
[INFO] |  |  \- jakarta.activation:jakarta.activation-api:jar:1.2.2:compile
[INFO] |  +- org.assertj:assertj-core:jar:3.21.0:test
[INFO] |  +- org.hamcrest:hamcrest:jar:2.2:test
[INFO] |  +- org.junit.jupiter:junit-jupiter:jar:5.8.2:test
[INFO] |  |  +- org.junit.jupiter:junit-jupiter-api:jar:5.8.2:test
[INFO] |  |  |  +- org.opentest4j:opentest4j:jar:1.2.0:test
[INFO] |  |  |  +- org.junit.platform:junit-platform-commons:jar:1.8.2:test
[INFO] |  |  |  \- org.apiguardian:apiguardian-api:jar:1.1.2:test
[INFO] |  |  +- org.junit.jupiter:junit-jupiter-params:jar:5.8.2:test
[INFO] |  |  \- org.junit.jupiter:junit-jupiter-engine:jar:5.8.2:test
[INFO] |  |     \- org.junit.platform:junit-platform-engine:jar:1.8.2:test
[INFO] |  +- org.mockito:mockito-core:jar:4.0.0:test
[INFO] |  |  +- net.bytebuddy:byte-buddy-agent:jar:1.11.22:test
[INFO] |  |  \- org.objenesis:objenesis:jar:3.2:test
[INFO] |  +- org.mockito:mockito-junit-jupiter:jar:4.0.0:test
[INFO] |  +- org.skyscreamer:jsonassert:jar:1.5.0:test
[INFO] |  |  \- com.vaadin.external.google:android-json:jar:0.0.20131108.vaadin1:test
[INFO] |  +- org.springframework:spring-core:jar:5.3.14:compile
[INFO] |  |  \- org.springframework:spring-jcl:jar:5.3.14:compile
[INFO] |  +- org.springframework:spring-test:jar:5.3.14:test
[INFO] |  \- org.xmlunit:xmlunit-core:jar:2.8.4:test
[INFO] \- com.graphql-java-kickstart:graphql-spring-boot-starter-test:jar:12.0.0:test
[INFO]    \- com.graphql-java-kickstart:graphql-spring-boot-test-autoconfigure:jar:12.0.0:test
[INFO]       +- com.graphql-java-kickstart:graphql-spring-boot-test:jar:12.0.0:test
[INFO]       |  \- org.awaitility:awaitility:jar:4.1.1:test
[INFO]       +- org.springframework.boot:spring-boot-starter-actuator:jar:2.6.2:test
[INFO]       |  +- org.springframework.boot:spring-boot-actuator-autoconfigure:jar:2.6.2:test
[INFO]       |  |  \- org.springframework.boot:spring-boot-actuator:jar:2.6.2:test
[INFO]       |  \- io.micrometer:micrometer-core:jar:1.8.1:test
[INFO]       |     +- org.hdrhistogram:HdrHistogram:jar:2.1.12:test
[INFO]       |     \- org.latencyutils:LatencyUtils:jar:2.0.3:test
[INFO]       \- org.springframework.boot:spring-boot-starter-websocket:jar:2.6.2:test
[INFO]          +- org.springframework:spring-messaging:jar:5.3.14:test
[INFO]          \- org.springframework:spring-websocket:jar:5.3.14:test
[INFO] ------------------------------------------------------------------------
[INFO] BUILD SUCCESS
[INFO] ------------------------------------------------------------------------
[INFO] Total time: 2.413 s
[INFO] Finished at: 2022-01-08T15:03:49Z
[INFO] Final Memory: 29M/114M
[INFO] ------------------------------------------------------------------------
```

## 3. Validate the Update

We can now validate we have mitigated the vulnerability by checking the [Snyk Vulnerability Scanner](https://plugins.jetbrains.com/plugin/10972-snyk-vulnerability-scanner) Intellij plugin:

### Before

![Snyk Vulnerability Scanner Before](/img/blog/2022-01-08-overriding-a-dependency-in-maven/snyk-vuln-scan-before.png "Snyk Vulnerability Scanner Before")

### After

![Snyk Vulnerability Scanner After](/img/blog/2022-01-08-overriding-a-dependency-in-maven/snyk-vuln-scan-after.png "Snyk Vulnerability Scanner After")
