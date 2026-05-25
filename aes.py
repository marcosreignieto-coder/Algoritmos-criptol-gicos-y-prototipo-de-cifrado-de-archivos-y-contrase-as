"""Crea un acceso directo en el escritorio para la app de ataques."""

from __future__ import annotations

import os
import sys
from pathlib import Path

try:
    import win32com.client
except ImportError:
    print("Instala pywin32 si quieres crear el acceso directo automáticamente:")
    print("py -m pip install pywin32")
    raise SystemExit(1)

BASE_DIR = Path(__file__).resolve().parent
APP_PATH = BASE_DIR / "app_ataques.py"
ICON_PATH = BASE_DIR / "programa_ataques" / "app_icon.ico"
DESKTOP = Path(os.path.join(os.path.expanduser("~"), "Desktop"))
SHORTCUT = DESKTOP / "Cripto App Ataques.lnk"

shell = win32com.client.Dispatch("WScript.Shell")
shortcut = shell.CreateShortcut(str(SHORTCUT))
shortcut.TargetPath = sys.executable
shortcut.Arguments = f'"{APP_PATH}"'
shortcut.WorkingDirectory = str(BASE_DIR)
if ICON_PATH.exists():
    shortcut.IconLocation = str(ICON_PATH)
shortcut.Save()
print(f"Acceso directo creado en: {SHORTCUT}")
