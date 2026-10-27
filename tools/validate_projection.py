#!/usr/bin/env python3
"""Validate the released public projection offline, using only the standard library.

The canonical form is the existing exporter's UTF-8 JSON, sorted keys, compact
separators, with only the document's own content_hash removed. Nested hashes are
reference pins, not hashes of the small reference object. Source receipt hashes
describe private original bytes; they are metadata, never public-file digests.
"""
from __future__ import annotations

import hashlib
import json
import os
import re
import subprocess
import sys
import xml.etree.ElementTree as ET
from pathlib import Path, PurePosixPath
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
CATALOG = "manifests/bundles.catalog.v1.json"
RECEIPT = "manifests/export-receipt.v1.json"
TOKENS = "assets/design/tokens.json"
PILLARS = {"memory", "control", "uas", "domain"}
HASH = re.compile(r"[0-9a-f]{64}\Z")
BUNDLE_ID = re.compile(r"ellmos-[a-z0-9-]+-bundle\Z")


class Invalid(ValueError):
    pass


def require(condition: Any, path: str, invariant: str) -> None:
    if not condition:
        raise Invalid(f"{path}: {invariant}")


def public_path(root: Path, value: Any, owner: str) -> Path:
    """Accept only canonical repo-relative POSIX paths; contain resolved links too."""
    require(isinstance(value, str) and bool(value), owner, "public target path must be a string")
    path = PurePosixPath(value)
    require(not path.is_absolute() and not re.search(r"[:\\\x00]", value)
            and all(p not in {"", ".", ".."} for p in value.split("/")),
            owner, "public target path must be canonical and repository-relative")
    resolved = (root / value).resolve()
    require(resolved.is_relative_to(root.resolve()), owner, "public target escapes repository root")
    require(resolved.is_file(), owner, f"public target missing: {value}")
    return resolved


def canonical_digest(value: dict[str, Any]) -> str:
    unsigned = {key: item for key, item in value.items() if key != "content_hash"}
    payload = json.dumps(unsigned, sort_keys=True, ensure_ascii=False,
                         separators=(",", ":"), allow_nan=False).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


