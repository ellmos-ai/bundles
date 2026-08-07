# Working Memory Bundle

![Working Memory Bundle — Tiefenwasser (MEMORY-Säule)](../../assets/banners/ellmos-working-memory-bundle.svg)

> Der kurzlebige Arbeitszustand einer Agenten-Sitzung — was erfasst wurde, was offen ist, was noch beantwortet werden muss.

| | |
|---|---|
| **Bundle-ID** | `ellmos-working-memory-bundle` |
| **Säule** | `memory` — hält und findet Zustand |
| **Klasse** | `platform` — funktional, zählt in der Deployment-Auflösung |
| **Version** | 1.0.0 |
| **Status / Lifecycle** | `registered` / `draft` |
| **Sichtbarkeit** | `private` (bis eine Welle freigegeben ist) |
| **Komponenten** | 5 — zwei erforderlich, drei empfohlen |
| **Ring** | Ring 1 der Erstprojektion |

## Wofür dieses Bundle da ist

Dieses Bundle sammelt den Zustand, der **während** einer Sitzung entsteht und nach ihr wieder verfällt: die Haken, die mitschreiben, und die Träger, die das Aufgeschriebene offen halten. Die Zweckzeile des Manifests nennt drei Fragen — *was wurde erfasst, was ist offen, was muss noch beantwortet werden*.

Der Grund für den Schnitt steht im Manifest selbst: Die beiden Hook-Träger und die beiden Aufgaben-Träger lagen bis dahin in **drei verschiedenen Bundles** und hatten kein gemeinsames Zuhause. Dass sie dort weiterhin auftauchen, ist kein Fehler — `overlap_is_intended` verweist auf R2 der Sovereign-Anforderungen: Ein Bundle ist eine Referenzliste, keine Ausschließlichkeitszuweisung.

`task-master` und `ticket-master` sind dabei ausdrücklich **keine Alternativen**, sondern ein komplementäres Rollenpaar (`tasks.default` und `tickets.capture`, je höchstens einmal besetzt). Das Manifest zitiert dafür die Regel im Klartext: *„Keine Konkurrenz zum Taskmanagement“* — ticket-master erfasst die Eingabe in dem Moment, in dem sie auftaucht, task-master trägt die bleibende Aufgabe. Genau deshalb ist es **keine** Choice-Gruppe: Eine Gruppe bindet genau eine Rolle, und diese beiden teilen sich keine.

## Das Bild: Tiefenwasser

Das Tiefenwasser ist die Memory-Säule, und ihr Zeichen ist das Boot mit seinem Kielwasser. Das Gedächtnis **trägt** — deshalb das Boot — und es **ist** zugleich der zurückgelegte Weg: die Spur hinter dem Heck, die sich nach hinten öffnet, hell dort, wo sie eben entstanden ist, und blasser, je weiter sie zurückliegt. Zwei passierte Tonnen stehen noch in der Bahn: Wegmarken derselben Fahrt.

Für den Arbeitsspeicher ist es das **frischeste Stück** der Spur, direkt hinter dem Heck: das, was noch hell ist und gleich verblasst.

## Komponenten

Vier Module und ein Skill. `v4-shadow` heißt: Die Version stammt aus der Schattenprojektion des Kompositionsplans, nicht aus einer Laufzeit; `registry-current` heißt, dass die Skill-Registry die Version bestimmt.

| Rolle | Komponente | Version | Bedarf | liefert | braucht |
|---|---|---|---|---|---|
| Sitzungs-Haken | `module:memory-hooker` | `v4-shadow` | erforderlich | — | — |
| Workflow-Haken | `module:WORKFLOWHOOKER` | `v4-shadow` | erforderlich | — | — |
| Aufgaben-Träger | `module:task-master` | `v4-shadow` | empfohlen | — | — |
| Ticket-Erfassung | `module:ticket-master` | `v4-shadow` | empfohlen | — | — |
| Aufgaben-Gate | `skill:condition` | `registry-current` | empfohlen | `checkable-gate` | `stated-condition` |

**Zwei** erforderliche Komponenten sind für dieses Repo ungewöhnlich — die meisten Bundles halten sich mit Pflicht zurück. Hier ist es folgerichtig: Ohne die beiden Haken gibt es nichts, was mitschreibt, und damit keinen Arbeitsspeicher.

**Profile:** `full` und `operator` sind angelegt, beide ohne Ein- oder Ausschlüsse und ohne Overrides. Sie unterscheiden hier heute nichts.

## Ampel

Der Rollout ist inkrementell: Ein Bundle geht grün, wenn **jede** seiner Komponenten öffentlich und geprüft ist. Genau das ist das Aufnahmekriterium dieses Repos — die 13 projizierten Bundles sind die, deren Komponenten heute vollständig öffentlich sind, optionale eingeschlossen. Dieses Bundle ist damit **grün-fähig**.

Grün-fähig heißt nicht veröffentlicht. Die Freigabe einer Welle ist eine ausdrückliche Entscheidung des Eigentümers (`PRIVATE.txt`), und keine Automatik nimmt sie vorweg.

## Herkunft und Prüfbarkeit

| | |
|---|---|
| Manifest | [`manifests/bundles/ellmos-working-memory-bundle/bundle.v1.json`](../../manifests/bundles/ellmos-working-memory-bundle/bundle.v1.json) |
| Katalog-Eintrag | [`manifests/bundles.catalog.v1.json`](../../manifests/bundles.catalog.v1.json) |
| Funktionsvertrag | [`contracts/bundle-family-contract.v1.json`](../../contracts/bundle-family-contract.v1.json) |
| Zusicherungsvertrag | `contract:mandatory-assurance-v1` (1.0.0) |
| `content_hash` | `7c6ffa90eb20dad72bf72ad254102b6fa9206751962cc0b0d8774af8cb1fc7e2` |

Der `content_hash` läuft über das Manifest ohne das Hash-Feld selbst — er ist an Ort und Stelle nachrechenbar, ohne Zusatzdatei.

Das Manifest wird **nicht hier gepflegt**, sondern aus der privaten Kompositionsquelle projiziert (`tools/export_from_source.py`). Der Banner dagegen entsteht in diesem Repo, aus `assets/design/` heraus: `python tools/generate_banner.py ellmos-working-memory-bundle`. `--check` statt Schreiben meldet Abweichung.

---

*Teil der Banner- und Seitenserie über alle 13 Bundles — [Übersicht](README.md). Bildsprache und Regeln der Serie: [`assets/design/README.md`](../../assets/design/README.md).*
