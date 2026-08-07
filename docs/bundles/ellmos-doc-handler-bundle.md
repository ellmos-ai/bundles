# Document Handler Bundle

![Document Handler Bundle — Frachtwasser (DOMAIN-Säule)](../../assets/banners/ellmos-doc-handler-bundle.svg)

> Dokumentarbeit als Handwerk: Dokumente herstellen, säubern, anonymisieren und ablegen.

| | |
|---|---|
| **Bundle-ID** | `ellmos-doc-handler-bundle` |
| **Säule** | `domain` — trägt Fachgut |
| **Klasse** | `domain` — funktional, zählt in der Deployment-Auflösung |
| **Version** | 1.0.0 |
| **Status / Lifecycle** | `registered` / `draft` |
| **Sichtbarkeit** | `private` (bis eine Welle freigegeben ist) |
| **Komponenten** | 11 — acht empfohlen, drei optional |
| **Ring** | Ring 2 der Erstprojektion |

## Wofür dieses Bundle da ist

Das größte Bundle der Projektion, und das einzige, dessen Zweck sich am besten in Verben sagen lässt: herstellen, säubern, anonymisieren, ablegen. Nichts davon ist Recherche — das Wiederauffinden bleibt im [Knowledge-Bundle](ellmos-knowledge-bundle.md).

Warum es überhaupt ein eigenes Bundle ist, steht im Manifest, und die Antwort ist erfreulich unromantisch: Das Knowledge-Bundle wäre das nächstgelegene Zuhause, **aber sein Manifest-Hash ist durch eine lebende Freigabe mit `default_action: deny` festgenagelt** — es darf nicht erweitert werden. Dazu kommt der sachliche Grund: Der Schnitt ist ein anderer.

Eine Komponente ist ausdrücklich **nicht** mitgewandert: `WikiStub-Seed` bleibt im Knowledge-Bundle, denn genau dafür wurde die lebende Freigabe erteilt. Sie zu verschieben oder zu duplizieren würde die festgenagelte Entscheidung berühren.

## Das Bild: Frachtwasser

Das Frachtwasser ist die Domain-Säule: das Fachgut als Ladung — umgeschlagen, gestapelt, transportiert. Ein Kran hebt genau **ein** Stück Fracht, und dieses eine ist der Akzent des Bildes; an Land liegt, was schon gelöscht ist, auf dem Leichter, was noch fährt. Bewegt wird immer nur ein Stück auf einmal — das ist der Unterschied zwischen einem Stapel und einem Umschlag.

Elf Komponenten, und trotzdem hängt immer nur ein Stück am Haken: Ein Dokument durchläuft die Werkstatt der Reihe nach, nicht alles auf einmal.

## Komponenten

Fünf Module und sechs Skills — die dichteste Zutatenliste im Repo.

| Rolle | Komponente | Version | Bedarf | liefert | braucht |
|---|---|---|---|---|---|
| Berichtsbau | `module:report-forge` | `v4-shadow` | empfohlen | — | — |
| Arbeitsblätter | `module:worksheet-generator` | `v4-shadow` | empfohlen | — | — |
| Anonymisierung | `module:anonymizer` | `v4-shadow` | empfohlen | — | — |
| Aufnahme und Suche | `module:KnowledgeDigest` | `v4-shadow` | optional | — | — |
| Notiz-Werkzeug | `module:llm-note` | `v4-shadow` | optional | — | — |
| Bedarfsanalyse | `skill:docs-analysis` | `registry-current` | empfohlen | `document-gap-analysis` | `document-sources` |
| Retrieval-Vorbereitung | `skill:document-chunker` | `registry-current` | empfohlen | `retrieval-chunks` | `approved-document-input` |
| Sprachparität | `skill:bilingual-doc-sync` | `registry-current` | empfohlen | `semantic-drift-report` | `stable-canonical-text` |
| Texthygiene | `skill:llm-text-hygiene` | `registry-current` | empfohlen | `text-hygiene-report` | `finished-text` |
| Notizfluss | `skill:notizblock` | `registry-current` | optional | `captured-note` | `approved-personal-context` |
| Encoding-Reparatur | `skill:encoding-fix` | `registry-current` | optional | `encoding-repair-plan` | `narrow-verified-file-set` |

Die Spalte *braucht* ist hier besonders sprechend. `encoding-fix` verlangt ein `narrow-verified-file-set` — kein Verzeichnis, kein Glob, sondern eine eng geprüfte Dateiliste. Und `llm-text-hygiene` setzt `finished-text` voraus: Hygiene läuft am Ende, nicht nebenher.

**Profile:** `full` und `operator`, beide ohne Ein- oder Ausschlüsse.

## Ampel

Der Rollout ist inkrementell: Ein Bundle geht grün, wenn **jede** seiner Komponenten öffentlich und geprüft ist. Genau das ist das Aufnahmekriterium dieses Repos — die 13 projizierten Bundles sind die, deren Komponenten heute vollständig öffentlich sind, optionale eingeschlossen. Dieses Bundle ist damit **grün-fähig**.

Grün-fähig heißt nicht veröffentlicht. Die Freigabe einer Welle ist eine ausdrückliche Entscheidung des Eigentümers (`PRIVATE.txt`), und keine Automatik nimmt sie vorweg.

## Herkunft und Prüfbarkeit

| | |
|---|---|
| Manifest | [`manifests/bundles/ellmos-doc-handler-bundle/bundle.v1.json`](../../manifests/bundles/ellmos-doc-handler-bundle/bundle.v1.json) |
| Katalog-Eintrag | [`manifests/bundles.catalog.v1.json`](../../manifests/bundles.catalog.v1.json) |
| Funktionsvertrag | [`contracts/bundle-family-contract.v1.json`](../../contracts/bundle-family-contract.v1.json) |
| Zusicherungsvertrag | `contract:mandatory-assurance-v1` (1.0.0) |
| `content_hash` | `e277ed61862c627687a275150ff23393e95b08cf1d14c949dea79773081f4005` |

Der `content_hash` läuft über das Manifest ohne das Hash-Feld selbst — er ist an Ort und Stelle nachrechenbar, ohne Zusatzdatei.

Das Manifest wird **nicht hier gepflegt**, sondern aus der privaten Kompositionsquelle projiziert (`tools/export_from_source.py`). Der Banner dagegen entsteht in diesem Repo, aus `assets/design/` heraus: `python tools/generate_banner.py ellmos-doc-handler-bundle`. `--check` statt Schreiben meldet Abweichung.

---

*Teil der Banner- und Seitenserie über alle 13 Bundles — [Übersicht](README.md). Bildsprache und Regeln der Serie: [`assets/design/README.md`](../../assets/design/README.md).*
