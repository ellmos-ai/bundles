# Voice and Media Assist Bundle

![Voice and Media Assist Bundle — Hafen (UAS-Säule)](../../assets/banners/ellmos-voice-media-assist-bundle.svg)

> Sprechen und Hören statt Tippen, dazu das persönliche Medienregal.

| | |
|---|---|
| **Bundle-ID** | `ellmos-voice-media-assist-bundle` |
| **Säule** | `uas` — bedient die Person direkt |
| **Klasse** | `domain` — funktional, zählt in der Deployment-Auflösung |
| **Version** | 1.0.0 |
| **Status / Lifecycle** | `registered` / `draft` |
| **Sichtbarkeit** | `private` (bis eine Welle freigegeben ist) |
| **Komponenten** | 3 — zwei empfohlen, eine optional |
| **Ring** | Ring 2 der Erstprojektion |

## Wofür dieses Bundle da ist

Ein UAS-Bundle im Wortsinn: Es ändert nicht, **was** das System kann, sondern **wie** eine Person daran kommt. Wer nicht tippen will oder kann, diktiert; wer nicht lesen will, hört.

Die Grenze zieht das Manifest selbst: *„Assistance, not production.“* Das [Media-Production-Bundle](ellmos-media-production-bundle.md) trägt die herstellende Seite, dieses hier hilft der Person nur beim Konsumieren und Diktieren.

Alle drei Komponenten verlangen eine ausdrückliche Freigabe — `approved-audio-scope`, `approved-audio-source`, `approved-media-source`. Ein Mikrofon-Dienst, der sich seinen Umfang selbst nimmt, wäre in dieser Säule ein Widerspruch in sich.

## Das Bild: Hafen

Der Hafen ist die UAS-Säule — der Ort, an dem Mensch und System aneinander andocken. Am Kai hängen **verschiedene Netze**: jeder Dienst ein eigenes, für seinen eigenen Fang gebaut. Und was darin liegt, sind **verschiedene Fischarten** — die Endprodukte, so wie man sie bekommt: aufbereitet und verwertbar, nicht Rohdaten. Ein Netz hält den Fang, auf den das Licht fällt; die anderen hängen daneben, bereit.

Sprache ist hier ein Netz wie jedes andere: eines, das seinen eigenen Fang holt.

## Komponenten

Drei Skills, keine Module.

| Rolle | Komponente | Version | Bedarf | liefert | braucht |
|---|---|---|---|---|---|
| Sprach-Ein- und -Ausgabe | `skill:voice` | `registry-current` | empfohlen | `voice-interaction-plan` | `approved-audio-scope` |
| Transkription | `skill:transkription` | `registry-current` | empfohlen | `source-backed-transcript` | `approved-audio-source` |
| Mediendurchsicht | `skill:mediabrain-reader` | `registry-current` | optional | `media-list-review` | `approved-media-source` |

`transkription` liefert denselben `source-backed-transcript` wie der `video-transcriber` der produzierenden Seite — dieselbe Zusicherung, andere Blickrichtung.

**Profile:** `full` und `operator`, beide ohne Ein- oder Ausschlüsse.

## Ampel

Der Rollout ist inkrementell: Ein Bundle geht grün, wenn **jede** seiner Komponenten öffentlich und geprüft ist. Genau das ist das Aufnahmekriterium dieses Repos — die 13 projizierten Bundles sind die, deren Komponenten heute vollständig öffentlich sind, optionale eingeschlossen. Dieses Bundle ist damit **grün-fähig**.

Grün-fähig heißt nicht veröffentlicht. Die Freigabe einer Welle ist eine ausdrückliche Entscheidung des Eigentümers (`PRIVATE.txt`), und keine Automatik nimmt sie vorweg.

## Herkunft und Prüfbarkeit

| | |
|---|---|
| Manifest | [`manifests/bundles/ellmos-voice-media-assist-bundle/bundle.v1.json`](../../manifests/bundles/ellmos-voice-media-assist-bundle/bundle.v1.json) |
| Katalog-Eintrag | [`manifests/bundles.catalog.v1.json`](../../manifests/bundles.catalog.v1.json) |
| Funktionsvertrag | [`contracts/bundle-family-contract.v1.json`](../../contracts/bundle-family-contract.v1.json) |
| Zusicherungsvertrag | `contract:mandatory-assurance-v1` (1.0.0) |
| `content_hash` | `520f794c4bc77ffaee7b05efe90b2ec90dae18c76074941b40f11a7ca169558e` |

Der `content_hash` läuft über das Manifest ohne das Hash-Feld selbst — er ist an Ort und Stelle nachrechenbar, ohne Zusatzdatei.

Das Manifest wird **nicht hier gepflegt**, sondern aus der privaten Kompositionsquelle projiziert (`tools/export_from_source.py`). Der Banner dagegen entsteht in diesem Repo, aus `assets/design/` heraus: `python tools/generate_banner.py ellmos-voice-media-assist-bundle`. `--check` statt Schreiben meldet Abweichung.

---

*Teil der Banner- und Seitenserie über alle 13 Bundles — [Übersicht](README.md). Bildsprache und Regeln der Serie: [`assets/design/README.md`](../../assets/design/README.md).*
