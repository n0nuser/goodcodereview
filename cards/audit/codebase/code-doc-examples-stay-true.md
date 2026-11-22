---
id: code-doc-examples-stay-true
level: codebase
tags: [maintainability, docs, testing]
severity: discuss
status: draft
lacks: orgs, Rust and Go (Google) run doc examples as tests; Kubernetes and Spotify embed examples from source files; each clause has two organisations
lang: core
applies_when: Auditing docs, READMEs or doc comments that contain code samples.
tool_gate: Rust `cargo test --doc`, Go example functions, Python `doctest`, or a build step that includes samples from files that CI compiles.
borrowed_from:
  - https://doc.rust-lang.org/rustdoc/write-documentation/documentation-tests.html
  - https://go.dev/blog/examples
  - https://kubernetes.io/docs/contribute/style/hugo-shortcodes/
  - https://backstage.io/blog/2020/09/08/announcing-tech-docs
---

**Rule.** Run each code example in the docs as a test, or include it from a source file that CI builds, instead of pasting it.

**Why.** A pasted example drifts from the API it shows, and readers copy it. A tested or included example fails the build when the API changes.

**FAIL**

```text
README.md: a 12-line ```python block pasted by hand, never run
```

**PASS**

```text
README.md: {% include examples/quickstart.py %}   # tests/test_examples.py runs it
```

**Counterpoint.** "Some samples are fragments that cannot run." Mark those as fragments and keep them short. The rule is for samples a reader will copy and run.
