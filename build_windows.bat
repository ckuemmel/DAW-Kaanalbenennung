@echo off
echo 🚀 Pro Tools Track Namer - Windows Build
echo ==========================================

REM Prüfe Python Installation
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python ist nicht installiert oder nicht im PATH
    echo Bitte installiere Python von https://python.org
    pause
    exit /b 1
)

echo ✅ Python gefunden

REM Erstelle virtuelle Umgebung falls nicht vorhanden
if not exist "venv" (
    echo 📦 Erstelle virtuelle Umgebung...
    python -m venv venv
)

REM Aktiviere virtuelle Umgebung
echo 🔧 Aktiviere virtuelle Umgebung...
call venv\Scripts\activate.bat

REM Installiere Abhängigkeiten
echo 📥 Installiere Abhängigkeiten...
python -m pip install --upgrade pip
pip install -r requirements.txt

REM Baue Executable
echo 🏗️ Erstelle Windows Executable...
python build.py

if errorlevel 1 (
    echo ❌ Build fehlgeschlagen!
    pause
    exit /b 1
)

echo ✅ Build erfolgreich!
echo 📁 Executable befindet sich im dist/ Ordner
echo.
echo Zum Testen: dist\ProTools_TrackNamer.exe starten
pause
