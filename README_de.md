# bundles

Die Rezept-Schicht des ellmos-Ökosystems: Bundle-Manifeste, Kataloge und Kompositionswissen.

*[English](README.md)*

> **Privater Aufbau.** Dieses Repository öffnet sich **Welle für Welle**, nicht auf einen Schlag.
> Die Bedingungen dafür stehen geschrieben und sind prüfbar — siehe
> *[Freigabebedingungen](#freigabebedingungen)*.

---

## Zuerst lesen: was ein Bundle ist und was nicht

**Ein Bundle ist ein Rezept, kein Programm.** Diese Dateien beschreiben, welche Komponenten eine
arbeitsfähige Einheit bilden, welche Rolle jede füllt, was sie bereitstellt und verbraucht und
welche Alternativen abgewogen wurden. Sie sind maschinenlesbar, man kann mit ihnen rechnen — aber
hier startet nichts.

Einen Installer gibt es noch nicht und eine eigene Laufzeit auch nicht; ein Rezept wird deshalb
von einem Agenten-CLI ausgeführt, das Sie ohnehin betreiben. Das Vollsystem, das diese Rezepte
einmal konsumieren wird, entsteht in einem eigenen Repository: **open-ocean**. Die Trennung ist
Absicht — die Rezepte sind Monate vor dem System fertig, und ein Repository, das Rezepte unter dem
Namen des Systems ausliefert, verspräche etwas, das es noch nicht gibt.

## Warum ein Rezept überhaupt veröffentlichenswert ist

Ein Bundle-Manifest ist ein **Rezept = Seed + Zutatenliste**.

Die Zutatenliste ist die leichte Hälfte. Jedes Bundle löst sich vollständig in eine flache Liste
aus Repositories, Skills und Agentenrollen auf — und jedes davon ist einzeln öffentlich und
auffindbar.

Der **Seed** ist die Hälfte, die sich nicht auflöst: welche Teile zusammengehören, welche Rolle
jedes füllt, welche Alternative unter welchen Kriterien gewählt wurde, in welcher Reihenfolge
gebaut wird. Dieses Wissen lässt sich aus der Zutatenliste nicht rekonstruieren. **Wer alle Module
hat, hat damit noch nicht das System** — und genau deshalb sind die Rezepte das Interessante an
dieser Veröffentlichung und kein Beiwerk.

## Was heute darin liegt

13 Bundles in zwei Ringen. Von jedem einzelnen ist jede Komponente heute öffentlich verfügbar,
auch die optionalen — das ist das Aufnahmekriterium.

**Ring 1 — der Funktionskern.** Das Minimum, das zusammen ein arbeitsfähiges System ergibt:
Gedächtnis kurz und lang, Zugang zu einem Agenten, Auswahlwissen, Wissensbeschaffung.

| Bundle | Klasse | Säule | Komponenten | Was es trägt |
|---|---|---|---|---|
| `ellmos-working-memory-bundle` | platform | memory | 5 | Sitzungszustand: was erfasst wurde, was offen ist |
| `ellmos-memory-human-context-bundle` | platform | memory | 6 | dauerhaftes Gedächtnis und Nutzermodell |
| `ellmos-agents-bundle` | platform | control | 7 | Zugang zur Laufzeit — der Ersatz für eine eigene |
| `ellmos-coordination-choice-bundle` | choice | control | 2 | Auswahlwissen: der sichtbare Beweis, dass ein Rezept mehr ist als eine Liste |
| `ellmos-knowledge-bundle` | platform | — | 8 | Wissen finden und aufbereiten |

**Ring 2 — Breite ohne Zusatzrisiko.** Ebenso sauber und ab Tag 1 nützlich.

| Bundle | Klasse | Säule | Komponenten |
|---|---|---|---|
| `ellmos-doc-handler-bundle` | domain | domain | 11 |
| `ellmos-media-production-bundle` | domain | — | 7 |
| `ellmos-daily-life-bundle` | domain | uas | 6 |
| `ellmos-voice-media-assist-bundle` | domain | uas | 3 |
| `ellmos-health-assist-bundle` | domain | uas | 2 |
| `ellmos-briefing-bundle` | domain | uas | 1 |
| `ellmos-finance-assist-bundle` | domain | uas | 1 |
| `ellmos-knowledge-search-choice-bundle` | choice | — | 1 |

Zusammen 60 Komponenten-Belegungen. `manifests/bundles.catalog.v1.json` ist das Register.

**Was bewusst fehlt:** Bundles, deren Komponenten noch nicht alle öffentlich sind. Ein Rezept, dem
man die Alternativen wegkürzt, damit es publizierbar wird, verliert genau den Seed, der es
wertvoll macht — solche warten lieber, statt beschnitten zu erscheinen.

## Wie man ein Manifest liest

| Feld | Was es sagt |
|---|---|
| `components[]` | die Zutatenliste: Module, Skills, Zugangsflächen, Software-Apps |
| `requirement` | `required`, `recommended` oder `optional` — was ein Deployment weglassen darf |
| `provides` / `consumes` | welche Fähigkeit eine Komponente mitbringt und welche sie braucht; das macht aus der Liste einen Graphen statt eines Haufens |
| `role` | wofür eine Komponente hier da ist — nicht dasselbe wie das, was sie ist |
| `choice_groups` | Alternativen für eine Rolle samt Auswahlkriterien; die Kardinalität gehört den Kompositionsregeln, nicht dem Bundle |
| `pillar` | die Familie: memory hält Zustand, control steuert ihn, uas bedient die Person, domain trägt Fachlichkeit |
| `class` | `platform`, `domain` und `hosted-private` sind funktional; `choice` ist ein Auswahlregister; `synthetic` expandiert auf seine Mitglieder |
| `content_hash` | über das Manifest ohne dieses Feld — dadurch an Ort und Stelle prüfbar |

## Status: die Ampel

Der Rollout ist inkrementell, kein Big Bang. Ein Bundle geht grün, wenn jede seiner Komponenten
öffentlich und geprüft ist.

| | |
|---|---|
| Bundles grün-fähig | **13** |
| Blockiert durch nicht-öffentliche Komponenten | 17 weitere Bundles |
| Größter Einzelhebel | vier private Repositories blockieren zusammen sieben Bundles |

Ob diese vier öffentlich werden, entscheidet der Eigentümer des Ökosystems; kein automatischer
Prozess nimmt das vorweg.

## Freigabebedingungen

Dieses Repository trägt ein bedingtes Publikations-Gate (`PRIVATE.txt`, bewusst committet, damit
das Gate dort sichtbar ist, wo Sichtbarkeit geschaltet wird). Eine Welle wird freigegeben, wenn
alle drei Bedingungen erfüllt sind:

1. **Branding-Paket fertig** — Repo-Schnitt, Banner, Auftritt der Bundles auf dem
   Organisationsprofil.
2. **Publikationsprüfung bestanden** — Recht, Privacy und Lizenz für die Welle geprüft, keine
   Blocker.
3. **User-Klick für diese Welle** — jede Welle wird einzeln freigegeben; eine gelungene Welle sagt
   nichts über die nächste.

## Wie diese Dateien hierher kommen

Die Rezepte werden nicht hier gepflegt. Sie werden aus einem privaten Kompositions-Repository
**projiziert**, durch `tools/export_from_source.py`; und was dabei entfernt oder umgeschrieben
wird, steht als Daten in einem Export-Vertrag statt versteckt im Skript:

- Hostnamen, interne Pfade und nicht auflösbare interne Kennungen werden entfernt oder neutralisiert
- Komponenten mit Betriebsdaten einer realen Organisation werden ausgeschlossen — die Quelle
  behält sie, diese Projektion nicht
- das private Quell-Repository wird nirgends benannt

Zwei Eigenschaften machen das Ergebnis prüfbar statt bloß behauptet:

- **Reproduzierbar.** Zweimal gegen denselben Quellstand ausgeführt, erzeugt der zweite Lauf
  keinen Unterschied. `--check` meldet Drift, statt zu schreiben.
- **Verifizierbar.** Jedes Manifest trägt einen `content_hash` über seine exportierte Fassung, und
  `manifests/export-receipt.v1.json` hält fest, aus welchem Quellstand jede Datei stammt. Ein
  Hash, der zum unexportierten Original gehört, ließe eine ehrliche Datei manipuliert aussehen —
  deshalb setzt der Export die Pins neu.

```bash
python tools/export_from_source.py --source <pfad-zur-quelle> --check
```

## Banner & Seiten

**Status: Pilot.** Ein Bundle — `ellmos-daily-life-bundle` — hat einen Banner und eine Seite,
als Designprobe. Palette, Szene und Seitenaufbau gehen erst zur Abnahme, bevor die übrigen
folgen; was heute existiert, ist also mit Absicht eins von dreizehn und nicht dreizehn von
dreizehn.

Die Bildsprache kommt aus dem Wasser-Lexikon des Ökosystems: Jede der vier Säulen ist ein
Gewässer mit eigenem Licht und eigenem Symbol — der Hafen für `uas`, wo verschiedene Netze
verschiedenen Fisch fangen. `assets/design/README.md` hält die Regeln der Serie fest;
`assets/design/tokens.json` ist der eine Ort, an dem eine Farbe entschieden wird.

| | |
|---|---|
| Banner | [`assets/banners/ellmos-daily-life-bundle.svg`](assets/banners/ellmos-daily-life-bundle.svg) |
| Seite | [`docs/bundles/ellmos-daily-life-bundle.md`](docs/bundles/ellmos-daily-life-bundle.md) |
| Lokale Vorschau | [`docs/preview/ellmos-daily-life-bundle.html`](docs/preview/ellmos-daily-life-bundle.html) |

```bash
python tools/generate_banner.py ellmos-daily-life-bundle          # Titel und Säule aus dem Manifest
python tools/generate_banner.py ellmos-daily-life-bundle --check  # Drift melden statt schreiben
```

Banner werden hier gezeichnet statt aus der Quelle projiziert — und sind auf dieselbe Weise
reproduzierbar wie die Manifeste: keine Zeitstempel, keine zufällige Platzierung, zweimal
ausgeführt erzeugt der zweite Lauf keinen Unterschied. Jeder Banner ist in sich geschlossenes
SVG: keine externen Schriften, keine Rastergrafiken, keine Netzverweise.

## Lizenz

Noch nicht entschieden. Sie ist Teil der Publikationsprüfung und wird vor der ersten Welle
geklärt.
