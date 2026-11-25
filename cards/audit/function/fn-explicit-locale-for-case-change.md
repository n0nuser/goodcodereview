---
id: fn-explicit-locale-for-case-change
level: function
tags: [correctness, i18n]
severity: should-fix
status: stable
lang: core
applies_when: The code changes the case of a string that a program reads (an identifier, header name or protocol key), in a runtime whose default depends on the machine's locale, such as Java, Kotlin or .NET.
tool_gate: none
note: Oracle, Google (Android) and Microsoft back the case-change Rule. Number formatting and parsing has Google and Microsoft only, so it sits in the Why. Rust's to_lowercase is locale independent, so the rule does not apply there
borrowed_from:
  - https://docs.oracle.com/en/java/javase/21/docs/api/java.base/java/lang/String.html
  - https://developer.android.com/reference/java/util/Locale
  - https://learn.microsoft.com/en-us/dotnet/standard/base-types/best-practices-strings
---

**Rule.** Change the case of a machine-read string with an explicit root or invariant locale, never the default one.

**Why.** The default locale is whatever the machine or user has set. In Turkish, `"TITLE".toLowerCase()` gives `"tıtle"` in Java, so a header lookup or a key match that works on one host fails on another. The same applies to numbers: formatting a number with the default locale writes a decimal comma on some machines, and the program that reads the file cannot parse it. Use the locale of the person only for text shown to that person.

**FAIL**

```java
String header = name.toLowerCase();
```

```csharp
var key = name.ToUpper();
```

**PASS**

```java
String header = name.toLowerCase(Locale.ROOT);
```

```csharp
var key = name.ToUpperInvariant();
```

**Counterpoint.** "Our users and servers are all in en-US." The default is a property of each host, and a laptop, a container image or one customer in Istanbul is enough to change it. The explicit argument costs one word. For text a person reads, such as a name in a heading, the user's locale is the right one.
