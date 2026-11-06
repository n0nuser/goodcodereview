"""Which organisation publishes each source URL. The build and validate.py read this one map.

docs/PROMOTION.md says how to count organisations, and the groups below follow it: every OWASP project is OWASP,
every w3.org page is W3C, Google covers web.dev, Chrome, the SRE books, and Go, and Microsoft covers Learn and the
engineering playbook. A URL that matches no prefix fails validation, so add a prefix when you cite a new site.
"""
import json
from dataclasses import dataclass
from pathlib import Path
from urllib.parse import urlparse

# id -> display name. An org with an entry in org_icons.json shows its logo. Every other org shows a monogram.
ORGS = {
    "debian": "Debian", "hashicorp": "HashiCorp", "git": "Git", "gnu": "GNU Project", "tuf": "The Update Framework", "sparkle": "Sparkle", "sigstore": "Sigstore", "mender": "Mender", "opengroup": "The Open Group", "clig": "Command Line Interface Guidelines", "go-update": "go-update (Alan Shreve)",
    "a11yproject": "The A11y Project", "airbnb": "Airbnb", "apache": "Apache Software Foundation", "appian": "Appian",
    "apple": "Apple", "atlassian": "Atlassian", "auth0": "Okta (Auth0)", "aws": "AWS", "baymard": "Baymard Institute",
    "ben-manes": "Caffeine project", "brendan-gregg": "Brendan Gregg", "cabify": "Cabify", "cisa": "CISA",
    "cloudflare": "Cloudflare", "cognitect": "Cognitect", "cursor": "Cursor", "dan-luu": "Dan Luu", "datadog": "Datadog",
    "deque": "Deque", "django": "Django Software Foundation", "drf": "Django REST framework", "dropbox": "Dropbox",
    "eiffel": "Eiffel Software", "elastic": "Elastic", "gatling": "Gatling", "gdpr-info": "intersoft consulting",
    "ghostty": "Ghostty", "github": "GitHub", "gitlab": "GitLab", "google": "Google", "govuk": "GOV.UK",
    "grafana": "Grafana Labs", "heroku": "Heroku", "heydon": "Heydon Pickering", "hickey": "Rich Hickey",
    "honeycomb": "Honeycomb", "ico": "ICO", "ietf": "IETF", "jnd": "Don Norman", "joel": "Joel Spolsky",
    "jsx-eslint": "jsx-eslint project", "kane": "Andrew Kane", "zupo": "awesome-pytest-speedup (zupo)", "pylint": "Pylint", "checkstyle": "Checkstyle", "rubocop": "RuboCop", "pmd": "PMD", "importjs": "eslint-plugin-import", "nx": "Nx", "archunit": "ArchUnit", "oxide": "Oxide Computer Company", "laravel": "Laravel", "ecto": "Ecto", "pytest-django": "pytest-django", "pytest-xdist": "pytest-xdist", "alloy": "Alloy.ai", "trailofbits": "Trail of Bits", "exante": "EXANTE", "alan": "Alan", "kent-beck": "Kent Beck", "kent-c-dodds": "Kent C. Dodds",
    "kernel": "Linux kernel", "kleppmann": "Martin Kleppmann", "kubernetes": "Kubernetes", "liskov-wing": "Barbara Liskov and Jeannette Wing",
    "llvm": "LLVM", "lucumr": "Armin Ronacher", "mcintosh": "McIntosh et al.", "meta": "Meta", "feathers": "Michael Feathers",
    "microsoft": "Microsoft", "mit": "MIT", "mitre": "MITRE", "mozilla": "Mozilla", "mypy": "mypy project",
    "ncsc": "NCSC", "netflix": "Netflix", "nist": "NIST", "pytest": "pytest", "vodafone": "Vodafone", "nngroup": "Nielsen Norman Group", "nodejs": "OpenJS Foundation",
    "npm": "npm", "openapi": "OpenAPI Initiative", "openssf": "OpenSSF", "opentelemetry": "OpenTelemetry",
    "docker": "Docker", "oracle": "Oracle", "sonarsource": "SonarSource", "openjdk": "OpenJDK", "godot": "Godot Engine", "usgs": "USGS", "va": "US Department of Veterans Affairs", "ethereum": "Ethereum Foundation", "ousterhout": "John Ousterhout", "pact": "Pact", "palantir": "Palantir", "pgbouncer": "PgBouncer project",
    "phacility": "Phacility", "portswigger": "PortSwigger", "portebois": "Sébastien Portebois", "postgresql": "PostgreSQL",
    "pragmatic-engineer": "The Pragmatic Engineer", "prometheus": "Prometheus", "psf": "Python Software Foundation",
    "pyjwt": "PyJWT project", "rails": "Ruby on Rails", "redis": "Redis", "refactoring-guru": "Refactoring.Guru",
    "repro-builds": "Reproducible Builds", "requests": "Requests project", "rust": "Rust project", "salvatore": "Salvatore Sanfilippo", "sandi-metz": "Sandi Metz",
    "sans-io": "Sans-I/O project", "section508": "Section508.gov", "shneiderman": "Ben Shneiderman", "shopify": "Shopify",
    "sitnik": "Size Limit project", "slack": "Slack", "smartbear": "SmartBear", "snyk": "Snyk", "spotify": "Spotify",
    "spring": "Spring", "sqlalchemy": "SQLAlchemy", "sqlite": "SQLite", "stepsecurity": "StepSecurity", "stripe": "Stripe",
    "tef": "tef (programmingisterrible)", "tokio": "Tokio project", "uber": "Uber", "uswds": "USWDS", "utsa": "University of Texas at San Antonio", "vorpus": "Nathaniel J. Smith",
    "warne": "Henrik Warne", "wayne": "Hillel Wayne", "webaim": "WebAIM", "whatwg": "WHATWG", "winand": "Markus Winand",
    "wordpress": "WordPress", "w3c": "W3C", "envoy": "Envoy", "hyrum": "Hyrum Wright", "owasp": "OWASP", "zalando": "Zalando", "fastly": "Fastly", "scipy": "SciPy project", "ndepend": "NDepend", "nimblepros": "NimblePros (DevIQ)", "openid": "OpenID Foundation", "oasis": "OASIS", "gradle": "Gradle", "hibernate": "Hibernate (Red Hat)", "skypilot": "SkyPilot project", "svix": "Svix", "nginx": "NGINX", "pytest-socket": "pytest-socket project", "sequelize": "Sequelize", "akamai": "Akamai", "vercel": "Vercel", "typeorm": "TypeORM", "varnish": "Varnish Cache project", "attrs": "attrs project", "etsy": "Etsy", "standardwebhooks": "Standard Webhooks", "saml-toolkits": "SAML-Toolkits project",
    "jetbrains": "JetBrains", "nvidia": "NVIDIA", "statsig": "Statsig", "etcd": "etcd", "hazelcast": "Hazelcast",
    "cockroach": "CockroachDB", "anthropic": "Anthropic",
    "vitest": "Vitest", "typescript-eslint": "typescript-eslint project", "testing-library": "Testing Library", "cmu-sei": "Carnegie Mellon SEI", "wikimedia": "Wikimedia (MediaWiki)", "lockheed": "Lockheed Martin", "fowler": "Martin Fowler", "pablo-gonzalez": "Pablo González",
    "thoughtworks": "Thoughtworks", "eslint": "ESLint", "buf": "Buf", "amex": "American Express", "reactive-streams": "Reactive Streams", "pulumi": "Pulumi", "bcgov": "Government of British Columbia", "ukhsa": "UKHSA", "thoughtbot": "thoughtbot", "softwaremill": "SoftwareMill", "scrimba": "Scrimba", "safeguard": "Safeguard.sh", "drupal": "Drupal", "postgresai": "Postgres.ai", "moodle": "Moodle", "airtable": "Airtable", "gocardless": "GoCardless", "gerrit": "Gerrit Code Review", "fsd": "Feature-Sliced Design", "paradigma": "Paradigma Digital", "gusto": "Gusto", "webkit": "WebKit", "temporal": "Temporal", "xurrent": "Xurrent", "monday": "monday.com", "jobber": "Jobber", "civicactions": "CivicActions", "arizona": "University of Arizona", "doctolib": "Doctolib", "istio": "Istio", "posthog": "PostHog", "remix": "Remix",
    "astral": "Astral", "swift": "Swift project", "symfony": "Symfony",
    "dagster": "Dagster", "deliveroo": "Deliveroo", "gnome": "GNOME", "siemens": "Siemens", "epicgames": "Epic Games", "getyourguide": "GetYourGuide", "almalinux": "AlmaLinux", "island": "Ísland.is", "mozilla-ai": "Mozilla.ai", "pycqa": "PyCQA", "tum": "TUM ESI", "csa": "Cloud Security Alliance", "paypal": "PayPal", "aisi": "UK AI Security Institute", "retool": "Retool", "nasa": "NASA", "industriallogic": "Industrial Logic", "infoq": "InfoQ", "notion": "Notion", "redhat": "Red Hat",
}

