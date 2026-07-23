#!/usr/bin/env python3
"""
Pro Tools Track Namer - App Builder
Erstellt eine standalone Anwendung für Mac und Windows
"""

import os
import sys
import subprocess
import platform
import shutil

def create_standalone_script():
    """Erstelle eine standalone Version der App"""
    
    standalone_content = '''#!/usr/bin/env python3
"""
Pro Tools Track Namer - Standalone Version
Automatische Track-Erstellung und Benennung für Pro Tools
"""

import os
import sys
import tempfile
import subprocess
import webbrowser
import time
from threading import Timer
import signal

# Flask und andere Imports
try:
    from flask import Flask, render_template_string, request, jsonify, redirect, url_for, flash
    import openpyxl
    from pynput import keyboard
    from pynput.keyboard import Key, Controller as KeyboardController
except ImportError as e:
    print(f"❌ Fehler: Benötigte Bibliothek fehlt: {e}")
    print("🔧 Bitte installiere die Abhängigkeiten mit: pip install flask openpyxl pynput")
    input("Drücke Enter zum Beenden...")
    sys.exit(1)

# Globale Variablen
app = Flask(__name__)
app.secret_key = 'protools_track_namer_secret_key_2025'
current_data = []
current_layout = "auto"

# === HIER DEN GESAMTEN INHALT VON tracknamer_web.py EINFÜGEN ===
''' + open('/Users/carsten/Nextcloud Carsten/GitHub/DAW-Kaanalbenennung-master/tracknamer_web.py', 'r').read().replace('if __name__ == "__main__":', 'def start_server():') + '''

def open_browser():
    """Öffnet den Browser nach kurzer Verzögerung"""
    time.sleep(2)
    webbrowser.open('http://127.0.0.1:5000')
    print("🌐 Browser sollte sich automatisch öffnen...")

def signal_handler(sig, frame):
    """Behandelt Ctrl+C für sauberes Beenden"""
    print("\\n🛑 Pro Tools Track Namer wird beendet...")
    sys.exit(0)

def main():
    """Hauptfunktion für standalone App"""
    print("🎵 Pro Tools Track Namer - Standalone Version")
    print("=" * 50)
    print("🚀 Starte Server...")
    
    # Ctrl+C Handler
    signal.signal(signal.SIGINT, signal_handler)
    
    # Browser nach 2 Sekunden öffnen
    Timer(2.0, open_browser).start()
    
    # Server starten
    try:
        app.run(host='127.0.0.1', port=5000, debug=False)
    except Exception as e:
        print(f"❌ Fehler beim Starten: {e}")
        input("Drücke Enter zum Beenden...")

if __name__ == "__main__":
    main()
'''
    
    with open('protools_tracknamer_standalone.py', 'w', encoding='utf-8') as f:
        f.write(standalone_content)
    
    print("✅ Standalone Script erstellt: protools_tracknamer_standalone.py")

def build_macos_app():
    """Erstelle macOS .app Bundle"""
    print("🍎 Erstelle macOS .app Bundle...")
    
    # PyInstaller Befehl für macOS
    cmd = [
        'pyinstaller',
        '--onefile',
        '--windowed',
        '--name=ProToolsTrackNamer',
        '--icon=icon.icns',  # Wenn vorhanden
        '--add-data=templates:templates',  # Falls Templates vorhanden
        '--hidden-import=openpyxl',
        '--hidden-import=pynput',
        '--hidden-import=flask',
        'protools_tracknamer_standalone.py'
    ]
    
    try:
        subprocess.run(cmd, check=True)
        print("✅ macOS .app Bundle erfolgreich erstellt!")
        print("📂 App befindet sich in: dist/ProToolsTrackNamer.app")
        print("🚀 Du kannst die App jetzt durch Doppelklick starten!")
    except subprocess.CalledProcessError as e:
        print(f"❌ Fehler beim Erstellen der App: {e}")
        return False
    
    return True

def build_windows_exe():
    """Erstelle Windows .exe (nur unter Windows)"""
    if platform.system() != 'Windows':
        print("⚠️ Windows .exe kann nur unter Windows erstellt werden!")
        return False
        
    print("🪟 Erstelle Windows .exe...")
    
    cmd = [
        'pyinstaller',
        '--onefile',
        '--windowed',
        '--name=ProToolsTrackNamer',
        '--icon=icon.ico',  # Wenn vorhanden
        '--hidden-import=openpyxl',
        '--hidden-import=pynput', 
        '--hidden-import=flask',
        'protools_tracknamer_standalone.py'
    ]
    
    try:
        subprocess.run(cmd, check=True)
        print("✅ Windows .exe erfolgreich erstellt!")
        print("📂 Exe befindet sich in: dist/ProToolsTrackNamer.exe")
    except subprocess.CalledProcessError as e:
        print(f"❌ Fehler beim Erstellen der .exe: {e}")
        return False
    
    return True

def main():
    """Hauptfunktion des Build-Scripts"""
    print("🎵 Pro Tools Track Namer - App Builder")
    print("=" * 50)
    
    # 1. Standalone Script erstellen
    create_standalone_script()
    
    # 2. Clean up alte Builds
    for folder in ['build', 'dist', '__pycache__']:
        if os.path.exists(folder):
            shutil.rmtree(folder)
            print(f"🧹 Bereinigt: {folder}")
    
    # 3. Betriebssystem erkennen und entsprechende App erstellen
    system = platform.system()
    
    if system == 'Darwin':  # macOS
        print("🍎 macOS erkannt - erstelle .app Bundle...")
        if build_macos_app():
            print("\\n🎉 Fertig! Du kannst die App jetzt verwenden:")
            print("📱 dist/ProToolsTrackNamer.app")
            print("\\n🚀 Starten: Doppelklick auf die App")
            
    elif system == 'Windows':
        print("🪟 Windows erkannt - erstelle .exe...")
        if build_windows_exe():
            print("\\n🎉 Fertig! Du kannst die App jetzt verwenden:")
            print("💻 dist/ProToolsTrackNamer.exe") 
            print("\\n🚀 Starten: Doppelklick auf die .exe")
            
    else:
        print(f"⚠️ Betriebssystem '{system}' nicht unterstützt!")
        print("💡 Unterstützt: macOS, Windows")

if __name__ == "__main__":
    main()