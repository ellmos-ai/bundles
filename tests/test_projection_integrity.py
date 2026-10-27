"""Public gate acceptance and mutation tests; fixtures never touch released data."""
from __future__ import annotations

import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path

import pytest

from tools.export_from_source import canonical_hash, repin
from tools.validate_projection import banner_options, canonical_digest, public_path

ROOT = Path(__file__).resolve().parents[1]
CATALOG = "manifests/bundles.catalog.v1.json"
RECEIPT = "manifests/export-receipt.v1.json"
AGENTS = "manifests/bundles/ellmos-agents-bundle/bundle.v1.json"
KNOWLEDGE = "ellmos-knowledge-search-choice-bundle"


@pytest.fixture
def projection(tmp_path: Path) -> Path:
    for folder in ("manifests", "contracts", "assets/design", "assets/banners", "docs/preview", "tools"):
        shutil.copytree(ROOT / folder, tmp_path / folder, ignore=shutil.ignore_patterns("__pycache__"))
    return tmp_path


def read(root: Path, path: str) -> dict:
    return json.loads((root / path).read_text(encoding="utf-8"))


def write(root: Path, path: str, value: dict, *, repin: bool = True) -> None:
    # Existing exporter supplies fixture hashes, independently of the new gate.
    if repin:
        value["content_hash"] = canonical_hash(value)
    (root / path).write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def run_gate(root: Path) -> subprocess.CompletedProcess:
    return subprocess.run([sys.executable, "-I", "-S", str(root / "tools/validate_projection.py")],
                          cwd=root.parent, capture_output=True, text=True, encoding="utf-8", check=False,
                          env={**os.environ, "PYTHONIOENCODING": "utf-8", "BUNDLES_SOURCE": str(root / "absent")})


def rejected(root: Path, path: str, invariant: str) -> None:
    result = run_gate(root)
    assert result.returncode != 0
    assert path in result.stderr and invariant in result.stderr, result.stderr
    assert "Traceback" not in result.stderr


def test_offline_stdlib_gate_and_read_only_inventory(projection: Path) -> None:
    before = {p.relative_to(projection): hashlib.sha256(p.read_bytes()).hexdigest()
              for p in projection.rglob("*") if p.is_file()}
    result = run_gate(projection)
    assert result.returncode == 0, result.stderr
    assert "json=18, hashes=17, catalog=13, receipt_targets=16, banners=13, previews=13" in result.stdout
    after = {p.relative_to(projection): hashlib.sha256(p.read_bytes()).hexdigest()
             for p in projection.rglob("*") if p.is_file()}
    assert before == after


def test_canonical_unicode_vector_preserves_nested_pin() -> None:
    value = {"z": "ä", "a": {"content_hash": "pin"}, "content_hash": "ignored"}
    payload = '{"a":{"content_hash":"pin"},"z":"ä"}'.encode()
    assert canonical_digest(value) == hashlib.sha256(payload).hexdigest()


@pytest.mark.parametrize("path", [AGENTS, CATALOG, RECEIPT, "contracts/bundle-family-contract.v1.json"])
def test_hash_drift(projection: Path, path: str) -> None:
    value = read(projection, path)
    value["note"] = "changed without rehashing"
    write(projection, path, value, repin=False)
    rejected(projection, path, "canonical content_hash mismatch")


def test_missing_hash_is_not_silently_skipped(projection: Path) -> None:
    value = read(projection, AGENTS)
    del value["content_hash"]
    write(projection, AGENTS, value, repin=False)
    rejected(projection, AGENTS, "canonical content_hash must")


@pytest.mark.parametrize("content", ['{"a":1,"a":2}', '{"a":NaN}', '[]', '{broken'])
def test_every_json_including_unhashed_tokens_is_parsed(projection: Path, content: str) -> None:
    path = "assets/design/tokens.json"
    (projection / path).write_text(content, encoding="utf-8")
    rejected(projection, path, "JSON")


@pytest.mark.parametrize(("field", "value", "message"), [
    ("content_hash", "0" * 64, "content_hash pin differs"),
    ("id", "ellmos-wrong-bundle", "reference ID differs"),
    ("manifest", "other.json", "manifest path/ID mismatch"),
    ("pillar", "domain", "pillar differs"),
    ("class", "invented", "unknown catalog class"),
    ("path", "../outside.json", "repository-relative"),
    ("path", "contracts/bundle-family-contract.v1.json", "content_hash pin differs"),
])
def test_catalog_drift_after_valid_rehash(projection: Path, field: str, value: str, message: str) -> None:
    catalog = read(projection, CATALOG)
    catalog["bundles"][0][field] = value
    write(projection, CATALOG, catalog)
    rejected(projection, CATALOG, message)


