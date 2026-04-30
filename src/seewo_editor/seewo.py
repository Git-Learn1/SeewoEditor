from __future__ import annotations

import os
import re
from dataclasses import dataclass
from pathlib import Path

import winreg

from .constants import LEGACY_SHORTCUT_NAME, SHORTCUT_NAME


@dataclass(frozen=True)
class SeewoPaths:
    system_image: Path | None
    user_image: Path
    launcher: Path | None
    current_user_desktop: Path
    shortcut_desktop: Path
    program_dir: Path
    found_install: bool


def _query_value(root: int, key_path: str, value_name: str) -> str | None:
    try:
        with winreg.OpenKey(root, key_path) as key:
            return winreg.QueryValueEx(key, value_name)[0]
    except OSError:
        return None


def _query_default(root: int, key_path: str) -> str | None:
    try:
        with winreg.OpenKey(root, key_path) as key:
            return winreg.QueryValueEx(key, "")[0]
    except OSError:
        return None


def _program_files_x86() -> Path:
    key = "PROGRAMFILES(X86)" if os.getenv("PROGRAMFILES(X86)") else "PROGRAMFILES"
    return Path(os.getenv(key, r"C:\Program Files (x86)"))


def _extract_exe_from_command(command: str | None) -> Path | None:
    if not command:
        return None
    match = re.search(r'"([^"]+\.exe)"', command, flags=re.IGNORECASE)
    if match:
        return Path(match.group(1))
    match = re.search(r"([^\s]+\.exe)", command, flags=re.IGNORECASE)
    return Path(match.group(1)) if match else None


def _desktop_path(root: int, name: str, fallback: Path) -> Path:
    value = _query_value(
        root,
        r"SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer\Shell Folders",
        name,
    )
    return Path(value) if value else fallback


def _existing_system_image(version_path: Path | None) -> Path | None:
    if version_path is None:
        return None
    for candidate in (
        version_path / "Main" / "Assets" / "SplashScreen.png",
        version_path / "Main" / "Resources" / "Startup" / "SplashScreen.png",
    ):
        if candidate.exists():
            return candidate
    return None


def _launcher_path(version_path: Path | None, program_dir: Path) -> Path | None:
    command_launcher = _extract_exe_from_command(
        _query_default(winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\Classes\easinote\shell\open\command")
    )
    candidates: list[Path] = []
    if command_launcher is not None:
        candidates.append(command_launcher)
    if version_path is not None:
        candidates.extend(
            [
                version_path / "swenlauncher" / "swenlauncher.exe",
                version_path / "Main" / "EasiNote.exe",
            ]
        )
    candidates.append(program_dir / "swenlauncher" / "swenlauncher.exe")
    for candidate in candidates:
        if candidate.exists():
            return candidate
    return candidates[0] if candidates else None


def detect_seewo_paths() -> SeewoPaths:
    version_value = _query_value(
        winreg.HKEY_LOCAL_MACHINE,
        r"SOFTWARE\Wow6432Node\Seewo\EasiNote5",
        "VersionPath",
    )
    version_path = Path(version_value) if version_value else None
    program_dir = version_path.parent if version_path else _program_files_x86() / "Seewo" / "EasiNote5"
    system_image = _existing_system_image(version_path)

    appdata = Path(os.getenv("APPDATA", str(Path.home())))
    user_image_dir = appdata / "Seewo" / "EasiNote5" / "Resources" / "Banner"
    user_image_dir.mkdir(parents=True, exist_ok=True)
    user_image = user_image_dir / "Banner.png"

    current_user_desktop = _desktop_path(
        winreg.HKEY_CURRENT_USER, "DESKTOP", Path.home() / "Desktop"
    )
    common_desktop = _desktop_path(
        winreg.HKEY_LOCAL_MACHINE, "COMMON DESKTOP", current_user_desktop
    )
    shortcut_desktop = (
        common_desktop
        if (common_desktop / SHORTCUT_NAME).exists()
        or (common_desktop / LEGACY_SHORTCUT_NAME).exists()
        else current_user_desktop
    )

    return SeewoPaths(
        system_image=system_image,
        user_image=user_image,
        launcher=_launcher_path(version_path, program_dir),
        current_user_desktop=current_user_desktop,
        shortcut_desktop=shortcut_desktop,
        program_dir=program_dir,
        found_install=version_path is not None,
    )
