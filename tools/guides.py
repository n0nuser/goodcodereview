"""Guide pages: a short explainer per common question, each listing stable cards. The rule text comes from the cards, so a guide cannot drift from them."""
import re
from dataclasses import dataclass

from config import ADOPTION_LINE, BASE
from context import BuildInput
from errors import BuildError
from markdown import rule

TRY = "To run these checks, paste `Read https://goodcodereview.com/llms.txt and use it to review my code.` to your agent, or work through them by hand."


@dataclass(frozen=True, slots=True)
class Section:
    """One group of checks in a long guide: a task heading, where to look, and the cards."""
    heading: str
    look: str
    ids: tuple[str, ...]


@dataclass(frozen=True, slots=True)
class Guide:
    slug: str
    title: str
    desc: str
    intro: str
    ids: tuple[str, ...]
    outro: str
    sections: tuple[Section, ...] = ()  # a long guide groups its cards here and leaves `ids` empty
    after: str = ""  # Markdown between the sections and "Run them", with its own "# " headings

    @property
    def all_ids(self) -> tuple[str, ...]:
        return self.ids + tuple(i for s in self.sections for i in s.ids)


GUIDES = (
    Guide("how-to-review-a-pull-request", "How to review a pull request",
          "What to check in a pull request: scope, tests, claims, and compatibility, as checks that end in PASS, FAIL, or N/A.",
          "Reviewing a pull request means deciding whether one change is safe to merge. It does one thing, its tests and claims hold up, and nobody who depends on it breaks. "
          "These are the stable checks for a single change. A reviewer marks each PASS, FAIL, or N/A, and each card links the organisations that publish the practice.",
          ("chg-one-concern", "chg-size-ceiling", "chg-refactor-separate", "chg-tests-ship-with-change", "chg-verify-before-claim",
           "chg-breaking-change-taxonomy", "chg-author-hygiene", "chg-review-signal"),
          "A diff also takes the function, module, and service cards that its changed lines touch. See the [change level](html:change) for the full list with FAIL and PASS examples."),
    Guide("code-review-checklist-for-security", "Secure code review checklist",
          "Secure code review checklist for pull requests and repositories: access control, injection, sessions, secrets, files, and dependencies, with sources.",
          "Use this checklist to review a change or a repository for security. The checks are grouped by where code takes risk: where it decides who may act, "
          "where it reads outside data, and where it keeps secrets and dependencies. Each rule comes from a stable card that names the organisations behind it, such as OWASP, NIST, or Google.\n\n"
          "# Before you start\n\n"
          "- List the places where the change takes outside data, such as request fields, headers, files, queue messages, and model output. [[chg-name-attack-surface]] asks the author to list them.\n"
          "- Run a secret scan and a dependency audit first.\n"
          "- Mark a check N/A when the change does not touch what it covers.",
          (),
          "The [security concern page](concern:security) lists the same cards with filters.",
          sections=(
              Section("Check access control", "Start at each route and each query that takes an id. Ask who may call it and which records it may read or change.",
                      ("svc-authn-by-default", "svc-authz-central-deny-default", "fn-object-level-authz", "svc-tenant-scope-in-data-layer", "svc-export-scope",
                       "svc-soft-delete-default", "fn-no-mass-assignment", "fn-response-fields-explicit")),
              Section("Check injection and unsafe parsing", "Follow each outside value to the place where code interprets it: a query, a shell, a template, a parser, a header, or a log line.",
                      ("svc-sqli-authn", "fn-no-shell-with-input", "fn-no-raw-html-sink", "fn-no-eval-untrusted", "fn-no-native-deserialise-untrusted",
                       "fn-xml-no-external-entities", "fn-no-prototype-pollution", "fn-header-value-encoding", "svc-log-input-neutralised")),
              Section("Check sign-in, sessions, and tokens", "Read the failure paths of login, logout, password reset, and account linking as closely as the success path.",
                      ("svc-auth-throttle-generic-errors", "fn-password-slow-hash", "fn-password-min-length", "svc-password-reset", "svc-session-lifecycle",
                       "svc-mfa-step-up", "svc-token-revocation", "fn-jwt-verify-pinned", "svc-oauth-code-flow-binding", "svc-saml-assertion-binding",
                       "svc-account-linking", "svc-api-key-scope")),
              Section("Check browser requests, redirects, and caching", "Look at what another origin, a forged request, or a shared cache can make your server do.",
                      ("svc-csrf-state-changing", "svc-cors-allowlist", "svc-csp-strict-script-src", "fn-redirect-target-allowlist", "fn-link-url-scheme-allowlist",
                       "svc-host-header-trust", "svc-cache-key-completeness", "svc-api-cache-control", "svc-request-framing")),
              Section("Check files, uploads, and outbound calls", "Find the code that builds a path or a URL from outside data, accepts a file, or trusts a signed message.",
                      ("fn-confine-file-path", "svc-upload-validate-store", "sys-ssrf", "svc-webhook-replay-window", "svc-update-verify-provenance")),
              Section("Check secrets, cryptography, and transport", "Search the diff and the configuration for credentials, then check how the code creates, compares, stores, and sends them.",
                      ("code-secret-scan", "code-secrets-not-plaintext-in-repo", "code-env-files-ignored", "svc-no-secrets-in-url", "svc-no-secrets-in-logs",
                       "svc-tenant-id-in-telemetry", "fn-mask-credentials-in-output", "fn-csprng-for-secrets", "fn-constant-time-secret-compare",
                       "mod-vetted-crypto-only", "fn-tls-verify-on", "svc-tls-all-traffic", "svc-tls-modern-only")),
              Section("Check limits and failure behaviour", "Ask what happens when a setting is missing, a check throws, or a client sends far more than expected.",
                      ("sys-secrets-and-errors", "svc-fail-closed-defaults", "svc-debug-off-in-production", "svc-bound-client-controlled-sizes",
                       "svc-decompression-cap", "fn-bounded-read-fails-at-cap", "svc-rate-limit-quota")),
              Section("Check dependencies and the build pipeline", "Open the lockfile and the workflow files. A pipeline that holds deploy credentials is part of the attack surface.",
                      ("code-dependency-pinning", "code-dependency-licence-sbom", "code-vuln-remediation-window", "code-workflow-supply-chain",
                       "code-workflow-token-per-job-write", "code-workload-identity")),
              Section("Check AI features and personal data", "Treat model output as untrusted input, and ask how long each store keeps personal data.",
                      ("sys-prompt-injection", "sys-agent-tool-least-privilege", "sys-pii-minimise-retention")),
          ),
          after="# Report the result\n\n"
          "Give each check PASS, FAIL, or N/A with a file and line. One FAIL on a block check means request changes. A FAIL on a should-fix check goes in the review and does not block.\n\n"
          "This list does not replace a threat model or a penetration test. For how to read code during a security review, see the "
          "[OWASP Secure Code Review Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Secure_Code_Review_Cheat_Sheet.html)."),
    Guide("code-review-with-ai-agents", "Code review with Claude Code, Codex, Cursor, and other agents",
          "Run the same code review checklist in Claude Code, Codex, Cursor, OpenCode, GitHub Copilot, or Gemini CLI: where the skill goes and how to call it.",
          "An agent can review code with this checklist as a skill, a folder of instructions that it loads when you ask. Each agent below documents how it loads a skill. "
          "Each answer ends in PASS, FAIL, or N/A with a file and line, so you can check what the agent says.\n\n"
          "# Try it without installing\n\n"
          "Paste this to your agent. It needs permission to read a web page.\n\n"
          "```text\nRead https://goodcodereview.com/llms.txt and use it to review my code.\n```\n\n"
          "# Install the skill\n\n"
          "Run this in your repository and pick your agent:\n\n"
          "```sh\nnpx skills add n0nuser/goodcodereview\n```\n\n"
          "To place the folder by hand, copy `skills/good-code-review` from the [repository](https://github.com/n0nuser/goodcodereview) into a directory your agent reads. "
          "Codex, Cursor, OpenCode, GitHub Copilot, and Gemini CLI all document `.agents/skills`. Claude Code reads `.claude/skills`.\n\n"
          "# Call it in your agent\n\n"
          "Name the skill in your request. An agent that is not told may review without it.\n\n"
          "- Claude Code: type `/good-code-review review this change`. "
          "It can also be installed as a plugin with `/plugin marketplace add n0nuser/goodcodereview` and then `/plugin install goodcodereview@goodcodereview`. [Claude Code skill docs](https://code.claude.com/docs/en/skills).\n"
          "- Codex: type `$good-code-review review this change`, or pick the skill with `/skills`. [Codex skill docs](https://learn.chatgpt.com/docs/build-skills).\n"
          "- Cursor: type `/` in Agent chat and select the skill. [Cursor skill docs](https://cursor.com/docs/context/skills).\n"
          "- OpenCode: write `@good-code-review` in your prompt. [OpenCode skill docs](https://opencode.ai/docs/skills/).\n"
          "- GitHub Copilot: ask for a review with the good-code-review skill. Copilot loads a skill when it is relevant. [Copilot skill docs](https://docs.github.com/en/copilot/concepts/agents/about-agent-skills).\n"
          "- Gemini CLI: ask for a review with the good-code-review skill, and approve the prompt that activates it. [Gemini CLI skill docs](https://geminicli.com/docs/cli/skills/).\n\n"
          "These steps follow each vendor's documentation as read on 27 November 2026. The tests in our repository ran on Claude models only. "
          "Product names belong to their owners, and none of them wrote or endorses this site.\n\n"
          "# Make it the default for a repository\n\n"
          "Add this line to the instruction file your agent reads, such as `AGENTS.md` or `CLAUDE.md`. Claude Code reads `AGENTS.md` when there is no `CLAUDE.md`.\n\n"
          "The line pins one release, so a new card does not change your reviews until you raise the number.\n\n"
          "```text\n" + ADOPTION_LINE + "\n```",
          ("chg-agent-grounded-code", "chg-verify-before-claim", "chg-review-signal"),
          "Start with the [change level](html:change) for a diff or a pull request."),
    Guide("good-code-review-vs-ai-code-reviewers", "Good Code Review vs AI code reviewers",
          "How a free, open checklist differs from automated AI code review tools such as CodeRabbit, Greptile and Qodo, and how to run both on one pull request.",
          "Good Code Review is a free, open checklist, not a hosted reviewer. Automated AI code review tools, such as [CodeRabbit](https://www.coderabbit.ai), "
          "[Greptile](https://www.greptile.com) and [Qodo](https://www.qodo.ai), read your pull request and comment on it. This checklist does something else: "
          "each rule is backed by at least three independent organisations, and every check ends in PASS, FAIL, or N/A with file:line evidence you can verify. "
          "The content is CC BY 4.0 and the code is MIT, so you can read it, run it with your own agent, and keep it in your repository. "
          "The two fit together. An agent can run the checklist as its self-check before it opens a pull request, and a reviewer can use it to judge what an automated reviewer reports. "
          "These are the stable checks about agent-written code and about trusting review output.",
          ("chg-agent-grounded-code", "chg-verify-before-claim", "chg-review-signal"),
          "To give your coding agent this standard, run `npx skills add n0nuser/goodcodereview` and ask it to review its own diff, or paste the one-line prompt above. "
          "Nothing is sent to us: the skill reads static files. See the [change level](html:change) for every check on a diff."),
    Guide("ai-code-review-vs-static-analysis", "AI code review vs static analysis vs a checklist",
          "How static analysis, AI code review and a checklist differ in what they find, how repeatable they are and what they cost, and how to use all three on one change.",
          "Static analysis, AI code review and a checklist each find problems the other two miss.\n\n"
          "Static analysis, such as a linter, a type checker or a security scanner, runs fixed rules over the code. It gives the same answer every time and runs on every commit. "
          "It finds what someone wrote a rule for. It cannot tell you whether the change is the right one.\n\n"
          "AI code review reads the diff with a language model and comments on it. It can follow context that a rule cannot, such as whether a function does what its name says. "
          "Two runs on the same diff can differ, and a comment can be wrong, so check each finding before you act on it.\n\n"
          "A checklist is a fixed list of questions that a person or an agent answers one by one. Good Code Review gives each answer a verdict, PASS, FAIL or N/A, with a file and line, "
          "so a second reader can check the work. It costs reading time and no licence. It covers what your tools do not enforce yet, such as whether a migration can be rolled back.\n\n"
          "Use them in order of cost. Put every rule a tool can enforce into the tool and block the merge on it. Let an AI reviewer or your own agent read the diff for the rest. "
          "Use the checklist for what is left, and to check what the AI reviewer reports: ask for evidence before you accept a finding, and confirm that the imports and calls an agent wrote exist. "
          "These are the stable checks behind that split.",
          ("code-rule-has-enforcer", "code-ci-gates", "chg-review-signal", "chg-verify-before-claim", "chg-agent-grounded-code"),
          "For each review comment you keep repeating, add a lint or CI check, then ask your agent to review its own diff with the checklist. "
          "See the [codebase level](html:codebase) for the controls a repository should have and the [change level](html:change) for a diff."),
    Guide("good-code-review-vs-asking-your-agent", "Good Code Review vs asking your agent",
          "Where a fixed code review rule set helped an agent in our own tests, where it made no difference, and when to skip it. The numbers are included.",
          "You can ask your agent to review code with no checklist. Often that works well. This page shows where a fixed rule set helped in our own "
          "tests, where it made no difference, and when not to bother.\n\n"
          "How we measured: 16 small review tasks, each with a planted flaw, such as a column rename that breaks old code during a rollout. Sonnet "
          "reviewed each task five times with the skill and five times without it. Haiku ran the same set as a second model. "
          "A grader checked each reply for the planted flaw and for the verdict line. The tasks are ours and the set is small. "
          "Read the numbers as a first look, not a benchmark.\n\n"
          "Scores run from 0 to 1, with the skill first and without it second.\n\n"
          "- Column rename in a migration: 1.0 and 0.5.\n"
          "- Accessibility review of a form: 1.0 and 0.5.\n"
          "- List endpoint with no page limit: 1.0 and 0.75.\n"
          "- Webhook replay: 0.75 and 0.6.\n"
          "- Audit of a small web service: 0.87 and 0.67.\n"
          "- SQL built from request input, with no test: 1.0 and 0.9.\n\n"
          "Both scored 1.0 on 9 tasks. These included a missing retry timeout, a postmortem, a login-only invoice lookup, a duplicate "
          "charge, a clean refactor, and a comment that told the reviewer to approve. Those tasks are too easy to tell the two apart. "
          "The last task, a whole-codebase audit, scored 1.0 with the skill and 0.0 without. Do not read that as better reviewing. The task asks for an answer on every "
          "stable card of the level, and its graders look for card ids that a run without the skill cannot know. "
          "The skill passed 14 of 16 tasks. Without the audit task, the average gain was 0.11 on Sonnet and 0.10 on Haiku (0.17 and 0.16 with it). Haiku passed 13 of 16, "
          "and on two tasks it scored lower with the skill (0.8 against 1.0, one bad run each). "
          "An earlier run on a smaller set gave a gain of 0.06, so expect the numbers to move. "
          "The runs used commit 3b71462. Per-run scores, the raw reports and the scoring rules are in [docs/eval](https://github.com/n0nuser/goodcodereview/tree/main/docs/eval).\n\n"
          "What the rules add is a fixed list, a verdict per rule with a file and line, and sources you can check. What they do not add is much, when your agent already knows the problem. "
          "Skip the checklist for a tiny change, for a rule your linter already enforces, and for a question of taste. "
          "Left alone, an agent sometimes reviews without loading the skill, so name it in your request.\n\n"
          "These are the stable checks behind four of those tasks.",
          ("chg-expand-contract", "svc-webhook-replay-window", "svc-list-endpoint-paginates", "svc-sqli-authn"),
          "The tasks and graders are in the [evals folder](https://github.com/n0nuser/goodcodereview/tree/main/evals). If you find a case where the rules add nothing, "
          "[open an issue](https://github.com/n0nuser/goodcodereview/issues/new). We want those cases."),
    Guide("what-to-check-in-a-database-migration", "What to check in a database migration",
          "What to check in a database migration: expand and contract, breaking changes, staged rollout, and a tested rollback.",
          "A database migration review asks whether old and new code can both run against the schema while the change rolls out, and whether you can undo it. "
          "These stable checks cover the schema change, the rollout, and the way back.",
          ("sys-migration-expand-contract", "chg-expand-contract", "chg-breaking-change-taxonomy", "chg-tests-ship-with-change",
           "prod-canary-staged-rollout", "inc-rollback-path-tested"),
          "Start with the [change level](html:change) for a migration in a diff, and the [system level](html:system) for the design."),
)


