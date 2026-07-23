# 🍎 macOS App Bundle erstellen

## Voraussetzungen auf macOS:
```bash
# Python installieren (falls nicht vorhanden)
brew install python

# Abhängigkeiten installieren
pip install pyinstaller openpyxl pynput
```

## Build-Prozess:

### Option 1: Automatisches Build-Skript
```bash
# Repository klonen/herunterladen
git clone https://github.com/ckuemmel/DAW-Kaanalbenennung.git
cd DAW-Kaanalbenennung

# Build-Skript ausführen (erkennt automatisch macOS)
python build.py
```

### Option 2: Manueller Build
```bash
# PyInstaller direkt ausführen
pyinstaller --onefile --windowed \
    --name "ProTools TrackNamer" \
    --icon icon.icns \
    --add-data "Data:Data" \
    protools_gui.py
```

## Ergebnis:
- **App Bundle**: `dist/ProTools TrackNamer.app` 
- **Doppelklick** zum Starten
- **Keine Terminal-Fenster**
- **Native macOS App**

## Wichtige Unterschiede zu Windows:
- **Tastenkombination**: `Cmd+Shift+N` statt `Ctrl+Shift+N` für New Track Dialog
- **Modifier-Tasten**: `Cmd` statt `Ctrl` für Shortcuts
- **App Bundle**: `.app` Ordner statt `.exe` Datei

## Installation auf macOS:
1. `ProTools TrackNamer.app` nach `/Applications` kopieren
2. Bei erster Ausführung: **Rechtsklick → Öffnen** (Gatekeeper umgehen)
3. **Accessibility Permissions** erlauben für Tastatur-Automation

## Code-Anpassungen für macOS:
Das System erkennt automatisch macOS und verwendet:
- `Key.cmd` statt `Key.ctrl`
- `Cmd+Shift+N` für New Track Dialog
- Native macOS Keyboard Handling

## Test auf macOS:
1. Excel-Datei laden ✅
2. F8 drücken → `Cmd+Shift+N` → "42" → Enter ✅  
3. F9 drücken → Automatische Namen ✅

## Troubleshooting:
- **"Cannot be opened"**: System Preferences → Security → Allow App
- **Keyboard not working**: System Preferences → Privacy → Accessibility → Add App
- **Import errors**: `pip install --upgrade pyinstaller openpyxl pynput`