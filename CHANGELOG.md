# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.2] - 2026-09-14

### Added
- **CI Hardening**: Added `timeout-minutes: 15` and concurrency cancel-in-progress to `.github/workflows/ci.yml`.
- **Stale Automation Hardening**: Added `timeout-minutes: 10` and concurrency cancel-in-progress to `.github/workflows/stale.yml`.
- **Welcome Contributor Workflow**: Added `.github/workflows/welcome.yml` with `actions/first-interaction@v3` (timeout-minutes: 5, least-privilege permissions).
- **Security Policy**: Added `SECURITY.md` establishing local-first zero-network-egress guarantees, declarative manifest integrity, and 48h vulnerability response SLA.
- **Discoverability & Marketing Log**: Added `MARKETING-LOG.txt` defining value proposition, target personas, SEO queries, and ecosystem positioning.
- **Extended Contract Tests**: Added new tests in `tests/test_repository_hygiene.py` validating CI timeouts, welcome workflow, security policy SLA, marketing log, and multi-host lock exclusions.

### Changed
- **Gitignore Hardening**: Expanded `.gitignore` with comprehensive multi-host cloud-sync conflict masks (`* (kopie)*`, `* (copy)*`, `*conflicted copy*`, `*-ASUS*`, `*-WORKSTATION*`, `*.sync-conflict-*`), multi-agent locks (`LOCK`, `LOCK.*`, `*.lock`, `uv.lock`), and coverage/test caches.
- **PEP 621 Standardisation**: Harmonized `pyproject.toml` version to `1.0.2`, added URLs (`Documentation`, `LLM Ready`, `Security Policy`, `Marketing Log`), and standardized pytest `addopts`.
- **LLM Context Refresh**: Updated `llms.txt` verification timestamp to 2026-09-14 and indexed security policy and marketing log.

## [1.0.1] - 2026-09-10

### Added
- **PEP 621 Metadata**: Added `pyproject.toml` declaring package metadata, classifiers, URLs, test/dev dependencies, and pytest/ruff configuration.
- **CI Matrix Workflow**: Added GitHub Actions Multi-OS Matrix (`.github/workflows/ci.yml`) testing on Python 3.10, 3.11, and 3.12 across Ubuntu and Windows runners.
- **Stale Automation**: Added `.github/workflows/stale.yml` for automated issue and pull request lifecycle management.
- **Automated Contract & Hygiene Tests**:
  - `tests/test_repository_hygiene.py`: Contract tests for PEP 621 metadata, license integrity, multi-agent lock gitignores, CI matrix specification, and bilingual README parity.
  - `tests/test_bundle_contracts.py`: Comprehensive schema and contract validation for all 13 bundles in `manifests/bundles/`, verification of `manifests/bundles.catalog.v1.json`, contract validation against `contracts/bundle-family-contract.v1.json` and `contracts/choice-bundle-contract.v1.json`, verification of `manifests/export-receipt.v1.json` file listings, and bit-level canonical `content_hash` verification across all 17 JSON artifacts.
- **Status Badges**: Added Shields.io badges in `README.md` and `README_de.md` for CI status, supported Python versions, MIT license, bundle catalog count, schema version, public release status, llms.txt readiness, and ecosystem affiliation.

### Changed
- **Gitignore Hardening**: Added exclusions for multi-agent locks (`LOCK.*`, `*.lock`, `LOCK.permissions.json`), multi-host synchronization conflicts (`*-conflict-*`, `*-ASUS-GEI.*`, `*-WORKSTATION-LG.*`), and test/build artifacts.
- **Metadata Refresh**: Updated `llms.txt` verification timestamp to 2026-09-10.

## [1.0.0] - 2026-08-08

### Added
- **Initial Public Release (Waves 1 and 2)**: 13 bundle manifests released across two functional rings:
  - Ring 1 (Functional Core): `ellmos-working-memory-bundle`, `ellmos-memory-human-context-bundle`, `ellmos-agents-bundle`, `ellmos-coordination-choice-bundle`, `ellmos-knowledge-bundle`.
  - Ring 2 (Life, Work, and Domain Assistants): `ellmos-daily-life-bundle`, `ellmos-finance-assist-bundle`, `ellmos-health-assist-bundle`, `ellmos-doc-handler-bundle`, `ellmos-media-production-bundle`, `ellmos-voice-media-assist-bundle`, `ellmos-briefing-bundle`, `ellmos-knowledge-search-choice-bundle`.
- **Reproducible Export**: Tool `tools/export_from_source.py` projecting bundle manifests from private composition repository with bit-identical repeatability.
- **Visual Design System & Banners**: Tool `tools/generate_banner.py`, frozen design tokens (`assets/design/tokens.json`), SVG template, and dedicated banners for all 13 bundles in `assets/banners/`.
- **Contracts**: Declarative contracts in `contracts/` (`bundle-family-contract.v1.json`, `choice-bundle-contract.v1.json`).
- **Catalog & Manifests**: `manifests/bundles.catalog.v1.json` and export receipt `manifests/export-receipt.v1.json`.
- **Bilingual Documentation**: Comprehensive `README.md` and `README_de.md` with 1:1 parity and dedicated detail pages in `docs/bundles/`.
- **Machine-Readable Context**: `llms.txt` defining bundle architecture, audience, and search phrases.
