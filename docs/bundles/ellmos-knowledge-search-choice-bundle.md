# Knowledge Search Choice Bundle

![Knowledge Search Choice Bundle — Auswahlregister über memory und domain (Palette geliehen von domain)](../../assets/banners/ellmos-knowledge-search-choice-bundle.svg)

> Auswahlregister für den einen, ausschließlichen Standard der Wissenssuche. Es liegt getrennt, weil seine Kandidaten in zwei verschiedenen funktionalen Bundles wohnen.

| | |
|---|---|
| **Bundle-ID** | `ellmos-knowledge-search-choice-bundle` |
| **Säule** | offen — Reichweite über `memory` und `domain`; Palette geliehen von `domain` |
| **Klasse** | `choice` — Auswahlregister, zählt **nicht** in der Deployment-Auflösung |
| **Version** | 1.0.0 |
| **Status / Lifecycle** | `registered` / `draft` |
| **Sichtbarkeit** | `private` (bis eine Welle freigegeben ist) |
| **Komponenten** | 1 — eine empfohlen, dazu eine Choice-Gruppe |
| **Ring** | Ring 2 der Erstprojektion |

## Wofür dieses Bundle da ist

Eine Rolle, zwei Kandidaten, `pick: exactly-one` — und der dokumentierte Grund für die Ausschließlichkeit ist bemerkenswert: Es geht **nicht** um Qualität, sondern um Adressierbarkeit. Ein Router braucht ein eindeutiges Ziel. Beide Komponenten dürfen nebeneinander existieren; exklusiv ist nur der Standard.

Dass dieses Register überhaupt für sich steht, ist selbst die Aussage: Seine beiden Kandidaten sind in verschiedenen Bundles registriert — GARDENER im [Memory-Human-Context-Bundle](ellmos-memory-human-context-bundle.md), KnowledgeDigest im [Knowledge-Bundle](ellmos-knowledge-bundle.md). Eine Wahl, die zwei Häuser überspannt, kann in keinem von beiden wohnen.

## Säule: woher sie kommt

Dieses Bundle hat **absichtlich keine Säule**, und der Katalog begründet das: Die Rolle `knowledge.search.default` *„spans two pillars: GARDENER sits in memory, KnowledgeDigest in domain. A single pillar would misstate the reach.“* Eine einzige Säule wäre hier also nicht bloß ungenau, sondern falsch.

Der Banner behauptet deshalb keine. Sein Chip nennt **Klasse und Reichweite** — `CHOICE · MEMORY + DOMAIN` — und gibt damit genau wieder, was im Katalog steht. Die Beschriftung ist die Fläche, auf der ein Fehler am teuersten wäre: Sie wird gelesen, wenn sonst nichts gelesen wird.

Eine **Palette** braucht ein Banner trotzdem, und es gibt nur vier. Sie ist deshalb geliehen, und zwar dort, wo die Vorauswahl wohnt: `default_selection` ist `KnowledgeDigest`, registriert im Knowledge-Bundle, dessen Säule der Katalog mit `domain` angibt. Das Frachtwasser ist hier also eine Farbe, keine Zuordnung — ändert sich die Vorauswahl, wechselt die Palette mit, und die Säule bleibt offen.

## Das Bild: Frachtwasser

Das Frachtwasser ist die Domain-Säule: das Fachgut als Ladung — umgeschlagen, gestapelt, transportiert. Ein Kran hebt genau **ein** Stück Fracht, und dieses eine ist der Akzent des Bildes; an Land liegt, was schon gelöscht ist, auf dem Leichter, was noch fährt. Bewegt wird immer nur ein Stück auf einmal — das ist der Unterschied zwischen einem Stapel und einem Umschlag.

Für dieses Register ist das Bild **geliehen**, nicht zugeordnet: Die Farben kommen aus dem Frachtwasser, die Beschriftung nennt trotzdem beide Säulen. Der Abschnitt *Säule: woher sie kommt* oben sagt, warum das kein Widerspruch ist.

## Komponenten

Ein einziger Skill, und der dient der Entscheidung, nicht der Suche.

| Rolle | Komponente | Version | Bedarf | liefert | braucht |
|---|---|---|---|---|---|
| Auswahlanalyse | `skill:decide` | `registry-current` | empfohlen | `candidate-comparison` | `choice-group-criteria` |

## Die Wahl: `knowledge.search.default`

