from __future__ import annotations

import shutil
import stat
from pathlib import Path


def _make_writable(path: Path) -> None:
    if path.exists():
        path.chmod(stat.S_IWRITE)


def _make_readonly(path: Path) -> None:
    if path.exists():
        path.chmod(stat.S_IREAD)


def _backup_existing(path: Path, backup_path: Path) -> None:
    if not path.exists():
        return
    backup_path.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(path, backup_path)


def replace_images(
    system_image: str | Path,
    user_image: str | Path,
    replacement_image: str | Path,
    backup_dir: str | Path,
) -> None:
    replacement = Path(replacement_image)
    if not replacement.exists():
        raise FileNotFoundError(f"替换图片不存在：{replacement}")

    system_target = Path(system_image)
    user_target = Path(user_image)
    if not system_target.exists():
        raise FileNotFoundError(f"系统图片不存在：{system_target}")

    backup = Path(backup_dir)
    targets = (
        (system_target, backup / "replaced.png"),
        (user_target, backup / "replaced_user.png"),
    )
    for target, backup_path in targets:
        target.parent.mkdir(parents=True, exist_ok=True)
        try:
            _make_writable(target)
            _backup_existing(target, backup_path)
            shutil.copy2(replacement, target)
        finally:
            _make_readonly(target)


def restore_images(
    system_image: str | Path,
    user_image: str | Path,
    original_image: str | Path,
) -> None:
    original = Path(original_image)
    if not original.exists():
        raise FileNotFoundError(f"原始备份图片不存在：{original}")

    for target in (Path(system_image), Path(user_image)):
        target.parent.mkdir(parents=True, exist_ok=True)
        try:
            _make_writable(target)
            _backup_existing(target, target.with_name(target.name + ".bak"))
            shutil.copy2(original, target)
        finally:
            _make_readonly(target)
