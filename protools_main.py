import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from pathlib import Path
import sys
import subprocess

class ProToolsMainGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("ProTools Helper")
        
        # Variablen
        self.excel_path = tk.StringVar()
        self.header_row = tk.StringVar(value="8")  # Standardwert
        self.include_numbers = tk.BooleanVar(value=True)
        self.include_mics = tk.BooleanVar(value=True)
        self.status_var = tk.StringVar(value="Bereit.")
        
        # GUI erstellen
        self.create_widgets()
        
        # Status
        self.status_var = tk.StringVar(value="Bereit.")

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
        
        ttk.Button(action_frame, text="1. Spuren erstellen", 
                  command=self.create_tracks).pack(side="left", padx=5, pady=10)
        ttk.Button(action_frame, text="2. Spuren benennen", 
                  command=self.rename_tracks).pack(side="left", padx=5, pady=10)
        
        # Statusanzeige
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

    def run_script(self, script_name, args):
        """Führt ein Python-Skript als separaten Prozess aus"""
        try:
            cmd = [sys.executable, script_name] + args
            self.status_var.set(f"Führe {script_name} aus...")
            self.root.update()
            
            # Starte Skript als separaten Prozess
            process = subprocess.Popen(cmd, 
                                    stdout=subprocess.PIPE, 
                                    stderr=subprocess.PIPE,
                                    text=True)
            
            # Warte auf Beendigung
            stdout, stderr = process.communicate()
            
            if process.returncode != 0:
                # Fehler aufgetreten
                error_msg = f"Fehler beim Ausführen von {script_name}:\n"
                error_msg += f"STDOUT:\n{stdout}\n\n"
                error_msg += f"STDERR:\n{stderr}"
                messagebox.showerror("Fehler", error_msg)
                self.status_var.set("Fehler aufgetreten.")
            else:
                # Erfolgreich beendet
                self.status_var.set("Fertig! Bereit für nächste Aktion.")
                
        except Exception as e:
            messagebox.showerror("Fehler", str(e))
            self.status_var.set("Fehler aufgetreten.")

    def create_tracks(self):
        """Startet die Spurerstellung"""
        if not self.validate_input():
            return
            
        msg = messagebox.showinfo(
            "Spuren erstellen",
            "1. Stelle sicher, dass ProTools geöffnet ist\n" +
            "2. Klicke OK\n" +
            "3. Drücke F8 in ProTools zum Erstellen der Spuren\n" +
            "4. ESC zum Abbrechen"
        )
        
        if msg:
            # Starte protools_create_tracks.py
            args = [
                self.excel_path.get(),
                "--header-row", self.header_row.get()
            ]
            self.run_script("protools_create_tracks.py", args)

    def rename_tracks(self):
        """Startet die Spurbenennung"""
        if not self.validate_input():
            return
            
        msg = messagebox.showinfo(
            "Spuren benennen",
            "1. Markiere die erste Spur in ProTools\n" +
            "2. Klicke OK\n" +
            "3. Drücke F9 zum Starten der Benennung\n" +
            "4. ESC zum Abbrechen"
        )
        
        if msg:
            # Starte protools_tracknamer.py
            try:
                from track_namer import TrackNamer
                
                namer = TrackNamer(
                    excel_path=self.excel_path.get(),
                    header_row=int(self.header_row.get()),
                    include_numbers=self.include_numbers.get(),
                    include_mics=self.include_mics.get()
                )
                
                def on_complete():
                    self.status_var.set("Spurbenennung abgeschlossen!")
                    self.root.update()
                
                namer.on_complete = on_complete
                namer.run()
                
            except Exception as e:
                messagebox.showerror("Fehler", f"Fehler beim Ausführen der Spurbenennung:\n{str(e)}")
                self.status_var.set("Fehler aufgetreten.")

def main():
    root = tk.Tk()
    root.resizable(False, False)  # Fixe Fenstergröße
    app = ProToolsMainGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()