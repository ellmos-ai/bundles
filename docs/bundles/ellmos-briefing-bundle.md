# Briefing Bundle

![Briefing Bundle — Hafen (UAS-Säule)](../../assets/banners/ellmos-briefing-bundle.svg)

> Eine Person auf ein Gespräch, einen Termin oder eine Entscheidung vorbereiten.

| | |
|---|---|
| **Bundle-ID** | `ellmos-briefing-bundle` |
| **Säule** | `uas` — bedient die Person direkt |
| **Klasse** | `domain` — funktional, zählt in der Deployment-Auflösung |
| **Version** | 1.0.0 |
| **Status / Lifecycle** | `registered` / `draft` |
| **Sichtbarkeit** | `private` (bis eine Welle freigegeben ist) |
| **Komponenten** | 1 — empfohlen |
| **Ring** | Ring 2 der Erstprojektion |

## Wofür dieses Bundle da ist

Das kleinste Bundle der Projektion: eine Komponente, ein Zweck. Es ist trotzdem eines — weil ein Bundle eine **Rolle im Zusammenspiel** benennt, nicht eine Mindestmenge an Zutaten. Die Rolle „jemanden vorbereiten“ ist eine eigene, auch wenn heute genau ein Dienst sie füllt.

Der Skill verlangt `approved-source-set` und liefert ein `research-dossier`. Beides zusammen ist die ganze Aussage: Ein Briefing entsteht aus einem freigegebenen Quellensatz — nicht aus allem, was auffindbar ist.

## Das Bild: Hafen

Der Hafen ist die UAS-Säule — der Ort, an dem Mensch und System aneinander andocken. Am Kai hängen **verschiedene Netze**: jeder Dienst ein eigenes, für seinen eigenen Fang gebaut. Und was darin liegt, sind **verschiedene Fischarten** — die Endprodukte, so wie man sie bekommt: aufbereitet und verwertbar, nicht Rohdaten. Ein Netz hält den Fang, auf den das Licht fällt; die anderen hängen daneben, bereit.

Ein einzelnes Netz am Kai, für einen einzigen, genau bestimmten Fang.

## Komponenten

Ein Skill.

| Rolle | Komponente | Version | Bedarf | liefert | braucht |
|---|---|---|---|---|---|
| Recherche-Briefing | `skill:dossier-briefing` | `registry-current` | empfohlen | `research-dossier` | `approved-source-set` |

**Profile:** `full` und `operator`, beide ohne Ein- oder Ausschlüsse. Bei einer einzigen Komponente könnten sie auch gar nichts anderes tun.

## Ampel

Der Rollout ist inkrementell: Ein Bundle geht grün, wenn **jede** seiner Komponenten öffentlich und geprüft ist. Genau das ist das Aufnahmekriterium dieses Repos — die 13 projizierten Bundles sind die, deren Komponenten heute vollständig öffentlich sind, optionale eingeschlossen. Dieses Bundle ist damit **grün-fähig**.

Grün-fähig heißt nicht veröffentlicht. Die Freigabe einer Welle ist eine ausdrückliche Entscheidung des Eigentümers (`PRIVATE.txt`), und keine Automatik nimmt sie vorweg.

## Herkunft und Prüfbarkeit

| | |
|---|---|
| Manifest | [`manifests/bundles/ellmos-briefing-bundle/bundle.v1.json`](../../manifests/bundles/ellmos-briefing-bundle/bundle.v1.json) |
| Katalog-Eintrag | [`manifests/bundles.catalog.v1.json`](../../manifests/bundles.catalog.v1.json) |
| Funktionsvertrag | [`contracts/bundle-family-contract.v1.json`](../../contracts/bundle-family-contract.v1.json) |
| Zusicherungsvertrag | `contract:mandatory-assurance-v1` (1.0.0) |
| `content_hash` | `f7d3aee4c4c18b35a38976fd34de4a7bd10efeb93b5a34ce28a6097dd03ba518` |

Der `content_hash` läuft über das Manifest ohne das Hash-Feld selbst — er ist an Ort und Stelle nachrechenbar, ohne Zusatzdatei.

Das Manifest wird **nicht hier gepflegt**, sondern aus der privaten Kompositionsquelle projiziert (`tools/export_from_source.py`). Der Banner dagegen entsteht in diesem Repo, aus `assets/design/` heraus: `python tools/generate_banner.py ellmos-briefing-bundle`. `--check` statt Schreiben meldet Abweichung.

---

*Teil der Banner- und Seitenserie über alle 13 Bundles — [Übersicht](README.md). Bildsprache und Regeln der Serie: [`assets/design/README.md`](../../assets/design/README.md).*
