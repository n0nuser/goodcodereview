---
id: code-doc-examples-stay-true
level: codebase
tags: [maintainability, docs, testing]
severity: discuss
status: stable
note: Rust, Go (Google) and Elixir state running doc examples as tests. Including examples from a file that CI builds has two (Kubernetes, Microsoft), so it sits in the Why
lang: core
applies_when: Auditing docs, READMEs or doc comments that contain code samples.
tool_gate: Rust `cargo test --doc`, Go example functions, Python `doctest`, or a build step that includes samples from files that CI compiles.
borrowed_from:
  - https://doc.rust-lang.org/rustdoc/write-documentation/documentation-tests.html
  - https://go.dev/blog/examples
  - https://hexdocs.pm/elixir/writing-documentation.html
---

**Rule.** Run each code example in the docs as a test.

**Why.** A pasted example drifts from the API it shows, and readers copy it. A tested example fails the build when the API changes. Including the sample from a source file that CI builds, instead of pasting it, gives the same protection.

**FAIL**

```text
README.md: a 12-line ```python block pasted by hand, never run
```

**PASS**

```text
README.md: the sample is the body of tests/test_quickstart.py, run by `pytest --doctest-glob`
```

**Counterpoint.** "Some samples are fragments that cannot run." Mark those as fragments and keep them short. The rule is for samples a reader will copy and run.
