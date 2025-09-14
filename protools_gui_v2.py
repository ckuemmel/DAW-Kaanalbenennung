import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from pathlib import Path
import threading
import sys
import traceback
import os
import time

# Import unserer Module
try:
    from protools_tracknamer import TrackNamer
except ImportError as e:
    print(f"Fehler beim Importieren: {e}")
    sys.exit(1)

class SmartTrackCreator:
    """Intelligenter Track Creator für Pro Tools New Track Dialog"""
    
    def __init__(self):
        try:
            from pynput.keyboard import Key, Controller
            from pynput import mouse
            self.keyboard = Controller()
            self.mouse = mouse.Controller()
            self.Key = Key
        except ImportError as e:
            raise ImportError(f"pynput nicht verfügbar: {e}")
    
    def create_tracks_with_f8(self, num_tracks, callback=None):
        """Erstellt Spuren mit bewährter F8-Methode - einfach und zuverlässig"""
        print(f"Erstelle {num_tracks} Spuren mit F8...")
        
        try:
            for i in range(num_tracks):
                print(f"Erstelle Spur {i+1}/{num_tracks}...")
                
                # F8 drücken für neue Spur
                self.keyboard.press(self.Key.f8)
                time.sleep(0.05)
                self.keyboard.release(self.Key.f8)
                
                # Kurze Pause zwischen den F8-Drücken
                time.sleep(0.1)
                
                # Status-Update alle 10 Spuren
                if (i + 1) % 10 == 0 and callback:
                    callback(f"Spur {i+1}/{num_tracks} erstellt...")
            
            print(f"Fertig! {num_tracks} Spuren mit F8 erstellt.")
            if callback:
                callback(f"{num_tracks} Spuren mit F8 erstellt")
                
        except Exception as e:
            print(f"Fehler bei der F8-Erstellung: {e}")
            if callback:
                callback(f"Fehler: {str(e)}")
            raise
            
    def create_tracks_with_dialog(self, num_tracks, callback=None):
        """Erstellt Spuren über Pro Tools New Track Dialog - alternative Methode"""
        print(f"Erstelle {num_tracks} Spuren über New Track Dialog...")
        
        try:
            # Alternative 1: Versuche Track > New... Menu
            print("Schritt 1: Öffne Track Menu...")
            self.keyboard.press(self.Key.alt)
            self.keyboard.press('t')  # Track Menu
            time.sleep(0.1)
            self.keyboard.release('t')
            self.keyboard.release(self.Key.alt)
            time.sleep(0.5)
            
            # "New..." auswählen
            print("Schritt 2: Wähle 'New...'")
            self.keyboard.press('n')
            time.sleep(0.1)
            self.keyboard.release('n')
            time.sleep(1.5)  # Warte bis Dialog geöffnet ist
            
            # 3. Finde das Anzahl-Feld - versuche mehrere Ansätze
            print("Schritt 3: Navigiere zum Number of Tracks Feld...")
            
            # Erste Strategie: Direkt ins erste Feld
            self.keyboard.press(self.Key.home)  # Gehe zum Anfang
            time.sleep(0.1)
            self.keyboard.release(self.Key.home)
            time.sleep(0.2)
            
            # Alles auswählen und überschreiben
            self.keyboard.press(self.Key.ctrl)
            self.keyboard.press('a')
            time.sleep(0.1)
            self.keyboard.release('a')
            self.keyboard.release(self.Key.ctrl)
            time.sleep(0.2)
            
            # 4. Gib die Anzahl ein
            print(f"Schritt 4: Gebe {num_tracks} ein...")
            # Lösche zuerst den aktuellen Inhalt
            self.keyboard.press(self.Key.delete)
            time.sleep(0.1)
            self.keyboard.release(self.Key.delete)
            time.sleep(0.1)
            
            # Gib neue Zahl ein
            self.keyboard.type(str(num_tracks))
            time.sleep(0.8)
            
            # 5. Bestätige mit Enter oder OK Button
            print("Schritt 5: Bestätige Dialog...")
            # Versuche Tab zu OK Button und dann Space
            self.keyboard.press(self.Key.tab)
            time.sleep(0.1)
            self.keyboard.release(self.Key.tab)
            time.sleep(0.2)
            
            self.keyboard.press(self.Key.tab)  # Nochmal Tab falls nötig
            time.sleep(0.1)
            self.keyboard.release(self.Key.tab)
            time.sleep(0.2)
            
            # Drücke Enter für OK
            self.keyboard.press(self.Key.enter)
            time.sleep(0.1)
            self.keyboard.release(self.Key.enter)
            
            # Warte bis Spuren erstellt sind
            time.sleep(3)
            
            print(f"Fertig! {num_tracks} Spuren sollten erstellt sein.")
            if callback:
                callback(f"{num_tracks} Spuren über Track Menu erstellt")
                
        except Exception as e:
            print(f"Fehler bei der Dialog-Erstellung: {e}")
            # Fallback: Escape drücken um Dialog zu schließen
            try:
                self.keyboard.press(self.Key.esc)
                time.sleep(0.1)
                self.keyboard.release(self.Key.esc)
            except:
                pass
            if callback:
                callback(f"Fehler: {str(e)}")
            raise

class ProToolsGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Pro Tools Track Namer v2.0")
        
        # Status-Variablen
        self.running = False
        self.current_thread = None
        self.tracknamer = None
        
        # Track Creator
        self.creator = SmartTrackCreator()
        
        # GUI erstellen
        self.create_widgets()
        
        # Tastenkombination zum Abbrechen
        self.root.bind('<Escape>', lambda e: self.cancel_current_task())
        
        # Fehler-Logging aktivieren
        self.enable_error_logging()
    
    def enable_error_logging(self):
        """Aktiviert detailliertes Fehler-Logging"""
        def log_exception(exc_type, exc_value, exc_traceback):
            if issubclass(exc_type, KeyboardInterrupt):
                sys.__excepthook__(exc_type, exc_value, exc_traceback)
                return
            
            error_msg = f"Unbehandelter Fehler: {''.join(traceback.format_exception(exc_type, exc_value, exc_traceback))}"
            print(error_msg)
            
            # Schreibe in Datei
            try:
                with open("error_log.txt", "w", encoding="utf-8") as f:
                    f.write(f"Fehler-Log - Pro Tools Track Namer v2.0\n")
                    f.write(f"==========================================\n")
                    f.write(error_msg)
                print("Fehler wurde in error_log.txt gespeichert")
            except:
                pass
                
            # Zeige Benutzer-freundliche Meldung
            try:
                messagebox.showerror("Kritischer Fehler", 
                    f"Ein unerwarteter Fehler ist aufgetreten:\n\n{str(exc_value)}\n\n"
                    f"Details wurden in 'error_log.txt' gespeichert.")
            except:
                pass
        
        sys.excepthook = log_exception
    
    def create_widgets(self):
        # Hauptframe
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.pack(fill="both", expand=True)
        
        # Excel-Datei Auswahl
        file_frame = ttk.LabelFrame(main_frame, text="1. Excel-Datei auswählen", padding="10")
        file_frame.pack(fill="x", pady=(0, 10))
        
        self.file_path_var = tk.StringVar()
        file_entry = ttk.Entry(file_frame, textvariable=self.file_path_var, width=60)
        file_entry.pack(side="left", padx=(0, 10))
        
        ttk.Button(file_frame, text="Durchsuchen...", 
                  command=self.browse_excel_file).pack(side="left")
        
        # Info-Label
        info_text = ("Erwartete Excel-Struktur:\n"
                    "• Spalte B: Kanalnummern (1, 2, 3, ...)\n" 
                    "• Spalte D: Instrumentennamen (A, FL, Ob, ...)\n"
                    "• Spalte E: Mikrofontypen (sE 8, KM 184, ...)")
        
        info_frame = ttk.LabelFrame(main_frame, text="Excel-Format Info", padding="10")
        info_frame.pack(fill="x", pady=(0, 10))
        ttk.Label(info_frame, text=info_text, justify="left").pack(anchor="w")
        
        # Aktions-Buttons
        action_frame = ttk.LabelFrame(main_frame, text="2. Pro Tools Automation", padding="10")
        action_frame.pack(fill="x", pady=(0, 10))
        
        button_frame = ttk.Frame(action_frame)
        button_frame.pack(fill="x")
        
        self.create_button = ttk.Button(button_frame, text="Spuren erstellen (Auto)", 
                                       command=self.create_tracks, width=25)
        self.create_button.pack(side="left", padx=(0, 10))
        
        self.rename_button = ttk.Button(button_frame, text="Spuren benennen (F9)", 
                                       command=self.rename_tracks, width=25)
        self.rename_button.pack(side="left", padx=(0, 10))
        
        self.cancel_button = ttk.Button(button_frame, text="Abbrechen (ESC)", 
                                       command=self.cancel_current_task, width=20)
        self.cancel_button.pack(side="left")
        
        # Status
        status_frame = ttk.LabelFrame(main_frame, text="Status", padding="10")
        status_frame.pack(fill="x")
        
        self.status_var = tk.StringVar(value="Bereit. Bitte Excel-Datei auswählen.")
        ttk.Label(status_frame, textvariable=self.status_var, font=("TkDefaultFont", 9)).pack(anchor="w")
        
        # Anweisungen
        instructions_frame = ttk.LabelFrame(main_frame, text="Anweisungen", padding="10")
        instructions_frame.pack(fill="x", pady=(10, 0))
        
        instructions = ("1. Excel-Datei mit Instrumentenliste auswählen\n"
                       "2. Pro Tools öffnen und Mix-Fenster aktivieren\n" 
                       "3. 'Spuren erstellen' klicken → Automatischer New Track Dialog\n"
                       "4. Programm gibt Spurenanzahl automatisch ein und bestätigt\n"
                       "5. Erste Spur in Pro Tools auswählen\n"
                       "6. 'Spuren benennen' klicken, dann F9 in Pro Tools drücken\n"
                       "7. ESC zum Abbrechen einer laufenden Aktion")
        
        ttk.Label(instructions_frame, text=instructions, justify="left", 
                 font=("TkDefaultFont", 8)).pack(anchor="w")
    
    def browse_excel_file(self):
        """Excel-Datei auswählen"""
        try:
            filepath = filedialog.askopenfilename(
                title="Excel-Datei mit Instrumentenliste auswählen",
                filetypes=[
                    ("Excel-Dateien", "*.xlsx *.xlsm *.xls"),
                    ("Alle Dateien", "*.*")
                ],
                initialdir=os.path.join(os.getcwd(), "Data") if os.path.exists("Data") else os.getcwd()
            )
            
            if filepath:
                self.file_path_var.set(filepath)
                
                # TrackNamer mit Excel-Datei initialisieren
                try:
                    self.tracknamer = TrackNamer(filepath)
                    
                    # Namen sind bereits in self.names geladen
                    names = self.tracknamer.names
                    self.status_var.set(f"Excel-Datei geladen: {len(names)} Instrumente gefunden")
                    
                    # Aktiviere Buttons
                    self.create_button.configure(state="normal")
                    self.rename_button.configure(state="normal")
                    
                except Exception as e:
                    self.status_var.set(f"Warnung: Fehler beim Lesen der Excel-Datei: {str(e)}")
                    print(f"Fehler beim Laden der Excel-Datei: {e}")
                    traceback.print_exc()
                    
        except Exception as e:
            messagebox.showerror("Fehler", f"Fehler beim Auswählen der Datei: {str(e)}")
    
    def task_completed(self, message):
        """Callback für abgeschlossene Tasks"""
        self.running = False
        self.current_thread = None
        self.status_var.set(message)
        
        # GUI-Elemente wieder aktivieren
        self.create_button.configure(state="normal")
        self.rename_button.configure(state="normal")
        
        print(f"Task abgeschlossen: {message}")
    
    def cancel_current_task(self):
        """Bricht die aktuelle Aktion ab"""
        if self.running:
            print("Abbruch angefordert")
            self.running = False
            if self.current_thread and self.current_thread.is_alive():
                self.current_thread = None
            self.task_completed("Aktion abgebrochen. Bereit für neue Aufgabe.")
            messagebox.showinfo("Info", "Aktion wurde abgebrochen.")
    
    def create_tracks(self):
        """Erstellt automatisch alle Spuren - Du drückst nur EINMAL F8!"""
        if self.running:
            messagebox.showinfo("Info", "Es läuft bereits eine Aktion. Bitte warten oder ESC drücken.")
            return
        
        if not self.tracknamer:
            messagebox.showerror("Fehler", "Bitte wählen Sie zuerst eine Excel-Datei aus.")
            return
            
        names = self.tracknamer.names
        num_tracks = len(names)
        
        messagebox.showinfo("Smart Track Dialog - EINMAL F8!", 
            f"INTELLIGENTE SPURERSTELLUNG:\n\n"
            f"Das Programm erstellt {num_tracks} Spuren über New Track Dialog!\n\n"
            f"SO GEHT'S:\n"
            f"1. Klicke OK\n" 
            f"2. Gehe zu Pro Tools\n"
            f"3. Drücke EINMAL F8\n"
            f"4. Programm drückt Shift+Ctrl+N → Dialog öffnet sich\n"
            f"5. Programm gibt '{num_tracks}' ein → Enter\n"
            f"6. Alle {num_tracks} Spuren sind sofort da!\n\n"
            f"⭐ Dann F9 für automatische Benennung!")
            
        # Starte F8-Automation
        self.status_var.set(f"Bereit: F8 → Shift+Ctrl+N → '{num_tracks}' → Enter → Fertig!")
        
        def f8_creation_worker():
            """Wartet auf F8, dann automatische Spurerstellung"""
            try:
                self.running = True
                
                def on_key_press(key):
                    try:
                        if key == keyboard.Key.f8:
                            print(f"F8 gedrückt! Öffne New Track Dialog und erstelle {num_tracks} Spuren...")
                            
                            # 1. Öffne New Track Dialog mit Shift+Ctrl+N
                            print("Schritt 1: Öffne New Track Dialog (Shift+Ctrl+N)")
                            self.tracknamer.kb.press(keyboard.Key.shift)
                            self.tracknamer.kb.press(keyboard.Key.ctrl)
                            self.tracknamer.kb.press('n')
                            time.sleep(0.1)
                            self.tracknamer.kb.release('n')
                            self.tracknamer.kb.release(keyboard.Key.ctrl)
                            self.tracknamer.kb.release(keyboard.Key.shift)
                            
                            # Warte bis Dialog geöffnet ist
                            time.sleep(1.5)
                            
                            # 2. Gib die Anzahl der Spuren ein
                            print(f"Schritt 2: Gebe {num_tracks} in das Anzahl-Feld ein")
                            self.root.after(0, lambda: self.status_var.set(f"Dialog geöffnet, gebe {num_tracks} ein..."))
                            
                            # Alten Wert auswählen (falls da)
                            self.tracknamer.kb.press(keyboard.Key.ctrl)
                            self.tracknamer.kb.press('a')
                            time.sleep(0.1)
                            self.tracknamer.kb.release('a')
                            self.tracknamer.kb.release(keyboard.Key.ctrl)
                            time.sleep(0.2)
                            
                            # Neue Anzahl eingeben
                            self.tracknamer.kb.type(str(num_tracks))
                            time.sleep(0.5)
                            
                            # 3. Mit Enter bestätigen
                            print("Schritt 3: Bestätige mit Enter")
                            self.tracknamer.kb.press(keyboard.Key.enter)
                            time.sleep(0.1)
                            self.tracknamer.kb.release(keyboard.Key.enter)
                            
                            # Warte bis Spuren erstellt sind
                            time.sleep(2)
                            
                            # Fertig!
                            print(f"✅ {num_tracks} Spuren über New Track Dialog erstellt!")
                            self.root.after(0, lambda: self.status_var.set(f"✅ {num_tracks} Spuren erstellt! Bereit für F9-Benennung"))
                            self.root.after(0, lambda: setattr(self, 'running', False))
                            return False  # Stop listener
                            
                        elif key == keyboard.Key.esc:
                            print("ESC - Spurerstellung abgebrochen")
                            self.root.after(0, lambda: self.status_var.set("Spurerstellung abgebrochen"))
                            self.root.after(0, lambda: setattr(self, 'running', False))
                            return False
                            
                    except Exception as e:
                        print(f"Fehler bei F8-Verarbeitung: {e}")
                        self.root.after(0, lambda: self.status_var.set("Fehler bei Spurerstellung"))
                        self.root.after(0, lambda: setattr(self, 'running', False))
                        return False
                
                # Keyboard Listener starten
                with keyboard.Listener(on_press=on_key_press) as listener:
                    listener.join()
                    
            except Exception as e:
                print(f"Fehler im F8-Worker: {e}")
                self.root.after(0, lambda: messagebox.showerror("Fehler", f"F8-Automatik Fehler: {str(e)}"))
                self.root.after(0, lambda: setattr(self, 'running', False))
        
        # Starte F8-Worker Thread
        import threading
        from pynput import keyboard
        self.f8_thread = threading.Thread(target=f8_creation_worker, daemon=True) 
        self.f8_thread.start()
    
    def rename_tracks(self):
        """Benennt Spuren in Pro Tools - verwendet die run() Methode der TrackNamer-Klasse"""
        if self.running:
            messagebox.showinfo("Info", "Es läuft bereits eine Aktion. Bitte warten oder ESC drücken.")
            return
        
        if not self.tracknamer:
            messagebox.showerror("Fehler", "Bitte wählen Sie zuerst eine Excel-Datei aus.")
            return
        
        def run_renaming():
            try:
                names = self.tracknamer.names
                print(f"{len(names)} Namen für Benennung gelesen")
                
                if not names:
                    self.root.after(0, lambda: messagebox.showerror("Fehler", "Keine Namen in der Excel-Datei gefunden."))
                    return
                
                self.running = True
                
                # GUI-Update im Main Thread
                self.root.after(0, lambda: self.status_var.set(f"Bereit zum Benennen von {len(names)} Spuren..."))
                self.root.after(0, lambda: self.create_button.configure(state="disabled"))
                self.root.after(0, lambda: self.rename_button.configure(state="disabled"))
                
                # Info-Dialog im Main Thread
                self.root.after(0, lambda: messagebox.showinfo("Spurbenennung", 
                    f"Bereit zum Benennen von {len(names)} Spuren.\n\n"
                    f"Nächste Schritte:\n"
                    f"1. Erste Spur in Pro Tools auswählen\n" 
                    f"2. F9 drücken um die Benennung zu starten\n"
                    f"3. ESC um abzubrechen\n\n"
                    f"Drücken Sie OK und dann F9 in Pro Tools..."))
                
                # Callback für TrackNamer setzen
                self.tracknamer.on_complete = lambda: self.root.after(0, 
                    lambda: self.task_completed("Alle Spuren wurden erfolgreich benannt!"))
                
                # TrackNamer run() Methode starten  
                # Diese wartet auf F9 und führt dann die Benennung aus
                self.tracknamer.run()
                    
            except Exception as e:
                print(f"Fehler in run_renaming: {e}")
                traceback.print_exc()
                error_msg = f"Fehler beim Benennen der Spuren: {str(e)}"
                self.root.after(0, lambda: messagebox.showerror("Fehler", error_msg))
                self.root.after(0, lambda: self.task_completed("Fehler beim Benennen der Spuren"))
        
        # Thread starten
        try:
            self.current_thread = threading.Thread(target=run_renaming, daemon=True)
            self.current_thread.start()
            print("Spurbenennungs-Thread gestartet")
        except Exception as e:
            print(f"Fehler beim Thread-Start: {e}")
            traceback.print_exc()
            messagebox.showerror("Fehler", f"Fehler beim Starten der Spurbenennung: {str(e)}")

def main():
    """Hauptfunktion"""
    print("Pro Tools Track Namer v2.0")
    print("==========================")
    
    try:
        root = tk.Tk()
        root.resizable(False, False)
        
        # Icon setzen falls vorhanden
        try:
            if os.path.exists("icon.ico"):
                root.iconbitmap("icon.ico")
        except:
            pass
        
        app = ProToolsGUI(root)
        
        # Zentriere Fenster
        root.update_idletasks()
        x = (root.winfo_screenwidth() // 2) - (root.winfo_width() // 2)
        y = (root.winfo_screenheight() // 2) - (root.winfo_height() // 2)
        root.geometry(f"+{x}+{y}")
        
        print("GUI gestartet")
        root.mainloop()
        
    except Exception as e:
        print(f"Kritischer Fehler beim Start: {e}")
        traceback.print_exc()
        
        # Schreibe Fehler in Datei
        try:
            with open("startup_error.txt", "w", encoding="utf-8") as f:
                f.write(f"Startup-Fehler:\n{traceback.format_exc()}")
            print("Fehler in startup_error.txt gespeichert")
        except:
            pass
        
        input("Drücke Enter zum Beenden...")

if __name__ == "__main__":
    main()