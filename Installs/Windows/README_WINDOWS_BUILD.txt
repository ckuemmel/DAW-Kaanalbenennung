Windows build (real .exe)
=========================

Why this exists:
- A true Windows .exe cannot be built natively on macOS with PyInstaller.
- Use BUILD_WINDOWS_EXE.bat on a Windows machine to produce the installable .exe.

Steps on Windows:
1) Copy this whole repository to Windows.
2) Double-click Installs\\Windows\\BUILD_WINDOWS_EXE.bat
3) Wait for build completion.
4) Get the installer from:
   Installs\\Windows\\output\\ProToolsTrackNamer_Windows_EXE.exe
