from __future__ import annotations

import os
import shutil
from dataclasses import dataclass
from importlib import resources
from pathlib import Path

from .constants import (
    APP_NAME,
    DEFAULT_ICON_NAME,
    DEFAULT_IMAGE_NAME,
    DEFAULT_SOUND_NAME,
    ORIGINAL_BACKUP_NAME,
)


@dataclass(frozen=True)
class BuiltinAssets:
    default_image: Path
    icon: Path
    sound: Path
    backup_dir: Path
    original_backup: Path


def app_data_dir() -> Path:
    base = os.getenv("APPDATA")
    if base:
        return Path(base) / APP_NAME
    return Path.home() / f".{APP_NAME.lower()}"


def _copy_resource_if_needed(resource_name: str, destination: Path) -> None:
    data = resources.files("seewo_editor.resources").joinpath(resource_name).read_bytes()
    if destination.exists() and destination.read_bytes() == data:
        return
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_bytes(data)


def ensure_assets() -> BuiltinAssets:
    builtin_dir = app_data_dir() / "builtin"
    backup_dir = app_data_dir() / "backup"
    backup_dir.mkdir(parents=True, exist_ok=True)

    image_path = builtin_dir / DEFAULT_IMAGE_NAME
    icon_path = builtin_dir / DEFAULT_ICON_NAME
    sound_path = builtin_dir / DEFAULT_SOUND_NAME

    _copy_resource_if_needed(DEFAULT_IMAGE_NAME, image_path)
    _copy_resource_if_needed(DEFAULT_ICON_NAME, icon_path)
    _copy_resource_if_needed(DEFAULT_SOUND_NAME, sound_path)

    return BuiltinAssets(
        default_image=image_path,
        icon=icon_path,
        sound=sound_path,
        backup_dir=backup_dir,
        original_backup=backup_dir / ORIGINAL_BACKUP_NAME,
    )


def backup_default_resources(seewo_pic_path: str | Path, assets: BuiltinAssets | None = None) -> None:
    assets = assets or ensure_assets()
    source = Path(seewo_pic_path)
    if not source.exists() or assets.original_backup.exists():
        return
    assets.original_backup.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(source, assets.original_backup)


def get_builtin_assets() -> BuiltinAssets:
    return ensure_assets()
