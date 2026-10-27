"""Which organisation publishes each source URL. build.py and validate.py read this one map.

docs/PROMOTION.md says how to count organisations, and the groups below follow it: every OWASP project is OWASP,
every w3.org page is W3C, Google covers web.dev, Chrome, the SRE books, and Go, and Microsoft covers Learn and the
engineering playbook. A URL that matches no prefix fails validation, so add a prefix when you cite a new site.
"""
import json
from pathlib import Path
from urllib.parse import urlparse

# id -> display name. An org with an entry in org_icons.json shows its logo. Every other org shows a monogram.
ORGS = {
    "a11yproject": "The A11y Project", "airbnb": "Airbnb", "apache": "Apache Software Foundation", "appian": "Appian",
    "apple": "Apple", "atlassian": "Atlassian", "auth0": "Okta (Auth0)", "aws": "AWS", "baymard": "Baymard Institute",
    "ben-manes": "Caffeine project", "brendan-gregg": "Brendan Gregg", "cabify": "Cabify", "cisa": "CISA",
    "cloudflare": "Cloudflare", "cognitect": "Cognitect", "cursor": "Cursor", "dan-luu": "Dan Luu", "datadog": "Datadog",
    "deque": "Deque", "django": "Django Software Foundation", "drf": "Django REST framework", "dropbox": "Dropbox",
    "eiffel": "Eiffel Software", "elastic": "Elastic", "gatling": "Gatling", "gdpr-info": "intersoft consulting",
    "ghostty": "Ghostty", "github": "GitHub", "gitlab": "GitLab", "google": "Google", "govuk": "GOV.UK",
    "grafana": "Grafana Labs", "heroku": "Heroku", "heydon": "Heydon Pickering", "hickey": "Rich Hickey",
    "honeycomb": "Honeycomb", "ico": "ICO", "ietf": "IETF", "jnd": "Don Norman", "joel": "Joel Spolsky",
    "jsx-eslint": "jsx-eslint project", "kane": "Andrew Kane", "kent-beck": "Kent Beck", "kent-c-dodds": "Kent C. Dodds",
    "kernel": "Linux kernel", "kleppmann": "Martin Kleppmann", "kubernetes": "Kubernetes", "liskov-wing": "Barbara Liskov and Jeannette Wing",
    "llvm": "LLVM", "lucumr": "Armin Ronacher", "mcintosh": "McIntosh et al.", "meta": "Meta", "feathers": "Michael Feathers",
    "microsoft": "Microsoft", "mit": "MIT", "mitre": "MITRE", "mozilla": "Mozilla", "mypy": "mypy project",
    "ncsc": "NCSC", "netflix": "Netflix", "nist": "NIST", "nngroup": "Nielsen Norman Group", "nodejs": "OpenJS Foundation",
    "npm": "npm", "openapi": "OpenAPI Initiative", "openssf": "OpenSSF", "opentelemetry": "OpenTelemetry",
    "oracle": "Oracle", "ousterhout": "John Ousterhout", "pact": "Pact", "palantir": "Palantir", "pgbouncer": "PgBouncer project",
    "phacility": "Phacility", "portswigger": "PortSwigger", "portebois": "Sébastien Portebois", "postgresql": "PostgreSQL",
    "pragmatic-engineer": "The Pragmatic Engineer", "prometheus": "Prometheus", "psf": "Python Software Foundation",
    "pyjwt": "PyJWT project", "rails": "Ruby on Rails", "redis": "Redis", "refactoring-guru": "Refactoring.Guru",
    "repro-builds": "Reproducible Builds", "requests": "Requests project", "rust": "Rust project", "salvatore": "Salvatore Sanfilippo", "sandi-metz": "Sandi Metz",
    "sans-io": "Sans-I/O project", "section508": "Section508.gov", "shneiderman": "Ben Shneiderman", "shopify": "Shopify",
    "sitnik": "Size Limit project", "slack": "Slack", "smartbear": "SmartBear", "snyk": "Snyk", "spotify": "Spotify",
    "spring": "Spring", "sqlalchemy": "SQLAlchemy", "sqlite": "SQLite", "stepsecurity": "StepSecurity", "stripe": "Stripe",
    "tef": "tef (programmingisterrible)", "tokio": "Tokio project", "uber": "Uber", "uswds": "USWDS", "utsa": "University of Texas at San Antonio", "vorpus": "Nathaniel J. Smith",
    "warne": "Henrik Warne", "wayne": "Hillel Wayne", "webaim": "WebAIM", "whatwg": "WHATWG", "winand": "Markus Winand",
    "wordpress": "WordPress", "w3c": "W3C", "envoy": "Envoy", "hyrum": "Hyrum Wright", "owasp": "OWASP", "zalando": "Zalando",
    "jetbrains": "JetBrains", "nvidia": "NVIDIA", "statsig": "Statsig", "etcd": "etcd", "hazelcast": "Hazelcast",
    "ecto": "Ecto", "cockroach": "CockroachDB", "anthropic": "Anthropic",
}

