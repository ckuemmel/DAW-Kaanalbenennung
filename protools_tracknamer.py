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


def find_column_index(header: list[str], column_name: str | None) -> int | None:
    if column_name is None:
        return None
    # Wenn column_name eine Zahl ist, als 0-basierten Index interpretieren
    try:
        if column_name.isdigit():
            idx = int(column_name)
            if 0 <= idx < len(header):
                return idx
    except (ValueError, AttributeError):
        pass
    # Ansonsten als Spaltenname behandeln
    try:
        return next(i for i, h in enumerate(header) if h.lower() == column_name.strip().lower())
    except StopIteration:
        print(f"Spaltenname '{column_name}' nicht gefunden. Verfügbare Spalten:")
        print(", ".join(header))
        sys.exit(1)

def read_names_from_csv(
    path: Path,
    column: int | None = 0,
    column_name: str | None = None,
    channel_column: str | None = None,
    mic_column: str | None = None,
    skip_header: bool = False
) -> list[tuple[str, str | None, str | None]]:
    names: list[tuple[str, str | None, str | None]] = []
    with path.open('r', encoding='utf-8-sig', newline='') as f:
        reader = csv.reader(f)
        header_checked = False
        header: list[str] | None = None
        channel_idx: int | None = None
        mic_idx: int | None = None
        
        for idx, row in enumerate(reader):
            if not header_checked:
                # Ersten Datensatz als möglichen Header auswerten
                header_checked = True
                if column_name is not None or channel_column is not None or mic_column is not None:
                    header = [str(x).strip() for x in row]
                    if column_name is not None:
                        column = find_column_index(header, column_name)
                    if channel_column is not None:
                        channel_idx = find_column_index(header, channel_column)
                    if mic_column is not None:
                        mic_idx = find_column_index(header, mic_column)
                    # Wenn wir nach Namen gemappt haben, ist dies die Headerzeile → überspringen
                    continue
                # Falls kein Spaltenname genutzt wird, kann optional die erste Zeile als Header übersprungen werden
                if skip_header:
                    continue
            if not row:
                continue
            assert column is not None
            if column < len(row):
                name = str(row[column]).strip()
                if name:
                    channel = str(row[channel_idx]).strip() if channel_idx is not None and channel_idx < len(row) else None
                    mic = str(row[mic_idx]).strip() if mic_idx is not None and mic_idx < len(row) else None
                    names.append((name, channel, mic))
    return names


