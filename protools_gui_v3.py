import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from pathlib import Path
import threading
import sys
import traceback
import os

# Import unserer Module
try:
    from protools_tracknamer import TrackNamer
except ImportError as e:
    print(f"Fehler beim Importieren: {e}")
    # Fallback für Development
    import protools_tracknamer
    TrackNamer = protools_tracknamer.TrackNamer

class SimpleTrackCreator:
    """Einfacher Track Creator für F8-Automation"""
    
    def __init__(self):
        try:
            from pynput.keyboard import Key, Listener, Controller
            self.keyboard = Controller()
            self.Key = Key
        except ImportError as e:
            raise ImportError(f"pynput nicht verfügbar: {e}")
    
    def create_tracks_with_f8(self, num_tracks, callback=None):
        """Erstellt Spuren durch wiederholtes Drücken von F8"""
        import time
        
        print(f"Erstelle {num_tracks} Spuren mit F8...")
        
        for i in range(num_tracks):
            print(f"Erstelle Spur {i+1}/{num_tracks}")
            
            # F8 drücken
            self.keyboard.press(self.Key.f8)
            time.sleep(0.1)
            self.keyboard.release(self.Key.f8)
            
            # Kurze Pause zwischen den Spuren
            time.sleep(0.5)
        
        print("Alle Spuren erstellt!")
        if callback:
            callback("Spurerstellung abgeschlossen")

class ProToolsGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Pro Tools Track Namer v3.0 - FUNKTIONIEREND")
        
        # Status-Variablen
        self.running = False
        self.current_thread = None
        
        # Objekte initialisieren
        self.tracknamer = None  # Wird später initialisiert
        self.creator = SimpleTrackCreator()
        
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
                    f.write(f"Fehler-Log - Pro Tools Track Namer\n")
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
        
        self.create_button = ttk.Button(button_frame, text="Spuren erstellen (F8)", 
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
                       "3. 'Spuren erstellen' klicken für automatische F8-Sequenz\n"
                       "4. 'Spuren benennen' klicken und dann F9 drücken für Namen\n"
                       "5. ESC zum Abbrechen einer laufenden Aktion")
        
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
                except Exception as e:
                    self.status_var.set(f"Warnung: Fehler beim Lesen der Excel-Datei: {str(e)}")
                    
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
        """Erstellt Spuren in Pro Tools durch F8-Tastendruck"""
        if self.running:
            messagebox.showinfo("Info", "Es läuft bereits eine Aktion. Bitte warten oder ESC drücken.")
            return
        
        def run_creation():
            try:
                if not self.tracknamer:
                    self.root.after(0, lambda: messagebox.showerror("Fehler", "Bitte wählen Sie zuerst eine Excel-Datei aus."))
                    return
                
                print(f"Verwende Excel-Datei: {self.tracknamer.excel_path}")
                names = self.tracknamer.names
                print(f"{len(names)} Namen gelesen")
                
                if not names:
                    self.root.after(0, lambda: messagebox.showerror("Fehler", "Keine Namen in der Excel-Datei gefunden."))
                    return
                
                self.running = True
                
                # GUI-Update im Main Thread
                self.root.after(0, lambda: self.status_var.set(f"Erstelle {len(names)} Spuren..."))
                self.root.after(0, lambda: self.create_button.configure(state="disabled"))
                self.root.after(0, lambda: self.rename_button.configure(state="disabled"))
                
                # Info-Dialog im Main Thread
                self.root.after(0, lambda: messagebox.showinfo("Spurenerstellung", 
                    f"Erstelle {len(names)} Spuren.\n\n"
                    f"Stelle sicher, dass:\n"
                    f"• Pro Tools geöffnet und aktiv ist\n"
                    f"• Das Mix-Fenster im Vordergrund ist\n\n"
                    f"Drücken Sie OK und die F8-Sequenz startet..."))
                
                # F8-Sequenz ausführen
                import time
                time.sleep(2)  # Kurze Pause nach Dialog
                
                self.creator.create_tracks_with_f8(len(names), 
                    lambda msg: self.root.after(0, lambda: self.task_completed("Spuren erstellt! Bereit zum Benennen.")))
                    
            except Exception as e:
                print(f"Fehler in run_creation: {e}")
                traceback.print_exc()
                error_msg = f"Fehler beim Erstellen der Spuren: {str(e)}"
                self.root.after(0, lambda: messagebox.showerror("Fehler", error_msg))
                self.root.after(0, lambda: self.task_completed("Fehler beim Erstellen der Spuren"))
        
        # Thread starten
        try:
            self.current_thread = threading.Thread(target=run_creation, daemon=True)
            self.current_thread.start()
            print("Spurerstellungs-Thread gestartet")
        except Exception as e:
            print(f"Fehler beim Thread-Start: {e}")
            traceback.print_exc()
            messagebox.showerror("Fehler", f"Fehler beim Starten der Spurerstellung: {str(e)}")
    
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
                    f"Benenne {len(names)} Spuren.\n\n"
                    f"Vorbereitung:\n"
                    f"• Pro Tools geöffnet und Mix-Fenster aktiv\n" 
                    f"• Erste Spur auswählen/markieren\n\n"
                    f"Drücken Sie OK, dann F9 in Pro Tools\n"
                    f"um die automatische Benennung zu starten."))
                
                # Setze Completion Callback
                def completion_callback():
                    self.root.after(0, lambda: self.task_completed("Alle Spuren erfolgreich benannt!"))
                
                self.tracknamer.on_complete = completion_callback
                
                # Starte das ursprüngliche run() System mit F9
                import threading
                naming_thread = threading.Thread(target=self.tracknamer.run, daemon=True)
                naming_thread.start()
                    
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
    print("Pro Tools Track Namer v3.0 - ZURÜCK ZUM FUNKTIONIERENDEN CODE")
    print("=================================================================")
    
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
        
        print("GUI gestartet - FUNKTIONIERENDEN CODE WIEDERHERGESTELLT")
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