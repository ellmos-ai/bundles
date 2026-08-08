#!/usr/bin/env python3
"""Render a bundle banner from the shared template, the pillar palette and a scene.

One banner per bundle, all of them in one visual language: the frame, the type
and the colour come from ``assets/design/``, and only the scene changes with the
pillar. Adding a bundle to the series is a call, not a drawing session.

Nothing here is generated from the moment it runs - no timestamps, no random
placement, no machine paths. Run it twice and the second run produces a byte
identical file, which is what makes ``--check`` meaningful: it reports drift
between the committed banner and what the sources say it should be.

    python tools/generate_banner.py ellmos-daily-life-bundle
    python tools/generate_banner.py ellmos-daily-life-bundle --check

The bundle manifest supplies the title and the pillar, so the series is a loop
over the catalogue. Both can be overridden for a bundle whose banner should say
something the manifest does not.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
DESIGN = ROOT / "assets" / "design"
TOKENS_PATH = DESIGN / "tokens.json"
TEMPLATE_PATH = DESIGN / "banner.template.svg"
SCENES_DIR = DESIGN / "scenes"
BANNERS_DIR = ROOT / "assets" / "banners"
MANIFESTS_DIR = ROOT / "manifests" / "bundles"


class BannerError(RuntimeError):
    pass


def rel(path: Path) -> str:
    """Repository-relative display path, tolerating a path given from elsewhere."""
    try:
        return str(path.resolve().relative_to(ROOT))
    except ValueError:
        return str(path)


def read_text(path: Path) -> str:
    """Read as text with newlines normalised, so a checkout on Windows and one on
    Linux produce the same banner instead of differing by line ending alone."""
    if not path.exists():
        raise BannerError(f"missing source file: {rel(path)}")
    return path.read_text(encoding="utf-8").replace("\r\n", "\n")


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(read_text(path))


def xml_escape(value: str) -> str:
    return (
        value.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
    )


def num(value: float) -> str:
    """Fixed formatting, so a float never reaches the file as 8.299999999999999."""
    text = f"{value:.1f}"
    return text[:-2] if text.endswith(".0") else text


def title_size(tokens: dict[str, Any], title: str) -> int:
    """Largest size at which the title still clears the scene.

    Fitted rather than stepped: bundle names run from 15 to 30-odd characters, and
    a fixed ladder either wastes the short ones or lets the long ones collide with
    the nets. Integer result, so the same name always yields the same file.
    """
    rule = tokens["typography"]["title"]
    if not title:
        return int(rule["max_size"])
    fitted = rule["max_width"] / (len(title) * rule["advance_ratio"])
    return int(max(rule["min_size"], min(rule["max_size"], fitted)))


def chip_width(tokens: dict[str, Any], label: str) -> float:
    """Width of the pillar chip.

    SVG has no text metrics at write time and the banner must not depend on a
    font being installed, so the pill is sized from an advance estimate for
    uppercase text at the chip size. Erring wide keeps the label off the stroke.
    """
    advance = tokens["typography"]["chip_size"] * 0.66 + tokens["typography"]["chip_tracking"]
    return round(30.0 + max(0.0, len(label) * advance - tokens["typography"]["chip_tracking"]), 1)


def load_manifest(bundle_id: str) -> dict[str, Any]:
    path = MANIFESTS_DIR / bundle_id / "bundle.v1.json"
    if not path.exists():
        raise BannerError(
            f"no manifest for {bundle_id!r} - pass --title and --pillar to render a banner "
            f"for a bundle this repository does not carry"
        )
    return read_json(path)


def build(bundle_id: str, pillar: str | None, scene: str | None,
          title: str | None, subtitle: str | None, chip: str | None = None) -> str:
    tokens = read_json(TOKENS_PATH)
    manifest: dict[str, Any] = {}
    if pillar is None or title is None:
        manifest = load_manifest(bundle_id)

    pillar = pillar or manifest.get("pillar")
    if not pillar:
        raise BannerError(
            f"{bundle_id} carries no pillar in its manifest - pass --pillar explicitly"
        )
    if pillar not in tokens["pillars"]:
        known = ", ".join(sorted(tokens["pillars"]))
        raise BannerError(f"unknown pillar {pillar!r}; tokens.json knows: {known}")

    spec = tokens["pillars"][pillar]
    palette = spec["palette"]
    scene_name = scene or spec["scene"]
    scene_path = SCENES_DIR / f"{scene_name}.svg"
    if not scene_path.exists():
        have = ", ".join(sorted(p.stem for p in SCENES_DIR.glob("*.svg"))) or "none yet"
        raise BannerError(
            f"scene {scene_name!r} for pillar {pillar!r} is not drawn yet "
            f"(scenes present: {have}). Scenes are plain SVG fragments in "
            f"assets/design/scenes/ - adding one needs no change to this script."
        )

    title = title or manifest.get("display_name") or bundle_id
    subtitle = subtitle if subtitle is not None else bundle_id

    # The chip normally names the pillar, because normally the pillar is the truth about a
    # bundle. It is overridable for the one case where it is not: a bundle whose reach spans
    # two pillars still needs a palette to be drawn in, but must not carry a single pillar's
    # name on the most visible surface it has. The palette is then borrowed and said to be
    # borrowed; the chip says what the catalogue says instead.
    borrowed = chip is not None
    chip = chip or f"{pillar.upper()} · {spec['label'].upper()}"
    aria = f"{title} — {chip}" if borrowed else f"{title} — {spec['label']} ({pillar} pillar)"

    canvas = tokens["canvas"]
    typo = tokens["typography"]
    colours = {
        "C_HULL": palette["hull"],
        "C_ABYSS": palette["abyss"],
        "C_DEEP": palette["deep"],
        "C_MID": palette["mid"],
        "C_SURFACE": palette["surface"],
        "C_ACCENT": palette["accent"],
        "C_INK": palette["ink"],
        "C_MUTED": palette["muted"],
    }

    scene_svg = read_text(scene_path).rstrip("\n")
    for key, value in colours.items():
        scene_svg = scene_svg.replace("{{" + key + "}}", value)

    slots: dict[str, str] = {
        **colours,
        "WIDTH": num(canvas["width"]),
        "HEIGHT": num(canvas["height"]),
        "WATERLINE": num(canvas["waterline"]),
        "WATER_HEIGHT": num(canvas["height"] - canvas["waterline"]),
        "HORIZON_X": num(canvas["horizon_from"]),
        "HORIZON_W": num(canvas["width"] - canvas["horizon_from"]),
        "VEIL_WIDTH": num(canvas["veil_width"]),
        "MARGIN_LEFT": num(canvas["margin_left"]),
        "RULE_HEIGHT": num(canvas["rule_height"]),
        "RULE_Y": num(canvas["height"] - canvas["rule_height"]),
        "FONT_SANS": xml_escape(typo["sans"]),
        "FONT_MONO": xml_escape(typo["mono"]),
        "TITLE_SIZE": num(title_size(tokens, title)),
        "SUBTITLE_SIZE": num(typo["subtitle_size"]),
        "CHIP_SIZE": num(typo["chip_size"]),
        "CHIP_TRACKING": num(typo["chip_tracking"]),
        "CHIP_WIDTH": num(chip_width(tokens, chip)),
        "TITLE": xml_escape(title),
        "SUBTITLE": xml_escape(subtitle),
        "PILLAR_CHIP": xml_escape(chip),
        "ARIA": xml_escape(aria),
        "SCENE": scene_svg,
    }

    svg = read_text(TEMPLATE_PATH)
    for key, value in slots.items():
        svg = svg.replace("{{" + key + "}}", value)

    unresolved = sorted({s.split("}}")[0] for s in svg.split("{{")[1:] if "}}" in s})
    if unresolved:
        raise BannerError(f"template slots left unfilled: {', '.join(unresolved)}")
    return svg


OPEN_MARK = "<!--BANNER-SVG-->"
CLOSE_MARK = "<!--/BANNER-SVG-->"


def embed(html_path: Path, svg: str) -> str:
    """Put the banner inside a preview page, between the two markers.

    The preview embeds the banner rather than linking it, so the page is one
    file that opens anywhere. That would rot the moment the banner changes, so
    the embedding is done by the same run that draws it and is covered by the
    same ``--check``.
    """
    html = read_text(html_path)
    start, end = html.find(OPEN_MARK), html.find(CLOSE_MARK)
    if start < 0 or end < 0 or end < start:
        raise BannerError(
            f"{rel(html_path)} carries no {OPEN_MARK} … {CLOSE_MARK} pair to embed into"
        )
    indent = " " * (start - (html.rfind("\n", 0, start) + 1))
    body = "\n".join(indent + line if line else line for line in svg.strip().split("\n"))
    return html[: start + len(OPEN_MARK)] + "\n" + body + "\n" + indent + html[end:]


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("bundle_id")
    parser.add_argument("--pillar", help="override the pillar from the manifest")
    parser.add_argument("--scene", help="override the pillar's default scene fragment")
    parser.add_argument("--title", help="override the display name from the manifest")
    parser.add_argument("--subtitle", help="override the mono line under the title")
    parser.add_argument(
        "--chip",
        help="override the pillar chip, for a bundle whose reach is not a single pillar",
    )
    parser.add_argument("--out", type=Path, help="output path (default assets/banners/<id>.svg)")
    parser.add_argument(
        "--inline-into",
        type=Path,
        help="also embed the banner into a preview page between its BANNER-SVG markers",
    )
    parser.add_argument(
        "--check",
        action="store_true",
        help="report drift against the committed banner instead of writing",
    )
    args = parser.parse_args(argv)

    try:
        svg = build(args.bundle_id, args.pillar, args.scene, args.title, args.subtitle,
                    args.chip)
    except BannerError as error:
        print(f"error: {error}", file=sys.stderr)
        return 2

    out = args.out or BANNERS_DIR / f"{args.bundle_id}.svg"
    digest = hashlib.sha256(svg.encode("utf-8")).hexdigest()

    try:
        if args.check:
            if not out.exists():
                print(f"drift: {rel(out)} does not exist", file=sys.stderr)
                return 1
            if read_text(out) != svg:
                print(f"drift: {rel(out)} differs from its sources", file=sys.stderr)
                return 1
            if args.inline_into and read_text(args.inline_into) != embed(args.inline_into, svg):
                print(
                    f"drift: {rel(args.inline_into)} carries an older banner",
                    file=sys.stderr,
                )
                return 1
            print(f"clean  {rel(out)}  sha256={digest}")
            return 0

        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(svg, encoding="utf-8", newline="\n")
        print(f"wrote  {rel(out)}  sha256={digest}")
        if args.inline_into:
            args.inline_into.write_text(
                embed(args.inline_into, svg), encoding="utf-8", newline="\n"
            )
            print(f"embed  {rel(args.inline_into)}")
    except BannerError as error:
        print(f"error: {error}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
