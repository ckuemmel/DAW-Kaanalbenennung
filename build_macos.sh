#!/bin/bash

echo "🚀 Pro Tools Track Namer - macOS Build"
echo "======================================="

# Prüfe Python Installation
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 ist nicht installiert"
    echo "Bitte installiere Python von https://python.org oder mit Homebrew:"
    echo "brew install python"
    exit 1
fi

echo "✅ Python3 gefunden: $(python3 --version)"

# Erstelle virtuelle Umgebung falls nicht vorhanden
if [ ! -d "venv" ]; then
    echo "📦 Erstelle virtuelle Umgebung..."
    python3 -m venv venv
fi

# Aktiviere virtuelle Umgebung
echo "🔧 Aktiviere virtuelle Umgebung..."
source venv/bin/activate

# Installiere Abhängigkeiten
echo "📥 Installiere Abhängigkeiten..."
python -m pip install --upgrade pip
pip install -r requirements.txt

# Baue Executable
echo "🏗️ Erstelle macOS App Bundle..."
python build.py

if [ $? -eq 0 ]; then
    echo "✅ Build erfolgreich!"
    echo "📁 App befindet sich im dist/ Ordner"
    echo ""
    echo "Zum Testen: dist/ProTools\ TrackNamer.app öffnen"
    echo "oder: open dist/ProTools\ TrackNamer.app"
else
    echo "❌ Build fehlgeschlagen!"
    exit 1
fi
