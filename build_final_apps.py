#!/usr/bin/env python3
"""
Final App Builder für Pro Tools Track Namer
Erstellt plattformspezifische Apps für macOS und Windows
"""

import os
import subprocess
import sys
import shutil
import platform

def clean_build():
    """Räumt alte Build-Ordner auf"""
    dirs_to_clean = ['build', 'dist', '__pycache__']
    for dirname in dirs_to_clean:
        if os.path.exists(dirname):
            shutil.rmtree(dirname)
            print(f"✓ {dirname} folder cleaned")

def build_macos_app():
    """Erstellt macOS .app Bundle (onedir Modus)"""
    print("\n🍎 Building macOS App...")
    
    cmd = [
        'python3', '-m', 'PyInstaller',
        '--onedir',  # Besserer Modus für .app bundles
        '--windowed',
        '--name=ProToolsTrackNamer',
        '--icon=icons/app_icon.icns' if os.path.exists('icons/app_icon.icns') else '',
        '--hidden-import=openpyxl',
        '--hidden-import=pynput',
        '--hidden-import=flask',
        '--hidden-import=werkzeug',
        '--add-data=templates:templates' if os.path.exists('templates') else '',
        'protools_tracknamer_standalone.py'
    ]
    
    # Entferne leere Argumente
    cmd = [arg for arg in cmd if arg]
    
    try:
        result = subprocess.run(cmd, check=True, capture_output=True, text=True)
        print("✅ macOS App erfolgreich erstellt!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ macOS Build Fehler: {e}")
        print(f"STDOUT: {e.stdout}")
        print(f"STDERR: {e.stderr}")
        return False

def build_windows_exe():
    """Erstellt Windows .exe mit Batch-Datei"""
    print("\n🪟 Building Windows Exe...")
    
    # Erstelle die Batch-Datei für Windows
    batch_content = '''@echo off
echo Pro Tools Track Namer wird gestartet...
echo Bitte warten Sie einen Moment...
start "" "%~dp0ProToolsTrackNamer.exe"
timeout /t 2 /nobreak >nul
echo Die App sollte sich in Ihrem Browser öffnen.
pause
'''
    
    with open('StartApp.bat', 'w', encoding='utf-8') as f:
        f.write(batch_content)
    
    cmd = [
        'python3', '-m', 'PyInstaller',
        '--onefile',
        '--console',  # Zeigt Terminal für Windows
        '--name=ProToolsTrackNamer',
        '--icon=icons/app_icon.ico' if os.path.exists('icons/app_icon.ico') else '',
        '--hidden-import=openpyxl',
        '--hidden-import=pynput',
        '--hidden-import=flask',
        '--hidden-import=werkzeug',
        'protools_tracknamer_standalone.py'
    ]
    
    # Entferne leere Argumente
    cmd = [arg for arg in cmd if arg]
    
    try:
        result = subprocess.run(cmd, check=True, capture_output=True, text=True)
        
        # Kopiere Batch-Datei zum dist Ordner
        if os.path.exists('dist/ProToolsTrackNamer.exe'):
            shutil.copy('StartApp.bat', 'dist/')
            print("✅ Windows Exe erfolgreich erstellt!")
            print("✅ StartApp.bat hinzugefügt für einfachen Start")
            return True
        return False
    except subprocess.CalledProcessError as e:
        print(f"❌ Windows Build Fehler: {e}")
        print(f"STDOUT: {e.stdout}")
        print(f"STDERR: {e.stderr}")
        return False

def create_readme():
    """Erstellt README für die gebauten Apps"""
    readme_content = """# Pro Tools Track Namer - Standalone Apps

## 🍎 macOS Installation
1. Öffnen Sie den `dist` Ordner
2. Doppelklicken Sie auf `ProToolsTrackNamer.app`
3. Falls macOS eine Warnung zeigt: Rechtsklick → "Öffnen" → "Öffnen"
4. Die App öffnet automatisch Ihren Browser mit der Benutzeroberfläche

## 🪟 Windows Installation  
1. Öffnen Sie den `dist` Ordner
2. Doppelklicken Sie auf `StartApp.bat` (empfohlen)
   - ODER doppelklicken Sie direkt auf `ProToolsTrackNamer.exe`
3. Die App öffnet automatisch Ihren Browser mit der Benutzeroberfläche

## 🎵 Verwendung
1. Starten Sie Pro Tools
2. Laden Sie Ihre Excel (.xlsm) Datei in der Web-App hoch
3. Wählen Sie das Namensformat (Kanal/Instrument/Mikrofon)
4. Klicken Sie "Tracks erstellen" - die App übernimmt automatisch die Arbeit!

## ⚠️ Wichtige Hinweise
- **macOS**: Accessibility-Berechtigung für Terminal.app erforderlich
  (Systemeinstellungen → Sicherheit → Bedienungshilfen → Terminal.app aktivieren)
- **Windows**: Pro Tools muss im Vordergrund sein
- Die App funktioniert vollständig offline - keine Internetverbindung nötig
- Excel-Dateien werden nur lokal verarbeitet - keine Daten verlassen Ihren Computer

## 🔧 Problemlösung
- Falls die App nicht startet: Überprüfen Sie Antivirus-Einstellungen
- Falls Pro Tools nicht automatisiert wird: Überprüfen Sie Accessibility-Permissions
- Browser öffnet nicht automatisch? Gehen Sie manuell zu http://127.0.0.1:5000

## 📧 Support
Bei Problemen schauen Sie in die Konsole/Terminal für Fehlermeldungen.
"""

    with open('dist/README.md', 'w', encoding='utf-8') as f:
        f.write(readme_content)
    
    print("✅ README.md erstellt")

def main():
    """Hauptfunktion - Baut beide App-Versionen"""
    print("🚀 Pro Tools Track Namer - Final App Builder")
    print("=" * 50)
    
    # Prüfe ob wir auf macOS sind
    current_os = platform.system()
    print(f"Aktuelle Plattform: {current_os}")
    
    # Cleanup
    clean_build()
    
    success_count = 0
    
    # Baue macOS App (nur auf macOS)
    if current_os == "Darwin":
        if build_macos_app():
            success_count += 1
    else:
        print("⚠️ macOS App kann nur auf macOS gebaut werden")
    
    # Baue Windows Exe (funktioniert auch Cross-Platform)
    if build_windows_exe():
        success_count += 1
    
    # Erstelle README
    if success_count > 0:
        create_readme()
    
    print("\n" + "=" * 50)
    print(f"✅ Build abgeschlossen! {success_count} App(s) erfolgreich erstellt.")
    
    if os.path.exists('dist'):
        print(f"\n📁 Apps befinden sich in: {os.path.abspath('dist')}")
        print("\nInhalt des dist Ordners:")
        for item in os.listdir('dist'):
            print(f"  📄 {item}")
    
    print("\n🎉 Ihre Apps sind bereit zur Verwendung!")
    print("   Folgen Sie den Anweisungen in dist/README.md")

if __name__ == "__main__":
    main()