# Orgs that are one author. They show in "Backed by" but never count toward the three organisations a stable card needs.
PERSONS = {
    "brendan-gregg", "dan-luu", "feathers", "heydon", "hickey", "hyrum", "jnd", "joel", "kane", "kent-beck", "kent-c-dodds",
    "kleppmann", "liskov-wing", "lucumr", "mcintosh", "ousterhout", "portebois", "salvatore", "sandi-metz", "shneiderman",
    "tef", "vorpus", "warne", "wayne", "winand",
}

# URL prefix (no scheme) -> org id. The longest matching prefix wins. A prefix without "/" also matches subdomains,
# so "owasp.org" covers cheatsheetseries.owasp.org. On code hosts the org is the repository owner, never the host.
PREFIXES = {
    "12factor.net": "heroku", "airbnb.tech": "airbnb", "alphagov.github.io": "govuk", "angular.dev": "google",
    "antirez.com": "salvatore", "arxiv.org/abs/2406.10279": "utsa", "atlassian.design": "atlassian", "auth0.com": "auth0",
    "aws.amazon.com": "aws", "aws.com": "aws", "baymard.com": "baymard", "bazel.build": "google", "blog.google": "google",
    "blog.palantir.com": "palantir", "blog.pragmaticengineer.com": "pragmatic-engineer", "newsletter.pragmaticengineer.com": "pragmatic-engineer",
    "cassandra.apache.org": "apache", "cloudflare.com": "cloudflare", "codeql.github.com": "github", "cwe.mitre.org": "mitre",
    "danluu.com": "dan-luu", "datatracker.ietf.org": "ietf", "dequeuniversity.com": "deque", "deque.com": "deque",
    "designsystem.digital.gov": "uswds", "gov.uk": "govuk", "ncsc.gov.uk": "ncsc", "dev.to/sportebois/": "portebois",
    "developer.apple.com": "apple", "mozilla.org": "mozilla", "cloud.google.com": "google", "developers.google.com": "google",
    "devguide.python.org": "psf", "docs.python.org": "psf", "peps.python.org": "psf", "pip.pypa.io": "psf",
    "requests.readthedocs.io": "requests", "docs.appian.com": "appian", "docs.djangoproject.com": "django", "dev.mysql.com": "oracle",
    "docs.oracle.com": "oracle", "docs.gatling.io": "gatling", "docs.github.com": "github", "github.blog": "github",
    "docs.gitlab.com": "gitlab", "kernel.org": "kernel", "docs.npmjs.com": "npm", "docs.pact.io": "pact",
    "docs.rs/regex/": "rust", "docs.rs/tokio/": "tokio", "docs.spring.io": "spring", "docs.sqlalchemy.org": "sqlalchemy",
    "stripe.com": "stripe", "stripe.dev": "stripe", "dropbox.tech": "dropbox", "engineering.atspotify.com": "spotify",
    "engineering.fb.com": "meta", "react.dev": "meta", "gdpr-info.eu": "gdpr-info", "owasp.org": "owasp",
    "chrome.com": "google", "chromium.org": "google", "go.dev": "google", "google.aip.dev": "google", "google.github.io": "google", "sre.google": "google", "abseil.io": "google", "testing.googleblog.com": "google", "web.dev": "google",
    "grafana.com": "grafana", "grpc.io": "google", "protobuf.dev": "google", "guides.rubyonrails.org": "rails",
    "henrikwarne.com": "warne", "honeycomb.io": "honeycomb", "html.spec.whatwg.org": "whatwg", "ico.org.uk": "ico",
    "inclusive-components.design": "heydon", "jnd.org": "jnd", "kentcdodds.com": "kent-c-dodds", "learn.microsoft.com": "microsoft",
    "microsoft.github.io": "microsoft", "microsoft.com": "microsoft", "playwright.dev": "microsoft", "learn.snyk.io": "snyk",
    "llvm.org": "llvm", "lucumr.pocoo.org": "lucumr", "martin.kleppmann.com": "kleppmann", "michaelfeathers.silvrback.com": "feathers",
    "mypy.readthedocs.io": "mypy", "netflixtechblog.com": "netflix", "newsletter.kentbeck.com": "kent-beck", "testdesiderata.com": "kent-beck", "nodejs.org": "nodejs",
    "nist.gov": "nist", "opensource.zalando.com": "zalando", "opentelemetry.io": "opentelemetry", "pkg.go.dev": "google",
    "portswigger.net": "portswigger", "programmingisterrible.com": "tef", "prometheus.io": "prometheus", "pyjwt.readthedocs.io": "pyjwt",
    "rebels.cs.uwaterloo.ca/papers/msr2014_mcintosh.pdf": "mcintosh", "redis.io": "redis", "refactoring.guru": "refactoring-guru",
    "reproducible-builds.org": "repro-builds", "sandimetz.com": "sandi-metz", "sans-io.readthedocs.io": "sans-io",
    "sback.it/publications/icse2018seip.pdf": "google", "secure.phabricator.com": "phacility", "shopify.engineering": "shopify",
    "slack.engineering": "slack", "slsa.dev": "openssf", "smartbear.com": "smartbear", "spec.openapis.org": "openapi",
    "tech.cabify.com": "cabify", "use-the-index-luke.com": "winand", "vorpus.org": "vorpus",
    "web.mit.edu/Saltzer/": "mit", "webaim.org": "webaim", "a11yproject.com": "a11yproject", "barroso.org": "google",
    "brendangregg.com": "brendan-gregg", "cisa.gov": "cisa", "cognitect.com": "cognitect",
    "cs.columbia.edu/~wing/publications/LiskovWing94.pdf": "liskov-wing", "cs.umd.edu/users/ben/": "shneiderman",
    "datadoghq.com": "datadog", "django-rest-framework.org": "drf", "eiffel.org": "eiffel", "elastic.co": "elastic",
    "envoyproxy.io": "envoy", "hillelwayne.com": "wayne", "hyrumslaw.com": "hyrum", "joelonsoftware.com": "joel",
    "kubernetes.dev": "kubernetes", "pgbouncer.org": "pgbouncer", "postgresql.org": "postgresql", "nngroup.com": "nngroup",
    "rfc-editor.org": "ietf", "section508.gov": "section508", "sqlite.org": "sqlite", "stepsecurity.io": "stepsecurity",
    "uber.com": "uber", "w3.org": "w3c",
    "flink.apache.org": "apache", "hadoop.apache.org": "apache", "kubernetes.io": "kubernetes", "research.google": "google",
    "jetbrains.com": "jetbrains", "github.com/NVIDIA/": "nvidia", "statsig.com": "statsig", "etcd.io": "etcd",
    "docs.hazelcast.com": "hazelcast", "ecto-sql.hexdocs.pm": "ecto", "docs.cockroachlabs.com": "cockroach",
    "github.com/GoogleChrome/": "google", "github.com/Netflix/": "netflix", "github.com/ai/size-limit": "sitnik",
    "github.com/ankane/": "kane", "github.com/ben-manes/caffeine": "ben-manes", "github.com/cursor/plugins/": "cursor",
    "github.com/dequelabs/": "deque", "github.com/ghostty-org/": "ghostty", "github.com/johnousterhout/": "ousterhout",
    "github.com/jsx-eslint/": "jsx-eslint", "github.com/matthiasn/talk-transcripts/blob/master/Hickey_Rich/": "hickey",
    "github.com/microsoft/": "microsoft", "github.com/mozilla/": "mozilla", "github.com/ossf/": "openssf",
    "x.com/addyosmani/status/2114604912520921136": "anthropic",
    "raw.githubusercontent.com/OWASP/": "owasp", "raw.githubusercontent.com/WordPress/": "wordpress",
    "raw.githubusercontent.com/elastic/": "elastic", "raw.githubusercontent.com/mozilla/": "mozilla",
}

