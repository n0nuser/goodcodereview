---
id: code-build-hermetic
level: codebase
tags: [process, build, reproducibility]
severity: should-fix
status: draft
lang: core
applies_when: The repository has a build, a packaging, or a release step.
tool_gate: Build twice in a clean container and compare checksums; pinned toolchain files checked in.
borrowed_from:
  - https://bazel.build/basics/hermeticity
  - https://reproducible-builds.org/docs/definition/
---

**Rule.** Build from declared inputs only (pinned tool and compiler versions, no host binaries), so that the same source revision gives the same artifact.

**Why.** A build that reads whatever is installed on the machine gives different output on different machines, so a bug cannot be reproduced and a release cannot be checked against its source.

**FAIL**

```text
build:
  run: make            # uses whatever gcc, node and protoc the runner has
  run: date > BUILD_ID # timestamp in the artifact
```

**PASS**

```text
build:
  image: builder@sha256:...     # toolchain pinned by digest
  run: make                     # no clock, absolute paths or host tools in output
```

**Counterpoint.** "Bit-identical builds are overkill." Full reproducibility is the ceiling. Pinned tools and a recorded revision are the floor, and they cost little. [[code-dependency-pinning]] covers dependency pins.