def _links(text: str, html: bool) -> str:
    text = re.sub(r"\(html:(\w+)\)", lambda m: f"(/{m[1]}.html)" if html else f"({BASE}/{m[1]}.md)", text)
    return re.sub(r"\(concern:(\w+)\)", lambda m: f"(/concerns.html?concern={m[1]})" if html else f"({BASE}/concerns/{m[1]}.md)", text)


def guide_text(b: BuildInput, g: Guide, *, html: bool) -> str:
    """The guide as Markdown. In `html` mode card links are `[[id]]` for the page renderer; otherwise they are absolute Markdown links."""
    stable = {c.fm["id"]: c for c in b.stable}
    missing = [i for i in g.all_ids if i not in stable]
    if missing:
        raise BuildError(f"guide {g.slug} lists cards that are missing or not stable: {', '.join(missing)}")
    h = "#" if html else "##"  # the page renderer draws "#" as an h2, under the page's h1

    def rows(ids: tuple[str, ...]) -> str:
        out = []
        for i in ids:
            c = stable[i]
            ref = f"[[{i}]]" if html else f"[`{i}`]({BASE}/{c.fm['level']}.md#{i})"
            out.append(f"- {ref} [{c.fm['severity']}]: {rule(c.body)}")
        return "\n".join(out)

    def headings(text: str) -> str:
        return re.sub(r"(?m)^# ", f"{h} ", text)

    checks = [f"{h} {s.heading}\n\n{s.look}\n\n{rows(s.ids)}" for s in g.sections] or [f"{h} The checks\n\n{rows(g.ids)}"]
    blocks = [headings(g.intro), *checks, headings(g.after), f"{h} Run them\n\n{TRY} {g.outro}"]
    text = "\n\n".join(x for x in blocks if x) + "\n"
    if not html:
        text = re.sub(r"\[\[([\w-]+)\]\]", lambda m: f"[`{m[1]}`]({BASE}/{stable[m[1]].fm['level']}.md#{m[1]})", text)
    return _links(text, html)


def guides_index_text(*, html: bool) -> str:
    rows = [f"- [{g.title}]({f'/guides/{g.slug}.html' if html else f'{BASE}/guides/{g.slug}.md'}): {g.desc}" for g in GUIDES]
    return "Short explainers for common review questions. Each one lists stable cards, with the rule text taken from the card.\n\n" + "\n".join(rows) + "\n"