# Orgs that are one author. They show in "Backed by" but never count toward the three organisations a stable card needs.
PERSONS = {
    "clig", "go-update",
    "brendan-gregg", "dan-luu", "feathers", "heydon", "hickey", "hyrum", "jnd", "joel", "kane", "zupo", "kent-beck", "kent-c-dodds",
    "kleppmann", "liskov-wing", "lucumr", "mcintosh", "ousterhout", "portebois", "salvatore", "sandi-metz", "shneiderman",
    "tef", "fowler", "pablo-gonzalez", "vorpus", "warne", "wayne", "winand",
}

# Creators: the repository's author. A stable card that cites one of these passes the organisation floor.
CREATORS = {"pablo-gonzalez"}

# Standing of a person under the test in docs/PROMOTION.md (checked 2026-10-28): id -> (yes|no, deciding evidence). Standing never makes a person count toward the three organisations.
STANDING = {
    "kent-beck": ("yes", "Tidy First?, O'Reilly 2023, ISBN 9781098151232; TDD by Example, Addison-Wesley 2002, ISBN 9780321146533; created Extreme Programming and TDD, en.wikipedia.org/wiki/Kent_Beck"),
    "joel": ("yes", "Joel on Software, Apress 2004, ISBN 9781590593899, chapter doi.org/10.1007/978-1-4302-0753-5_24"),
    "hickey": ("yes", "Created Clojure; Clojure/Conj 2010 keynote, web.archive.org/web/20101021055240/http://clojure-conj.org/schedule; A History of Clojure, ACM HOPL 2020, doi.org/10.1145/3386321. The cited page backs code-adr, not chg-matches-spec"),
    "jnd": ("no", "The Design of Everyday Things, Basic Books 2013, ISBN 9780465050659, but the cited essay states no rule for fn-native-button-or-link"),
    "salvatore": ("no", "Created Redis and Redlock, but sys-lock-fencing is about fencing, not Redlock; the cited page argues against requiring fencing tokens"),
}

