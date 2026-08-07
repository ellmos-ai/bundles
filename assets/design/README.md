# Banner design

One banner per bundle, all of them in one visual language. This folder holds the parts that
stay the same across the series; only the scene and the palette change with the pillar.

> **Status: pilot.** One banner exists — `ellmos-daily-life-bundle`. Palette, scene and page
> layout are up for approval before the remaining bundles follow. Nothing here is settled.

## The picture, and why

The visual language comes from the water lexicon the ecosystem already uses (see
`SYSTEM-PRODUKTLINIE.md` §1 and §6b): the stream is the process, the vessels are the
structure. Each of the four pillars is therefore a body of water with its own light, and each
gets the symbol the ecosystem already assigned it.

| Pillar | Water | Symbol | Scene |
|---|---|---|---|
| `memory` | deep water | the boat and its wake | `wake` — not drawn yet |
| `control` | clear water | the helm | `helm` — not drawn yet |
| `uas` | the harbour | nets and species of fish | `harbour` ✔ |
| `domain` | freight water | cargo, crane, containers | `freight` — not drawn yet |

The harbour scene carries the UAS reading verbatim: **different nets catch different fish**,
and the species are the end products as food — the plan, the route, the morning digest. One
net holds the catch the light falls on; the others hang ready.

## Files

| File | What it is |
|---|---|
| `tokens.json` | the palettes, the canvas geometry and the type scale — the single place a colour is decided |
| `banner.template.svg` | the frame: sky, water, veil, title block, pillar chip, accent rule. Slots are `{{NAME}}` |
| `scenes/<name>.svg` | a scene fragment. Plain SVG, with `{{C_*}}` where a colour belongs |
| `../banners/<bundle-id>.svg` | the output, one per bundle |

## Rules the series keeps

1. **Self-contained.** No external fonts, no raster images, no network references. Fonts are
   named as a stack with generic fallbacks, so a banner looks right without anything installed.
2. **Primitives only.** Gradients, shapes, strokes, transforms. No `<style>`, no `<filter>`,
   no `<script>`, no `xlink:href` — GitHub sanitises SVG in markdown, and everything used here
   survives that.
3. **Dark on purpose.** A banner brings its own background, so one file reads the same in a
   light and a dark README. A light variant per bundle would double the series for nothing.
4. **The accent is a mark, not decoration.** It appears at the pillar chip, the bottom rule,
   the scene's light source, and on the single element the eye should land on. Nowhere else.
5. **Little text.** Display name, the bundle id in mono, the pillar chip. The page carries the
   words; the banner carries the identity.
6. **Deterministic.** No timestamps, no random placement, no machine paths. Run it twice, get
   the same bytes — which is what makes `--check` worth anything.

## Making one

```bash
python tools/generate_banner.py <bundle-id>                    # title and pillar from the manifest
python tools/generate_banner.py <bundle-id> --scene harbour    # override the pillar's scene
python tools/generate_banner.py <bundle-id> --check            # report drift instead of writing
```

The manifest supplies the display name and the pillar, so the series is a loop over the
catalogue rather than a drawing session per bundle. `--title`, `--subtitle`, `--pillar` and
`--scene` override that for a bundle whose banner should say something else.

## Adding a scene for another pillar

Drop `scenes/<name>.svg` next to `harbour.svg` and name it in `tokens.json` under the
pillar's `scene`. **No change to the generator is needed** — it loads whatever fragment the
tokens point at, and refuses with a readable error when the file is missing.

A fragment is a plain SVG fragment (no `<svg>` wrapper, no `<defs>`), drawn on the same
1200 × 300 canvas with the waterline at `canvas.waterline`. Colours go in as `{{C_HULL}}`,
`{{C_ABYSS}}`, `{{C_DEEP}}`, `{{C_MID}}`, `{{C_SURFACE}}`, `{{C_ACCENT}}`, `{{C_INK}}`,
`{{C_MUTED}}` so the same drawing works in all four palettes. Two gradients from the frame
are available to a scene: `url(#bnr-lamp)` for a light source and `url(#bnr-water)`.

Keep the left 600 px calm: the title sits there, under a veil that fades out toward the scene.

## The bundle page

Each banner comes with a page under `docs/bundles/<bundle-id>.md`, in German, structured:
purpose retold from the manifest, the picture explained, the component table, the traffic
light, provenance. Its preview under `docs/preview/<bundle-id>.html` is one self-contained
file — the banner is embedded into it by the same run that draws it:

```bash
python tools/generate_banner.py <bundle-id> --inline-into docs/preview/<bundle-id>.html
```

Pages are written by hand today. Whether they become generated too is a question for after
the design is approved — generating a layout nobody has signed off on would only make the
rework larger.
