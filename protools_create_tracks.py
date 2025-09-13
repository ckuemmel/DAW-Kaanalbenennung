import argparse
import sys
import time
from pathlib import Path
import threading

try:
    from pynput import keyboard
    from pynput.keyboard import Key, Controller
except Exception as e:
    print("Fehler: Das Paket 'pynput' ist nicht installiert oder konnte nicht geladen werden.")
    print("Installiere es mit: pip install pynput")
    sys.exit(1)

# Import Konfiguration
try:
    from config import REPO_ROOT, DATA_DIR, is_path_in_repo
except ImportError:
    print("Fehler: config.py nicht gefunden. Stelle sicher, dass die Datei im gleichen Verzeichnis liegt.")
    sys.exit(1)

def validate_path(path: Path) -> Path:
    """Validiert den Pfad und stellt sicher, dass er im Data-Verzeichnis liegt"""
    try:
        abs_path = path.resolve()
        if not DATA_DIR in abs_path.parents:
            print(f"Fehler: Die Datei {path} liegt außerhalb des Data-Verzeichnisses.")
            print(f"Bitte lege die Datei im {DATA_DIR} Verzeichnis ab.")
            sys.exit(1)
        if not abs_path.exists():
            print(f"Fehler: Die Datei {path} existiert nicht.")
            sys.exit(1)
        return abs_path
    except Exception as e:
        print(f"Fehler beim Zugriff auf die Datei {path}: {e}")
        sys.exit(1)

def count_entries_xlsx(path: Path, header_row: int | None = None) -> int:
    """Zählt die Anzahl der relevanten Einträge in der Excel-Datei"""
    try:
        import openpyxl
    except ImportError:
        print("Fehler: 'openpyxl' ist für XLSX erforderlich. Installiere es mit: pip install openpyxl")
        sys.exit(1)

    wb = openpyxl.load_workbook(path, read_only=True, data_only=True)
    ws = wb.active
    
    # Startzeile bestimmen
    start_row = 1 if header_row is None else header_row
    
    # Zähle relevante Zeilen (wo Spalte 3 nicht leer ist)
    count = 0
    for row in ws.iter_rows(min_row=start_row):
        if len(row) >= 3 and row[2].value:  # Spalte 3 (index 2) enthält die Namen
            count += 1
            
    # Wenn eine Header-Zeile angegeben wurde, diese abziehen
    if header_row is not None:
        count -= 1
        
    return count

class TrackCreator:
    def __init__(self, num_tracks: int):
        self.num_tracks = num_tracks
        self.kb = Controller()
        self.stop_requested = False
        
    def release_all_keys(self):
        """Stellt sicher, dass alle Modifier-Tasten freigegeben sind"""
        try:
            self.kb.release(Key.ctrl)
            self.kb.release(Key.shift)
            self.kb.release(Key.alt)
            self.kb.release(Key.cmd)
            self.kb.release(Key.enter)
        except Exception as e:
            print(f"Warnung beim Freigeben der Tasten: {e}")
            
    def create_tracks(self):
        """Erstellt die angegebene Anzahl an Spuren"""
        print(f"Erstelle {self.num_tracks} Spuren...")
        
        for i in range(self.num_tracks):
            if self.stop_requested:
                break
                
            # Strg+Shift+N für "Neue Spur"
            self.kb.press(Key.ctrl)
            time.sleep(0.01)
            self.kb.press(Key.shift)
            time.sleep(0.01)
            self.kb.press('n')
            time.sleep(0.01)
            self.kb.release('n')
            time.sleep(0.01)
            self.kb.release(Key.shift)
            time.sleep(0.01)
            self.kb.release(Key.ctrl)
            
            # Kurze Pause für den Dialog
            time.sleep(0.1)
            
            # Enter drücken um den Standard-Track zu bestätigen
            self.kb.press(Key.enter)
            time.sleep(0.01)
            self.kb.release(Key.enter)
            
            # Pause zwischen den Spuren
            time.sleep(0.1)
            
            print(f"Spur {i+1}/{self.num_tracks} erstellt")
            
        print("Fertig!")
        self.release_all_keys()
        
    def on_press(self, key):
        """Überwacht Tastatureingaben"""
        try:
            if key == Key.f8:
                # Starte das Erstellen der Spuren
                self.stop_requested = False
                thread = threading.Thread(target=self.create_tracks)
                thread.start()
            elif key == Key.esc:
                # Stoppe das Erstellen und gebe alle Tasten frei
                self.stop_requested = True
                self.release_all_keys()
                print("\nAbgebrochen.")
                return False
        except Exception as e:
            self.release_all_keys()
            print(f"Fehler: {e}")
            
    def run(self):
        """Startet den Listener für Tastatureingaben"""
        print("\nBereit! Anleitung:")
        print("1) Öffne Pro Tools und stelle sicher, dass das Fenster aktiv ist.")
        print("2) Drücke F8 um die Spuren zu erstellen.")
        print("3) ESC zum Abbrechen.")
        print(f"Es werden {self.num_tracks} Spuren erstellt.")
        
        try:
            with keyboard.Listener(on_press=self.on_press) as listener:
                listener.join()
        finally:
            self.release_all_keys()

def main():
    parser = argparse.ArgumentParser(
        description="Erstellt die benötigte Anzahl an Spuren in Pro Tools basierend auf einer Excel-Datei.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument('datei', type=str, help=f'Pfad zur XLSX Datei im {DATA_DIR} Verzeichnis')
    parser.add_argument('--header-row', type=int, help='Headerzeile (1-basiert). Diese Zeile wird beim Zählen übersprungen.')
    args = parser.parse_args()
    
    # Pfadvalidierung
    path = validate_path(Path(args.datei))
    
    # Zähle Einträge
    num_tracks = count_entries_xlsx(path, args.header_row)
    if num_tracks <= 0:
        print("Keine Einträge gefunden!")
        sys.exit(1)
        
    # Erstelle Spuren
    creator = TrackCreator(num_tracks)
    creator.run()

if __name__ == '__main__':
    main()