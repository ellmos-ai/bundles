# Memory Human Context Bundle

![Memory Human Context Bundle — Tiefenwasser (MEMORY-Säule)](../../assets/banners/ellmos-memory-human-context-bundle.svg)

> Sitzungszustand, Gedächtnissuche und der daraus abgeleitete menschliche Kontext.

| | |
|---|---|
| **Bundle-ID** | `ellmos-memory-human-context-bundle` |
| **Säule** | `memory` — hält und findet Zustand |
| **Klasse** | `platform` — funktional, zählt in der Deployment-Auflösung |
| **Version** | 1.0.0 |
| **Status / Lifecycle** | `registered` / `draft` |
| **Sichtbarkeit** | `private` (bis eine Welle freigegeben ist) |
| **Komponenten** | 6 — eine erforderlich, drei empfohlen, zwei optional |
| **Ring** | Ring 1 der Erstprojektion |

## Wofür dieses Bundle da ist

Wo das Working-Memory-Bundle den Zustand **einer** Sitzung hält, hält dieses das, was über Sitzungen hinweg bleibt: das kuratierte Gedächtnis, den Index über die Quellen, und das daraus gebaute Modell der Person.

Der interessante Teil ist eine Entscheidung, die das Manifest offenlegt: `USMC` und `GARDENER` sind ein **komplementäres Rollenpaar** (`memory.curated` und `memory.organic`), keine Auswahl. USMC ist die kuratierte Fassade, GARDENER der organische quellenübergreifende Index, der sie speist — *eines zu wählen ersetzt das andere nicht, weil sie verschiedene Fragen beantworten*. Als Choice-Gruppe wäre das nicht ausdrückbar: Eine Gruppe bindet genau eine Rolle, und die Rollen zusammenzulegen würde die Unterscheidung zerstören, die das Paar erst nützlich macht (Operator-Entscheidung vom 2026-08-07).

Ein Zeiger geht von hier ausdrücklich nach draußen: `choice_bundle_refs` verweist auf das [Knowledge-Search-Choice-Bundle](ellmos-knowledge-search-choice-bundle.md), weil GARDENER dort einer der beiden Kandidaten für `knowledge.search.default` ist. Der Spiegel-Zeiger aus dem Knowledge-Bundle fehlt bewusst — dessen Manifest-Hash ist durch eine lebende Freigabe festgenagelt, und ein Auswahlregister darf keine Neufreigabe erzwingen.

## Das Bild: Tiefenwasser

Das Tiefenwasser ist die Memory-Säule, und ihr Zeichen ist das Boot mit seinem Kielwasser. Das Gedächtnis **trägt** — deshalb das Boot — und es **ist** zugleich der zurückgelegte Weg: die Spur hinter dem Heck, die sich nach hinten öffnet, hell dort, wo sie eben entstanden ist, und blasser, je weiter sie zurückliegt. Zwei passierte Tonnen stehen noch in der Bahn: Wegmarken derselben Fahrt.

Hier ist es die **ganze** Fahrt, nicht nur das letzte Stück: die Spur bis zur Bildkante, mit den Marken, die längst passiert sind.

## Komponenten

Vier Module, eine Zugangsfläche und ein Skill.

| Rolle | Komponente | Version | Bedarf | liefert | braucht |
|---|---|---|---|---|---|
| Kuratiertes Gedächtnis | `module:USMC` | `v4-shadow` | erforderlich | — | — |
| Organischer Index | `module:GARDENER` | `v4-shadow` | empfohlen | — | — |
| Sitzungs-Haken | `module:memory-hooker` | `v4-shadow` | empfohlen | — | — |
| Nutzermodell | `module:build-your-users-mind` | `v4-shadow` | empfohlen | — | — |
| Zugang zum Gedächtnis | `access_surface:Homebase-memory` | `v4-shadow` | optional | — | — |
| Kontext-Synthese | `skill:decision-briefing` | `registry-current` | optional | `decision-context-brief` | `explicit-user-scope` |

Der einzige Skill des Bundles verlangt `explicit-user-scope` — menschlicher Kontext wird nicht aus dem Vorhandenen abgeleitet, sondern nur in dem Rahmen gebildet, den die Person ausdrücklich aufspannt.

**Profile:** `full` und `operator`, beide ohne Ein- oder Ausschlüsse.

## Ampel

Der Rollout ist inkrementell: Ein Bundle geht grün, wenn **jede** seiner Komponenten öffentlich und geprüft ist. Genau das ist das Aufnahmekriterium dieses Repos — die 13 projizierten Bundles sind die, deren Komponenten heute vollständig öffentlich sind, optionale eingeschlossen. Dieses Bundle ist damit **grün-fähig**.

Grün-fähig heißt nicht veröffentlicht. Die Freigabe einer Welle ist eine ausdrückliche Entscheidung des Eigentümers (`PRIVATE.txt`), und keine Automatik nimmt sie vorweg.

## Herkunft und Prüfbarkeit

| | |
|---|---|
| Manifest | [`manifests/bundles/ellmos-memory-human-context-bundle/bundle.v1.json`](../../manifests/bundles/ellmos-memory-human-context-bundle/bundle.v1.json) |
| Katalog-Eintrag | [`manifests/bundles.catalog.v1.json`](../../manifests/bundles.catalog.v1.json) |
| Funktionsvertrag | keiner — dieses Manifest führt kein `functional_contracts` |
| Zusicherungsvertrag | `contract:mandatory-assurance-v1` (1.0.0) |
| `content_hash` | `a61c9efe8f456c6ed037ee339293ae80705101583dc7f9d174940b788f0aba06` |

Der `content_hash` läuft über das Manifest ohne das Hash-Feld selbst — er ist an Ort und Stelle nachrechenbar, ohne Zusatzdatei.

Das Manifest wird **nicht hier gepflegt**, sondern aus der privaten Kompositionsquelle projiziert (`tools/export_from_source.py`). Der Banner dagegen entsteht in diesem Repo, aus `assets/design/` heraus: `python tools/generate_banner.py ellmos-memory-human-context-bundle`. `--check` statt Schreiben meldet Abweichung.

---

*Teil der Banner- und Seitenserie über alle 13 Bundles — [Übersicht](README.md). Bildsprache und Regeln der Serie: [`assets/design/README.md`](../../assets/design/README.md).*
