---
id: fn-doc-summary-sentence
level: function
tags: [maintainability, docs]
severity: discuss
status: stable
lang: core
applies_when: A function, class or module has a doc comment or docstring.
tool_gate: Ruff `D205` and `D415` (pydocstyle), Checkstyle `SummaryJavadoc`, or the language's doc lint.
note: Python PEP 257, Swift, Rust, Google, Drupal, WordPress, OpenStack and NumPy each state it. The exact form varies (sentence or fragment, one line or two), so the Rule keeps only what they share
borrowed_from:
  - https://peps.python.org/pep-0257/
  - https://www.swift.org/documentation/api-design-guidelines/
  - https://rust-lang.github.io/rfcs/0505-api-comment-conventions.html
  - https://google.github.io/styleguide/pyguide.html
  - https://project.pages.drupalcode.org/coding_standards/php/documentation/
  - https://developer.wordpress.org/coding-standards/inline-documentation-standards/php/
  - https://docs.openstack.org/hacking/latest/user/hacking.html
  - https://numpydoc.readthedocs.io/en/latest/format.html
---

**Rule.** Open each doc comment with one short summary line, then a blank line before any detail.

**Why.** Tools and readers show only the first line in indexes, hovers and search results. A summary that wraps, or that starts with detail, shows up cut off or empty.

**FAIL**

```python
def fetch(url):
    """Fetches the page at the URL, and if the server answers with a redirect
    follows it up to five times before it gives up and raises."""
```

**PASS**

```python
def fetch(url):
    """Return the page body, following up to five redirects.

    Raise FetchError when the server keeps redirecting.
    """
```

**Counterpoint.** "A one-line docstring is enough for a trivial function." It is, and the rule is met: the summary line is the whole comment. The rule only applies the moment a second line appears.
