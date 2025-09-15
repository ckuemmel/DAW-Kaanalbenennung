# -*- mode: python ; coding: utf-8 -*-

# Optimierte Spec-Datei für Sequoia TrackNamer GUI (ohne pandas)

a = Analysis(
    ['tracknamer_gui_optimized.py'],
    pathex=[],
    binaries=[],
    datas=[],
    hiddenimports=[
        'openpyxl',
        'openpyxl.workbook',
        'openpyxl.reader.excel',
        'openpyxl.styles',
        'openpyxl.cell',
        'tkinter',
        'tkinter.filedialog',
        'tkinter.ttk',
        'tkinter.messagebox',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[
        'pandas',
        'numpy',
        'matplotlib',
        'pytest',
        'setuptools',
        'PIL',
        'cv2',
        'scipy',
        'IPython',
        'jupyter',
        'notebook',
        'sphinx',
        'test',
        'tests',
        'testing',
    ],
    noarchive=False,
    optimize=2,  # Optimierung aktivieren
)

pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='Sequoia_TrackNamer_Optimized',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,         # Strip für bessere Kompatibilität deaktiviert
    upx=True,            # UPX-Kompression aktivieren
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,       # Kein Konsolenfenster
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)