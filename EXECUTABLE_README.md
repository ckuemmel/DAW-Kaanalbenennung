# Sequoia TrackNamer GUI - Ausführbare Version

## 🎉 Erfolgreich erstellt!

**Datei:** `dist/Sequoia_TrackNamer_GUI.exe`  
**Größe:** ~34 MB  
**Erstellt:** 15.09.2025 17:19

## ✨ Funktionen

- ✅ **Excel-Import**: Lädt Excel-Dateien ab Zeile 6 (Header)
- ✅ **Intelligente Filterung**: Nur Daten bis zum letzten Eintrag in Spalte D (Instrument)
- ✅ **Mehrfachauswahl**: Zeilen mit Maus auswählen (Strg/Shift)
- ✅ **Synchronisierte Checkboxen**: Ein Klick schaltet alle selektierten Zeilen um
- ✅ **Bulk-Operationen**: Buttons für schnelle Massenbearbeitung
- ✅ **Spalten-Auswahl**: Bestimme welche Spalten für Namensbildung verwendet werden
- ✅ **Live-Info**: Zeigt aktuelle Auswahl und Export-Status an
- ✅ **Sequoia-Export**: Erstellt Textdatei im korrekten Sequoia-Format

## 🚀 Verwendung

1. **Doppelklick auf** `Sequoia_TrackNamer_GUI.exe`
2. **Excel laden**: Klicke auf "Excel laden" und wähle deine Datei
3. **Zeilen auswählen**: 
   - Einzeln: Klicke auf Zeilen
   - Mehrfach: Strg + Klick oder Shift + Klick für Bereiche
4. **Export-Status setzen**:
   - Checkbox in Export-Spalte: Einzelne Zeile umschalten
   - Bei Mehrfachauswahl: Alle selektierten Zeilen werden synchron umgeschaltet
   - Bulk-Buttons: "✓ Export AN", "✗ Export AUS", "↕ Export umkehren"
5. **Spalten wählen**: Bestimme welche Spalten für Namen verwendet werden
6. **Speichern**: Wähle Zielort und exportiere

## 📋 Arbeitsweise

### Excel-Import:
- **Header**: Automatisch ab Zeile 6
- **Spalten**: B (Kanal), D (Instrument), E (Mikrofon) werden angezeigt
- **Filter**: Nur bis zur letzten Zeile mit Instrument-Eintrag
- **Standard-Auswahl**: Zeilen mit Instrument-Daten sind vorausgewählt

### Mehrfachauswahl:
- **Normale Auswahl**: Klick auf Zeile (außer Export-Spalte)
- **Erweitern**: Strg + Klick für einzelne Zeilen hinzufügen
- **Bereich**: Shift + Klick für Bereich auswählen
- **Synchronisation**: Checkbox-Klick bei Mehrfachauswahl schaltet alle um

### Export:
- **Format**: Sequoia Track List mit Header
- **Namen**: Aus gewählten Spalten mit Unterstrich verbunden
- **Nummerierung**: Automatische Spur-Nummerierung
- **Master-Track**: Wird automatisch als letzte Spur hinzugefügt

## 🛠️ Technische Details

- **Python**: Kompiliert mit PyInstaller 6.16.0
- **Abhängigkeiten**: tkinter (GUI), pandas (Excel), openpyxl (Excel-Format)
- **Optimiert**: UPX-Kompression, unnötige Module ausgeschlossen
- **Kompatibilität**: Windows 10/11 (64-bit)

## 📁 Dateien

```
dist/
├── Sequoia_TrackNamer_GUI.exe    # Hauptprogramm (34 MB)
└── ProTools_TrackNamer.exe       # Alte Version (31 MB)

build_tracknamer_gui.bat          # Windows Build-Skript  
build_gui.py                      # Python Build-Skript
Sequoia_TrackNamer_GUI.spec       # PyInstaller-Konfiguration
```

## 🎯 Vorteile der .exe-Version

- ✅ **Keine Python-Installation nötig**
- ✅ **Alle Abhängigkeiten enthalten**
- ✅ **Einfache Verteilung**
- ✅ **Direkt ausführbar**
- ✅ **Professioneller Windows-Integration**

## 📝 Hinweise

- Die .exe-Datei ist **vollständig eigenständig**
- **Keine Installation erforderlich** - einfach ausführen
- Bei erstem Start eventuell kurze Ladezeit (normale Initialisierung)
- **Windows Defender** könnte nachfragen (normal bei neuen .exe-Dateien)

---

## 🎉 Fertig!

Deine **Sequoia TrackNamer GUI** ist jetzt als professionelle Windows-Anwendung verfügbar!

**Viel Erfolg beim Export deiner Tracknamen! 🎵**