def test_duplicate_catalog_entry(projection: Path) -> None:
    catalog = read(projection, CATALOG)
    catalog["bundles"][1] = catalog["bundles"][0]
    write(projection, CATALOG, catalog)
    rejected(projection, CATALOG, "duplicate catalog ID")


@pytest.mark.parametrize(("field", "value", "message"), [
    ("exported_path", "contracts/missing.json", "public target missing"),
    ("exported_path", "../outside.json", "repository-relative"),
    ("exported_path", "assets/design/tokens.json", "hashed public artifact"),
    ("source_sha256", "0" * 63, "invalid source_sha256"),
])
def test_receipt_drift_after_valid_rehash(projection: Path, field: str, value: str, message: str) -> None:
    receipt = read(projection, RECEIPT)
    receipt["files"][0][field] = value
    write(projection, RECEIPT, receipt)
    rejected(projection, RECEIPT, message)


def test_duplicate_receipt_target(projection: Path) -> None:
    receipt = read(projection, RECEIPT)
    receipt["files"][1] = receipt["files"][0]
    write(projection, RECEIPT, receipt)
    rejected(projection, RECEIPT, "duplicate exported target")


def test_source_metadata_is_not_a_public_byte_hash(projection: Path) -> None:
    receipt = read(projection, RECEIPT)
    # A structurally valid provenance assertion is not independently authenticatable.
    receipt["files"][0]["source_path"] = "unavailable-original.json"
    receipt["files"][0]["source_sha256"] = "1" * 64
    write(projection, RECEIPT, receipt)
    result = run_gate(projection)
    assert result.returncode == 0, result.stderr


def test_nested_contract_pin_is_checked_after_repinning_manifest_and_catalog(projection: Path) -> None:
    manifest = read(projection, AGENTS)
    manifest["functional_contracts"][0]["content_hash"] = "0" * 64
    write(projection, AGENTS, manifest)
    catalog = read(projection, CATALOG)
    next(e for e in catalog["bundles"] if e["path"] == AGENTS)["content_hash"] = canonical_hash(manifest)
    write(projection, CATALOG, catalog)
    rejected(projection, AGENTS, "content_hash pin differs")


@pytest.mark.parametrize("change", ["contract-target", "missing-choice-ref"])
def test_reference_kind_and_required_id(projection: Path, change: str) -> None:
    path = AGENTS if change == "contract-target" else "manifests/bundles/ellmos-memory-human-context-bundle/bundle.v1.json"
    manifest = read(projection, path)
    if change == "contract-target":
        target = "manifests/bundles/ellmos-briefing-bundle/bundle.v1.json"
        manifest["functional_contracts"][0] = {"path": target, "content_hash": read(projection, target)["content_hash"]}
    else:
        del manifest["choice_bundle_refs"][0]["ref"]
    write(projection, path, manifest)
    catalog = read(projection, CATALOG)
    next(e for e in catalog["bundles"] if e["path"] == path)["content_hash"] = canonical_hash(manifest)
    write(projection, CATALOG, catalog)
    rejected(projection, path, "must target public contracts" if change == "contract-target" else "requires a reference ID")


@pytest.mark.parametrize("value", ["/absolute.json", "C:/absolute.json", "a\\b.json", "./file.json",
                                  "a//b.json", "a/../file.json", "https://example.org/data.json"])
def test_path_rejection_before_io(tmp_path: Path, value: str) -> None:
    with pytest.raises(ValueError, match="repository-relative"):
        public_path(tmp_path, value, CATALOG)


def test_resolved_link_must_remain_in_root(tmp_path: Path) -> None:
    outside_dir = tmp_path / "outside"
    outside_dir.mkdir()
    outside = outside_dir / "outside.json"
    outside.write_text("{}", encoding="utf-8")
    public = tmp_path / "public"
    public.mkdir()
    try:
        (public / "link").symlink_to(outside_dir, target_is_directory=True)
    except OSError:
        if os.name != "nt":
            raise
        # Directory junctions need no Windows developer-mode/admin permission.
        import _winapi
        _winapi.CreateJunction(str(outside_dir), str(public / "link"))
    with pytest.raises(ValueError, match="escapes repository root"):
        public_path(public, "link/outside.json", RECEIPT)


