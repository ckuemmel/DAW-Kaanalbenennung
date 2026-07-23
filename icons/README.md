# Pro Tools Track Namer - Icon Resource

Dieses Verzeichnis kann Icons für die verschiedenen Plattformen enthalten:

## Icon-Dateien:
- `icon.ico` - Windows Icon (256x256, 128x128, 64x64, 48x48, 32x32, 16x16)
- `icon.icns` - macOS Icon Bundle (1024x1024, 512x512, 256x256, 128x128, 64x64, 32x32, 16x16)
- `icon.png` - Original PNG Icon (1024x1024 empfohlen)

## Icon erstellen:

### Für Windows (.ico):
1. Erstelle ein 256x256 PNG Icon
2. Verwende ein Online-Tool wie https://convertio.co/png-ico/
3. Oder verwende ImageMagick: `convert icon.png -resize 256x256 icon.ico`

### Für macOS (.icns):
1. Erstelle ein 1024x1024 PNG Icon
2. Auf macOS: Verwende den `iconutil` Befehl
3. Oder verwende ein Online-Tool wie https://cloudconvert.com/png-to-icns

## Standard-Icon:
Falls kein Icon vorhanden ist, wird das Standard-Python-Icon verwendet.

Das Build-Script sucht automatisch nach `icon.ico` (Windows) und `icon.icns` (macOS).