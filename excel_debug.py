import openpyxl
from pathlib import Path

# Excel-Datei öffnen
path = Path("Data/Inputliste Blasorchester 2025 V2.xlsm")
wb = openpyxl.load_workbook(path, read_only=True, data_only=True)
ws = wb.active

# Erste 10 Zeilen und Spalten A-G anzeigen
print(f"Arbeitsblatt: {ws.title}\n")

for row in range(1, 11):
    rowdata = []
    for col in range(1, 8):  # A bis G
        val = ws.cell(row=row, column=col).value
        if val is not None:
            val = str(val).strip()
        rowdata.append(f"{chr(64+col)}{row}: {val}")
    print(" | ".join(rowdata))