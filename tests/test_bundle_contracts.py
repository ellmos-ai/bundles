"""Contract, schema, and manifest integrity tests for ellmos-bundles."""
from __future__ import annotations

from pathlib import Path

from tools.export_from_source import canonical_hash, read_json

REPO_ROOT = Path(__file__).resolve().parents[1]
CONTRACTS_DIR = REPO_ROOT / "contracts"
MANIFESTS_DIR = REPO_ROOT / "manifests"


def test_declarative_contracts_validity() -> None:
    """Verify contracts/bundle-family-contract.v1.json and choice-bundle-contract.v1.json."""
    for contract_name in [
        "bundle-family-contract.v1.json",
        "choice-bundle-contract.v1.json",
    ]:
        path = CONTRACTS_DIR / contract_name
        assert path.is_file(), f"{contract_name} must exist"
        data = read_json(path)
        assert "schema" in data
        assert "id" in data
        assert "version" in data
        assert "authority" in data


def test_bundles_catalog_integrity() -> None:
    """Verify manifests/bundles.catalog.v1.json covers exactly 13 bundles."""
    catalog_path = MANIFESTS_DIR / "bundles.catalog.v1.json"
    assert catalog_path.is_file(), "bundles.catalog.v1.json must exist"

    catalog = read_json(catalog_path)
    assert catalog.get("schema") == "ellmos.bundles.catalog.v1"
    bundles = catalog.get("bundles", [])
    assert len(bundles) == 13, f"Expected 13 bundles, got {len(bundles)}"

    for bundle_info in bundles:
        bundle_id = bundle_info.get("id")
        assert bundle_id, "Bundle entry missing id"
        manifest_rel = bundle_info.get("path")
        assert manifest_rel, f"Bundle {bundle_id} has no manifest path"
        manifest_path = REPO_ROOT / manifest_rel
        assert manifest_path.is_file(), f"Manifest file missing: {manifest_path}"


def test_all_bundle_manifests_schema_and_components() -> None:
    """Validate all 13 bundle manifests against schema and contract rules."""
    allowed_pillars = {"memory", "control", "uas", "domain"}
    manifest_files = list((MANIFESTS_DIR / "bundles").rglob("bundle.v1.json"))
    assert len(manifest_files) == 13, f"Expected 13 manifests, found {len(manifest_files)}"

    for manifest_path in manifest_files:
        manifest = read_json(manifest_path)
        bundle_id = manifest.get("id")
        assert bundle_id, f"Missing id in {manifest_path}"
        assert manifest.get("schema") == "ellmos.bundle.v1"
        assert manifest.get("version") == "1.0.0"

        pillar = manifest.get("pillar")
        if pillar is not None:
            assert pillar in allowed_pillars, f"Invalid pillar '{pillar}' in {bundle_id}"

        components = manifest.get("components")
        assert isinstance(components, list) and len(components) > 0, f"No components in {bundle_id}"
        for comp in components:
            assert "type" in comp, f"Component missing type in {bundle_id}"
            assert "ref" in comp, f"Component missing ref in {bundle_id}"
            assert "role" in comp, f"Component missing role in {bundle_id}"


def test_export_receipt_files_exist() -> None:
    """Verify export-receipt.v1.json lists all 13 bundles and exported files exist."""
    receipt_path = MANIFESTS_DIR / "export-receipt.v1.json"
    assert receipt_path.is_file(), "export-receipt.v1.json must exist"

    receipt = read_json(receipt_path)
    assert receipt.get("schema") == "ellmos.open-ocean-export-receipt.v1"
    assert receipt.get("bundle_count") == 13

    files = receipt.get("files", [])
    assert len(files) >= 16, f"Expected at least 16 exported files, got {len(files)}"
    for entry in files:
        exported_path = entry.get("exported_path")
        assert exported_path, "Entry missing exported_path"
        target = REPO_ROOT / exported_path
        assert target.is_file(), f"Exported file {exported_path} does not exist"


def test_all_json_canonical_content_hashes() -> None:
    """Verify bit-level canonical content_hash on all 17 declared JSON artifacts."""
    checked = 0
    all_json = list(MANIFESTS_DIR.rglob("*.json")) + list(CONTRACTS_DIR.rglob("*.json"))

    for path in all_json:
        data = read_json(path)
        if "content_hash" in data:
            expected_hash = data["content_hash"]
            computed_hash = canonical_hash(data)
            assert computed_hash == expected_hash, (
                f"Content hash mismatch in {path.relative_to(REPO_ROOT)}: "
                f"expected {expected_hash}, calculated {computed_hash}"
            )
            checked += 1

    assert checked == 17, f"Expected 17 JSON artifacts with content_hash, validated {checked}"


def test_design_tokens_validity() -> None:
    """Verify design tokens define palettes for all four architectural pillars."""
    tokens_path = REPO_ROOT / "assets" / "design" / "tokens.json"
    assert tokens_path.is_file(), "tokens.json must exist"

    tokens = read_json(tokens_path)
    assert "pillars" in tokens
    pillars = tokens["pillars"]
    for pillar_name in ["memory", "control", "uas", "domain"]:
        assert pillar_name in pillars, f"Pillar '{pillar_name}' missing from design tokens"
        p_data = pillars[pillar_name]
        assert "palette" in p_data
        palette = p_data["palette"]
        for key in ["hull", "abyss", "deep", "mid", "surface", "accent", "ink", "muted"]:
            assert key in palette, f"Key '{key}' missing from palette for pillar '{pillar_name}'"
