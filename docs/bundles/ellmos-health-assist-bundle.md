# Health Assist Bundle

![Health Assist Bundle — Hafen (UAS-Säule)](../../assets/banners/ellmos-health-assist-bundle.svg)

> Gesundheitliches organisieren: Termine, Dokumente, Medikation, Unterlagen.

| | |
|---|---|
| **Bundle-ID** | `ellmos-health-assist-bundle` |
| **Säule** | `uas` — bedient die Person direkt |
| **Klasse** | `domain` — funktional, zählt in der Deployment-Auflösung |
| **Version** | 1.0.0 |
| **Status / Lifecycle** | `registered` / `draft` |
| **Sichtbarkeit** | `private` (bis eine Welle freigegeben ist) |
| **Komponenten** | 2 — beide empfohlen |
| **Ring** | Ring 2 der Erstprojektion |

## Wofür dieses Bundle da ist

Zwei Komponenten, eine sehr scharfe Grenze. Das Manifest sagt sie in einem Satz: **Organisation only.** Therapeutische und diagnostische Sachfragen sind eine Domain-Frage und hier ausdrücklich nicht abgedeckt.

Diese Trennung ist der eigentliche Inhalt des Bundles. Ein Werkzeug, das Termine ordnet und Unterlagen sortiert, ist etwas grundlegend anderes als eines, das mitredet, was zu tun ist — und die Zuordnung zur UAS-Säule steht und fällt damit, dass es beim Ersten bleibt.

Beide Komponenten verlangen `explicit-user-scope`. In dieser Säule ist das die stärkste verfügbare Bedingung: nicht freigegebener Kontext im Allgemeinen, sondern ein von der Person ausdrücklich aufgespannter Rahmen.

## Das Bild: Hafen

Der Hafen ist die UAS-Säule — der Ort, an dem Mensch und System aneinander andocken. Am Kai hängen **verschiedene Netze**: jeder Dienst ein eigenes, für seinen eigenen Fang gebaut. Und was darin liegt, sind **verschiedene Fischarten** — die Endprodukte, so wie man sie bekommt: aufbereitet und verwertbar, nicht Rohdaten. Ein Netz hält den Fang, auf den das Licht fällt; die anderen hängen daneben, bereit.

Ein kleines Bundle, zwei Netze — und beide ausdrücklich nicht für den Fang, der einem Arzt gehört.

## Komponenten

Zwei Skills, keine Module.

| Rolle | Komponente | Version | Bedarf | liefert | braucht |
|---|---|---|---|---|---|
| Gesundheitsorganisation | `skill:gesundheit` | `registry-current` | empfohlen | `health-organisation-plan` | `explicit-user-scope` |
| Medizinische Daten | `skill:medizin-daten` | `registry-current` | empfohlen | `private-health-record-plan` | `explicit-user-scope` |

Beide liefern einen **Plan**, keine Bewertung: `health-organisation-plan` und `private-health-record-plan`. Auch das ist die Grenze, diesmal in der `provides`-Spalte statt in der Prosa.

**Profile:** `full` und `operator`, beide ohne Ein- oder Ausschlüsse.

## Ampel

Der Rollout ist inkrementell: Ein Bundle geht grün, wenn **jede** seiner Komponenten öffentlich und geprüft ist. Genau das ist das Aufnahmekriterium dieses Repos — die 13 projizierten Bundles sind die, deren Komponenten heute vollständig öffentlich sind, optionale eingeschlossen. Dieses Bundle ist damit **grün-fähig**.

Grün-fähig heißt nicht veröffentlicht. Die Freigabe einer Welle ist eine ausdrückliche Entscheidung des Eigentümers (`PRIVATE.txt`), und keine Automatik nimmt sie vorweg.

## Herkunft und Prüfbarkeit

| | |
|---|---|
| Manifest | [`manifests/bundles/ellmos-health-assist-bundle/bundle.v1.json`](../../manifests/bundles/ellmos-health-assist-bundle/bundle.v1.json) |
| Katalog-Eintrag | [`manifests/bundles.catalog.v1.json`](../../manifests/bundles.catalog.v1.json) |
| Funktionsvertrag | [`contracts/bundle-family-contract.v1.json`](../../contracts/bundle-family-contract.v1.json) |
| Zusicherungsvertrag | `contract:mandatory-assurance-v1` (1.0.0) |
| `content_hash` | `beadd9e51896bbe078d61adc8c3c1b8d0dbef415592c5ac2c47989fe25f43f21` |

Der `content_hash` läuft über das Manifest ohne das Hash-Feld selbst — er ist an Ort und Stelle nachrechenbar, ohne Zusatzdatei.

Das Manifest wird **nicht hier gepflegt**, sondern aus der privaten Kompositionsquelle projiziert (`tools/export_from_source.py`). Der Banner dagegen entsteht in diesem Repo, aus `assets/design/` heraus: `python tools/generate_banner.py ellmos-health-assist-bundle`. `--check` statt Schreiben meldet Abweichung.

---

*Teil der Banner- und Seitenserie über alle 13 Bundles — [Übersicht](README.md). Bildsprache und Regeln der Serie: [`assets/design/README.md`](../../assets/design/README.md).*
