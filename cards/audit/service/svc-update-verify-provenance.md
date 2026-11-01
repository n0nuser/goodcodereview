---
id: svc-update-verify-provenance
level: service
tags: [security, supply-chain, cli]
severity: should-fix
status: stable
note: Backed by Sparkle (signed archive, keys kept off the web server), Sigstore (signing covers a compromised hosting site), TUF (SSL alone leaves one key to steal) and Debian (checksums are only trusted once the Release file is signed); GitHub and Google (Go checksum database) show the same practice; go-update is a reference
lang: core
applies_when: The code downloads and installs or runs a new version of itself or of another program, such as a self-updater or an install script.
tool_gate: none
borrowed_from:
  - https://sparkle-project.org/documentation/
  - https://docs.sigstore.dev/about/overview/
  - https://theupdateframework.io/security/
  - https://wiki.debian.org/SecureApt
  - https://docs.github.com/en/actions/concepts/security/artifact-attestations
  - https://go.dev/blog/supply-chain
  - https://pkg.go.dev/github.com/inconshreveable/go-update
---

**Rule.** Verify a downloaded update against a signature, an attestation or a pinned key, or against a checksum that reached you by another route than the file; a checksum fetched from the same host as the file does not count.

**Why.** An attacker who controls the download host replaces the archive and its checksum file together, so the check passes and the new binary runs with the user's rights. A signature made with a key that is not on that host, or a hash from a different channel, still fails for the attacker.

**FAIL**

```go
archive, _ := get(base + "/tool.tar.gz")
want, _ := get(base + "/tool.tar.gz.sha256") // same host as the archive
got := sha256.Sum256(archive)
if hex.EncodeToString(got[:]) != strings.TrimSpace(string(want)) {
	return errors.New("checksum mismatch")
}
install(archive)
```

**PASS**

```go
var releaseKey = mustDecodeKey("<base64 public key>") // compiled into the binary, never downloaded

archive, _ := get(base + "/tool.tar.gz")
sig, _ := get(base + "/tool.tar.gz.sig")
if !ed25519.Verify(releaseKey, archive, sig) {
	return errors.New("bad signature")
}
install(archive)
```

**Counterpoint.** "HTTPS already protects the download, and signing needs key management." TLS protects the connection to the host, not the files on it once the host or its account is breached. Keyless signing and build attestations remove most of the key handling.
