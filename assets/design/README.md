# Banner design

One banner per bundle, all of them in one visual language. This folder holds the parts that
stay the same across the series; only the scene and the palette change with the pillar.

> **Status: settled, and the series is complete.** The pilot — `ellmos-daily-life-bundle` — was
> ratified by the owner on 2026-08-08, and with it the whole design system: the four pillar
> palettes, the 1200 × 300 template, the quay lamp as the one warm light, the scene fragments.
> **Tokens, template and generator are frozen from here on.** Changing any of them is a design
> decision for the owner; the series only adds scenes and polishes over the catalogue. All 13
> bundles have a banner today.

## The picture, and why

The visual language comes from the water lexicon the ecosystem already uses (see
`SYSTEM-PRODUKTLINIE.md` §1 and §6b): the stream is the process, the vessels are the
structure. Each of the four pillars is therefore a body of water with its own light, and each
gets the symbol the ecosystem already assigned it.

| Pillar | Water | Symbol | Scene | The single accent |
|---|---|---|---|---|
| `memory` | deep water | the boat and its wake | `wake` ✔ | the track itself |
| `control` | clear water | the helm | `helm` ✔ | the king spoke |
| `uas` | the harbour | nets and species of fish | `harbour` ✔ | the quay lamp and the lit catch |
| `domain` | freight water | cargo, crane, containers | `freight` ✔ | the one box on the hook |

The harbour scene carries the UAS reading verbatim: **different nets catch different fish**,
and the species are the end products as food — the plan, the route, the morning digest. One
net holds the catch the light falls on; the others hang ready.

The three that followed keep the same grammar — calm silhouettes, structures standing in the
water on piles, one accent that carries the meaning rather than decorating it:

- **`wake`** — the boat, bow to the right, and the track opening astern: bright where it was
  just laid, thinner and fainter the further back it goes, with cross ribs and two buoys
  already passed. The memory pillar reads *the memory carries, and it is the distance covered*,
  so the accent is the track and not the boat.
- **`helm`** — the wheel on a platform, bridge rails either side, and a straight dashed ray
  running out to the horizon: the course you can read because the water is calm. The accent is
  the king spoke, which by convention marks the rudder amidships. Steering means making **one**
  course legible.
- **`freight`** — a gantry over a laden barge, stacks already landed on the quay, and one
  container on the hook heading for the berth left open on deck. The accent is that one box:
  a stack is not a transfer, and only one piece moves at a time.

**The quay lamp stays exclusive to `uas`.** It is the human contact point, and the only pillar
whose accent is a warm light. The other three scenes carry no lamp and use no `url(#bnr-lamp)`;
their accent is a marked object, not a light source.

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

**The whole series, and the drift check over it.** Nine of the thirteen manifests carry a
`pillar` and need nothing but their id; the three named below carry none and are handed the
pillar the catalogue records for them (see *When a bundle has no pillar*):

```bash
for id in $(ls manifests/bundles); do
  case "$id" in
    ellmos-knowledge-bundle|ellmos-media-production-bundle|ellmos-knowledge-search-choice-bundle)
      python tools/generate_banner.py "$id" --pillar domain \
             --inline-into "docs/preview/$id.html" ;;
    *)
      python tools/generate_banner.py "$id" \
             --inline-into "docs/preview/$id.html" ;;
  esac
done
```

Append `--check` to the same loop to get the drift report instead of the write: it compares
both the banner and the copy embedded in its preview page, and exits non-zero on the first
difference. The `--pillar` arguments have to be identical in both runs — a banner drawn with
one pillar and checked with another reports drift that is not there.

## When a bundle has no pillar

Three manifests carry no `pillar`, and a banner cannot be drawn without one — the generator
refuses rather than inventing a palette. The rule is that **the pillar is looked up, never
guessed**, and the catalogue is where it is looked up: `manifests/bundles.catalog.v1.json`
records under `pillars.omissions` why each field is absent, and the two reasons are answered
differently.

| Case in `pillars.omissions` | Bundles | What the banner does |
|---|---|---|
| `approval_pinned` — the pillar is known, the field just could not be written | `ellmos-knowledge-bundle`, `ellmos-media-production-bundle` | takes the pillar the catalogue names verbatim (*intended pillar domain, not written*), because a live approval pins the manifest hash with `default_action: deny` and adding a field would silently invalidate a granted approval |
| `hosted_and_cross_pillar` — there deliberately is none, because one value would misstate the reach | `ellmos-knowledge-search-choice-bundle` | **borrows** a palette instead of claiming a pillar: the home bundle of its `default_selection` decides it. `KnowledgeDigest` lives in `ellmos-knowledge-bundle`, so the banner runs on `domain` |

Both cases are stated on the bundle page under *Säule: woher sie kommt*, and marked in the
[index](../../docs/bundles/README.md). Nothing is silent about it: a chip reading
`DOMAIN · FRACHTWASSER` on a bundle whose manifest names no pillar is a **borrowed label**, and
the page says so. Should the default selection change, the palette follows it — and the pillar
stays open, which is the honest state.

## Adding a scene for another pillar

Drop `scenes/<name>.svg` next to `harbour.svg`, under **the name `tokens.json` already gives
that pillar's `scene`**. Since the tokens are frozen, the file name follows the tokens and not
the other way round: `memory` is `wake`, not any other word for the same picture — otherwise
every banner of that pillar would need a `--scene` override and the loop above would stop being
the whole truth. **No change to the generator is needed** — it loads whatever fragment the
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
light, provenance. Where a bundle carries a `choice_groups` entry, its candidates get a
section of their own — that selection knowledge is the reason a recipe beats an ingredient
list, so it is not summarised away. Its preview under `docs/preview/<bundle-id>.html` is one
self-contained file — the banner is embedded into it by the same run that draws it:

```bash
python tools/generate_banner.py <bundle-id> --inline-into docs/preview/<bundle-id>.html
```

All 13 pages exist, and [`docs/bundles/README.md`](../../docs/bundles/README.md) is the index
over them, grouped by pillar. The prose is written by hand and says only what the manifest and
the catalogue actually carry: where a page states a fact, the field it came from is nameable.
Where something is missing or undecided — a skill nobody has built, a role no stack fills yet —
the page says that too rather than rounding it up.
