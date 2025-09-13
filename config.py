import os
from pathlib import Path

# Basisverzeichnis des Projekts (wo die .git Datei liegt)
REPO_ROOT = Path(__file__).parent.absolute()

# Datenverzeichnis für Excel/CSV Dateien
DATA_DIR = REPO_ROOT / 'Data'

# Stelle sicher dass die Verzeichnisse existieren
DATA_DIR.mkdir(exist_ok=True)

def is_path_in_repo(path: Path) -> bool:
    """Prüft ob ein Pfad innerhalb des Repository-Verzeichnisses liegt"""
    try:
        return REPO_ROOT in path.resolve().parents
    except:
        return False