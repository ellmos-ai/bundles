# Security Policy — bundles

## Overview

`bundles` provides the declarative recipe layer of the ellmos ecosystem: bundle manifests, catalogues, and composition knowledge. Security in `bundles` centers around static declarative integrity, cryptographic hash verification, zero external network egress, and non-elevated tooling.

## Security Architecture & Principles

### 1. Pure Declarative & Static Data
- `bundles` consists exclusively of structured JSON manifests, schemas, contracts, documentation, and frozen visual design tokens.
- There are no executable runtime binaries, no background daemon processes, and no dynamic code evaluation pipelines.

### 2. Local-First & Zero Network Egress
- All tools in `tools/` (`tools/generate_banner.py`, `tools/export_from_source.py`) and test suites operate entirely offline.
- The repository requires **zero network dependencies**, opens no network ports, and transmits no telemetry or background requests.

### 3. Bit-Identical Reproducibility & Cryptographic Hashes
- Every bundle manifest, contract, catalog, and export receipt carries an explicit canonical SHA-256 `content_hash`.
- Integrity is continuously validated via automated contract test suites (`tests/test_bundle_contracts.py`), preventing tampering or bit rot.

### 4. Non-Elevated Execution & Privilege Isolation
- Repository tools and automation scripts run in standard user mode (`RunAsInvoker`).
- No administrative or elevated operating system privileges are required or requested.

## Supported Versions

| Version | Supported          |
| ------- | ------------------ |
| 1.0.x   | :white_check_mark: |
| < 1.0.0 | :x:                |

## Reporting a Vulnerability

If you discover a security vulnerability or integrity hazard in `bundles`:

1. **Do not open a public issue.**
2. Report the vulnerability privately via GitHub Security Advisories at [https://github.com/ellmos-ai/bundles/security/advisories](https://github.com/ellmos-ai/bundles/security/advisories) or directly to the repository maintainers.
3. Include detailed steps to reproduce, affected manifests or tools, and observed behavior.
4. Reports are acknowledged within **48 hours**, and resolutions will be coordinated prior to publication.