# URL prefix (no scheme) -> org id. The longest matching prefix wins. A prefix without "/" also matches subdomains,
# so "owasp.org" covers cheatsheetseries.owasp.org. On code hosts the org is the repository owner, never the host.
PREFIXES = {
    "wiki.debian.org": "debian", "source.android.com": "google", "docs.mender.io": "mender", "pubs.opengroup.org": "opengroup", "rust-cli.github.io": "rust", "developer.hashicorp.com": "hashicorp", "git-scm.com": "git", "gnu.org": "gnu", "theupdateframework.io": "tuf", "sparkle-project.org": "sparkle", "docs.sigstore.dev": "sigstore", "clig.dev": "clig", "pkg.go.dev/github.com/inconshreveable/go-update": "go-update", "devcenter.heroku.com": "heroku", "raw.githubusercontent.com/Azure/": "microsoft", "github.com/Azure/": "microsoft", "github.com/usnistgov/": "nist", "tech.gr.vodafone.com": "vodafone", "docs.pytest.org": "pytest",
    "12factor.net": "heroku", "airbnb.tech": "airbnb", "alphagov.github.io": "govuk", "angular.dev": "google",
    "antirez.com": "salvatore", "flex.apache.org": "apache", "cwiki.apache.org/confluence/display/QUICKSTEP": "apache", "github.com/google/": "google", "wiki.openjdk.org": "openjdk", "sonarsource.com": "sonarsource", "contributing.godotengine.org": "godot", "astrogeology.usgs.gov": "usgs", "depo-platform-documentation.scrollhelp.site": "va", "geth.ethereum.org": "ethereum", "rustc-dev-guide.rust-lang.org": "rust", "edgeguides.rubyonrails.org": "rails", "usenix.org/legacy/event/osdi06/tech/full_papers/burrows/burrows.pdf": "google", "arxiv.org/abs/2406.10279": "utsa", "atlassian.design": "atlassian", "auth0.com": "auth0",
    "aws.amazon.com": "aws", "aws.com": "aws", "baymard.com": "baymard", "bazel.build": "google", "blog.google": "google",
    "blog.palantir.com": "palantir", "fastly.com": "fastly", "airbnb.io": "airbnb", "openjdk.org": "openjdk", "scipy.github.io": "scipy", "blog.ndepend.com": "ndepend", "deviq.com": "nimblepros", "openid.net": "openid", "oasis-open.org": "oasis", "about.gitlab.com": "gitlab", "code.visualstudio.com": "microsoft", "develocity.ai": "gradle", "docs.gradle.com": "gradle", "docs.jboss.org/hibernate/": "hibernate", "docs.skypilot.ai": "skypilot", "docs.svix.com": "svix", "httpd.apache.org": "apache", "next.sonarqube.com": "sonarsource", "nginx.org": "nginx", "pytest-socket.readthedocs.io": "pytest-socket", "raw.githubusercontent.com/SonarSource/": "sonarsource", "sequelize.org": "sequelize", "techdocs.akamai.com": "akamai", "turborepo.com": "vercel", "typeorm.io": "typeorm", "varnish-cache.org": "varnish", "attrs.org": "attrs", "etsy.com": "etsy", "ietf.org": "ietf", "standardwebhooks.com": "standardwebhooks", "github.com/SAML-Toolkits/": "saml-toolkits", "blog.pragmaticengineer.com": "pragmatic-engineer", "newsletter.pragmaticengineer.com": "pragmatic-engineer",
    "cassandra.apache.org": "apache", "cloudflare.com": "cloudflare", "codeql.github.com": "github", "cwe.mitre.org": "mitre",
    "danluu.com": "dan-luu", "datatracker.ietf.org": "ietf", "dequeuniversity.com": "deque", "deque.com": "deque",
    "designsystem.digital.gov": "uswds", "gov.uk": "govuk", "ncsc.gov.uk": "ncsc", "dev.to/sportebois/": "portebois",
    "developer.apple.com": "apple", "mozilla.org": "mozilla", "cloud.google.com": "google", "developers.google.com": "google",
    "devguide.python.org": "psf", "docs.python.org": "psf", "peps.python.org": "psf", "pip.pypa.io": "psf",
    "requests.readthedocs.io": "requests", "docs.appian.com": "appian", "docs.djangoproject.com": "django", "dev.mysql.com": "oracle",
    "docs.oracle.com": "oracle", "docs.gatling.io": "gatling", "docs.github.com": "github", "cli.github.com": "github", "github.blog": "github",
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
    "primer.style": "github", "github.com/GoogleChrome/": "google", "github.com/Netflix/": "netflix", "github.com/ai/size-limit": "sitnik",
    "github.com/ankane/": "kane", "github.com/zupo/awesome-pytest-speedup": "zupo", "pylint.readthedocs.io": "pylint", "github.com/pylint-dev/": "pylint", "checkstyle.sourceforge.io": "checkstyle", "docs.rubocop.org": "rubocop", "pmd.github.io": "pmd", "docs.pmd-code.org": "pmd", "github.com/import-js/": "importjs", "nx.dev": "nx", "archunit.org": "archunit", "pylint.pycqa.org": "pylint", "rfd.shared.oxide.computer": "oxide", "laravel.com": "laravel", "hexdocs.pm/ecto": "ecto", "pytest-django.readthedocs.io": "pytest-django", "pytest-xdist.readthedocs.io": "pytest-xdist", "alloy.ai": "alloy", "blog.trailofbits.com": "trailofbits", "exante.eu": "exante", "medium.com/alan/": "alan", "github.com/ben-manes/caffeine": "ben-manes", "github.com/cursor/plugins/": "cursor",
    "github.com/dequelabs/": "deque", "github.com/ghostty-org/": "ghostty", "github.com/johnousterhout/": "ousterhout",
    "github.com/jsx-eslint/": "jsx-eslint", "github.com/matthiasn/talk-transcripts/blob/master/Hickey_Rich/": "hickey",
    "github.com/microsoft/": "microsoft", "typescriptlang.org": "microsoft", "vitest.dev": "vitest", "typescript-eslint.io": "typescript-eslint", "testing-library.com": "testing-library", "github.com/uber-go/": "uber", "github.com/google-gemini/": "google", "cursor.com": "cursor", "github.com/mozilla/": "mozilla", "github.com/ossf/": "openssf", "bestpractices.dev": "openssf", "github.com/github/": "github", "github.com/rust-lang/": "rust",
    "cmu-sei.github.io": "cmu-sei", "sei.cmu.edu": "cmu-sei", "mediawiki.org": "wikimedia",
    "stroustrup.com/JSF-AV-rules.pdf": "lockheed", "martinfowler.com": "fowler", "pablogonzalez.me": "pablo-gonzalez",
    "x.com/addyosmani/status/2114604912520921136": "anthropic",
    "raw.githubusercontent.com/OWASP/": "owasp", "raw.githubusercontent.com/WordPress/": "wordpress",
    "raw.githubusercontent.com/elastic/": "elastic", "raw.githubusercontent.com/mozilla/": "mozilla",
    "docs.docker.com": "docker", "github.com/kubernetes/": "kubernetes", "doc.rust-lang.org": "rust",
    "thoughtworks.com": "thoughtworks", "shopify.dev": "shopify", "rust-lang.github.io": "rust", "handbook.gitlab.com": "gitlab", "eslint.org": "eslint", "buf.build": "buf", "americanexpress.io": "amex", "reactive-streams.org": "reactive-streams", "pulumi.com": "pulumi", "atlassian.com": "atlassian", "www2.gov.bc.ca": "bcgov", "gov.bc.ca": "bcgov", "ukhsa-collaboration.github.io": "ukhsa", "thoughtbot.com": "thoughtbot", "softwaremill.com": "softwaremill", "scrimba.com": "scrimba", "safeguard.sh": "safeguard", "project.pages.drupalcode.org": "drupal", "postgres.ai": "postgresai", "moodledev.io": "moodle", "medium.com/airtable-eng": "airtable", "gocardless.com": "gocardless", "gerrit-review.googlesource.com": "gerrit", "feature-sliced.design": "fsd", "en.paradigmadigital.com": "paradigma", "engineering.gusto.com": "gusto", "docs.webkit.org": "webkit", "docs.temporal.io": "temporal", "docs.slack.dev": "slack", "docs.prow.k8s.io": "kubernetes", "developer.xurrent.com": "xurrent", "developer.wordpress.org": "wordpress", "developer.monday.com": "monday", "developer.getjobber.com": "jobber", "design.va.gov": "va", "accessibility.civicactions.com": "civicactions", "accessibility.arizona.edu": "arizona", "github.com/doctolib/": "doctolib", "github.com/envoyproxy/": "envoy", "github.com/istio/": "istio", "github.com/nodejs/": "nodejs", "github.com/open-telemetry/": "opentelemetry", "github.com/PostHog/": "posthog", "github.com/spring-projects/": "spring", "raw.githubusercontent.com/remix-run/": "remix",
    "docs.astral.sh": "astral", "kotlinlang.org": "jetbrains", "swift.org": "swift", "legacy.reactjs.org": "meta", "reactjs.org": "meta", "symfony.com": "symfony",
    "airflow.apache.org": "apache", "android.googlesource.com": "google", "azure.github.io": "microsoft", "dagster.io": "dagster", "deliveroo.engineering": "deliveroo", "developer.gnome.org": "gnome", "developer.siemens.com": "siemens", "docs.unrealengine.com": "epicgames", "dev.epicgames.com": "epicgames", "engineering.zalando.com": "zalando", "getyourguide.careers": "getyourguide", "github.com/AlmaLinux/": "almalinux", "github.com/island-is/": "island", "github.com/mozilla-ai/": "mozilla-ai", "github.com/PyCQA/": "pycqa", "github.com/tum-esi/": "tum", "labs.cloudsecurityalliance.org": "csa", "medium.com/paypal-tech": "paypal", "raw.githubusercontent.com/UKGovernmentBEIS/": "aisi", "retool.com": "retool", "swehb.nasa.gov": "nasa", "anthropic.com": "anthropic", "industriallogic.com": "industriallogic", "infoq.com": "infoq", "notion.com": "notion", "redhat.com": "redhat",
}

