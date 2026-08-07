# Knowledge Bundle

![Knowledge Bundle — Frachtwasser (Säule domain, abgeleitet)](../../assets/banners/ellmos-knowledge-bundle.svg)

> Dokumentwissen, Wiederauffinden, Berichte und neutrale Recherche.

| | |
|---|---|
| **Bundle-ID** | `ellmos-knowledge-bundle` |
| **Säule** | `domain` — trägt Fachgut — *abgeleitet* |
| **Klasse** | `platform` — funktional, zählt in der Deployment-Auflösung |
| **Version** | 1.0.0 |
| **Status / Lifecycle** | `registered` / `draft` |
| **Sichtbarkeit** | `private` (bis eine Welle freigegeben ist) |
| **Komponenten** | 8 — eine erforderlich, sechs empfohlen, eine optional |
| **Ring** | Ring 1 der Erstprojektion |

## Wofür dieses Bundle da ist

Dieses Bundle beantwortet die Frage, wie Wissen **hereinkommt und wiedergefunden wird**: aufnehmen, zerlegen, indizieren, berichten. Es gehört zum funktionalen Kern, weil ein System ohne Weg zum Wissen zwar laufen, aber nichts lernen kann.

Der Schnitt gegen das [Document-Handler-Bundle](ellmos-doc-handler-bundle.md) ist ausdrücklich: Dort ist Dokumentarbeit ein **Handwerk** — herstellen, säubern, anonymisieren, ablegen. Hier ist sie **Wiederauffinden**. Dass beide `report-forge`, `docs-analysis`, `document-chunker` und `bilingual-doc-sync` führen, ist erlaubt: Ein Bundle ist eine Referenzliste, keine Ausschließlichkeitszuweisung.

## Säule: woher sie kommt

Diese Säule steht **nicht** im Manifest, sondern im Katalog. `manifests/bundles.catalog.v1.json` führt unter `pillars.omissions.approval_pinned` wörtlich *„intended pillar domain, not written“* — und den Grund: Der Manifest-Hash ist durch eine lebende Freigabe (`manifests/module-readme-discovery.approvals.v1.json`, `default_action: deny`) festgenagelt. Ein zusätzliches Feld würde eine erteilte Freigabe stillschweigend entwerten. Der Banner nimmt die Säule also aus dem Katalog, wo sie belegt ist, statt sie zu raten — und diese Seite sagt es, statt es zu verschweigen.

## Das Bild: Frachtwasser

Das Frachtwasser ist die Domain-Säule: das Fachgut als Ladung — umgeschlagen, gestapelt, transportiert. Ein Kran hebt genau **ein** Stück Fracht, und dieses eine ist der Akzent des Bildes; an Land liegt, was schon gelöscht ist, auf dem Leichter, was noch fährt. Bewegt wird immer nur ein Stück auf einmal — das ist der Unterschied zwischen einem Stapel und einem Umschlag.

Wissen ist hier Fachgut wie jedes andere: Es wird geladen, gestapelt und weitergegeben — und immer nur ein Stück auf einmal bewegt.

## Komponenten

Fünf Module und drei Skills.

| Rolle | Komponente | Version | Bedarf | liefert | braucht |
|---|---|---|---|---|---|
| Aufnahme und Suche | `module:KnowledgeDigest` | `v4-shadow` | erforderlich | — | — |
| Wiki-Saat | `module:WikiStub-Seed` | `v4-shadow` | empfohlen | — | — |
| Berichtsbau | `module:report-forge` | `v4-shadow` | empfohlen | — | — |
| Netz-Abruf | `module:web-scraper` | `v4-shadow` | empfohlen | — | — |
| Projektdoku-Vorlage | `module:project-docs-template` | `v4-shadow` | empfohlen | — | — |
| Bedarfsanalyse | `skill:docs-analysis` | `registry-current` | empfohlen | `document-gap-analysis` | `document-sources` |
| Retrieval-Vorbereitung | `skill:document-chunker` | `registry-current` | empfohlen | `retrieval-chunks` | `approved-document-input` |
| Sprachparität | `skill:bilingual-doc-sync` | `registry-current` | optional | `semantic-drift-report` | `stable-canonical-text` |

`KnowledgeDigest` ist die einzige **erforderliche** Komponente — und zugleich einer der beiden Kandidaten im [Knowledge-Search-Choice-Bundle](ellmos-knowledge-search-choice-bundle.md). Dass es hier Pflicht ist, sagt nichts darüber, wer die Suche als Standard beantwortet; das entscheidet das Register.

**Profile:** `full` und `operator`, beide ohne Ein- oder Ausschlüsse.

## Ampel

Der Rollout ist inkrementell: Ein Bundle geht grün, wenn **jede** seiner Komponenten öffentlich und geprüft ist. Genau das ist das Aufnahmekriterium dieses Repos — die 13 projizierten Bundles sind die, deren Komponenten heute vollständig öffentlich sind, optionale eingeschlossen. Dieses Bundle ist damit **grün-fähig**.

Grün-fähig heißt nicht veröffentlicht. Die Freigabe einer Welle ist eine ausdrückliche Entscheidung des Eigentümers (`PRIVATE.txt`), und keine Automatik nimmt sie vorweg.

## Herkunft und Prüfbarkeit

| | |
|---|---|
| Manifest | [`manifests/bundles/ellmos-knowledge-bundle/bundle.v1.json`](../../manifests/bundles/ellmos-knowledge-bundle/bundle.v1.json) |
| Katalog-Eintrag | [`manifests/bundles.catalog.v1.json`](../../manifests/bundles.catalog.v1.json) |
| Funktionsvertrag | keiner — dieses Manifest führt kein `functional_contracts` |
| Zusicherungsvertrag | `contract:mandatory-assurance-v1` (1.0.0) |
| `content_hash` | `4e3dbf2b2e8adfb7dcd2ffbdc36fc7af98d815f9bfd40686e796e639b43e8ad9` |

Der `content_hash` läuft über das Manifest ohne das Hash-Feld selbst — er ist an Ort und Stelle nachrechenbar, ohne Zusatzdatei.

Das Manifest wird **nicht hier gepflegt**, sondern aus der privaten Kompositionsquelle projiziert (`tools/export_from_source.py`). Der Banner dagegen entsteht in diesem Repo, aus `assets/design/` heraus: `python tools/generate_banner.py ellmos-knowledge-bundle --pillar domain`. `--check` statt Schreiben meldet Abweichung.

---

*Teil der Banner- und Seitenserie über alle 13 Bundles — [Übersicht](README.md). Bildsprache und Regeln der Serie: [`assets/design/README.md`](../../assets/design/README.md).*
