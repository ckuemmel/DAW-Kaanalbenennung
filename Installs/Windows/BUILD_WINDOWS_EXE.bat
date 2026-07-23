@echo off
setlocal enabledelayedexpansion

cd /d "%~dp0\..\.."

echo [1/6] Checking Python...
where py >nul 2>nul
if errorlevel 1 (
  echo Python Launcher (py) not found. Install Python 3.11+ from python.org.
  pause
  exit /b 1
)

echo [2/6] Creating virtual environment...
if not exist .venv-win (
  py -3 -m venv .venv-win
)

echo [3/6] Installing dependencies...
call .venv-win\Scripts\activate.bat
python -m pip install --upgrade pip
pip install pyinstaller openpyxl pynput flask werkzeug

echo [4/6] Building Windows EXE...
python -m PyInstaller --noconfirm --clean --onefile --console --name ProToolsTrackNamer_Windows_EXE --hidden-import openpyxl --hidden-import pynput --hidden-import flask --hidden-import werkzeug --add-data "templates;templates" protools_tracknamer_standalone.py

echo [5/6] Copying result to Installs\Windows\output...
if not exist Installs\Windows\output mkdir Installs\Windows\output
copy /Y dist\ProToolsTrackNamer_Windows_EXE.exe Installs\Windows\output\

echo [6/6] Done.
echo Output: Installs\Windows\output\ProToolsTrackNamer_Windows_EXE.exe
pause
