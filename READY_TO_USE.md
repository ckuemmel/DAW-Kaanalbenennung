# 🎵 Pro Tools Track Namer - Standalone Executable

**Fertig zum Verwenden! Keine Python-Installation nötig!**

## 🚀 Sofort starten (Windows):

1. **Einfach doppelklicken:** `dist\ProTools_TrackNamer.exe`
2. **Fertig!** Das Programm startet ohne weitere Installation

## 📦 Was wurde erstellt:

- ✅ **Standalone Executable**: `dist\ProTools_TrackNamer.exe` (ca. 45MB)
- ✅ **Alle Abhängigkeiten eingebaut**: Python, Tkinter, OpenPyXL, PyNput
- ✅ **Kein Python nötig**: Läuft auf jedem Windows-PC
- ✅ **Portabel**: Einfach kopieren und ausführen

## 🔧 Für macOS erstellen:

```bash
# Auf einem Mac ausführen:
chmod +x build_macos.sh
./build_macos.sh

# Ergebnis: dist/ProTools TrackNamer.app
```

## 🎯 Verwendung:

1. **Pro Tools TrackNamer.exe starten**
2. **Excel-Datei auswählen** (Spalte B=Kanäle, D=Instrumente, E=Mikrofone)
3. **Pro Tools öffnen** (Mix-Fenster aktiv)
4. **"Spuren erstellen"** klicken → F8 für jede Spur
5. **"Spuren benennen"** klicken → F9 benennt alle Spuren

## ✅ Fertige Funktionen:

- 🎯 **Automatische Spurenerstellung** via F8
- 🏷️ **Intelligente Spurenbenennung** via F9  
- 📊 **Excel-Integration** (xlsx/xls Dateien)
- 🖱️ **GUI mit Threading** (keine Blockierung)
- ⚙️ **Robuste Fehlerbehandlung**
- 🔄 **Abbruch-Funktion** (ESC-Taste)

## 📋 Name-Format:

**Excel-Struktur:**
- Spalte B: `1, 2, 3, ...` (Kanalnummern)  
- Spalte D: `A, FL, Ob, ...` (Instrumente)
- Spalte E: `sE 8 Carsten, KM 184, ...` (Mikrofone)

**Ergebnis:** `"1_A_sE 8 Carsten"`, `"2_FL_KM 184"`, etc.

## 🎉 Status: **FERTIG!**

Das Programm ist vollständig funktionstüchtig und bereit für den Einsatz in Pro Tools Studios!