---
id: fn-deprecation-names-version-and-replacement
level: function
tags: [compatibility, maintainability, docs]
severity: should-fix
status: stable
lang: core
applies_when: A diff marks a function, class, option or setting as deprecated.
tool_gate: A deprecation helper that requires `since` and `replacement` arguments, or a lint on `@deprecated` without both.
note: Oracle (Java) and WordPress state both halves in the doc comment; Django requires a warning class that names the removal version, and says the upgrade path goes in the docs. Python, Angular, Node.js and Rust state parts of it
borrowed_from:
  - https://docs.djangoproject.com/en/dev/internals/contributing/writing-code/submitting-patches/
  - https://docs.oracle.com/en/java/javase/21/docs/specs/javadoc/doc-comment-spec.html
  - https://developer.wordpress.org/coding-standards/inline-documentation-standards/php/
---

**Rule.** Say in a deprecation notice which version deprecated it and what replaces it.

**Why.** A bare "deprecated" tells callers to stop but not what to do. The version lets them judge how long they have, and the replacement is the migration. Name the removal version too when you have one.

**FAIL**

```java
/** @deprecated Use something else. */
```

**PASS**

```java
/** @deprecated Since 3.2, use {@link #fetchAll()}. Removed in 4.0. */
```

**Counterpoint.** "We don't know the removal date." Then name the version it was deprecated in and the replacement, and leave the removal version out until it is decided.
