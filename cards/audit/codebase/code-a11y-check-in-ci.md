---
id: code-a11y-check-in-ci
level: codebase
tags: [accessibility, testing, frontend, ci]
severity: should-fix
status: draft
lang: core
applies_when: The repo builds a web UI with a CI pipeline.
tool_gate: This card is the gate: `eslint-plugin-jsx-a11y` in the lint step, and axe against rendered pages in the test step, both set to fail the build.
note: 3 orgs (jsx-eslint, Deque weak on CI, GOV.UK); GDS found the best of 13 automated tools caught 40% of planted barriers, so the gate does not replace the manual pass in chg-ui-change-screenshots-and-keyboard-pass
borrowed_from:
  - https://github.com/jsx-eslint/eslint-plugin-jsx-a11y
  - https://www.deque.com/axe/core-documentation/
  - https://alphagov.github.io/accessibility-tool-audit/
  - https://www.gov.uk/service-manual/helping-people-to-use-your-service/making-your-service-accessible-an-introduction
---

**Rule.** Run an automated accessibility check in CI, a JSX lint and an axe run on rendered pages, and fail the build on a violation.

**Why.** A violation that nobody sees at review ships. A failing check catches the missing label or `alt` on the pull request that adds it. It is a floor: tools find only part of the problems, so a person still tests with a keyboard.

**FAIL**

```yaml
# .github/workflows/ci.yml
steps:
  - run: npm test
  - run: npm run build
# no a11y lint, no axe run
```

**PASS**

```json
{ "extends": ["plugin:jsx-a11y/recommended"] }
```

```js
// e2e: fail on any axe violation
const results = await new AxeBuilder({ page }).analyze();
expect(results.violations).toEqual([]);
```

**Counterpoint.** "Tools only catch a minority, so why bother?" They catch the cheap failures at no review cost, which frees the manual pass for what only a person can judge. Start with `warn` if the backlog is large, and switch each rule to `error` once its backlog is clear.
