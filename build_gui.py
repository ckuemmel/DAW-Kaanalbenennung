#!/usr/bin/env python3
"""
Build-Skript für Sequoia TrackNamer GUI
Erstellt eine optimierte ausführbare Datei
"""

import os
import sys
import shutil
import subprocess
from pathlib import Path

def clean_build_files():
    """Lösche alte Build-Dateien"""
    print("🧹 Lösche alte Build-Dateien...")
    
    dirs_to_remove = ['dist', 'build', '__pycache__']
    files_to_remove = ['*.spec']
    
    for dir_name in dirs_to_remove:
        if os.path.exists(dir_name):
            shutil.rmtree(dir_name)
            print(f"   ✓ {dir_name}/ gelöscht")
    
    # Spec-Dateien löschen
    for spec_file in Path('.').glob('*.spec'):
        spec_file.unlink()
        print(f"   ✓ {spec_file} gelöscht")

def check_icon():
    """Prüfe ob Icon verfügbar ist"""
    icon_path = "icons/icon.ico"
    if not os.path.exists(icon_path):
        print(f"⚠️  Icon nicht gefunden: {icon_path}")
        print("   Verwende Standard-Icon")
        return None
    return icon_path

def build_exe():
    """Erstelle die ausführbare Datei"""
    print("\n🔨 Erstelle ausführbare Datei...")
    
    # PyInstaller-Kommando
    cmd = [
        'pyinstaller',
        '--onefile',                    # Alles in eine Datei
        '--windowed',                   # Kein Konsolen-Fenster
        '--name', 'Sequoia_TrackNamer_GUI',  # Name der .exe
        '--clean',                      # Cache leeren
        '--noconfirm',                  # Überschreiben ohne Nachfrage
    ]
    
    # Icon hinzufügen falls verfügbar
    icon_path = check_icon()
    if icon_path:
        cmd.extend(['--icon', icon_path])
    
    # Hauptdatei
    cmd.append('tracknamer_gui_new.py')
    
    print(f"   Kommando: {' '.join(cmd)}")
    print("   Bitte warten...")
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        print("   ✅ Build erfolgreich!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"   ❌ Build-Fehler: {e}")
        print(f"   Ausgabe: {e.stdout}")
        print(f"   Fehler: {e.stderr}")
        return False

def check_result():
    """Prüfe das Ergebnis"""
    exe_path = Path('dist/Sequoia_TrackNamer_GUI.exe')
    
    if exe_path.exists():
        size_mb = exe_path.stat().st_size / (1024 * 1024)
        print(f"\n✅ Erfolgreich erstellt!")
        print(f"   📁 Pfad: {exe_path.absolute()}")
        print(f"   📏 Größe: {size_mb:.1f} MB")
        
        # Test-Start anbieten
        print("\n🚀 Möchten Sie die .exe-Datei testen? (j/n)")
        if input().lower().startswith('j'):
            try:
                subprocess.Popen(str(exe_path))
                print("   ✓ .exe-Datei gestartet")
            except Exception as e:
                print(f"   ❌ Fehler beim Starten: {e}")
    else:
        print("\n❌ .exe-Datei wurde nicht erstellt!")
        return False
    
    return True

def main():
    """Haupt-Build-Prozess"""
    print("=" * 50)
    print("  Sequoia TrackNamer GUI - Build Script")
    print("=" * 50)
    
    # Arbeitsverzeichnis prüfen
    if not os.path.exists('tracknamer_gui_new.py'):
        print("❌ tracknamer_gui_new.py nicht gefunden!")
        print("   Bitte im richtigen Verzeichnis ausführen.")
        sys.exit(1)
    
    # Build-Prozess
    clean_build_files()
    
    if build_exe():
        check_result()
        print("\n🎉 Build abgeschlossen!")
    else:
        print("\n💥 Build fehlgeschlagen!")
        sys.exit(1)

if __name__ == "__main__":
    main()