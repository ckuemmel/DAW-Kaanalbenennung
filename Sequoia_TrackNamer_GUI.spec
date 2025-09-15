# -*- mode: python ; coding: utf-8 -*-

# Optimierte Spec-Datei für Sequoia TrackNamer GUI

a = Analysis(
    ['tracknamer_gui_new.py'],
    pathex=[],
    binaries=[],
    datas=[],
    hiddenimports=[
        'pandas',
        'pandas._libs',
        'pandas._libs.tslibs',
        'pandas._libs.tslibs.timedeltas',
        'pandas._libs.tslibs.np_datetime', 
        'pandas._libs.tslibs.nattype',
        'pandas._libs.properties',
        'pandas.io.formats.format',
        'openpyxl',
        'openpyxl.workbook',
        'openpyxl.reader.excel',
        'numpy',
        'numpy.core',
        'numpy.core.multiarray',
        'numpy.core.overrides',
        'numpy._core',
        'numpy._core.multiarray',
        'numpy._core.overrides',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[
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
    optimize=1,  # Weniger aggressive Optimierung
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='Sequoia_TrackNamer_GUI',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,         # Strip deaktivieren wegen Kompatibilitätsproblemen
    upx=False,           # UPX deaktivieren für Stabilität
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,       # Kein Konsolenfenster
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='icons/icon.ico' if __import__('os').path.exists('icons/icon.ico') else None,
)
