import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from pathlib import Path
import threading
import sys

try:
    from protools_create_tracks import TrackCreator, count_entries_xlsx, validate_path
    from protools_tracknamer import TrackNamer
except ImportError as e:
    print(f"Fehler beim Importieren der Skripte: {e}")
    print("Versuche alternative Imports...")
    try:
        # Alternative Imports für exe
        import protools_create_tracks
        import protools_tracknamer
        TrackCreator = protools_create_tracks.TrackCreator
        count_entries_xlsx = protools_create_tracks.count_entries_xlsx
        validate_path = protools_create_tracks.validate_path
        TrackNamer = protools_tracknamer.TrackNamer
    except Exception as e2:
        print(f"Auch alternative Imports fehlgeschlagen: {e2}")
        messagebox.showerror("Import Fehler", f"Konnte Module nicht laden: {e}")
        sys.exit(1)

class ProToolsGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("ProTools Automatisierung")
        
        # Variablen
        self.excel_path = tk.StringVar()
        self.header_row = tk.StringVar(value="8")  # Standardwert
        self.include_numbers = tk.BooleanVar(value=True)
        self.include_mics = tk.BooleanVar(value=True)
        
        # GUI erstellen
        self.create_widgets()
        
        # Status
        self.running = False
        self.current_thread = None
        
        # Tastenkombination zum Abbrechen
        self.root.bind('<Escape>', lambda e: self.cancel_current_task())
    
    def task_completed(self, message):
        """Wird aufgerufen, wenn eine Aktion abgeschlossen ist"""
        self.running = False
        self.current_thread = None
        self.status_var.set(message)
        print(f"DEBUG: Task completed - {message}")
        print(f"DEBUG: GUI running status: {self.running}")
    
    def create_widgets(self):
        # Frame für Dateiauswahl
        file_frame = ttk.LabelFrame(self.root, text="Excel-Datei", padding="5")
        file_frame.pack(fill="x", padx=5, pady=5)
        
        ttk.Entry(file_frame, textvariable=self.excel_path, width=50).pack(side="left", padx=5)
        ttk.Button(file_frame, text="Durchsuchen", command=self.browse_file).pack(side="left", padx=5)
        
        # Frame für Einstellungen
        settings_frame = ttk.LabelFrame(self.root, text="Einstellungen", padding="5")
        settings_frame.pack(fill="x", padx=5, pady=5)
        
        # Header-Row Einstellung
        header_frame = ttk.Frame(settings_frame)
        header_frame.pack(fill="x", pady=2)
        ttk.Label(header_frame, text="Header-Zeile:").pack(side="left", padx=5)
        ttk.Entry(header_frame, textvariable=self.header_row, width=5).pack(side="left")
        
        # Namensoptionen
        name_frame = ttk.Frame(settings_frame)
        name_frame.pack(fill="x", pady=2)
        ttk.Checkbutton(name_frame, text="Kanalnummern im Namen", 
                       variable=self.include_numbers).pack(side="left", padx=5)
        ttk.Checkbutton(name_frame, text="Mikrofontypen im Namen",
                       variable=self.include_mics).pack(side="left", padx=5)
        
        # Frame für Aktionen
        action_frame = ttk.LabelFrame(self.root, text="Aktionen", padding="5")
        action_frame.pack(fill="x", padx=5, pady=5)
        
        ttk.Button(action_frame, text="Spuren erstellen (F8)", 
                  command=self.create_tracks).pack(side="left", padx=5)
        ttk.Button(action_frame, text="Spuren benennen (F9)", 
                  command=self.rename_tracks).pack(side="left", padx=5)
        
        # Statusanzeige
        self.status_var = tk.StringVar(value="Bereit.")
        status_frame = ttk.LabelFrame(self.root, text="Status", padding="5")
        status_frame.pack(fill="x", padx=5, pady=5)
        ttk.Label(status_frame, textvariable=self.status_var).pack(fill="x")
    
    def browse_file(self):
        """Öffnet einen Dateidialog zur Auswahl der Excel-Datei"""
        filepath = filedialog.askopenfilename(
            title="Excel-Datei auswählen",
            filetypes=[("Excel-Dateien", "*.xlsx *.xlsm")],
            initialdir=str(Path("Data"))
        )
        if filepath:
            self.excel_path.set(filepath)
            
    def cancel_current_task(self):
        """Bricht die aktuelle Aktion ab"""
        if self.running:
            print("DEBUG: Abbruch angefordert")
            self.running = False
            if self.current_thread and self.current_thread.is_alive():
                self.current_thread = None
            self.task_completed("Aktion abgebrochen. Bereit für neue Aufgabe.")
            messagebox.showinfo("Info", "Aktion wurde abgebrochen.")
    
    def validate_input(self):
        """Überprüft die Eingaben"""
        if not self.excel_path.get():
            messagebox.showerror("Fehler", "Bitte wähle eine Excel-Datei aus.")
            return False
            
        try:
            header_row = int(self.header_row.get())
            if header_row < 1:
                raise ValueError()
        except ValueError:
            messagebox.showerror("Fehler", "Die Header-Zeile muss eine positive Zahl sein.")
            return False
            
        return True
    
    def create_tracks(self):
        """Startet die Spurerstellung"""
        if self.running:
            messagebox.showinfo("Info", "Es läuft bereits eine Aktion. Bitte warte, bis diese beendet ist oder drücke ESC zum Abbrechen.")
            return
            
        if not self.validate_input():
            return
            
        try:
            # Validiere Pfad
            path = validate_path(Path(self.excel_path.get()))
            header_row = int(self.header_row.get())
            
            # Zähle Einträge über TrackNamer (präziser)
            temp_namer = TrackNamer(
                path, 
                header_row=header_row,
                include_numbers=self.include_numbers.get(),
                include_mics=self.include_mics.get()
            )
            num_tracks = len(temp_namer.names)
            if num_tracks <= 0:
                messagebox.showerror("Fehler", "Keine Einträge in der Excel-Datei gefunden!")
                return
                
            # Starte Spurerstellung in eigenem Thread
            self.running = True
            self.status_var.set(f"Bereit zum Erstellen von {num_tracks} Spuren. Drücke F8 in ProTools.")
            
            def run_creator():
                try:
                    creator = TrackCreator(num_tracks)
                    
                    def on_success():
                        self.root.after(0, lambda: self.task_completed("Spuren wurden erstellt! Bereit für die nächste Aktion."))
                        
                    creator.on_complete = on_success
                    creator.run()
                except Exception as e:
                    self.root.after(0, lambda: messagebox.showerror("Fehler", str(e)))
                    self.root.after(0, lambda: setattr(self, 'running', False))
            
            self.current_thread = threading.Thread(target=run_creator, daemon=True)
            self.current_thread.start()
            
        except Exception as e:
            messagebox.showerror("Fehler", str(e))
            self.running = False
    
    def rename_tracks(self):
        """Startet die Spurbenennung"""
        if self.running:
            messagebox.showinfo("Info", "Es läuft bereits eine Aktion. Bitte warte, bis diese beendet ist oder drücke ESC zum Abbrechen.")
            return
            
        if not self.validate_input():
            return
            
        try:
            # Validiere Pfad
            path = validate_path(Path(self.excel_path.get()))
            header_row = int(self.header_row.get())
            
            # Starte Benennung in eigenem Thread
            self.running = True
            self.status_var.set("Bereit zum Benennen. Drücke F9 in ProTools.")
            
            def run_namer():
                try:
                    namer = TrackNamer(
                        path, 
                        header_row=header_row,
                        include_numbers=self.include_numbers.get(),
                        include_mics=self.include_mics.get()
                    )
                    
                    def on_success():
                        self.root.after(0, lambda: self.task_completed("Spuren wurden benannt! Bereit für die nächste Aktion."))
                        
                    namer.on_complete = on_success
                    namer.run()
                except Exception as e:
                    self.root.after(0, lambda: messagebox.showerror("Fehler", str(e)))
                    self.root.after(0, lambda: setattr(self, 'running', False))
            
            self.current_thread = threading.Thread(target=run_namer, daemon=True)
            self.current_thread.start()
            
        except Exception as e:
            messagebox.showerror("Fehler", str(e))
            self.running = False

def main():
    root = tk.Tk()
    root.resizable(False, False)  # Fixe Fenstergröße
    app = ProToolsGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()