ICONS = json.loads((Path(__file__).with_name("org_icons.json")).read_text())  # org id -> SVG path from Simple Icons 15.22.0 (CC0), https://simpleicons.org


def org_of(url: str) -> str | None:
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


@dataclass(frozen=True, slots=True)
class OrgUrls:
    """An organisation id and the source URLs it publishes."""

    id: str
    urls: list[str]


@dataclass(frozen=True, slots=True)
class Sources:
    """The sources of a card, split into organisations and people."""

    organisations: list[OrgUrls]
    people: list[OrgUrls]


def group(urls: list[str]) -> list[OrgUrls]:
    """Group URLs by organisation, in first-cited order. Raises KeyError on a URL no prefix matches."""
    out: dict[str, list[str]] = {}
    for u in urls:
        o = org_of(u)
        if o is None:
            raise KeyError(f"no organisation for {u}; add a prefix to tools/orgs.py")
        out.setdefault(o, []).append(u)
    return [OrgUrls(o, us) for o, us in out.items()]


def split(urls: list[str]) -> Sources:
    """Split the URLs into organisations and people, each in first-cited order."""
    g = group(urls)
    return Sources([x for x in g if x.id not in PERSONS], [x for x in g if x.id in PERSONS])


def monogram(oid: str) -> str:
    """Up to four characters for an org without a logo: the acronym ("W3C", "AWS") or the initials ("NN" for Nielsen Norman Group)."""
    name = ORGS[oid].split(" (")[0]
    if name.replace(".", "").isupper():
        return "".join(c for c in name if c.isalnum())[:4]
    return "".join(w[0] for w in name.split() if w[0].isupper())[:2] or name[0].upper()
