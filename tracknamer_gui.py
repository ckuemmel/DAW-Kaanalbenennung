import tkinter as tk
from tkinter import filedialog, ttk
import pandas as pd
import os

class TrackNamerGUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Sequoia TrackNamer - Import & Auswahl")
        self.geometry("900x600")
        self.filepath = None
        self.data = None
        self.selected_rows = set()
        self.selected_columns = []
        # Die restlichen GUI-Elemente werden erst nach Excel-Import erzeugt
        # Initialisierung erfolgt in create_widgets und init_data_gui
        self.create_widgets()

    def create_widgets(self):
        # Excel-Dateien im Verzeichnis suchen
        import glob, os
        excel_files = glob.glob(os.path.join(os.getcwd(), '*.xlsx')) + glob.glob(os.path.join(os.getcwd(), '*.xls')) + glob.glob(os.path.join(os.getcwd(), '*.xlsm'))
        if not excel_files:
            excel_files = ["Keine Excel-Datei gefunden"]
        self.selected_excel = tk.StringVar(value=excel_files[0])
        excel_label = tk.Label(self, text="Excel-Datei auswählen:")
        excel_label.pack(pady=5)
        excel_dropdown = tk.OptionMenu(self, self.selected_excel, *excel_files)
        excel_dropdown.pack(pady=5)
        select_btn = tk.Button(self, text="Excel-Datei auswählen...", command=self.select_excel_file)
        select_btn.pack(pady=5)
        # Excel wird automatisch geladen, wenn Auswahl geändert wird
        self.selected_excel.trace_add('write', lambda *args: self.open_selected_excel())
    def select_excel_file(self):
        filetypes = [("Excel files", "*.xlsx"), ("Excel files", "*.xls"), ("Excel files", "*.xlsm")]
        filepath = filedialog.askopenfilename(title="Excel-Datei auswählen", filetypes=filetypes)
        if filepath:
            self.selected_excel.set(filepath)
    def open_selected_excel(self):
        self.filepath = self.selected_excel.get()
        if not self.filepath:
            tk.messagebox.showinfo("Hinweis", "Bitte wähle eine Excel-Datei aus.")
            return
        # Vorschau der ersten 10 Zeilen, um Header zu wählen
        preview_df = pd.read_excel(self.filepath, header=None, nrows=10)
        header_window = tk.Toplevel(self)
        header_window.title("Header-Zeile auswählen")
        tk.Label(header_window, text="Wähle die Zeile, die die Spaltennamen enthält:").pack(pady=5)
        listbox = tk.Listbox(header_window, height=10, width=120)
        for i, row in preview_df.iterrows():
            listbox.insert(tk.END, f"Zeile {i+1}: " + ", ".join(str(x) for x in row))
        listbox.pack(pady=5)
        def set_header():
            sel = listbox.curselection()
            if not sel:
                tk.messagebox.showinfo("Hinweis", "Bitte wähle eine Zeile aus.")
                return
            header_row = sel[0]
            header_window.destroy()
            self.data = pd.read_excel(self.filepath, header=header_row)
            self.show_table()
            self.show_column_selectors()
        btn = tk.Button(header_window, text="Übernehmen", command=set_header)
        btn.pack(pady=5)

    def init_data_gui(self):
        # Entferne alte GUI-Elemente, falls vorhanden
        if hasattr(self, "table_frame") and self.table_frame:
            self.table_frame.destroy()
        if hasattr(self, "col_frame") and self.col_frame:
            self.col_frame.destroy()
        if hasattr(self, "export_btn") and self.export_btn:
            self.export_btn.destroy()
        if hasattr(self, "export_vip_btn") and self.export_vip_btn:
            self.export_vip_btn.destroy()

        # Treeview mit Auswahlhäkchen
        self.table_frame = tk.Frame(self)
        self.table_frame.pack(expand=True, fill="both")
        self.tree = ttk.Treeview(self.table_frame, columns=(), show="headings", selectmode="none")
        self.tree.pack(side=tk.LEFT, expand=True, fill="both")
        self.checkbox_frame = tk.Frame(self.table_frame)
        self.checkbox_frame.pack(side=tk.LEFT, fill="y")
        self.row_vars = []

        # Spaltenauswahl
        self.col_frame = tk.Frame(self)
        self.col_frame.pack(pady=10)
        self.col_label = tk.Label(self.col_frame, text="Spalten für Spurnamen auswählen:")
        self.col_label.pack(side=tk.LEFT)
        self.col_vars = []
        # Button zum Umschalten aller Spalten
        self.toggle_btn = tk.Button(self.col_frame, text="Alle Spalten anzeigen", command=self.toggle_columns)
        self.toggle_btn.pack(side=tk.LEFT, padx=10)
        self.show_all_columns = False

        # Export Button
        self.export_btn = tk.Button(self, text="Exportiere ausgewählte Spurnamen", command=self.export_names)
        self.export_btn.pack(pady=10)
        # Export zu Sequoia-Projekt (VIP)
        self.export_vip_btn = tk.Button(self, text="Exportiere Tracknamen ins Sequoia-Projekt (VIP)", command=self.export_to_vip)
        self.export_vip_btn.pack(pady=10)
    def export_to_vip(self):
        selected_rows = self.get_selected_rows()
        if not selected_rows:
            tk.messagebox.showinfo("Hinweis", "Bitte wähle mindestens eine Zeile aus.")
            return
        selected_cols = [col for col, var in self.col_vars if var.get()]
        if not selected_cols:
            tk.messagebox.showinfo("Hinweis", "Bitte wähle mindestens eine Spalte aus.")
            return
        names = []
        for idx in selected_rows:
            row = self.data.loc[int(idx)]
            name = "_".join(str(row[col]) for col in selected_cols)
            names.append(name)
        vip_path = filedialog.askopenfilename(title="Sequoia VIP-Projekt auswählen", filetypes=[("Sequoia VIP", "*.vip")])
        if not vip_path:
            return
        # Dummy-Implementierung: Tracknamen als Textdatei neben VIP speichern
        out_path = os.path.splitext(vip_path)[0] + "_tracknames.txt"
        with open(out_path, "w", encoding="utf-8") as f:
            for name in names:
                f.write(name + "\n")
        tk.messagebox.showinfo("Erfolg", f"Tracknamen exportiert nach {out_path}\n(VIP-Integration kann erweitert werden)")

    def open_file(self):
        filetypes = [("Excel files", "*.xlsx"), ("Excel files", "*.xls"), ("Excel files", "*.xlsm")]
        self.filepath = filedialog.askopenfilename(title="Datei auswählen", filetypes=filetypes)
        if not self.filepath:
            return
        # Vorschau der ersten 10 Zeilen, um Header zu wählen
        preview_df = pd.read_excel(self.filepath, header=None, nrows=10)
        header_window = tk.Toplevel(self)
        header_window.title("Header-Zeile auswählen")
        tk.Label(header_window, text="Wähle die Zeile, die die Spaltennamen enthält:").pack(pady=5)
        listbox = tk.Listbox(header_window, height=10, width=120)
        for i, row in preview_df.iterrows():
            listbox.insert(tk.END, f"Zeile {i+1}: " + ", ".join(str(x) for x in row))
        listbox.pack(pady=5)
        def set_header():
            sel = listbox.curselection()
            if not sel:
                tk.messagebox.showinfo("Hinweis", "Bitte wähle eine Zeile aus.")
                return
            header_row = sel[0]
            header_window.destroy()
            self.data = pd.read_excel(self.filepath, header=header_row)
            self.show_table()
            self.show_column_selectors()
        btn = tk.Button(header_window, text="Übernehmen", command=set_header)
        btn.pack(pady=5)

    def show_table(self):
        self.tree.delete(*self.tree.get_children())
        for widget in self.checkbox_frame.winfo_children():
            widget.destroy()
        self.row_vars = []
        columns_to_show = [col for col, var in self.col_vars if var.get()]
        if not columns_to_show:
            columns_to_show = list(self.data.columns)
        self.tree['columns'] = columns_to_show
        for col in columns_to_show:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=120)
        for idx, row in self.data.iterrows():
            values = [row[col] for col in columns_to_show]
            self.tree.insert('', 'end', iid=str(idx), values=values)
            var = tk.IntVar()
            cb = tk.Checkbutton(self.checkbox_frame, variable=var)
            cb.pack(anchor="w")
            self.row_vars.append((str(idx), var))

    def show_column_selectors(self):
        for widget in self.col_frame.winfo_children()[2:]:
            widget.destroy()
        self.col_vars = []
        columns_to_show = list(self.data.columns)
        for col in columns_to_show:
            var = tk.IntVar(value=1)
            cb = tk.Checkbutton(self.col_frame, text=col, variable=var)
            cb.pack(side=tk.LEFT)
            self.col_vars.append((col, var))
        self.show_table()
    def toggle_columns(self):
        self.show_all_columns = not self.show_all_columns
        if self.show_all_columns:
            self.toggle_btn.config(text="Nur relevante Spalten anzeigen")
        else:
            self.toggle_btn.config(text="Alle Spalten anzeigen")
        self.show_column_selectors()

    def open_selected_excel(self):
        self.filepath = self.selected_excel.get()
        if not self.filepath or self.filepath == "Keine Excel-Datei gefunden":
            tk.messagebox.showinfo("Hinweis", "Bitte wähle eine Excel-Datei aus.")
            return
        # Vorschau der ersten 10 Zeilen, um Header zu wählen
        preview_df = pd.read_excel(self.filepath, header=None, nrows=10)
        header_window = tk.Toplevel(self)
        header_window.title("Header-Zeile auswählen")
        tk.Label(header_window, text="Wähle die Zeile, die die Spaltennamen enthält:").pack(pady=5)
        listbox = tk.Listbox(header_window, height=10, width=120)
        for i, row in preview_df.iterrows():
            listbox.insert(tk.END, f"Zeile {i+1}: " + ", ".join(str(x) for x in row))
        listbox.pack(pady=5)
        def set_header():
            sel = listbox.curselection()
            if not sel:
                tk.messagebox.showinfo("Hinweis", "Bitte wähle eine Zeile aus.")
                return
            header_row = sel[0]
            header_window.destroy()
            self.data = pd.read_excel(self.filepath, header=header_row)
            self.init_data_gui()
            self.show_table()
            self.show_column_selectors()
        btn = tk.Button(header_window, text="Übernehmen", command=set_header)
        btn.pack(pady=5)
if __name__ == "__main__":
    app = TrackNamerGUI()
    app.mainloop()
