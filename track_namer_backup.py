import time
from pathlib import Path
import threading
from pynput import keyboard
from pynput.keyboard import Key, Controller

class TrackNamer:
    def __init__(self, excel_path, header_row=None, include_numbers=True, include_mics=True):
        print("DEBUG: TrackNamer initialization started")
        # Excel-Pfad als Path-Objekt speichern
        if isinstance(excel_path, str):
            self.excel_path = Path(excel_path)
        else:
            self.excel_path = excel_path
            
        # Parameter speichern
        self.header_row = header_row
        self.include_numbers = include_numbers
        self.include_mics = include_mics
        
        # Callback für GUI-Updates
        self.on_complete = None
        
        # Namen aus Excel laden
        from protools_tracknamer import load_names
        self.names = load_names(
            path=self.excel_path,
            column=1,  # Spalte B für Namen/Instrument
            column_name=None,
            channel_column="0" if include_numbers else None,  # Spalte A für Kanalnummern
            mic_column="3" if include_mics else None,  # Spalte D für Mikrofone
            skip_header=False,
            sheet=None,
            sheet_index=None,
            header_row=header_row
        )
        
        # Keyboard Controller und Status
        self.kb = Controller()
        self.idx = 0
        self.auto_running = False
        self.stop_requested = False
        self.worker_thread = None
        
        # Timing-Einstellungen
        self.delay = 0.2  # Verzögerung vor dem Tippen
        self.next_delay = 0.5  # Verzögerung zwischen Spuren
    
    def release_all_keys(self):
        """Stellt sicher, dass alle Modifier-Tasten freigegeben sind"""
        print("Gebe alle Tasten frei...")
        try:
            # Alle wichtigen Modifier-Tasten freigeben
            for key in [Key.ctrl, Key.shift, Key.alt, Key.cmd]:
                try:
                    self.kb.release(key)
                    time.sleep(0.05)  # Kleine Pause zwischen den Freigaben
                except:
                    pass
                    
            # Navigations- und Funktionstasten freigeben
            for key in [Key.right, Key.left, Key.up, Key.down, Key.enter, Key.tab]:
                try:
                    self.kb.release(key)
                    time.sleep(0.05)  # Kleine Pause zwischen den Freigaben
                except:
                    pass
                    
            # Sicherheitshalber auch die F-Tasten freigeben
            for i in range(1, 13):  # F1 bis F12
                try:
                    self.kb.release(getattr(Key, f'f{i}'))
                    time.sleep(0.05)  # Kleine Pause zwischen den Freigaben
                except:
                    pass
                    
        except Exception as e:
            print(f"Warnung beim Freigeben der Tasten: {e}")
        finally:
            print("Tastenfreigabe abgeschlossen.")
    
    def select_all(self):
        """Markiert den kompletten Text (Strg+A / Cmd+A)"""
        try:
            # Windows: Strg+A
            self.kb.press(Key.ctrl)
            time.sleep(0.01)
            self.kb.press('a')
            time.sleep(0.01)
            self.kb.release('a')
            time.sleep(0.01)
            self.kb.release(Key.ctrl)
        except Exception:
            pass

    def type_next_name(self):
        """Tippt den nächsten Namen und navigiert zur nächsten Spur"""
        if self.idx >= len(self.names):
            return False
            
        # Name abrufen und formatieren
        name, channel, mic = self.names[self.idx]
        self.idx += 1
        
        print(f"\nBenenne Spur {self.idx} von {len(self.names)}...")
        
        # Sicherstellen dass keine Tasten hängen
        self.release_all_keys()
        
        # Verzögerung vor dem Tippen
        time.sleep(self.delay)
        
        # Alten Text markieren
        self.select_all()
        time.sleep(0.1)  # Kurze Pause nach der Textmarkierung
        
        # Name formatieren nach dem Schema: [Kanal_]Instrument[_Mikrofon]
        name = name.strip() if name else ""
        channel = channel.strip() if channel else ""
        mic = mic.strip() if mic else ""
        
        parts = []
        
        # Kanalnummer hinzufügen wenn aktiviert und vorhanden
        if self.include_numbers and channel:
            parts.append(channel)
            
        # Instrument/Name ist immer dabei
        if name:
            parts.append(name)
            
        # Mikrofon hinzufügen wenn aktiviert und vorhanden
        if self.include_mics and mic:
            parts.append(mic)
            
        # Alles mit Unterstrichen verbinden
        formatted_name = "_".join(parts)
        
        # Namen eintippen
        self.kb.type(formatted_name)
        print(f"Getippt: {formatted_name}")
        
        # Wenn dies der letzte Name war, mit Enter bestätigen und fertig
        if self.idx >= len(self.names):
            time.sleep(0.01)
            self.kb.press(Key.enter)
            time.sleep(0.01)
            self.kb.release(Key.enter)
            return False
        
        # Sonst: Zur nächsten Spur navigieren (Strg+Rechts)
        try:
            self.release_all_keys()
            time.sleep(0.01)
            
            self.kb.press(Key.ctrl)
            time.sleep(0.01)
            self.kb.press(Key.right)
            time.sleep(0.01)
            self.kb.release(Key.right)
            time.sleep(0.01)
            self.kb.release(Key.ctrl)
            time.sleep(0.01)
        except Exception as e:
            print(f"Fehler bei der Navigation: {e}")
            
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
            # Sicherstellen, dass keine Tasten hängen
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
            if key == Key.f9 and not self.auto_running:  # F9 startet die Benennung
                print("F9 gedrückt, starte Benennung...")
                self.stop_requested = False
                # Zuerst alle Tasten freigeben
                self.release_all_keys()
                time.sleep(0.5)
                # Starte Benennung in separatem Thread
                self.worker_thread = threading.Thread(target=self.run_all)
                self.worker_thread.start()
                return True  # Listener bleibt aktiv für ESC
            
            elif key == Key.f8 and not self.auto_running:  # F8 für einzelnen Namen
                print("F8 gedrückt, tippe nächsten Namen...")
                # Zuerst alle Tasten freigeben
                self.release_all_keys()
                time.sleep(0.5)
                self.type_next_name()
                return True  # Listener bleibt aktiv
                
            elif key == Key.esc:  # ESC bricht ab
                print("ESC gedrückt, breche ab...")
                self.stop_requested = True
                self.release_all_keys()
                if self.on_complete:
                    self.on_complete()
                return False  # Beendet den Listener
                
        except Exception as e:
            print(f"Fehler in Tastenverarbeitung: {e}")
            self.release_all_keys()
            if self.on_complete:
                self.on_complete()
            return False

    def run(self):
        """Startet den TrackNamer und wartet auf F9"""
        # Zuerst alle Tasten freigeben um sicherzugehen
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
            print(f"Fehler: {e}")
            raise
        finally:
            # Unbedingt alle Tasten freigeben beim Beenden
            print("\nBeende Programm...")
            self.stop_requested = True
            self.auto_running = False
            self.release_all_keys()
            
            if self.on_complete:
                self.on_complete()