def read_names_from_xlsx(
    path: Path,
    column: int | None = 0,
    column_name: str | None = None,
    channel_column: str | None = None,
    mic_column: str | None = None,
    skip_header: bool = False,
    sheet: str | None = None,
    sheet_index: int | None = None,
    header_row: int | None = None,
) -> list[tuple[str, str | None, str | None]]:
    print("DEBUG: Reading XLSX file")
    print(f"DEBUG: column={column}, channel_column={channel_column}, mic_column={mic_column}")
    try:
        import openpyxl  # type: ignore
    except Exception:
        print("Fehler: 'openpyxl' ist für XLSX erforderlich. Installiere es mit: pip install openpyxl")
        sys.exit(1)

    wb = openpyxl.load_workbook(path, read_only=True, data_only=True)
    # Arbeitsblatt wählen
    if sheet is not None:
        if sheet in wb.sheetnames:
            ws = wb[sheet]
        else:
            matches = [s for s in wb.sheetnames if s.lower() == sheet.lower()]
            if matches:
                ws = wb[matches[0]]
            else:
                print("Blatt nicht gefunden. Verfügbare Blätter:")
                print(", ".join(wb.sheetnames))
                sys.exit(1)
    elif sheet_index is not None:
        if 0 <= sheet_index < len(wb.sheetnames):
            ws = wb[wb.sheetnames[sheet_index]]
        else:
            print(f"Blattindex {sheet_index} ist ungültig. Gültiger Bereich: 0..{len(wb.sheetnames)-1}")
            print("Verfügbare Blätter:")
            for i, name in enumerate(wb.sheetnames):
                print(f"  {i}: {name}")
            sys.exit(1)
    else:
        ws = wb.active
    names: list[tuple[str, str | None, str | None]] = []
    channel_idx: int | None = None
    mic_idx: int | None = None
    
    # Ermitteln der Headerzeile: explizit (--header-row) oder Suche in den ersten Zeilen
    def read_header_row(r: int) -> list[str]:
        vals: list[str] = []
        for c in range(1, ws.max_column + 1):
            v = ws.cell(row=r, column=c).value
            vals.append(str(v).strip() if v is not None else "")
        return vals

    # Spaltenindizes per Headername bestimmen, falls gewünscht
    if column_name is not None or channel_column is not None or mic_column is not None:
        headers: list[str]
        header_row_used: int
        search_limit = min(ws.max_row, 50)
        if header_row is not None and 1 <= header_row <= ws.max_row:
            headers = read_header_row(header_row)
            header_row_used = header_row
        else:
            # Erst Zeile 1 prüfen
            headers = read_header_row(1)
            header_row_used = 1
            # Wenn nicht gefunden, Suche in den ersten N Zeilen
            needed_columns = [c for c in [column_name, channel_column, mic_column] if c is not None]
            if any(all(h.lower() != col.strip().lower() for h in headers) for col in needed_columns):
                found_r: int | None = None
                for r in range(1, search_limit + 1):
                    hdr = read_header_row(r)
                    if any(any(h.lower() == col.strip().lower() for h in hdr) for col in needed_columns):
                        headers = hdr
                        found_r = r
                        break
                if found_r is not None:
                    header_row_used = found_r
                else:
                    print("Spaltennamen nicht gefunden. Tipp: --header-row N setzen.")
                    print("Erste Zeile (angenommener Header):")
                    print(", ".join(headers))
                    sys.exit(1)

        if column_name is not None:
            column = find_column_index(headers, column_name)
        if channel_column is not None:
            channel_idx = find_column_index(headers, channel_column)
        if mic_column is not None:
            mic_idx = find_column_index(headers, mic_column)

        start_row = header_row_used  # In diesem Fall ist die Header-Zeile auch die erste Datenzeile
    else:
        start_row = 2 if skip_header else 1
    for r in range(start_row, ws.max_row + 1):
        assert column is not None
        cell = ws.cell(row=r, column=column + 1)  # Excel ist 1-basiert
        val = cell.value
        if val is None:
            continue
        name = str(val).strip()
        if name:
            # Zusätzliche Spalten auslesen
            channel = None
            mic = None
            if channel_idx is not None:
                channel_cell = ws.cell(row=r, column=channel_idx + 1)
                if channel_cell.value is not None:
                    channel = str(channel_cell.value).strip()
            if mic_idx is not None:
                mic_cell = ws.cell(row=r, column=mic_idx + 1)
                if mic_cell.value is not None:
                    mic = str(mic_cell.value).strip()
            names.append((name, channel, mic))
    return names


def load_names(
    path: Path,
    column: int | None,
    column_name: str | None,
    channel_column: str | None,
    mic_column: str | None,
    skip_header: bool,
    sheet: str | None,
    sheet_index: int | None,
    header_row: int | None
) -> list[tuple[str, str | None, str | None]]:
    suffix = path.suffix.lower()
    if suffix == '.csv':
        return read_names_from_csv(
            path,
            column=column,
            column_name=column_name,
            channel_column=channel_column,
            mic_column=mic_column,
            skip_header=skip_header
        )
    elif suffix in ('.xlsx', '.xlsm'):
        return read_names_from_xlsx(
            path,
            column=column,
            column_name=column_name,
            channel_column=channel_column,
            mic_column=mic_column,
            skip_header=skip_header,
            sheet=sheet,
            sheet_index=sheet_index,
            header_row=header_row,
        )
    else:
        print("Unterstützte Formate: .csv, .xlsx, .xlsm")
        sys.exit(1)


def get_headers_csv(path: Path) -> list[str]:
    with path.open('r', encoding='utf-8-sig', newline='') as f:
        reader = csv.reader(f)
        try:
            row = next(reader)
        except StopIteration:
            return []
        return [str(x).strip() for x in row]


