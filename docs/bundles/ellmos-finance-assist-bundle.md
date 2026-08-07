# Finance Assist Bundle

![Finance Assist Bundle — Hafen (UAS-Säule)](../../assets/banners/ellmos-finance-assist-bundle.svg)

> Persönlicher Überblick über Geld und Versicherungen.

| | |
|---|---|
| **Bundle-ID** | `ellmos-finance-assist-bundle` |
| **Säule** | `uas` — bedient die Person direkt |
| **Klasse** | `domain` — funktional, zählt in der Deployment-Auflösung |
| **Version** | 1.0.0 |
| **Status / Lifecycle** | `registered` / `draft` |
| **Sichtbarkeit** | `private` (bis eine Welle freigegeben ist) |
| **Komponenten** | 1 — empfohlen |
| **Ring** | Ring 2 der Erstprojektion |

## Wofür dieses Bundle da ist

Ebenfalls eine Komponente — und ebenfalls mit einer Abgrenzung, die mehr trägt als die Zutatenliste. Das Manifest stellt dieses Bundle neben das private Büro-Bundle und unterscheidet die beiden in einem Satz: **Dieses gibt der Person einen Überblick, jenes gibt dem Fachmann ein Instrument.**

Der Unterschied ist keine Geschmacksfrage, sondern entscheidet die Säulenzuordnung. Ein Überblick für die betroffene Person gehört in den Hafen; ein steuerliches oder juristisches Werkzeug für die Berufsausübung wäre Fachgut und läge im Frachtwasser.

## Das Bild: Hafen

Der Hafen ist die UAS-Säule — der Ort, an dem Mensch und System aneinander andocken. Am Kai hängen **verschiedene Netze**: jeder Dienst ein eigenes, für seinen eigenen Fang gebaut. Und was darin liegt, sind **verschiedene Fischarten** — die Endprodukte, so wie man sie bekommt: aufbereitet und verwertbar, nicht Rohdaten. Ein Netz hält den Fang, auf den das Licht fällt; die anderen hängen daneben, bereit.

Der Fang ist hier der Überblick selbst — aufbereitet und verwertbar, nicht der Rohbestand.

## Komponenten

Ein Skill.

| Rolle | Komponente | Version | Bedarf | liefert | braucht |
|---|---|---|---|---|---|
| Finanz- und Versicherungsüberblick | `skill:finanz-versicherung` | `registry-current` | empfohlen | `insurance-overview` | `approved-private-context` |

`approved-private-context` ist die engste Freigabeform, die in der UAS-Säule vorkommt — enger als der `approved-personal-context` der Alltagsdienste.

**Profile:** `full` und `operator`, beide ohne Ein- oder Ausschlüsse.

## Ampel

Der Rollout ist inkrementell: Ein Bundle geht grün, wenn **jede** seiner Komponenten öffentlich und geprüft ist. Genau das ist das Aufnahmekriterium dieses Repos — die 13 projizierten Bundles sind die, deren Komponenten heute vollständig öffentlich sind, optionale eingeschlossen. Dieses Bundle ist damit **grün-fähig**.

Grün-fähig heißt nicht veröffentlicht. Die Freigabe einer Welle ist eine ausdrückliche Entscheidung des Eigentümers (`PRIVATE.txt`), und keine Automatik nimmt sie vorweg.

## Herkunft und Prüfbarkeit

| | |
|---|---|
| Manifest | [`manifests/bundles/ellmos-finance-assist-bundle/bundle.v1.json`](../../manifests/bundles/ellmos-finance-assist-bundle/bundle.v1.json) |
| Katalog-Eintrag | [`manifests/bundles.catalog.v1.json`](../../manifests/bundles.catalog.v1.json) |
| Funktionsvertrag | [`contracts/bundle-family-contract.v1.json`](../../contracts/bundle-family-contract.v1.json) |
| Zusicherungsvertrag | `contract:mandatory-assurance-v1` (1.0.0) |
| `content_hash` | `a7981f30dec611f1cf7fcb17ba0b2eefa239f954603bf75ea51156fa414d79c4` |

Der `content_hash` läuft über das Manifest ohne das Hash-Feld selbst — er ist an Ort und Stelle nachrechenbar, ohne Zusatzdatei.

Das Manifest wird **nicht hier gepflegt**, sondern aus der privaten Kompositionsquelle projiziert (`tools/export_from_source.py`). Der Banner dagegen entsteht in diesem Repo, aus `assets/design/` heraus: `python tools/generate_banner.py ellmos-finance-assist-bundle`. `--check` statt Schreiben meldet Abweichung.

---

*Teil der Banner- und Seitenserie über alle 13 Bundles — [Übersicht](README.md). Bildsprache und Regeln der Serie: [`assets/design/README.md`](../../assets/design/README.md).*
