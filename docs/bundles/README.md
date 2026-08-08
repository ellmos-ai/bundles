# Die Bundles im Überblick

Alle **13** Bundles dieser Projektion, jedes mit Banner und eigener Seite. Gruppiert nach
**Säule** — der Familie, zu der ein Bundle gehört: `memory` hält und findet Zustand, `control`
steuert, `uas` bedient die Person direkt, `domain` trägt Fachgut.

Die Säule ist keine zweite Klasse und hat an der Deployment-Auflösung keinen Anteil. Wer wissen
will, was ein Bundle im Betrieb *ist*, liest die Spalte **Klasse**: `platform` und `domain` sind
funktional und zählen, `choice` ist ein Auswahlregister und zählt nicht.

Zusammen 60 Komponenten-Plätze. Der maschinenlesbare Index ist
[`manifests/bundles.catalog.v1.json`](../../manifests/bundles.catalog.v1.json); diese Seite ist
die lesbare Fassung davon.

---

## Tiefenwasser — `memory`

> Das Gedächtnis trägt und ist zugleich der zurückgelegte Weg. Bild: das Boot und sein Kielwasser.

| Banner | Bundle | Klasse | Komponenten | Ring |
|---|---|---|---|---|
| [<img src="../../assets/banners/ellmos-working-memory-bundle.svg" width="330" alt="Working Memory Bundle — Tiefenwasser">](ellmos-working-memory-bundle.md) | **[Working Memory Bundle](ellmos-working-memory-bundle.md)**<br>`ellmos-working-memory-bundle`<br>Der Arbeitszustand einer Sitzung | `platform` | 5 | 1 |
| [<img src="../../assets/banners/ellmos-memory-human-context-bundle.svg" width="330" alt="Memory Human Context Bundle — Tiefenwasser">](ellmos-memory-human-context-bundle.md) | **[Memory Human Context Bundle](ellmos-memory-human-context-bundle.md)**<br>`ellmos-memory-human-context-bundle`<br>Dauerhaftes Gedächtnis und Nutzermodell | `platform` | 6 | 1 |

## Klarwasser — `control`

> Der Steuerstand: klares Wasser, in dem man den Kurs sieht. Bild: das Steuerrad.

| Banner | Bundle | Klasse | Komponenten | Ring |
|---|---|---|---|---|
| [<img src="../../assets/banners/ellmos-agents-bundle.svg" width="330" alt="Agents Bundle — Klarwasser">](ellmos-agents-bundle.md) | **[Agents Bundle](ellmos-agents-bundle.md)**<br>`ellmos-agents-bundle`<br>Zugang zur Laufzeit, die es noch nicht gibt | `platform` | 7 | 1 |
| [<img src="../../assets/banners/ellmos-coordination-choice-bundle.svg" width="330" alt="Coordination Choice Bundle — Klarwasser">](ellmos-coordination-choice-bundle.md) | **[Coordination Choice Bundle](ellmos-coordination-choice-bundle.md)**<br>`ellmos-coordination-choice-bundle`<br>Auswahlregister: Sperren und Koordination | `choice` | 2 | 1 |

## Hafen — `uas`

> Der Ort, an dem Mensch und System aneinander andocken. Bild: verschiedene Netze fangen
> verschiedenen Fisch — die Fischarten sind die Endprodukte, so wie man sie bekommt.

| Banner | Bundle | Klasse | Komponenten | Ring |
|---|---|---|---|---|
| [<img src="../../assets/banners/ellmos-daily-life-bundle.svg" width="330" alt="Daily Life Bundle — Hafen">](ellmos-daily-life-bundle.md) | **[Daily Life Bundle](ellmos-daily-life-bundle.md)**<br>`ellmos-daily-life-bundle`<br>Haushalt, Wetter, Wege, Morgenübersicht | `domain` | 6 | 2 |
| [<img src="../../assets/banners/ellmos-voice-media-assist-bundle.svg" width="330" alt="Voice and Media Assist Bundle — Hafen">](ellmos-voice-media-assist-bundle.md) | **[Voice and Media Assist Bundle](ellmos-voice-media-assist-bundle.md)**<br>`ellmos-voice-media-assist-bundle`<br>Sprechen und Hören statt Tippen | `domain` | 3 | 2 |
| [<img src="../../assets/banners/ellmos-health-assist-bundle.svg" width="330" alt="Health Assist Bundle — Hafen">](ellmos-health-assist-bundle.md) | **[Health Assist Bundle](ellmos-health-assist-bundle.md)**<br>`ellmos-health-assist-bundle`<br>Gesundheitliches organisieren — nur das | `domain` | 2 | 2 |
| [<img src="../../assets/banners/ellmos-briefing-bundle.svg" width="330" alt="Briefing Bundle — Hafen">](ellmos-briefing-bundle.md) | **[Briefing Bundle](ellmos-briefing-bundle.md)**<br>`ellmos-briefing-bundle`<br>Jemanden auf etwas vorbereiten | `domain` | 1 | 2 |
| [<img src="../../assets/banners/ellmos-finance-assist-bundle.svg" width="330" alt="Finance Assist Bundle — Hafen">](ellmos-finance-assist-bundle.md) | **[Finance Assist Bundle](ellmos-finance-assist-bundle.md)**<br>`ellmos-finance-assist-bundle`<br>Überblick über Geld und Versicherungen | `domain` | 1 | 2 |

