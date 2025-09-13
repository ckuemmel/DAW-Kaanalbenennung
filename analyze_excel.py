import openpyxl
from pathlib import Path

# Excel-Datei laden
path = Path("Data/Inputliste Blasorchester 2025 V2.xlsm")
wb = openpyxl.load_workbook(path, read_only=True, data_only=True)
ws = wb.active

# Mehrere Zeilen ausgeben
print("=== Spalteninhalt (erste 5 Zeilen) ===")
for row in range(8, 13):  # Zeilen 8-12
    print(f"\nZeile {row}:")
    for col in range(1, 7):  # Spalten A-F
        cell = ws.cell(row=row, column=col)
        print(f"Spalte {chr(64+col)} ({col-1}): {cell.value}")
