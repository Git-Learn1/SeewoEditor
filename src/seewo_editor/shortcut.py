from __future__ import annotations

import os
import shutil
from pathlib import Path

from win32com.client import Dispatch

from .constants import LEGACY_SHORTCUT_NAME, SHORTCUT_NAME
from .runtime import ShortcutCommand


def move_existing_shortcuts(desktop_path: str | Path) -> None:
    temp_dir = Path(os.getenv("TEMP", str(Path.home())))
    for name in (SHORTCUT_NAME, LEGACY_SHORTCUT_NAME):
        source = Path(desktop_path) / name
        if not source.exists():
            continue
        destination = temp_dir / name
        try:
            if destination.exists():
                destination.unlink()
            shutil.move(str(source), str(destination))
        except OSError:
            pass


def create_shortcut(
    shortcut_path: str | Path, command: ShortcutCommand, icon_path: str | Path | None = None
) -> None:
    shortcut_path = Path(shortcut_path)
    shortcut_path.parent.mkdir(parents=True, exist_ok=True)
    shell = Dispatch("WScript.Shell")
    shortcut = shell.CreateShortcut(str(shortcut_path))
    shortcut.TargetPath = str(command.target)
    shortcut.Arguments = command.arguments_text
    if icon_path:
        shortcut.IconLocation = str(icon_path)
    shortcut.Save()