def unique_object(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    value: dict[str, Any] = {}
    for key, item in pairs:
        if key in value:
            raise ValueError("duplicate JSON object key")
        value[key] = item
    return value


def read_document(root: Path, path: str) -> dict[str, Any]:
    try:
        def invalid_constant(value: str) -> None:
            raise ValueError("non-finite JSON number")
        value = json.loads(public_path(root, path, path).read_text(encoding="utf-8"),
                           object_pairs_hook=unique_object, parse_constant=invalid_constant)
    except (OSError, UnicodeError, ValueError) as exc:
        if isinstance(exc, Invalid):
            raise
        raise Invalid(f"{path}: valid UTF-8 JSON object required ({type(exc).__name__})") from exc
    require(isinstance(value, dict), path, "JSON document must be an object")
    return value


def rows(value: Any, path: str, field: str) -> list[dict[str, Any]]:
    require(isinstance(value, list) and all(isinstance(row, dict) for row in value),
            path, f"{field} must be an array of objects")
    return value


def check_pin(root: Path, docs: dict[str, dict[str, Any]], owner: str,
              pin: dict[str, Any]) -> str:
    path = pin.get("path")
    public_path(root, path, owner)
    require(path in docs and "content_hash" in docs[path], owner, "pin must target a hashed public document")
    target = docs[path]
    require(pin.get("content_hash") == canonical_digest(target), owner, f"content_hash pin differs: {path}")
    if "ref" in pin:
        require(pin["ref"] == target.get("id"), owner, f"reference ID differs: {path}")
    return path


def manifest_pillar(bundle_id: str, manifests: dict[str, dict[str, Any]],
                    catalog: dict[str, Any]) -> str:
    manifest = manifests[bundle_id]
    pillar = manifest.get("pillar")
    if pillar:
        require(pillar in PILLARS, CATALOG, f"unknown pillar for {bundle_id}")
        return pillar
    omissions = catalog.get("pillars", {}).get("omissions", {})
    reason = omissions.get("approval_pinned", {}).get(bundle_id, "")
    require(isinstance(reason, str), CATALOG, f"pillar evidence must be text: {bundle_id}")
    match = re.match(r"intended pillar (memory|control|uas|domain), not written:", reason)
    require(match is not None, CATALOG, f"no documented intended pillar for {bundle_id}")
    return match.group(1)


def banner_options(bundle_id: str, manifests: dict[str, dict[str, Any]],
                   catalog: dict[str, Any]) -> list[str]:
    """Follow assets/design/README.md: two pinned omissions and one cross-pillar chip."""
    manifest = manifests[bundle_id]
    omissions = catalog["pillars"]["omissions"]
    if bundle_id in omissions["approval_pinned"]:
        require("pillar" not in manifest, CATALOG, f"approval-pinned pillar must remain absent: {bundle_id}")
    if manifest.get("pillar"):
        return []
    if bundle_id in omissions["approval_pinned"]:
        return ["--pillar", manifest_pillar(bundle_id, manifests, catalog)]

    reason = omissions["hosted_and_cross_pillar"].get(bundle_id, "")
    require(isinstance(reason, str), CATALOG, f"pillar evidence must be text: {bundle_id}")
    entry = next(row for row in catalog["bundles"] if row["id"] == bundle_id)
    require(entry.get("class") == "choice" and "spans two pillars" in reason,
            CATALOG, f"missing cross-pillar evidence for {bundle_id}")
    groups = rows(manifest.get("choice_groups"), bundle_id, "choice_groups")
    require(len(groups) == 1, CATALOG, f"one cross-pillar choice group required: {bundle_id}")
    group = groups[0]
    candidates = rows(group.get("candidates"), bundle_id, "candidates")
    selected = [c for c in candidates if c.get("default") is True]
    require(len(selected) == 1 and group.get("default_selection") == [selected[0].get("ref")],
            CATALOG, f"default_selection must agree with candidate flags: {bundle_id}")
    homes = [c.get("registered_in_bundle") for c in candidates]
    require(all(isinstance(home, str) and home in manifests for home in homes),
            CATALOG, f"candidate homes must be public bundles: {bundle_id}")
    for candidate, home in zip(candidates, homes):
        components = rows(manifests[home].get("components"), home, "components")
        refs = [c.get("ref") for c in components]
        identities = [ref.get("ref") if isinstance(ref, dict) else ref for ref in refs]
        require(candidate.get("identity") in identities, CATALOG,
                f"candidate must be declared in its registered home: {bundle_id}")
    pillars = list(dict.fromkeys(manifest_pillar(home, manifests, catalog) for home in homes))
    require(len(pillars) == 2 and all(re.search(rf"\b{p}\b", reason) for p in pillars),
            CATALOG, f"candidate pillars must agree with omission evidence: {bundle_id}")
    palette = manifest_pillar(selected[0]["registered_in_bundle"], manifests, catalog)
    return ["--pillar", palette, "--chip", "CHOICE · " + " + ".join(p.upper() for p in pillars)]


def check_svg(text: str, path: str) -> None:
    require("<!DOCTYPE" not in text and "<!ENTITY" not in text and "{{" not in text,
            path, "SVG must be resolved and self-contained")
    try:
        svg = ET.fromstring(text)
    except ET.ParseError as exc:
        raise Invalid(f"{path}: valid SVG XML required") from exc
    ns = "{http://www.w3.org/2000/svg}"
    require(svg.tag == ns + "svg" and svg.get("viewBox") == "0 0 1200 300"
            and svg.get("role") == "img", path, "frozen SVG canvas and image role required")
    for node in svg.iter():
        require(node.tag not in {ns + tag for tag in ("script", "style", "filter", "image", "foreignObject")},
                path, "SVG must use self-contained primitives")
        for key, value in node.attrib.items():
            require(not key.lower().startswith("on") and not key.endswith("href")
                    and not re.search(r"url\(\s*[^#]", value), path, "SVG external or executable reference forbidden")


def validate(root: Path = ROOT) -> dict[str, int]:
    paths = sorted(p.relative_to(root).as_posix() for folder in ("manifests", "contracts", "assets/design")
                   for p in (root / folder).rglob("*.json"))
    require(len(paths) == 18, "manifests", "released projection must contain 18 JSON documents")
    docs = {path: read_document(root, path) for path in paths}
    require(all(p in docs for p in (CATALOG, RECEIPT, TOKENS)), "manifests", "catalog, receipt and tokens required")
    hashed = set(docs) - {TOKENS}
    for path, doc in docs.items():
        if path in hashed or "content_hash" in doc:
            require(isinstance(doc.get("content_hash"), str) and HASH.fullmatch(doc["content_hash"]),
                    path, "canonical content_hash must be lowercase SHA-256")
            require(doc["content_hash"] == canonical_digest(doc), path, "canonical content_hash mismatch")

    catalog, receipt = docs[CATALOG], docs[RECEIPT]
    require(catalog.get("schema") == "ellmos.bundles.catalog.v1", CATALOG, "catalog schema mismatch")
    entries = rows(catalog.get("bundles"), CATALOG, "bundles")
    require(len(entries) == 13, CATALOG, "released catalog must contain 13 entries")
    pillar_spec = catalog.get("pillars")
    require(isinstance(pillar_spec, dict), CATALOG, "pillars metadata must be an object")
    omissions = pillar_spec.get("omissions")
    require(isinstance(omissions, dict) and all(isinstance(omissions.get(key), dict)
            for key in ("approval_pinned", "hosted_and_cross_pillar")),
            CATALOG, "pillar omission evidence must be objects")
    manifests: dict[str, dict[str, Any]] = {}
    manifest_paths: set[str] = set()
    for entry in entries:
        bundle_id = entry.get("id")
        require(isinstance(bundle_id, str) and BUNDLE_ID.fullmatch(bundle_id), CATALOG, "invalid bundle ID")
        require(bundle_id not in manifests, CATALOG, f"duplicate catalog ID: {bundle_id}")
        path = check_pin(root, docs, CATALOG, {**entry, "ref": bundle_id})
        require(path == f"manifests/bundles/{bundle_id}/bundle.v1.json"
                and entry.get("manifest") == "bundle.v1.json", CATALOG, f"manifest path/ID mismatch: {bundle_id}")
        manifest = docs[path]
        require(manifest.get("schema") == "ellmos.bundle.v1", path, "bundle schema mismatch")
        require(entry.get("class") in {"platform", "domain", "hosted-private", "choice", "synthetic"},
                CATALOG, f"unknown catalog class: {bundle_id}")
        # Class is owned by the catalog; released manifests carry no class field.
        for field in ("pillar", "status", "visibility"):
            require(entry.get(field) == manifest.get(field), CATALOG, f"{field} differs from {path}")
        manifests[bundle_id] = manifest
        manifest_paths.add(path)
    require(manifest_paths == {p for p in docs if p.startswith("manifests/bundles/")},
            CATALOG, "catalog must cover every public bundle manifest exactly once")
    for path in manifest_paths:
        for field in ("functional_contracts", "choice_bundle_refs", "bundle_refs"):
            for pin in rows(docs[path].get(field, []), path, field):
                target = check_pin(root, docs, path, pin)
                if field == "functional_contracts":
                    require(target.startswith("contracts/"), path, "functional_contracts must target public contracts")
                else:
                    require(isinstance(pin.get("ref"), str), path, f"{field} requires a reference ID")
                    require(target in manifest_paths, path, f"{field} must target a cataloged bundle")
                if field == "choice_bundle_refs":
                    target_entry = next(e for e in entries if e["id"] == docs[target]["id"])
                    require(target_entry.get("class") == "choice", path, "choice reference must target class choice")

    require(receipt.get("schema") == "ellmos.open-ocean-export-receipt.v1"
            and receipt.get("bundle_count") == 13, RECEIPT, "receipt schema/bundle_count mismatch")
    require(isinstance(receipt.get("source_commit"), str)
            and re.fullmatch(r"[0-9a-f]{40}", receipt["source_commit"]), RECEIPT, "invalid source commit metadata")
    require(isinstance(receipt.get("export_contract_sha256"), str)
            and HASH.fullmatch(receipt["export_contract_sha256"]), RECEIPT, "invalid export contract hash metadata")
    files = rows(receipt.get("files"), RECEIPT, "files")
    require(len(files) == 16, RECEIPT, "receipt must contain 16 exported targets")
    targets: set[str] = set()
    for item in files:
        path = item.get("exported_path")
        public_path(root, path, RECEIPT)
        require(path in hashed - {RECEIPT}, RECEIPT, "receipt target must be a hashed public artifact")
        require(path not in targets, RECEIPT, f"duplicate exported target: {path}")
        require(isinstance(item.get("source_sha256"), str) and HASH.fullmatch(item["source_sha256"]),
                RECEIPT, f"invalid source_sha256 metadata for {path}")
        # source_path is intentionally not resolved: it addresses a private original.
        require(isinstance(item.get("source_path"), str) and bool(item["source_path"]),
                RECEIPT, f"source_path metadata required for {path}")
        targets.add(path)
    require(targets == hashed - {RECEIPT}, RECEIPT, "receipt must cover every exported public artifact exactly once")

    expected_banners = {f"assets/banners/{bundle_id}.svg" for bundle_id in manifests}
    actual_banners = {p.relative_to(root).as_posix() for p in (root / "assets/banners").glob("*.svg")}
    require(actual_banners == expected_banners, "assets/banners", "banner inventory must match the catalog")
    for bundle_id in manifests:
        banner = f"assets/banners/{bundle_id}.svg"
        preview = f"docs/preview/{bundle_id}.html"
        svg = public_path(root, banner, banner).read_text(encoding="utf-8")
        html = public_path(root, preview, preview).read_text(encoding="utf-8")
        check_svg(svg, banner)
        open_mark, close_mark = "<!--BANNER-SVG-->", "<!--/BANNER-SVG-->"
        require(html.count(open_mark) == html.count(close_mark) == 1
                and html.index(open_mark) < html.index(close_mark), preview, "exactly one ordered banner marker pair required")
        embedded = html.split(open_mark)[1].split(close_mark)[0]
        check_svg(embedded.strip(), preview)
        require(ET.canonicalize(embedded.strip(), strip_text=True) == ET.canonicalize(svg, strip_text=True),
                preview, "embedded preview SVG differs from banner")
        command = [sys.executable, "-I", "-S", str(root / "tools/generate_banner.py"), bundle_id,
                   *banner_options(bundle_id, manifests, catalog), "--check", "--inline-into", str(root / preview)]
        result = subprocess.run(command, cwd=root, capture_output=True, encoding="utf-8", check=False,
                                env={**os.environ, "PYTHONIOENCODING": "utf-8"})
        require(result.returncode == 0, banner, f"frozen renderer/preview drift (see {preview})")
    return {"json": len(docs), "hashes": len(hashed), "catalog": len(entries),
            "receipt_targets": len(targets), "banners": len(manifests), "previews": len(manifests)}


def main() -> int:
    try:
        result = validate()
    except Invalid as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1
    except (OSError, UnicodeError, KeyError, TypeError, ValueError) as exc:
        print(f"error: manifests: invalid projection structure ({type(exc).__name__})", file=sys.stderr)
        return 1
    print("projection clean: " + ", ".join(f"{key}={value}" for key, value in result.items()))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
