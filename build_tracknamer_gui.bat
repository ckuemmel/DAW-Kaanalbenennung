@echo off
echo =====================================
echo  Sequoia TrackNamer GUI - Build Script
echo =====================================
echo.

echo Lösche alte Build-Dateien...
if exist "dist" rmdir /s /q "dist"
if exist "build" rmdir /s /q "build"
if exist "*.spec" del /q "*.spec"

echo.
echo Erstelle ausführbare Datei...
pyinstaller --onefile --windowed --name "Sequoia_TrackNamer_GUI" --icon=icons/icon.ico tracknamer_gui_new.py

echo.
if exist "dist\Sequoia_TrackNamer_GUI.exe" (
    echo ✅ Erfolgreich erstellt: dist\Sequoia_TrackNamer_GUI.exe
    echo.
    echo Dateigröße:
    dir "dist\Sequoia_TrackNamer_GUI.exe" | find "Sequoia_TrackNamer_GUI.exe"
    echo.
    echo Die .exe-Datei befindet sich im 'dist' Ordner.
    echo.
    pause
) else (
    echo ❌ Fehler beim Erstellen der .exe-Datei
    pause
)