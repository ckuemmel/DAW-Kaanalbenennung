#!/bin/bash

# 🎵 Multi-DAW Track Namer - Doppelklick Starter
# Für Finder Doppelklick optimiert

# Terminal-Fenster Titel setzen
echo -n -e "\033]0;🎼 Multi-DAW Track Namer\007"

# Wechsle zum Script-Verzeichnis
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
MAIN_DIR="$(dirname "$SCRIPT_DIR")"

cd "$MAIN_DIR"

echo "🎼 ===== Multi-DAW Track Namer ====="
echo "🎯 Pro Tools + Reaper Support"
echo "⚡ Optimierte Geschwindigkeit"
echo "🌐 Web-Interface auf Port 5003"
echo ""

# Prüfe ob Virtual Environment existiert
if [ ! -d "venv" ]; then
    echo "❌ Virtual Environment nicht gefunden!"
    echo "💡 Erstelle venv mit: python3 -m venv venv"
    echo ""
    read -p "🔧 Soll ich das Virtual Environment jetzt erstellen? (j/n): " create_venv
    if [ "$create_venv" = "j" ] || [ "$create_venv" = "J" ]; then
        python3 -m venv venv
        echo "✅ Virtual Environment erstellt!"
    else
        echo "❌ Abbruch - Virtual Environment benötigt!"
        read -p "Drücke Enter zum Schließen..."
        exit 1
    fi
fi

# Aktiviere Virtual Environment
echo "🔧 Aktiviere Python Virtual Environment..."
source venv/bin/activate

# Prüfe ob Abhängigkeiten installiert sind
echo "📦 Installiere/Prüfe Abhängigkeiten..."
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
echo "⚠️  Zum Beenden: Dieses Terminal-Fenster schließen"
echo ""
echo "🔗 URL nochmal zum Kopieren: http://127.0.0.1:5003"
echo ""

# Warte auf App (bringt sie in den Vordergrund)
wait