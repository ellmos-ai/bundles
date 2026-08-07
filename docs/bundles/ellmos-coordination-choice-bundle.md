# Coordination Choice Bundle

![Coordination Choice Bundle — Klarwasser (CONTROL-Säule)](../../assets/banners/ellmos-coordination-choice-bundle.svg)

> Auswahlregister für einander ausschließende Koordinations- und Sperr-Anbieter. Es hält fest, warum ein Kandidat dem anderen vorgezogen wird — ausgerollt wird hier keiner.

| | |
|---|---|
| **Bundle-ID** | `ellmos-coordination-choice-bundle` |
| **Säule** | `control` — steuert das System |
| **Klasse** | `choice` — Auswahlregister, zählt **nicht** in der Deployment-Auflösung |
| **Version** | 1.0.0 |
| **Status / Lifecycle** | `registered` / `draft` |
| **Sichtbarkeit** | `private` (bis eine Welle freigegeben ist) |
| **Komponenten** | 2 — eine empfohlen, eine optional, dazu eine Choice-Gruppe |
| **Ring** | Ring 1 der Erstprojektion |

## Wofür dieses Bundle da ist

Ein Choice-Bundle ist keine Zutatenliste, sondern ein **Register einer Entscheidung**. Es zählt nicht in der Deployment-Auflösung; es beantwortet die Frage, die eine Zutatenliste nicht beantworten kann: *warum dieser und nicht jener*.

Damit ist es zugleich das sichtbarste Argument dafür, Rezepte überhaupt zu veröffentlichen. Die Zutaten sind einzeln auffindbar; das Auswahlwissen ist es nicht.

## Das Bild: Klarwasser

Das Klarwasser ist die Control-Säule, und ihr Zeichen ist das Steuerrad: ruhiges Wasser, in dem man den Kurs sieht, bevor man ihn hält. Eine Speiche ist markiert — die Königsspeiche, die traditionell anzeigt, dass das Ruder mittschiffs steht. Sie ist der einzige Akzent im Bild, weil Steuern heißt: **einen** Kurs kenntlich machen.

Ein Auswahlregister steuert nicht selbst — es hält fest, wie gesteuert werden soll. Deshalb steht das Rad hier leer am Stand: Der Kurs ist bestimmt, gefahren wird woanders.

## Komponenten

Zwei Skills, beide zur Entscheidung selbst — nicht zur Sache, über die entschieden wird.

| Rolle | Komponente | Version | Bedarf | liefert | braucht |
|---|---|---|---|---|---|
| Auswahlanalyse | `skill:decide` | `registry-current` | empfohlen | `candidate-comparison` | `choice-group-criteria` |
| Entscheidungsvorlage | `skill:decision-briefing` | `registry-current` | optional | `decision-options` | `choice-group-criteria` |

## Die Wahl: `coordination.locking`

Eine Gruppe, `pick: exactly-one`. Die Kardinalität gehört nicht dem Bundle, sondern `composition.rules.json` — das Register beschreibt die Wahl, es setzt sie nicht durch.

| Kandidat | Typ | Stellung | Stärken | Preis dafür |
|---|---|---|---|---|
| `lock-master` | Modul | **Vorauswahl** | Dateibasiert: `LOCK*.txt` im Projektordner ist die alleinige Autorität, Cache, SQLite und Web-UI sind abgeleitete Sichten. Netzgrenze `none`, Datengrenze `user-local`, läuft auf Windows, macOS und Linux. Status `active`, öffentlich. | Keine transaktionale Zusicherung — zwei gleichzeitig startende Agenten können beide einen leeren Ordner sehen. Koordination endet an der Ordnergrenze. Kein Gedächtnis über Ausgänge: Ein Lock hält einen Anspruch fest, nicht wie der Versuch ausging. |
| `roshambo` | Stack | Alternative | CockroachDB als System of Record: serialisierbare Leases statt Best-Effort-Ansprüchen. Gedächtnis über Ausgänge inklusive Fehlschläge, ausdrücklich herstellerneutral, schmaler Schreibpfad über `roshambo-mcp` mit erzwungenen Invarianten statt freiem SQL. | Braucht externe Infrastruktur, alles im Status `planned`. Nicht local-first (`local_first: false`, Netzpolitik `declared`). Reifegrad: Stack-Status `development`, für eine Wettbewerbsfrist entstanden. Datengrenze steigt auf `sensitive`. |

