---
id: code-env-files-ignored
level: codebase
tags: [security, secrets, config]
severity: should-fix
status: stable
lang: core
applies_when: Auditing a repo whose application reads settings from .env files.
tool_gate: A secret scan on push; a CI check that `git ls-files` lists no .env.local or .env file with real values.
note: Laravel (.env should not be committed; commit a .env.example with placeholders), Symfony (.env.local should be ignored by git), Next.js (default template ignores all .env files; you almost never want to commit them) and Vite (add *.local to .gitignore). Symfony, Next.js and Vite commit a non-secret .env of defaults, so the rule names the local files and the secrets, not every .env
borrowed_from:
  - https://laravel.com/docs/12.x/configuration
  - https://symfony.com/doc/current/configuration.html
  - https://nextjs.org/docs/app/guides/environment-variables
  - https://vite.dev/guide/env-and-mode
---

**Rule.** Git-ignore local environment files that hold real values; commit only a template with placeholders.

**Why.** An `.env` file with real credentials, once committed, sits in every clone and in history, and deleting it later does not recall the copies ([[code-secrets-not-plaintext-in-repo]]). A committed template with placeholder values still tells the next developer which variables the app needs.

**FAIL**

```text
.gitignore:   (no .env entries)
.env          DB_PASSWORD=S3cr37-prod        (tracked by git)
```

**PASS**

```text
.gitignore:   .env
              .env.*.local
.env.example  DB_PASSWORD=change-me          (tracked, placeholders only)
```

**Counterpoint.** Frameworks such as Symfony and Next.js commit a `.env` of non-secret defaults, and an encrypted env file can be committed too. Both are fine: the check is that no file in the repo holds a real credential in plaintext, and that local override files are ignored.
