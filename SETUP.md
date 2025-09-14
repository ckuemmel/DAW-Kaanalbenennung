# Pro Tools Track Namer - Setup und Verwendung

Ein Python-Tool zur automatischen Benennung von Pro Tools Spuren basierend auf Excel-Daten.

## 🚀 Schnellstart - Vorgefertigte Programme

### Windows:
1. Doppelklick auf `build_windows.bat`
2. Warten bis Build abgeschlossen
3. Programm starten: `dist\ProTools_TrackNamer.exe`

### macOS:
1. Terminal öffnen und zu diesem Ordner navigieren
2. Ausführbar machen: `chmod +x build_macos.sh`
3. Build starten: `./build_macos.sh`
4. App öffnen: `open dist/ProTools\ TrackNamer.app`

## 📋 Voraussetzungen

- **Python 3.8+** (von [python.org](https://python.org))
- **Pro Tools** (beliebige Version)
- **Excel-Datei** mit korrekter Struktur:
  - Spalte B: Kanalnummern (1, 2, 3, ...)
  - Spalte D: Instrumentennamen (A, FL, Ob, ...)
  - Spalte E: Mikrofontypen (sE 8 Carsten, KM 184, ...)

## 🛠️ Manuelle Installation (Entwickler)

```bash
# Repository klonen
git clone https://github.com/ckuemmel/DAW-Kaanalbenennung.git
cd DAW-Kaanalbenennung

# Abhängigkeiten installieren
pip install -r requirements.txt

# Programm starten
python protools_gui.py
```

## 🎯 Verwendung

1. **Excel-Datei auswählen**: Klicke "Excel-Datei auswählen" und wähle deine Instrumentenliste
2. **Pro Tools vorbereiten**: 
   - Öffne Pro Tools
   - Stelle sicher, dass der Mix-Bereich aktiv ist
3. **Spuren erstellen**: 
   - Klicke "Spuren erstellen" 
   - Das Tool drückt automatisch F8 für jede Spur
4. **Spuren benennen**:
   - Klicke "Spuren benennen"
   - Das Tool drückt automatisch F9 und benennt alle Spuren

## 📊 Excel-Struktur

Beispiel einer korrekten Excel-Tabelle:

| A | B | C | D | E |
|---|---|---|---|---|
|   | 1 |   | A | sE 8 Carsten |
|   | 2 |   | FL | KM 184 |
|   | 3 |   | Ob | KM 184 |
|   | ... | ... | ... | ... |

**Ergebnis**: Spurnamen wie "1_A_sE 8 Carsten", "2_FL_KM 184", etc.

## 🔧 Build-Optionen

### Eigene Executable erstellen:

**Automatisch:**
- Windows: `build_windows.bat` ausführen
- macOS: `./build_macos.sh` ausführen

**Manuell:**
```bash
# Abhängigkeiten installieren
pip install -r requirements.txt

# Build starten
python build.py
```

### Build-Konfiguration:

Das `build.py` Script unterstützt:
- ✅ Einzel-Datei Executable (--onefile)
- ✅ GUI ohne Konsole (--windowed)
- ✅ Custom Icon (falls vorhanden)
- ✅ Version Info (Windows)
- ✅ App Bundle (macOS)
- ✅ Automatische Abhängigkeits-Erkennung

## 📁 Projektstruktur

```
Pro Tools Track Namer/
├── protools_gui.py           # Haupt-GUI
├── protools_tracknamer.py    # Kern-Funktionalität
├── build.py                  # Build-Script
├── build_windows.bat         # Windows Build
├── build_macos.sh           # macOS Build
├── requirements.txt          # Python-Abhängigkeiten
├── beispiel_namen.csv       # Beispiel-Daten
├── icons/                   # Icon-Ressourcen
└── README.md               # Diese Datei
```

## 🐛 Problemlösung

**"PyInstaller nicht gefunden":**
```bash
pip install pyinstaller
```

**"Executable startet nicht":**
- Prüfe Antivirus-Software (False Positive möglich)
- Starte von Kommandozeile für Fehlermeldungen

**"Pro Tools reagiert nicht":**
- Stelle sicher, dass Pro Tools im Vordergrund ist
- Mix-Fenster muss aktiv sein
- F8/F9 Shortcuts müssen korrekt konfiguriert sein

**"Excel wird nicht richtig gelesen":**
- Prüfe Spaltenstruktur (B=Kanäle, D=Instrumente, E=Mikrofone)
- Stelle sicher, dass keine leeren Zeilen zwischen Daten sind

## 🔗 Links

- [Pro Tools Keyboard Shortcuts](https://www.avid.com/resource-center/pro-tools-keyboard-shortcuts)
- [Python Downloads](https://python.org)
- [PyInstaller Dokumentation](https://pyinstaller.readthedocs.io/)

## 📝 Lizenz

Dieses Projekt ist Open Source. Siehe Repository für Details.

---
*Entwickelt von Carsten Kümmel - 2025*