def get_headers_xlsx(path: Path, sheet: str | None, sheet_index: int | None, header_row: int | None) -> tuple[list[str], str, int, int]:
    try:
        import openpyxl  # type: ignore
    except Exception:
        print("Fehler: 'openpyxl' ist für XLSX erforderlich. Installiere es mit: pip install openpyxl")
        sys.exit(1)
    wb = openpyxl.load_workbook(path, read_only=True, data_only=True)
    # Arbeitsblatt auswählen (gleiche Logik wie oben)
    if sheet is not None:
        if sheet in wb.sheetnames:
            ws = wb[sheet]
            sel_name = sheet
            sel_idx = wb.sheetnames.index(sel_name)
        else:
            matches = [s for s in wb.sheetnames if s.lower() == sheet.lower()]
            if matches:
                sel_name = matches[0]
                ws = wb[sel_name]
                sel_idx = wb.sheetnames.index(sel_name)
            else:
                print("Blatt nicht gefunden. Verfügbare Blätter:")
                print(", ".join(wb.sheetnames))
                sys.exit(1)
    elif sheet_index is not None:
        if 0 <= sheet_index < len(wb.sheetnames):
            sel_name = wb.sheetnames[sheet_index]
            ws = wb[sel_name]
            sel_idx = sheet_index
        else:
            print(f"Blattindex {sheet_index} ist ungültig. Gültiger Bereich: 0..{len(wb.sheetnames)-1}")
            print("Verfügbare Blätter:")
            for i, name in enumerate(wb.sheetnames):
                print(f"  {i}: {name}")
            sys.exit(1)
    else:
        ws = wb.active
        sel_name = ws.title
        sel_idx = wb.sheetnames.index(sel_name)
    row_used = 1 if header_row is None else max(1, min(header_row, ws.max_row))
    headers: list[str] = []
    for c in range(1, ws.max_column + 1):
        val = ws.cell(row=row_used, column=c).value
        headers.append(str(val).strip() if val is not None else "")
    return headers, sel_name, sel_idx, row_used


