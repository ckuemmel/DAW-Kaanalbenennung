**Pro Tools Spur-Namen aus Excel/CSV importieren (Python)**
- Script: `protools_tracknamer.py`

Dieses kleine Tool liest Spur-Namen aus einer Excel- (`.xlsx`) oder CSV-Datei (erste Spalte) und tippt sie per Hotkey (F8) in den aktiven Pro Tools-Umbenennen-Dialog. So kannst du sehr schnell viele Spuren benennen, ohne eine offizielle Pro Tools-API zu brauchen.

**Voraussetzungen**
- Windows, Pro Tools geöffnet
- Python 3.10+ installiert (über `python --version` prüfen)
- Paket `pynput` (für Hotkeys/Tastatureingaben)
- Optional für `.xlsx`: `openpyxl`

Installation der Pakete:
- `pip install -r requirements.txt`

**Datei vorbereiten**
- CSV: Speichere deine Excel als `.csv` (UTF-8). Erste Spalte = Spur-Namen.
- XLSX: Belasse `.xlsx`; erste Spalte = Spur-Namen. Optional: erste Zeile als Überschrift.

Beispiel-CSV findest du in `beispiel_namen.csv`.

**Verwendung**
- Tracks in Pro Tools anlegen und in gewünschter Reihenfolge sortieren.
- Doppelklicke die erste Spurbezeichnung, sodass der Name-Dialog aktiv ist.
- Starte das Script aus diesem Ordner:
  - `python protools_tracknamer.py beispiel_namen.csv --enter`
  - oder mit Excel-Datei: `python protools_tracknamer.py namen.xlsx --skip-header --enter`

Wichtige Optionen:
- `--spalte N`  Nullbasierter Spaltenindex (0 = erste Spalte)
- `--spaltenname "instrument"`  Spalte per Überschrift auswählen (überschreibt `--spalte`)
- `--blatt "Tabelle1"`  Tabellenblatt wählen (case-insensitive; Standard = aktives Blatt)
- `--blatt-index N`  Tabellenblatt per Index (0 = erstes Blatt). Wird ignoriert, wenn `--blatt` gesetzt ist.
- `--header-row N`  Headerzeile (1-basiert) festlegen, wenn Überschriften nicht in Zeile 1 stehen (z. B. bei zusammengeführten Zellen in Zeile 6/7).
- `--skip-header`  Überschrift in der ersten Zeile überspringen (nur relevant ohne `--spaltenname`)
- `--delay 0.05`  Verzögerung vor dem Tippen (Sekunden)
- `--enter`  Nach dem Tippen automatisch Enter drücken (nicht mit `--auto-next` kombinieren)
- `--check`  Erkennung testen (Blatt, Header, Spalte, Vorschau) – keine Eingaben senden
- `--preview N`  Anzahl der Einträge, die in `--check` angezeigt werden (Standard 10)
- `--auto-next windows|mac`  Nach dem Tippen zur nächsten Spur wechseln (Windows: Ctrl+Right, macOS: Cmd+Right). Nicht zusammen mit `--enter` verwenden.
- `--auto-run`  Automatisch alle Namen in Folge übertragen (Start mit F8). Am besten mit `--auto-next` nutzen.
- `--next-delay 0.05`  Wartezeit vor dem Spurwechsel (wenn `--auto-next` aktiv ist)

Hotkeys während der Laufzeit:
- F8  Nächsten Namen tippen (in den aktiven Dialog)
- F7  Einen Namen zurückspringen
- F9  Pause ein/aus
- ESC Programm beenden

Hinweise:
- Das Tippen erfolgt in das aktuell aktive Fenster. Halte daher den Pro Tools-Umbenennen-Dialog im Vordergrund.
- Wenn F8 keine Wirkung zeigt, prüfe, ob das Terminal den Fokus hat; das Script braucht den Fokus NICHT, aber Pro Tools muss aktiv sein.
- In seltenen Fällen verlangt Windows Admin-Rechte für globale Hotkeys. Falls nichts reagiert: Terminal „Als Administrator ausführen“.

**Troubleshooting**
- "pynput nicht installiert": `pip install pynput`
- "openpyxl" fehlt bei `.xlsx`: `pip install openpyxl` oder Datei als CSV speichern und `.csv` verwenden.
- Umlaute/UTF-8: Bei CSV am besten UTF-8 speichern; das Script nutzt `utf-8-sig`.

Viel Erfolg beim Lernen und Automatisieren!