@pytest.mark.parametrize("surface", ["banner", "preview", "both", "markers", "external"])
def test_banner_and_preview_drift(projection: Path, surface: str) -> None:
    bundle_id = "ellmos-agents-bundle"
    banner = f"assets/banners/{bundle_id}.svg"
    preview = f"docs/preview/{bundle_id}.html"
    if surface in {"banner", "both"}:
        path = projection / banner
        path.write_text(path.read_text(encoding="utf-8").replace("Agents Bundle", "Changed Bundle"), encoding="utf-8")
    if surface in {"preview", "both", "markers", "external"}:
        path = projection / preview
        content = path.read_text(encoding="utf-8")
        if surface == "markers":
            content += "<!--BANNER-SVG-->"
        elif surface == "external":
            content = content.replace("</svg>", '<image href="https://example.org/image.png"/></svg>')
        else:
            content = content.replace("Agents Bundle", "Changed Bundle")
        path.write_text(content, encoding="utf-8")
    rejected(projection, banner if surface == "both" else preview,
             {"both": "renderer/preview drift", "markers": "marker pair", "external": "self-contained primitives"}
             .get(surface, "preview SVG differs"))


def test_three_catalog_overrides_and_no_invented_pillar() -> None:
    catalog = read(ROOT, CATALOG)
    manifests = {entry["id"]: read(ROOT, entry["path"]) for entry in catalog["bundles"]}
    expected = {
        "ellmos-knowledge-bundle": ["--pillar", "domain"],
        "ellmos-media-production-bundle": ["--pillar", "domain"],
        KNOWLEDGE: ["--pillar", "domain", "--chip", "CHOICE · MEMORY + DOMAIN"],
    }
    assert {key: banner_options(key, manifests, catalog) for key in expected} == expected
    for key in expected:
        assert "pillar" not in manifests[key]
    assert banner_options("ellmos-coordination-choice-bundle", manifests, catalog) == []
    catalog["pillars"]["omissions"]["approval_pinned"].pop("ellmos-knowledge-bundle")
    with pytest.raises(ValueError, match="cross-pillar evidence"):
        banner_options("ellmos-knowledge-bundle", manifests, catalog)


def test_default_change_moves_borrowed_palette_and_detects_frozen_banner_drift(projection: Path) -> None:
    path = f"manifests/bundles/{KNOWLEDGE}/bundle.v1.json"
    choice = read(projection, path)
    group = choice["choice_groups"][0]
    group["default_selection"] = ["GARDENER"]
    for candidate in group["candidates"]:
        candidate["default"] = candidate["ref"] == "GARDENER"
    write(projection, path, choice)
    values = {p.relative_to(projection).as_posix(): json.loads(p.read_text(encoding="utf-8"))
              for folder in ("manifests", "contracts") for p in (projection / folder).rglob("*.json")
              if p.name != "export-receipt.v1.json"}
    repin(values)
    for rel, value in values.items():
        write(projection, rel, value, repin=False)
    rejected(projection, f"assets/banners/{KNOWLEDGE}.svg", "renderer/preview drift")


@pytest.mark.parametrize("change", ["missing", "extra"])
def test_json_inventory_is_closed(projection: Path, change: str) -> None:
    if change == "missing":
        (projection / "assets/design/tokens.json").unlink()
    else:
        (projection / "contracts/unreleased.json").write_text("{}", encoding="utf-8")
    rejected(projection, "manifests", "18 JSON documents")


@pytest.mark.parametrize("surface", ["assets/banners", "docs/preview"])
def test_missing_banner_or_preview(projection: Path, surface: str) -> None:
    suffix = "svg" if surface == "assets/banners" else "html"
    path = f"{surface}/ellmos-agents-bundle.{suffix}"
    (projection / path).unlink()
    rejected(projection, surface, "inventory" if suffix == "svg" else "public target missing")


def test_ci_invokes_the_public_gate_before_installing_dependencies() -> None:
    ci = (ROOT / ".github/workflows/ci.yml").read_text(encoding="utf-8")
    command = "python -I -S tools/validate_projection.py"
    assert ci.index(command) < ci.index("python -m pip install")
    assert "pull_request:" in ci and "push:" in ci and "branches: [main, master]" in ci
    assert "permissions:\n  contents: read" in ci
    assert "persist-credentials: false" in ci
    actions = re.findall(r"uses: (actions/[a-z-]+)@([^\s]+)", ci)
    assert {name for name, _ in actions} == {"actions/checkout", "actions/setup-python"}
    assert all(re.fullmatch(r"[0-9a-f]{40}", revision) for _, revision in actions)