Eine Gruppe, `pick: exactly-one`, Vorauswahl `KnowledgeDigest`.

| Kandidat | Typ | Stellung | Stärken | Preis dafür |
|---|---|---|---|---|
| `GARDENER` | Modul | Alternative | Der einzige Kandidat mit Netzgrenze `local` statt `optional` — nichts kann die Maschine verlassen. Status `active` gegen `alpha` des anderen. Trägt zusätzlich `knowledge.index` und dazu `memory.organic`, also Suche und Gedächtnis in einer Komponente. | Keine Oberfläche — nur Bibliothek, CLI und Dienst. Liefert kein `knowledge.ingest`, Dokumentaufnahme ist nicht seine Aufgabe. Und: Seine `provides`-Liste nennt `knowledge.search`, nicht `knowledge.search.default`. |
| `KnowledgeDigest` | Modul | **Vorauswahl** | Der einzige Kandidat, der `knowledge.search.default` wörtlich deklariert, und der einzige mit `knowledge.ingest`. Vollständiger Oberflächensatz inklusive `ui`. | Status `alpha` gegen `active`. Netzgrenze `optional` statt `local`, weil die Zusammenfassung nach außen rufen darf. |

Die beiden sind im Umfang **nicht austauschbar**: GARDENER indiziert, was ohnehin existiert, und bedient zusätzlich `memory.organic`; KnowledgeDigest besitzt die Dokumentaufnahme. Einen davon zum Suchstandard zu machen entfernt den anderen nicht aus einem Stack.

Die Vorauswahl folgt dem einzigen Kandidaten, der die Fähigkeit **wörtlich** deklariert — das ist ausdrücklich kein Qualitätsurteil.

Zwei Lücken sind als Lücken vermerkt und brauchen den Repo-Eigentümer: Kein Dokument nennt eine Lage oder Schwelle, ab der GARDENER vorzuziehen wäre. Und GARDENERs Katalogeintrag deklariert `knowledge.search.default` nicht, obwohl `composition.rules` ihn als Anbieter führt.

Drei Profile, und zwei davon entscheiden: `full` (ohne Festlegung), `local-only-search` (Override auf `GARDENER`) und `document-ingest-search` (Override auf `KnowledgeDigest`).

## Ampel

Der Rollout ist inkrementell: Ein Bundle geht grün, wenn **jede** seiner Komponenten öffentlich und geprüft ist. Genau das ist das Aufnahmekriterium dieses Repos — die 13 projizierten Bundles sind die, deren Komponenten heute vollständig öffentlich sind, optionale eingeschlossen. Dieses Bundle ist damit **grün-fähig**.

Grün-fähig heißt nicht veröffentlicht. Die Freigabe einer Welle ist eine ausdrückliche Entscheidung des Eigentümers (`PRIVATE.txt`), und keine Automatik nimmt sie vorweg.

## Herkunft und Prüfbarkeit

| | |
|---|---|
| Manifest | [`manifests/bundles/ellmos-knowledge-search-choice-bundle/bundle.v1.json`](../../manifests/bundles/ellmos-knowledge-search-choice-bundle/bundle.v1.json) |
| Katalog-Eintrag | [`manifests/bundles.catalog.v1.json`](../../manifests/bundles.catalog.v1.json) |
| Funktionsvertrag | [`contracts/choice-bundle-contract.v1.json`](../../contracts/choice-bundle-contract.v1.json) |
| Zusicherungsvertrag | `contract:mandatory-assurance-v1` (1.0.0) |
| `content_hash` | `12b5181f1320404b781f73188e353ec32df748fc07d822f3509aa95a85290d8d` |

Der `content_hash` läuft über das Manifest ohne das Hash-Feld selbst — er ist an Ort und Stelle nachrechenbar, ohne Zusatzdatei.

Das Manifest wird **nicht hier gepflegt**, sondern aus der privaten Kompositionsquelle projiziert (`tools/export_from_source.py`). Der Banner dagegen entsteht in diesem Repo, aus `assets/design/` heraus: `python tools/generate_banner.py ellmos-knowledge-search-choice-bundle --pillar domain --chip "CHOICE · MEMORY + DOMAIN"`. `--check` statt Schreiben meldet Abweichung.

---

*Teil der Banner- und Seitenserie über alle 13 Bundles — [Übersicht](README.md). Bildsprache und Regeln der Serie: [`assets/design/README.md`](../../assets/design/README.md).*
