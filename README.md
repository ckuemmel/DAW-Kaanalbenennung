# 🎵 Pro Tools Track Namer v3.0

**Automatische Pro Tools Spuren-Erstellung und -Benennung aus Excel**

Dieses Tool automatisiert die komplette Workflow von Spurerstellung bis Benennung in Pro Tools:
- **F8**: Automatische Spurerstellung über New Track Dialog (Shift+Ctrl+N)  
- **F9**: Automatische Benennung aller Spuren aus Excel-Daten

✨ **Kein manueller Import nötig - alles automatisch!**

## 🚀 Installation

### Windows (Standalone)
1. **Download**: `ProTools_TrackNamer.exe` aus den [Releases](https://github.com/ckuemmel/DAW-Kaanalbenennung/releases)
2. **Starten**: Doppelklick - keine Installation nötig!

### macOS (Build erforderlich)  
```bash
git clone https://github.com/ckuemmel/DAW-Kaanalbenennung.git
cd DAW-Kaanalbenennung
chmod +x build_macos.sh
./build_macos.sh
```

### Python (Entwickler)
```bash
pip install -r requirements.txt
python protools_gui.py
```

## 📊 Excel-Format

**Erwartete Struktur:**
- **Spalte B**: Kanalnummern (1, 2, 3, ...)
- **Spalte D**: Instrumentennamen (A, FL, Ob, Trp, ...)  
- **Spalte E**: Mikrofontypen (sE 8, KM 184, U87, ...)

**Ergebnis-Format:** `"1_A_sE 8"`, `"21_FL_KM 184"`, etc.

## 🎯 Workflow

### 1. Spuren erstellen  
1. **Excel-Datei laden** in der GUI
2. **"Spuren erstellen"** klicken  
3. **F8 drücken** in Pro Tools
4. ➡️ **Automatisch**: Shift+Ctrl+N → Anzahl eingeben → Enter  
5. ✅ **Alle Spuren sofort erstellt!**

### 2. Spuren benennen
1. **"Spuren benennen"** klicken
2. **Erste Spur markieren** in Pro Tools
3. **F9 drücken**  
4. ➡️ **Automatisch**: Alle Namen werden gesetzt
5. ✅ **Fertig!**

## 🔧 Features

- **🚀 Cross-Platform**: Windows + macOS
- **⚡ Intelligent**: New Track Dialog statt 42x F8  
- **🎵 Smart Naming**: Kanal_Instrument_Mikrofon Format
- **🔄 Automated**: F8 → Alle Spuren, F9 → Alle Namen  
- **📦 Standalone**: Keine Python-Installation nötig
- **🛡️ Robust**: Fehlerbehandlung und Recovery

## ⌨️ Tastenkombinationen

| Taste | Funktion | Windows | macOS |
|-------|----------|---------|--------|
| **F8** | Spuren erstellen | Shift+Ctrl+N | Shift+Cmd+N |
| **F9** | Namen setzen | Automatisch | Automatisch |  
| **ESC** | Abbrechen | ✅ | ✅ |

## 🔍 Troubleshooting

**Windows:**
- **"Zugriff verweigert"**: Als Administrator ausführen
- **"Keine Reaktion"**: Pro Tools in Vordergrund bringen

**macOS:**  
- **"App kann nicht geöffnet werden"**: Rechtsklick → Öffnen
- **"Keyboard funktioniert nicht"**: System Preferences → Privacy → Accessibility

## 📝 Beispiel

**Excel Input:**
```
B    D    E
1    A    sE 8  
2    FL   KM 184
3    Ob   U87
```

**Pro Tools Output:**
```  
1_A_sE 8
2_FL_KM 184  
3_Ob_U87
```
- In seltenen Fällen verlangt Windows Admin-Rechte für globale Hotkeys. Falls nichts reagiert: Terminal „Als Administrator ausführen“.

**Troubleshooting**
- "pynput nicht installiert": `pip install pynput`
- "openpyxl" fehlt bei `.xlsx`: `pip install openpyxl` oder Datei als CSV speichern und `.csv` verwenden.
- Umlaute/UTF-8: Bei CSV am besten UTF-8 speichern; das Script nutzt `utf-8-sig`.

Viel Erfolg beim Lernen und Automatisieren!
