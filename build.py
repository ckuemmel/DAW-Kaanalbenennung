#!/usr/bin/env python3
"""
Pro Tools Track Namer - Build Script
Erstellt eigenständige Executables für Windows und macOS
"""

import os
import sys
import platform
import subprocess
import shutil
from pathlib import Path

def check_dependencies():
    """Prüft ob alle benötigten Pakete installiert sind"""
    try:
        import PyInstaller
        print("✅ PyInstaller ist installiert")
    except ImportError:
        print("❌ PyInstaller nicht gefunden. Installiere mit: pip install pyinstaller")
        return False
    
    # Prüfe andere Abhängigkeiten
    required_packages = ['openpyxl', 'pynput']
    missing = []
    
    for package in required_packages:
        try:
            __import__(package)
            print(f"✅ {package} ist installiert")
        except ImportError:
            missing.append(package)
            print(f"❌ {package} fehlt")
    
    if missing:
        print(f"\nInstalliere fehlende Pakete: pip install {' '.join(missing)}")
        return False
    
    return True

def clean_build_dirs():
    """Löscht alte Build-Verzeichnisse"""
    dirs_to_clean = ['build', 'dist', '__pycache__']
    for dir_name in dirs_to_clean:
        if os.path.exists(dir_name):
            print(f"🧹 Lösche {dir_name}")
            shutil.rmtree(dir_name)

def build_executable():
    """Erstellt die Executable"""
    current_os = platform.system()
    
    # PyInstaller Argumente
    args = [
        'pyinstaller',
        '--onefile',  # Eine einzige Datei
        '--windowed',  # Kein Konsolen-Fenster
        '--name=ProTools_TrackNamer',
        '--add-data=beispiel_namen.csv;.',  # Beispieldatei hinzufügen
    ]
    
    # OS-spezifische Einstellungen
    if current_os == 'Windows':
        print("🏗️  Erstelle Windows Executable...")
        if os.path.exists('icon.ico'):
            args.append('--icon=icon.ico')
            print("✅ Windows Icon gefunden")
        else:
            print("⚠️  Kein Windows Icon (icon.ico) gefunden - verwende Standard-Icon")
        if os.path.exists('version_info.txt'):
            args.append('--version-file=version_info.txt')
    elif current_os == 'Darwin':  # macOS
        print("🏗️  Erstelle macOS App Bundle...")
        if os.path.exists('icon.icns'):
            args.append('--icon=icon.icns')
            print("✅ macOS Icon gefunden")
        else:
            print("⚠️  Kein macOS Icon (icon.icns) gefunden - verwende Standard-Icon")
    else:  # Linux
        print("🏗️  Erstelle Linux Executable...")
    
    # Hauptdatei
    args.append('protools_gui.py')
    
    try:
        # PyInstaller ausführen
        result = subprocess.run(args, check=True, capture_output=True, text=True)
        print("✅ Build erfolgreich!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Build fehlgeschlagen: {e}")
        print(f"Fehler: {e.stderr}")
        return False

def create_spec_file():
    """Erstellt eine .spec Datei für erweiterte Konfiguration"""
    spec_content = """# -*- mode: python ; coding: utf-8 -*-

import sys
import platform

block_cipher = None

# Datendateien hinzufügen
datas = [
    ('beispiel_namen.csv', '.'),
]

# OS-spezifische Einstellungen
current_os = platform.system()
icon_file = None
if current_os == 'Windows':
    icon_file = 'icon.ico'
elif current_os == 'Darwin':
    icon_file = 'icon.icns'

a = Analysis(
    ['protools_gui.py'],
    pathex=[],
    binaries=[],
    datas=datas,
    hiddenimports=[
        'openpyxl',
        'pynput',
        'tkinter',
        'threading',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='ProTools_TrackNamer',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=icon_file,
)

# Für macOS: App Bundle erstellen
if current_os == 'Darwin':
    app = BUNDLE(
        exe,
        name='ProTools TrackNamer.app',
        icon=icon_file,
        bundle_identifier='com.ckuemmel.protools-tracknamer',
        info_plist={
            'NSHighResolutionCapable': 'True',
            'CFBundleShortVersionString': '1.0.0',
            'CFBundleVersion': '1.0.0',
        },
    )
"""
    
    with open('ProTools_TrackNamer.spec', 'w', encoding='utf-8') as f:
        f.write(spec_content)
    
    print("📄 .spec Datei erstellt")

def create_version_info():
    """Erstellt Windows-Versionsinformationen"""
    if platform.system() != 'Windows':
        return
    
    version_info = """# UTF-8
#
# For more details about fixed file info 'ffi' see:
# http://msdn.microsoft.com/en-us/library/ms646997.aspx
VSVersionInfo(
  ffi=FixedFileInfo(
    # filevers and prodvers should be always a tuple with four items: (1, 2, 3, 4)
    # Set not needed items to zero 0.
    filevers=(1, 0, 0, 0),
    prodvers=(1, 0, 0, 0),
    # Contains a bitmask that specifies the valid bits 'flags'r
    mask=0x3f,
    # Contains a bitmask that specifies the Boolean attributes of the file.
    flags=0x0,
    # The operating system for which this file was designed.
    # 0x4 - NT and there is no need to change it.
    OS=0x4,
    # The general type of file.
    # 0x1 - the file is an application.
    fileType=0x1,
    # The function of the file.
    # 0x0 - the function is not defined for this fileType
    subtype=0x0,
    # Creation date and time stamp.
    date=(0, 0)
  ),
  kids=[
    StringFileInfo(
      [
      StringTable(
        u'040904B0',
        [StringStruct(u'CompanyName', u'Carsten Kümmel'),
        StringStruct(u'FileDescription', u'Pro Tools Track Namer'),
        StringStruct(u'FileVersion', u'1.0.0.0'),
        StringStruct(u'InternalName', u'ProTools_TrackNamer'),
        StringStruct(u'LegalCopyright', u'Copyright © 2025 Carsten Kümmel'),
        StringStruct(u'OriginalFilename', u'ProTools_TrackNamer.exe'),
        StringStruct(u'ProductName', u'Pro Tools Track Namer'),
        StringStruct(u'ProductVersion', u'1.0.0.0')])
      ]), 
    VarFileInfo([VarStruct(u'Translation', [1033, 1200])])
  ]
)
"""
    
    with open('version_info.txt', 'w', encoding='utf-8') as f:
        f.write(version_info)
    
    print("📋 Windows Version Info erstellt")

def main():
    """Hauptfunktion"""
    print("🚀 Pro Tools Track Namer - Build Script")
    print(f"🖥️  Betriebssystem: {platform.system()}")
    print("-" * 50)
    
    # Abhängigkeiten prüfen
    if not check_dependencies():
        sys.exit(1)
    
    # Build-Verzeichnisse löschen
    clean_build_dirs()
    
    # Hilfsdateien erstellen
    create_spec_file()
    create_version_info()
    
    # Build starten
    success = build_executable()
    
    if success:
        print("\n🎉 Build erfolgreich abgeschlossen!")
        print(f"📁 Executable befindet sich in: {os.path.join(os.getcwd(), 'dist')}")
        
        # Ausgabedatei finden
        dist_dir = Path('dist')
        if dist_dir.exists():
            files = list(dist_dir.glob('*'))
            if files:
                print(f"📦 Erstellt: {files[0].name}")
    else:
        print("\n💥 Build fehlgeschlagen!")
        sys.exit(1)

if __name__ == '__main__':
    main()