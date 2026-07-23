#!/bin/bash

# 🎵 Multi-DAW Track Namer Starter Script
# Für Pro Tools + Reaper Support
# Erstellt von GitHub Copilot

echo "🎼 ===== Multi-DAW Track Namer ====="
echo "🎯 Pro Tools + Reaper Support"
echo "⚡ Optimierte Geschwindigkeit"
echo "🌐 Web-Interface auf Port 5003"
echo ""

# Wechsle zum Hauptverzeichnis
cd "/Users/carsten/Nextcloud Carsten/GitHub/DAW-Kaanalbenennung-master"

# Prüfe ob Virtual Environment existiert
if [ ! -d "venv" ]; then
    echo "❌ Virtual Environment nicht gefunden!"
    echo "💡 Erstelle venv mit: python3 -m venv venv"
    exit 1
fi

# Aktiviere Virtual Environment
echo "🔧 Aktiviere Python Virtual Environment..."
source venv/bin/activate

# Prüfe ob Abhängigkeiten installiert sind
echo "📦 Prüfe Abhängigkeiten..."
pip install -q flask openpyxl pynput

# Stoppe eventuell laufende Instanzen
echo "🔄 Stoppe vorherige App-Instanzen..."
pkill -f tracknamer_web_reaper 2>/dev/null || true
lsof -ti:5003 | xargs kill -9 2>/dev/null || true

# Starte die App
echo "🚀 Starte Multi-DAW Track Namer..."
echo ""

# App im Hintergrund starten
python tracknamer_web_reaper.py &

# Kurz warten bis Server läuft
echo "⏳ Warte auf Server-Start..."
sleep 3

# Informationen für manuelles Öffnen
echo ""
echo "✅ Server läuft!"
echo "🌐 Öffne diese URL in deinem Browser:"
echo "👉 http://127.0.0.1:5003"
echo ""
echo "💡 Kopiere die URL und füge sie in deinen Browser ein"
echo "⚠️  Zum Beenden: Strg+C drücken"
echo ""

# Warte auf App (bringt sie in den Vordergrund)
wait