def main():
    parser = argparse.ArgumentParser(
        description="Überträgt Spur-Namen aus CSV/XLSX in Pro Tools per Hotkey (F8).",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument('datei', type=str, help='Pfad zur CSV oder XLSX Datei (erste Spalte = Namen)')
    parser.add_argument('--spalte', type=int, default=None, help='Nullbasierter Spaltenindex (0 = erste Spalte)')
    parser.add_argument('--spaltenname', type=str, default=None, help="Spaltenüberschrift, z.B. 'instrument' (überschreibt --spalte)")
    parser.add_argument('--kanal-spalte', type=str, default=None, help="Name der Spalte mit Kanalnummern")
    parser.add_argument('--mikrofon-spalte', type=str, default=None, help="Name der Spalte mit Mikrofonbezeichnungen")
    parser.add_argument('--blatt', type=str, default=None, help='Tabellenblatt-Name (case-insensitive). Ohne Angabe wird das aktive Blatt verwendet.')
    parser.add_argument('--blatt-index', type=int, default=None, help='Tabellenblatt nach Index wählen (0 = erstes Blatt). Wird ignoriert, wenn --blatt gesetzt ist.')
    parser.add_argument('--header-row', type=int, default=None, help='Headerzeile (1-basiert). Nützlich, wenn Überschriften tiefer liegen oder zusammengeführt sind.')
    parser.add_argument('--skip-header', action='store_true', help='Erste Zeile überspringen (z.B. Überschrift)')
    parser.add_argument('--delay', type=float, default=0.5, help='Verzögerung vor dem Tippen (Sekunden)')
    parser.add_argument('--enter', action='store_true', help='Nach dem Namen automatisch Enter drücken (nicht mit --auto-next kombinieren)')
    parser.add_argument('--check', action='store_true', help='Nur Erkennung prüfen: Blatt, Header, Spalte und Vorschau anzeigen; keine Tasten senden')
    parser.add_argument('--preview', type=int, default=10, help='Anzahl anzuzeigender Namen in --check Modus')
    parser.add_argument('--auto-next', choices=['windows', 'mac'], default=None, help='Nach Bestätigen (Enter) automatisch zur nächsten Spur wechseln (Windows: Ctrl+Right, macOS: Cmd+Right)')
    parser.add_argument('--auto-run', action='store_true', help='Automatisch alle Namen in Folge übertragen (Start mit F8). Empfiehlt sich in Kombination mit --auto-next.')
    parser.add_argument('--next-delay', type=float, default=1.0, help='Verzögerung vor dem Spurwechsel (Sekunden)')
    args = parser.parse_args()

    path = Path(args.datei)
    if not path.exists():
        print(f"Datei nicht gefunden: {path}")
        sys.exit(1)

    names = load_names(
        path,
        column=args.spalte,
        column_name=args.spaltenname,
        channel_column=args.kanal_spalte,
        mic_column=args.mikrofon_spalte,
        skip_header=args.skip_header,
        sheet=args.blatt,
        sheet_index=args.blatt_index,
        header_row=args.header_row,
    )
    if not names:
        print("Keine Namen gefunden. Prüfe Datei/Spalte/Format.")
        sys.exit(1)
    
    # Format zur Anzeige bestimmen
    format_preview = "{name}"
    if args.kanal_spalte:
        format_preview = "{channel} {name}" if any(x[1] for x in names) else "{name}"
    if args.mikrofon_spalte:
        format_preview = format_preview + " {mic}" if any(x[2] for x in names) else format_preview

    if args.check:
        print("Erkennung:")
        if path.suffix.lower() in ('.xlsx', '.xlsm'):
            headers, sel_name, sel_idx, row_used = get_headers_xlsx(path, args.blatt, args.blatt_index, args.header_row)
            print(f"- Datei: {path.name} (XLSX/XLSM)")
            print(f"- Blatt: #{sel_idx} '{sel_name}'")
            print(f"- Headerzeile: {row_used}")
            if headers:
                print("- Header:")
                print("  " + ", ".join(f"[{i}] {h}" for i, h in enumerate(headers)))
            # Spaltenbestimmung für Anzeige
            col_used: str
            if args.spaltenname:
                try:
                    idx = next(i for i, h in enumerate(headers) if h.lower() == args.spaltenname.strip().lower())
                    col_used = f"Spaltenname '{args.spaltenname}' -> Index {idx}"
                except StopIteration:
                    col_used = f"Spaltenname '{args.spaltenname}' nicht in Header gefunden"
            else:
                col_idx = 0 if args.spalte is None else args.spalte
                col_used = f"Spaltenindex {col_idx}"
            print(f"- Spalte: {col_used}")
        else:
            print(f"- Datei: {path.name} (CSV)")
            headers = get_headers_csv(path)
            if headers:
                print("- Erste Zeile (Header/vermutet):")
                print("  " + ", ".join(f"[{i}] {h}" for i, h in enumerate(headers)))
            if args.spaltenname:
                try:
                    idx = next(i for i, h in enumerate(headers) if h.lower() == args.spaltenname.strip().lower())
                    print(f"- Spalte: Spaltenname '{args.spaltenname}' -> Index {idx}")
                except StopIteration:
                    print(f"- Spalte: Spaltenname '{args.spaltenname}' nicht in Header gefunden")
            else:
                col_idx = 0 if args.spalte is None else args.spalte
                print(f"- Spalte: Spaltenindex {col_idx}")

        print(f"- Gefundene Namen: {len(names)}")
        n = max(0, min(args.preview, len(names)))
        if n:
            print("- Vorschau:")
            for i in range(n):
                print(f"  {i}: {names[i]}")
        sys.exit(0)

    print("\nBereit! Anleitung:")
    print("1) Erstelle/Ordne die Spuren in Pro Tools.")
    print("2) Doppelklicke die erste Spurbezeichnung, damit der Umbenennen-Dialog aktiv ist.")
    print("3) Wechsle NICHT zurück zum Terminal.")
    print("4) Drücke F8 für jeden Namen. Mit F7 gehst du einen Namen zurück. ESC beendet.")
    print("   Tipp: Mit --enter drückt das Skript nach dem Tippen automatisch Enter.")
    print(f"Geladene Namen: {len(names)}. Starte mit Index 0.")

    idx = 0
    kb = Controller()
    paused = False
    auto_running = False
    stop_requested = False
    worker_thread: threading.Thread | None = None

    if args.auto_run and not args.auto_next and not args.enter:
        print("Hinweis: --auto-run ohne --auto-next oder --enter wird nach einem Namen stoppen. Empfohlen: --auto-next windows|mac.")

class TrackNamer:
    def __init__(self, args, names):
        self.args = args
        self.names = names
        self.kb = Controller()
        self.idx = 0
        self.paused = False
        self.auto_running = False
        self.stop_requested = False
        self.worker_thread = None
        
    def release_all_keys(self):
        """Stellt sicher, dass alle Modifier-Tasten freigegeben sind"""
        try:
            # Alle möglicherweise hängenden Tasten freigeben
            self.kb.release(Key.ctrl)
            self.kb.release(Key.shift)
            self.kb.release(Key.alt)
            self.kb.release(Key.cmd)
            self.kb.release(Key.right)
            self.kb.release(Key.left)
            self.kb.release(Key.enter)
        except Exception as e:
            print(f"Warnung beim Freigeben der Tasten: {e}")
            pass

    def select_all(self):
        try:
            if self.args.auto_next == 'mac':
                self.kb.press(Key.cmd)
                self.kb.press('a')
                self.kb.release('a')
                self.kb.release(Key.cmd)
            else:
                self.kb.press(Key.ctrl)
                self.kb.press('a')
                self.kb.release('a')
                self.kb.release(Key.ctrl)
        except Exception:
            pass

    def type_next_name(self):
        name, channel, mic = self.names[self.idx]
        self.idx += 1
        time.sleep(self.args.delay)
        self.select_all()
                
        # Formatiere den Namen mit Unterstrichen zwischen den Spalten
        formatted_name = name.strip()
        if self.args.kanal_spalte and channel:
            formatted_name = f"{channel.strip()}_{formatted_name}"
        if self.args.mikrofon_spalte and mic:
            formatted_name = f"{formatted_name}_{mic.strip()}"
                
        self.kb.type(formatted_name)
        
        # Prüfen ob dies der letzte Name ist
        is_last_name = self.idx >= len(self.names)
        
        # Beim letzten Namen mit Enter bestätigen und fertig
        if is_last_name:
            time.sleep(0.01)
            self.kb.press(Key.enter)
            time.sleep(0.01)
            self.kb.release(Key.enter)
            return

        # Ansonsten zur nächsten Spur navigieren
        if self.args.auto_next:
            print(f"DEBUG: Auto-Next ({self.args.auto_next})")
            try:
                if self.args.auto_next == 'windows':
                    # Sicherstellen dass alle Tasten losgelassen sind
                    self.release_all_keys()
                    time.sleep(0.01)
                    
                    # Strg+Rechts drücken um Namen zu bestätigen und zur nächsten Spur zu gehen
                    self.kb.press(Key.ctrl)
                    time.sleep(0.01)
                    self.kb.press(Key.right)
                    time.sleep(0.01)
                    self.kb.release(Key.right)
                    time.sleep(0.01)
                    self.kb.release(Key.ctrl)
                    time.sleep(0.01)  # Absolute Minimalpause nach der Navigation
                else:  # mac
                    self.kb.press(Key.cmd)
                    self.kb.press(Key.right)
                    self.kb.release(Key.right)
                    self.kb.release(Key.cmd)
            except Exception as e:
                print(f"DEBUG: Fehler bei Auto-Next: {e}")
        elif self.args.enter:
            self.kb.press(Key.enter)
            self.kb.release(Key.enter)
        print(f"Getippt: {formatted_name}")

    def handle_f8(self):
        # Auto-Run Modus
        if self.args.auto_run and not self.auto_running:
            self.stop_requested = False
            self.worker_thread = threading.Thread(target=self.run_all, daemon=True)
            self.worker_thread.start()
            print("Auto-Run gestartet. ESC zum Abbrechen, F9 für Pause.")
            return

        if self.idx >= len(self.names):
            print("Fertig: Alle Namen wurden verwendet.")
            return

        self.type_next_name()

    def on_press(self, key):
        try:
            if key == Key.f9:
                if self.auto_running:
                    self.stop_requested = True
                    if self.worker_thread and self.worker_thread.is_alive():
                        self.worker_thread.join(timeout=1)
                    self.auto_running = False
                self.paused = not self.paused
                print(f"Pause: {self.paused}")
                # Beim Pausieren Tasten freigeben
                self.release_all_keys()
            elif key == Key.f7:
                if self.idx > 0:
                    self.idx -= 1
                print(f"Zurück. Nächster Index: {self.idx}")
            elif key == Key.f8 and not self.paused:
                self.handle_f8()
            elif key == Key.esc:
                self.stop_requested = True
                if self.worker_thread and self.worker_thread.is_alive():
                    self.worker_thread.join(timeout=1)
                # Vor dem Beenden Tasten freigeben
                self.release_all_keys()
                print("Beendet.")
                return False
        except Exception as e:
            # Bei Fehlern auch Tasten freigeben
            self.release_all_keys()
            print(f"Fehler beim Senden der Tasten: {e}")
            print("Alle Tasten wurden sicherheitshalber freigegeben.")

    def run_all(self):
        self.auto_running = True
        try:
            while self.idx < len(self.names) and not self.stop_requested:
                self.type_next_name()
                time.sleep(self.args.next_delay)
            if self.idx >= len(self.names):
                print("Fertig: Alle Namen wurden verwendet.")
        finally:
            self.auto_running = False

    def run(self):
        try:
            with keyboard.Listener(on_press=self.on_press) as listener:
                listener.join()
        finally:
            # Beim Beenden sicherstellen, dass alle Tasten freigegeben sind
            self.release_all_keys()


def main():
    parser = argparse.ArgumentParser(
        description="Überträgt Spur-Namen aus CSV/XLSX in Pro Tools per Hotkey (F8).",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument('datei', type=str, help='Pfad zur CSV oder XLSX Datei (erste Spalte = Namen)')
    parser.add_argument('--spalte', type=int, default=None, help='Nullbasierter Spaltenindex (0 = erste Spalte)')
    parser.add_argument('--spaltenname', type=str, default=None, help="Spaltenüberschrift, z.B. 'instrument' (überschreibt --spalte)")
    parser.add_argument('--kanal-spalte', type=str, default=None, help="Name der Spalte mit Kanalnummern")
    parser.add_argument('--mikrofon-spalte', type=str, default=None, help="Name der Spalte mit Mikrofonbezeichnungen")
    parser.add_argument('--blatt', type=str, default=None, help='Tabellenblatt-Name (case-insensitive). Ohne Angabe wird das aktive Blatt verwendet.')
    parser.add_argument('--blatt-index', type=int, default=None, help='Tabellenblatt nach Index wählen (0 = erstes Blatt). Wird ignoriert, wenn --blatt gesetzt ist.')
    parser.add_argument('--header-row', type=int, default=None, help='Headerzeile (1-basiert). Nützlich, wenn Überschriften tiefer liegen oder zusammengeführt sind.')
    parser.add_argument('--skip-header', action='store_true', help='Erste Zeile überspringen (z.B. Überschrift)')
    parser.add_argument('--delay', type=float, default=0.5, help='Verzögerung vor dem Tippen (Sekunden)')
    parser.add_argument('--enter', action='store_true', help='Nach dem Namen automatisch Enter drücken (nicht mit --auto-next kombinieren)')
    parser.add_argument('--check', action='store_true', help='Nur Erkennung prüfen: Blatt, Header, Spalte und Vorschau anzeigen; keine Tasten senden')
    parser.add_argument('--preview', type=int, default=10, help='Anzahl anzuzeigender Namen in --check Modus')
    parser.add_argument('--auto-next', choices=['windows', 'mac'], default=None, help='Nach Bestätigen (Enter) automatisch zur nächsten Spur wechseln (Windows: Ctrl+Right, macOS: Cmd+Right)')
    parser.add_argument('--auto-run', action='store_true', help='Automatisch alle Namen in Folge übertragen (Start mit F8). Empfiehlt sich in Kombination mit --auto-next.')
    parser.add_argument('--next-delay', type=float, default=1.0, help='Verzögerung vor dem Spurwechsel (Sekunden)')
    args = parser.parse_args()

    path = Path(args.datei)
    if not path.exists():
        print(f"Datei nicht gefunden: {path}")
        sys.exit(1)

    names = load_names(
        path,
        column=args.spalte,
        column_name=args.spaltenname,
        channel_column=args.kanal_spalte,
        mic_column=args.mikrofon_spalte,
        skip_header=args.skip_header,
        sheet=args.blatt,
        sheet_index=args.blatt_index,
        header_row=args.header_row,
    )
    if not names:
        print("Keine Namen gefunden. Prüfe Datei/Spalte/Format.")
        sys.exit(1)

    print("\nBereit! Anleitung:")
    print("1) Erstelle/Ordne die Spuren in Pro Tools.")
    print("2) Doppelklicke die erste Spurbezeichnung, damit der Umbenennen-Dialog aktiv ist.")
    print("3) Wechsle NICHT zurück zum Terminal.")
    print("4) Drücke F8 für jeden Namen. Mit F7 gehst du einen Namen zurück. ESC beendet.")
    print("   Tipp: Mit --enter drückt das Skript nach dem Tippen automatisch Enter.")
    print(f"Geladene Namen: {len(names)}. Starte mit Index 0.")

    namer = TrackNamer(args, names)
    namer.run()


if __name__ == '__main__':
    main()
