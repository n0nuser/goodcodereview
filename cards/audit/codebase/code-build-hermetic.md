---
id: code-build-hermetic
level: codebase
tags: [process, build, reproducibility]
severity: should-fix
status: stable
lang: core
applies_when: The repository has a build, a packaging, or a release step.
tool_gate: Build twice in clean containers and compare checksums; `diffoscope` shows where two artifacts differ.
note: Rule backed by Google (Bazel hermeticity), Airbnb (Gradle tasks could touch the whole file system, Bazel sandboxes each action to its declared inputs) and Slack (a build step must use only the inputs it is given and give the same output for them); Dropbox lists hermetic, reproducible builds as a Bazel benefit; pinned toolchains (Google only) sit in Why
borrowed_from:
  - https://bazel.build/basics/hermeticity
  - https://reproducible-builds.org/docs/definition/
  - https://airbnb.tech/infrastructure/migrating-airbnbs-jvm-monorepo-to-bazel/
  - https://slack.engineering/build-better-software-to-build-software-better/
  - https://dropbox.tech/infrastructure/how-we-migrated-dropbox-from-nginx-to-envoy
---

**Rule.** Build from declared inputs only, so that the same source revision gives the same artifact.

**Why.** A build that reads whatever is installed on the machine gives different output on different machines, so a bug cannot be reproduced and a release cannot be checked against its source. Tools are inputs too: pin the compiler and toolchain versions, and do not call host binaries. Undeclared shared files also break builds at scale, for example two tasks that clean and use the same `/tmp` directory race each other.

**FAIL**

```yaml
steps:
  - run: make               # uses whatever gcc, node and protoc the runner has
  - run: date > BUILD_ID    # the clock is an undeclared input
```

**PASS**

```yaml
container:
  image: ghcr.io/acme/builder@sha256:4b1e...   # toolchain pinned by digest
steps:
  - run: SOURCE_DATE_EPOCH=$(git log -1 --format=%ct) make   # timestamps come from the commit
```

**Counterpoint.** "Bit-identical builds are overkill." Full reproducibility is the ceiling. Declared inputs, pinned tools, and a recorded revision are the floor, and they cost little. [[code-dependency-pinning]] covers dependency pins.