Die beiden sind zugleich Alternative **und** Abhängigkeit: roshambo übernimmt die Lease-Semantik von lock-master — Anspruch, Verfall, Rechte mit Vorrang `deny > ask > allow` — und verlegt nur die Ablage von `LOCK*.txt` in eine Datenbanktabelle. roshambo zu wählen verwirft lock-masters Modell also nicht, es verschiebt es.

Das Auswahlkriterium ist im Register benannt und es ist **nicht** die Funktionsliste: *Entscheide nach Reichweite.* Innerhalb eines Hosts oder eines synchronisierten Ordners genügt lock-master und ist um eine Größenordnung billiger; über Hersteller, Maschinen und Sitzungen hinweg kann eine Datei die Zusicherung nicht tragen, und roshambo wird die ehrliche Antwort.

Offen und als offen vermerkt: **Keiner der beiden Kandidaten ist derzeit in einem registrierten Stack dieser Rolle zugewiesen.** Die Gruppe hält den beabsichtigten Entscheidungsraum fest, nicht ein beobachtetes Deployment.

Drei Profile statt der üblichen zwei, und hier tun sie etwas: `full` (ohne Festlegung), `file-based-coordination` (Override auf `lock-master`) und `database-backed-coordination` (Override auf `roshambo`). Genau dort lebt eine getroffene Auswahl — im Profil, nicht im Register.

## Ampel

Der Rollout ist inkrementell: Ein Bundle geht grün, wenn **jede** seiner Komponenten öffentlich und geprüft ist. Genau das ist das Aufnahmekriterium dieses Repos — die 13 projizierten Bundles sind die, deren Komponenten heute vollständig öffentlich sind, optionale eingeschlossen. Dieses Bundle ist damit **grün-fähig**.

Grün-fähig heißt nicht veröffentlicht. Die Freigabe einer Welle ist eine ausdrückliche Entscheidung des Eigentümers (`PRIVATE.txt`), und keine Automatik nimmt sie vorweg.

## Herkunft und Prüfbarkeit

| | |
|---|---|
| Manifest | [`manifests/bundles/ellmos-coordination-choice-bundle/bundle.v1.json`](../../manifests/bundles/ellmos-coordination-choice-bundle/bundle.v1.json) |
| Katalog-Eintrag | [`manifests/bundles.catalog.v1.json`](../../manifests/bundles.catalog.v1.json) |
| Funktionsvertrag | [`contracts/choice-bundle-contract.v1.json`](../../contracts/choice-bundle-contract.v1.json) |
| Zusicherungsvertrag | `contract:mandatory-assurance-v1` (1.0.0) |
| `content_hash` | `4323952a7c04b8e4f4a935bf5f36c4cfec9a5220be0708a4c1549698489a8ed4` |

Der `content_hash` läuft über das Manifest ohne das Hash-Feld selbst — er ist an Ort und Stelle nachrechenbar, ohne Zusatzdatei.

Das Manifest wird **nicht hier gepflegt**, sondern aus der privaten Kompositionsquelle projiziert (`tools/export_from_source.py`). Der Banner dagegen entsteht in diesem Repo, aus `assets/design/` heraus: `python tools/generate_banner.py ellmos-coordination-choice-bundle`. `--check` statt Schreiben meldet Abweichung.

---

*Teil der Banner- und Seitenserie über alle 13 Bundles — [Übersicht](README.md). Bildsprache und Regeln der Serie: [`assets/design/README.md`](../../assets/design/README.md).*