ICONS = json.loads((Path(__file__).with_name("org_icons.json")).read_text())  # org id -> SVG path from Simple Icons 15.22.0 (CC0), https://simpleicons.org


def org_of(url):
    """The org id for a URL, or None when no prefix matches."""
    u = urlparse(url)
    host = u.netloc.lower().removeprefix("www.")
    key = host + u.path
    best = None
    for p in PREFIXES:
        hit = key.startswith(p) if "/" in p else host == p or host.endswith("." + p)
        if hit and (best is None or len(p) > len(best)):
            best = p
    return PREFIXES[best] if best else None


def group(urls):
    """[(org id, [urls])] in first-cited order. Raises KeyError on a URL no prefix matches."""
    out = {}
    for u in urls:
        o = org_of(u)
        if o is None:
            raise KeyError(f"no organisation for {u}; add a prefix to tools/orgs.py")
        out.setdefault(o, []).append(u)
    return list(out.items())


def split(urls):
    """(organisations, people), each [(id, [urls])] in first-cited order."""
    g = group(urls)
    return [x for x in g if x[0] not in PERSONS], [x for x in g if x[0] in PERSONS]


def monogram(oid):
    """Up to four characters for an org without a logo: the acronym ("W3C", "AWS") or the initials ("NN" for Nielsen Norman Group)."""
    name = ORGS[oid].split(" (")[0]
    if name.replace(".", "").isupper():
        return "".join(c for c in name if c.isalnum())[:4]
    return "".join(w[0] for w in name.split() if w[0].isupper())[:2] or name[0].upper()