## Frachtwasser — `domain`

> Das Fachgut als Fracht: umgeschlagen, gestapelt, transportiert. Bild: Kran, Leichter, Container.

| Banner | Bundle | Klasse | Komponenten | Ring |
|---|---|---|---|---|
| [<img src="../../assets/banners/ellmos-doc-handler-bundle.svg" width="330" alt="Document Handler Bundle — Frachtwasser">](ellmos-doc-handler-bundle.md) | **[Document Handler Bundle](ellmos-doc-handler-bundle.md)**<br>`ellmos-doc-handler-bundle`<br>Dokumentarbeit als Handwerk | `domain` | 11 | 2 |
| [<img src="../../assets/banners/ellmos-knowledge-bundle.svg" width="330" alt="Knowledge Bundle — Frachtwasser, Säule abgeleitet">](ellmos-knowledge-bundle.md) | **[Knowledge Bundle](ellmos-knowledge-bundle.md)**<br>`ellmos-knowledge-bundle`<br>Wissen aufnehmen und wiederfinden<br>Säule **abgeleitet** ¹ | `platform` | 8 | 1 |
| [<img src="../../assets/banners/ellmos-media-production-bundle.svg" width="330" alt="Media Production Bundle — Frachtwasser, Säule abgeleitet">](ellmos-media-production-bundle.md) | **[Media Production Bundle](ellmos-media-production-bundle.md)**<br>`ellmos-media-production-bundle`<br>Medien herstellen statt konsumieren<br>Säule **abgeleitet** ¹ | `domain` | 7 | 2 |

¹ Die Säule steht nicht im Manifest, sondern im Katalog: `pillars.omissions.approval_pinned` nennt
sie und den Grund — der Manifest-Hash ist durch eine lebende Freigabe festgenagelt, ein zusätzliches
Feld würde sie entwerten. Der Banner nimmt die belegte Säule, die Bundle-Seite sagt es dazu.

## Ohne Säule

> Ein Bundle, dessen Reichweite über zwei Säulen geht. Es bekommt keine zugewiesen — es **leiht**
> nur eine Palette.

| Banner | Bundle | Klasse | Komponenten | Ring |
|---|---|---|---|---|
| [<img src="../../assets/banners/ellmos-knowledge-search-choice-bundle.svg" width="330" alt="Knowledge Search Choice Bundle — Auswahlregister über memory und domain">](ellmos-knowledge-search-choice-bundle.md) | **[Knowledge Search Choice Bundle](ellmos-knowledge-search-choice-bundle.md)**<br>`ellmos-knowledge-search-choice-bundle`<br>Auswahlregister: der Standard der Wissenssuche<br>Reichweite `memory` + `domain` ² | `choice` | 1 | 2 |

² Der Katalog vermerkt ausdrücklich, dass die Rolle `knowledge.search.default` zwei Säulen
überspannt — GARDENER sitzt in `memory`, KnowledgeDigest in `domain` — und dass eine einzelne die
Reichweite falsch darstellen würde. Der Banner nennt deshalb keine Säule, sondern Klasse und
Reichweite (`CHOICE · MEMORY + DOMAIN`). Nur die **Farben** sind geliehen, und zwar von dem
Bundle, in dem die Vorauswahl registriert ist: Das Frachtwasser ist hier eine Palette, keine
Zuordnung.

---

## Wie diese Seiten entstehen

Der Banner kommt aus dem Generator, Titel und Säule aus dem Manifest:

```bash
python tools/generate_banner.py <bundle-id>          # zeichnen
python tools/generate_banner.py <bundle-id> --check  # Abweichung melden statt schreiben
```

Die drei Bundles ohne `pillar` im Manifest brauchen die belegte Säule als Argument — sonst bricht
der Generator ab, statt sich eine auszudenken:

```bash
python tools/generate_banner.py ellmos-knowledge-bundle --pillar domain
python tools/generate_banner.py ellmos-media-production-bundle --pillar domain
python tools/generate_banner.py ellmos-knowledge-search-choice-bundle --pillar domain
```

Regeln der Serie, Paletten und das Ergänzen einer Szene:
[`assets/design/README.md`](../../assets/design/README.md). Jede Bundle-Seite hat außerdem eine
in sich geschlossene Vorschau unter [`docs/preview/`](../preview) — eine Datei, die überall
aufgeht, mit dem Banner darin eingebettet statt verlinkt.
