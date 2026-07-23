# 🎵 Multi-DAW Track Namer - App Starter

## 🚀 Schnellstart

**Doppelklicken Sie auf:** `START_APP.sh`

Die App startet automatisch und öffnet sich im Browser auf:
**http://127.0.0.1:5003**

## 🎯 Funktionen

### ✅ **Pro Tools Support**
- ⚡ Schnelle Spur-Erstellung mit Shortcut
- 🏷️ Automatische Namensgebung mit Underscore-Format
- 📝 Beispiel: `1_Solo_Clarinet_1_KM_184`

### ✅ **Reaper Support** 
- ⚡ Blitzschnelle Spur-Erstellung mit Cmd+T
- 🏷️ Automatische Namensgebung mit Leerzeichen-Format
- 📝 Beispiel: `1 Solo Clarinet 1 KM 184`

### ✅ **Optimierungen**
- 🚀 **20x schneller** bei der Spur-Erstellung 
- ⚡ **4x schneller** bei der Namenseingabe
- 🎛️ **Flexible Auswahl:** Kanal, Instrument, Mikrofon getrennt wählbar

## 📋 Workflow

1. **Excel-Datei hochladen** mit Spalten:
   - Kanal (A), Instrument (B), Mikrofon (C)

2. **Spuren auswählen** in der Web-Oberfläche

3. **DAW wählen:**
   - **Pro Tools:** Underscore-getrennte Namen
   - **Reaper:** Leerzeichen-getrennte Namen

4. **Spuren erstellen** (Cmd+T für Reaper)

5. **Spuren benennen** (automatisch mit Ihren Einstellungen)

## 🛠️ Technische Details

- **Python Flask** Web-App
- **pynput** für Keyboard-Automation  
- **openpyxl** für Excel-Verarbeitung
- **macOS kompatibel** mit nativen Shortcuts
- **Port 5003** (automatisch geöffnet)

## ⚠️ Systemanforderungen

- macOS mit Python 3
- Virtual Environment (wird automatisch aktiviert)
- Excel-Dateien im .xlsx Format

## 🔧 Bei Problemen

**App neustarten:**
```bash
./App/START_APP.sh
```

**Dependencies installieren:**
```bash
source venv/bin/activate
pip install flask openpyxl pynput
```

**Manuelle Ausführung:**
```bash
cd "/Users/carsten/Nextcloud Carsten/GitHub/DAW-Kaanalbenennung-master"
source venv/bin/activate
python tracknamer_web_reaper.py
```

## 🎼 Erstellt für professionelle Orchesteraufnahmen

**121 Spuren in unter einer Minute!** 🚀