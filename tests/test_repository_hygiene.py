"""Repository hygiene, metadata, and configuration contract tests for ellmos-bundles."""
from __future__ import annotations

import compileall
from pathlib import Path
import tomllib

REPO_ROOT = Path(__file__).resolve().parents[1]


def test_pep621_pyproject_metadata() -> None:
    """Validate PEP 621 metadata completeness in pyproject.toml."""
    pyproject_path = REPO_ROOT / "pyproject.toml"
    assert pyproject_path.is_file(), "pyproject.toml must exist"

    data = tomllib.loads(pyproject_path.read_text(encoding="utf-8"))
    assert "project" in data, "pyproject.toml missing [project] table"
    project = data["project"]

    assert project["name"] == "ellmos-bundles"
    assert project["version"] == "1.0.2"
    assert project["requires-python"] == ">=3.10"
    assert project["license"] == {"text": "MIT"}
    assert len(project["keywords"]) >= 5
    assert len(project["classifiers"]) >= 5

    # Optional dependencies
    opt_deps = project.get("optional-dependencies", {})
    assert "test" in opt_deps, "Missing test optional dependencies"
    assert any("pytest" in dep for dep in opt_deps["test"])

    # URLs
    urls = project.get("urls", {})
    assert "Homepage" in urls
    assert "Repository" in urls
    assert "Issues" in urls
    assert "Documentation" in urls
    assert "Changelog" in urls
    assert "Organization" in urls
    assert "LLM Ready" in urls
    assert "Security Policy" in urls
    assert "Marketing Log" in urls


def test_license_integrity() -> None:
    """Verify LICENSE exists and specifies MIT terms."""
    license_path = REPO_ROOT / "LICENSE"
    assert license_path.is_file(), "LICENSE must exist"
    content = license_path.read_text(encoding="utf-8")
    assert "MIT License" in content
    assert "Copyright" in content


def test_gitignore_hygiene() -> None:
    """Verify .gitignore covers multi-agent locks, sync conflicts, and test caches."""
    gitignore_path = REPO_ROOT / ".gitignore"
    assert gitignore_path.is_file(), ".gitignore must exist"
    content = gitignore_path.read_text(encoding="utf-8")

    assert "LOCK" in content
    assert "LOCK.*" in content
    assert "*-conflict-*" in content
    assert "*-ASUS-GEI.*" in content
    assert "*-WORKSTATION-LG.*" in content
    assert "*conflicted copy*" in content
    assert "uv.lock" in content
    assert ".pytest_cache/" in content
    assert ".ruff_cache/" in content
    assert "__pycache__/" in content
    assert "PRIVATE.txt" in content


def test_ci_matrix_workflow() -> None:
    """Verify GitHub Actions CI matrix covers multi-OS, Python 3.10-3.12, and timeouts."""
    ci_path = REPO_ROOT / ".github" / "workflows" / "ci.yml"
    assert ci_path.is_file(), "CI workflow must exist"
    content = ci_path.read_text(encoding="utf-8")

    assert "ubuntu-latest" in content
    assert "windows-latest" in content
    assert '"3.10"' in content
    assert '"3.11"' in content
    assert '"3.12"' in content
    assert "timeout-minutes: 15" in content
    assert "cancel-in-progress: true" in content
    assert "contents: read" in content
    assert "pytest -ra -v" in content


def test_stale_workflow() -> None:
    """Verify stale issue/PR lifecycle workflow exists with timeouts and permissions."""
    stale_path = REPO_ROOT / ".github" / "workflows" / "stale.yml"
    assert stale_path.is_file(), "stale workflow must exist"
    content = stale_path.read_text(encoding="utf-8")
    assert "actions/stale@v9" in content
    assert "timeout-minutes: 10" in content
    assert "cancel-in-progress: true" in content
    assert "issues: write" in content
    assert "pull-requests: write" in content


def test_welcome_workflow() -> None:
    """Verify welcome workflow for first-time contributors exists with timeouts."""
    welcome_path = REPO_ROOT / ".github" / "workflows" / "welcome.yml"
    assert welcome_path.is_file(), "welcome workflow must exist"
    content = welcome_path.read_text(encoding="utf-8")
    assert "actions/first-interaction@v3" in content
    assert "timeout-minutes: 5" in content
    assert "cancel-in-progress: true" in content
    assert "issues: write" in content
    assert "pull-requests: write" in content


def test_readme_parity_and_banners() -> None:
    """Verify README.md and README_de.md exist, cross-link, and preserve header banners."""
    readme_en = REPO_ROOT / "README.md"
    readme_de = REPO_ROOT / "README_de.md"
    assert readme_en.is_file()
    assert readme_de.is_file()

    text_en = readme_en.read_text(encoding="utf-8")
    text_de = readme_de.read_text(encoding="utf-8")

    # Cross-links
    assert "README_de.md" in text_en
    assert "README.md" in text_de

    # Banner preservation
    assert '<img src="assets/banner.png" width="100%" alt="bundles Banner">' in text_en
    assert '<img src="assets/banner.png" width="100%" alt="bundles Banner">' in text_de

    # Shields.io badges present
    assert "shields.io" in text_en
    assert "shields.io" in text_de


def test_security_policy_structure() -> None:
    """Verify SECURITY.md exists, specifies zero egress, and 48h SLA."""
    sec_path = REPO_ROOT / "SECURITY.md"
    assert sec_path.is_file(), "SECURITY.md must exist"
    content = sec_path.read_text(encoding="utf-8")
    assert "48 hours" in content or "48h" in content
    assert "Zero Network Egress" in content
    assert "Reporting a Vulnerability" in content


def test_marketing_log_structure() -> None:
    """Verify MARKETING-LOG.txt exists and documents value proposition and personas."""
    mkt_path = REPO_ROOT / "MARKETING-LOG.txt"
    assert mkt_path.is_file(), "MARKETING-LOG.txt must exist"
    content = mkt_path.read_text(encoding="utf-8")
    assert "Value Proposition" in content
    assert "Target Audience" in content
    assert "Discoverability & SEO-Keywords" in content
    assert "ellmos-ai/bundles" in content


def test_llms_txt_structure() -> None:
    """Verify llms.txt exists and has up-to-date metadata."""
    llms_path = REPO_ROOT / "llms.txt"
    assert llms_path.is_file(), "llms.txt must exist"
    content = llms_path.read_text(encoding="utf-8")
    assert "## Last-checked: 2026-09-14" in content
    assert "Canonical repository: https://github.com/ellmos-ai/bundles" in content
    assert "SECURITY.md" in content
    assert "MARKETING-LOG.txt" in content


def test_changelog_structure() -> None:
    """Verify CHANGELOG.md exists and documents releases."""
    changelog_path = REPO_ROOT / "CHANGELOG.md"
    assert changelog_path.is_file(), "CHANGELOG.md must exist"
    content = changelog_path.read_text(encoding="utf-8")
    assert "## [1.0.2] - 2026-09-14" in content
    assert "## [1.0.1] - 2026-09-10" in content
    assert "## [1.0.0] - 2026-08-08" in content


def test_python_syntax_clean() -> None:
    """Verify all Python scripts compile cleanly without syntax errors."""
    success_tools = compileall.compile_dir(str(REPO_ROOT / "tools"), quiet=1)
    assert success_tools, "Syntax error in tools directory"
    success_tests = compileall.compile_dir(str(REPO_ROOT / "tests"), quiet=1)
    assert success_tests, "Syntax error in tests directory"
