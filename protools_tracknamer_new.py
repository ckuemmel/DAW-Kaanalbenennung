import argparse
import csv
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

class TrackNamer:
    def __init__(self, excel_path, header_row=None, include_numbers=True, include_mics=True):
        print("DEBUG: TrackNamer initialization started")
        
        # Excel-Pfad als Path-Objekt speichern
        if isinstance(excel_path, str):
            self.excel_path = Path(excel_path)
        else:
            self.excel_path = excel_path
            
        self.header_row = header_row
        self.include_numbers = include_numbers
        self.include_mics = include_mics
        self.on_complete = None  # Callback wenn fertig
        
        # Namen aus Excel laden
        load_args = {
            'path': self.excel_path,
            'column': 1,  # Spalte B für Namen/Instrument
            'column_name': None,
            'channel_column': "0" if include_numbers else None,  # Spalte A für Kanalnummern
            'mic_column': "4" if include_mics else None,  # Spalte E für Mikrofone
            'skip_header': False,
            'sheet': None,
            'sheet_index': None,
            'header_row': header_row,
        }
        
        print("DEBUG: Loading names with args:", load_args)
        from protools_tracknamer import load_names  # Importiere die Funktion aus dem Original
        self.names = load_names(**load_args)
        
        # Keyboard Controller und Status initialisieren
        self.kb = Controller()
        self.idx = 0
        self.auto_running = False
        self.stop_requested = False
        self.worker_thread = None
        
        # Konfiguration für das Verhalten
        self.delay = 0.05  # Verzögerung vor dem Tippen
        self.next_delay = 0.1  # Verzögerung zwischen Spuren
        self.auto_next = 'windows'  # Windows: Strg+Rechts für nächste Spur
        
    def release_all_keys(self):
        """Stellt sicher, dass alle Modifier-Tasten freigegeben sind"""
        print("DEBUG: Releasing all keys")
        try:
            # Alle wichtigen Modifier-Tasten freigeben
            for key in [Key.ctrl, Key.shift, Key.alt, Key.cmd]:
                try:
                    self.kb.release(key)
                    time.sleep(0.01)
                except:
                    pass
                    
            # Navigations- und Funktionstasten freigeben
            for key in [Key.right, Key.left, Key.up, Key.down, Key.enter, Key.tab]:
                try:
                    self.kb.release(key)
                    time.sleep(0.01)
                except:
                    pass
                    
            # F-Tasten freigeben
            for i in range(1, 13):
                try:
                    self.kb.release(getattr(Key, f'f{i}'))
                    time.sleep(0.01)
                except:
                    pass
                    
        except Exception as e:
            print(f"Warnung beim Freigeben der Tasten: {e}")
    
    def select_all(self):
        """Markiert den kompletten Text (Strg+A)"""
        try:
            if self.auto_next == 'mac':
                self.kb.press(Key.cmd)
                time.sleep(0.01)
                self.kb.press('a')
                time.sleep(0.01)
                self.kb.release('a')
                time.sleep(0.01)
                self.kb.release(Key.cmd)
            else:
                self.kb.press(Key.ctrl)
                time.sleep(0.01)
                self.kb.press('a')
                time.sleep(0.01)
                self.kb.release('a')
                time.sleep(0.01)
                self.kb.release(Key.ctrl)
        except Exception:
            print("DEBUG: Error in select_all")
            self.release_all_keys()

    def type_next_name(self):
        """Tippt den nächsten Namen und navigiert zur nächsten Spur"""
        if self.idx >= len(self.names):
            print("Ende der Liste erreicht!")
            self.release_all_keys()
            self.stop_requested = True
            if self.on_complete:
                self.on_complete()
            return False
            
        # Name abrufen und formatieren
        name, channel, mic = self.names[self.idx]
        self.idx += 1
        
        print(f"DEBUG: Tippe Namen {self.idx} von {len(self.names)}")
        
        # Sicherstellen dass keine Tasten hängen
        self.release_all_keys()
        time.sleep(self.delay)
        
        # Alten Text markieren und löschen
        self.select_all()
        
        # Name formatieren
        parts = []
        if self.include_numbers and channel:
            parts.append(channel.strip())
        parts.append(name.strip())
        if self.include_mics and mic:
            parts.append(mic.strip())
        
        formatted_name = "_".join(parts)
        print(f"DEBUG: Formatierter Name: {formatted_name}")
        
        # Namen eintippen
        self.kb.type(formatted_name)
        
        # Wenn dies der letzte Name war, mit Enter bestätigen
        if self.idx >= len(self.names):
            time.sleep(0.01)
            self.kb.press(Key.enter)
            time.sleep(0.01)
            self.kb.release(Key.enter)
            print("Letzter Name wurde getippt!")
            self.stop_requested = True
            return False
        
        # Sonst: Zur nächsten Spur navigieren
        try:
            self.release_all_keys()
            time.sleep(0.01)
            
            if self.auto_next == 'windows':
                self.kb.press(Key.ctrl)
                time.sleep(0.01)
                self.kb.press(Key.right)
                time.sleep(0.01)
                self.kb.release(Key.right)
                time.sleep(0.01)
                self.kb.release(Key.ctrl)
            else:  # mac
                self.kb.press(Key.cmd)
                time.sleep(0.01)
                self.kb.press(Key.right)
                time.sleep(0.01)
                self.kb.release(Key.right)
                time.sleep(0.01)
                self.kb.release(Key.cmd)
            
        except Exception as e:
            print(f"DEBUG: Error in navigation: {e}")
            self.release_all_keys()
        
        return True

    def run_all(self):
        """Führt die Umbenennung für alle Spuren durch"""
        print("Starte in 3 Sekunden...")
        for i in range(3, 0, -1):
            print(f"{i}...")
            time.sleep(1)
        print("Los!")
        
        self.auto_running = True
        try:
            self.release_all_keys()
            time.sleep(0.5)
            
            while self.idx < len(self.names) and not self.stop_requested:
                if not self.type_next_name():
                    break
                time.sleep(self.next_delay)
            
            if self.idx >= len(self.names):
                print("Fertig: Alle Namen wurden verwendet.")
            elif self.stop_requested:
                print("Abgebrochen durch Benutzer.")
        finally:
            self.auto_running = False
            self.release_all_keys()
            if self.on_complete:
                self.on_complete()

    def on_press(self, key):
        """Callback für Tastatureingaben"""
        try:
            if key == Key.f9 and not self.auto_running:
                print("DEBUG: F9 pressed, starting naming")
                self.stop_requested = False
                self.release_all_keys()
                time.sleep(0.5)
                
                self.worker_thread = threading.Thread(target=self.run_all)
                self.worker_thread.start()
                return True
            
            elif key == Key.f8 and not self.auto_running:
                print("DEBUG: F8 pressed, typing next name")
                self.release_all_keys()
                time.sleep(0.5)
                self.type_next_name()
                return True
                
            elif key == Key.esc:
                print("DEBUG: ESC pressed, stopping")
                self.stop_requested = True
                self.release_all_keys()
                if self.on_complete:
                    self.on_complete()
                return False
                
        except Exception as e:
            print(f"DEBUG: Error in key handling: {e}")
            self.release_all_keys()
            if self.on_complete:
                self.on_complete()
            return False

    def run(self):
        """Startet den TrackNamer und wartet auf F9"""
        self.release_all_keys()
        
        print("\nBereit zum Benennen!")
        print("1) Markiere die erste Spur in Pro Tools")
        print("2) Drücke F9 zum automatischen Durchlauf oder F8 für einzelne Namen")
        print("3) ESC zum Abbrechen")
        print(f"\nEs werden {len(self.names)} Spuren benannt.")
        print("WICHTIG: Klicke NICHT in andere Fenster während der Benennung!")
        
        try:
            with keyboard.Listener(on_press=self.on_press) as listener:
                listener.join()
        except Exception as e:
            print(f"DEBUG: Error in main loop: {e}")
            raise
        finally:
            print("\nBeende Programm...")
            self.stop_requested = True
            self.auto_running = False
            self.release_all_keys()
            
            if self.on_complete:
                self.on_complete()

def main():
    parser = argparse.ArgumentParser(
        description="Überträgt Spur-Namen aus CSV/XLSX in Pro Tools per Hotkey (F8/F9).",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument('datei', type=str, help='Pfad zur CSV oder XLSX Datei')
    parser.add_argument('--include-numbers', action='store_true', help='Kanalnummern aus Spalte A vor den Namen setzen')
    parser.add_argument('--include-mics', action='store_true', help='Mikrofontypen aus Spalte E hinter den Namen setzen')
    parser.add_argument('--header-row', type=int, default=None, help='Headerzeile (1-basiert)')
    args = parser.parse_args()

    path = Path(args.datei)
    if not path.exists():
        print(f"Datei nicht gefunden: {path}")
        sys.exit(1)

    namer = TrackNamer(
        excel_path=path,
        header_row=args.header_row,
        include_numbers=args.include_numbers,
        include_mics=args.include_mics
    )
    
    namer.run()

if __name__ == '__main__':
    main()