"""Guide pages: a short explainer per common question, each listing stable cards. The rule text comes from the cards, so a guide cannot drift from them."""
import re
from dataclasses import dataclass

from config import BASE
from context import BuildInput
from errors import BuildError
from markdown import rule

TRY = "To run these checks, paste `Read https://goodcodereview.com/llms.txt and use it to review my code.` to your agent, or work through them by hand."


@dataclass(frozen=True, slots=True)
class Guide:
    slug: str
    title: str
    desc: str
    intro: str
    ids: tuple[str, ...]
    outro: str


GUIDES = (
    Guide("how-to-review-a-pull-request", "How to review a pull request",
          "What to check in a pull request: scope, tests, claims, and compatibility, as checks that end in PASS, FAIL, or N/A.",
          "Reviewing a pull request means deciding whether one change is safe to merge. It does one thing, its tests and claims hold up, and nobody who depends on it breaks. "
          "These are the stable checks for a single change. A reviewer marks each PASS, FAIL, or N/A, and each card links the organisations that publish the practice.",
          ("chg-one-concern", "chg-size-ceiling", "chg-refactor-separate", "chg-tests-ship-with-change", "chg-verify-before-claim",
           "chg-breaking-change-taxonomy", "chg-author-hygiene", "chg-review-signal"),
          "A diff also takes the function, module, and service cards that its changed lines touch. See the [change level](html:change) for the full list with FAIL and PASS examples."),
    Guide("code-review-checklist-for-security", "Code review checklist for security",
          "A security checklist for code review: injection, authorisation, secrets, sessions, and supply chain, each with its published sources.",
          "A security code review checks the places where untrusted input, identity, or secrets cross a boundary. "
          "These are the blocking security checks from the stable cards, from a single function up to the dependency pipeline. Each card names the organisations behind it.",
          ("svc-sqli-authn", "fn-no-shell-with-input", "fn-no-raw-html-sink", "fn-object-level-authz", "svc-authz-central-deny-default",
           "svc-csrf-state-changing", "svc-session-lifecycle", "svc-auth-throttle-generic-errors", "fn-confine-file-path", "svc-upload-validate-store",
           "sys-ssrf", "sys-secrets-and-errors", "code-secret-scan", "code-dependency-pinning"),
          "Every stable security card, including the should-fix ones, is on the [security concern page](concern:security)."),
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
    Guide("good-code-review-vs-asking-your-agent", "Good Code Review vs asking your agent",
          "Where a fixed code review rule set helped an agent in our own tests, where it made no difference, and when to skip it. The numbers are included.",
          "You can ask your agent to review code with no checklist. Often that works well. This page shows where a fixed rule set helped in our own "
          "tests, where it made no difference, and when not to bother.\n\n"
          "How we measured: 16 small review tasks, each with a planted flaw, such as a column rename that breaks old code during a rollout. Sonnet "
          "reviewed each task five times with the skill and five times without it. Haiku ran the same set as a second model. "
          "A grader checked each reply for the planted flaw and for the verdict line. The tasks are ours and the set is small. "
          "Read the numbers as a first look, not a benchmark.\n\n"
          "Scores run from 0 to 1, with the skill first and without it second.\n\n"
          "- Whole-codebase audit: 1.0 and 0.0.\n"
          "- Column rename in a migration: 1.0 and 0.5.\n"
          "- Accessibility review of a form: 1.0 and 0.5.\n"
          "- List endpoint with no page limit: 1.0 and 0.75.\n"
          "- Webhook replay: 0.75 and 0.6.\n"
          "- Audit of a small web service: 0.87 and 0.67.\n"
          "- SQL built from request input, with no test: 1.0 and 0.9.\n\n"
          "Both scored 1.0 on the other 9 tasks. These included a missing retry timeout, a postmortem, a login-only invoice lookup, a duplicate "
          "charge, a clean refactor, and a comment that told the reviewer to approve. Those tasks are too easy to tell the two apart. "
          "The skill passed 14 of 16 tasks, and the average gain was 0.17. Haiku passed 13 of 16 with an average gain of 0.16, "
          "and on two tasks it scored lower with the skill (0.8 against 1.0, one bad run each). "
          "An earlier run on a smaller set gave a gain of 0.06, so expect the numbers to move. "
          "Per-run scores, the raw reports and the scoring rules are in [docs/eval](https://github.com/n0nuser/goodcodereview/tree/main/docs/eval).\n\n"
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
    missing = [i for i in g.ids if i not in stable]
    if missing:
        raise BuildError(f"guide {g.slug} lists cards that are missing or not stable: {', '.join(missing)}")
    rows = []
    for i in g.ids:
        c = stable[i]
        ref = f"[[{i}]]" if html else f"[`{i}`]({BASE}/{c.fm['level']}.md#{i})"
        rows.append(f"- {ref} [{c.fm['severity']}]: {rule(c.body)}")
    h = "#" if html else "##"  # the page renderer draws "#" as an h2, under the page's h1
    return _links(f"{g.intro}\n\n{h} The checks\n\n" + "\n".join(rows) + f"\n\n{h} Run them\n\n{TRY} {g.outro}\n", html)


def guides_index_text(*, html: bool) -> str:
    rows = [f"- [{g.title}]({f'/guides/{g.slug}.html' if html else f'{BASE}/guides/{g.slug}.md'}): {g.desc}" for g in GUIDES]
    return "Short explainers for common review questions. Each one lists stable cards, with the rule text taken from the card.\n\n" + "\n".join(rows) + "\n"
