from __future__ import annotations

import json
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, Sequence


@dataclass(frozen=True)
class RuntimeInfo:
    executable: Path
    argv0: Path
    entry_file: Path
    frozen: bool = False
    pyinstaller: bool = False
    nuitka: bool = False
    meipass: Path | None = None
    compiled_containing_dir: Path | None = None
    original_argv0: str | None = None

    @property
    def source_mode(self) -> bool:
        return not self.frozen and not self.nuitka


@dataclass(frozen=True)
class ShortcutCommand:
    target: Path
    arguments: tuple[str, ...] = ()

    @property
    def arguments_text(self) -> str:
        return subprocess.list2cmdline(list(self.arguments))


def _resolve_path(value: str | Path) -> Path:
    return Path(value).expanduser().resolve(strict=False)


def _compiled_object() -> object | None:
    compiled = globals().get("__compiled__")
    if compiled is not None:
        return compiled
    main_module = sys.modules.get("__main__")
    return getattr(main_module, "__compiled__", None)


def current_runtime_info(entry_file: str | Path) -> RuntimeInfo:
    compiled = _compiled_object()
    meipass = getattr(sys, "_MEIPASS", None)
    pyinstaller = bool(getattr(sys, "frozen", False) and meipass)

    return RuntimeInfo(
        executable=_resolve_path(sys.executable),
        argv0=_resolve_path(sys.argv[0]),
        entry_file=_resolve_path(entry_file),
        frozen=bool(getattr(sys, "frozen", False)),
        pyinstaller=pyinstaller,
        nuitka=compiled is not None,
        meipass=_resolve_path(meipass) if meipass else None,
        compiled_containing_dir=_resolve_path(getattr(compiled, "containing_dir"))
        if compiled is not None and getattr(compiled, "containing_dir", None)
        else None,
        original_argv0=getattr(compiled, "original_argv0", None)
        if compiled is not None
        else None,
    )


def launcher_base_command(info: RuntimeInfo) -> ShortcutCommand:
    if info.nuitka:
        return ShortcutCommand(info.argv0)
    if info.pyinstaller or info.frozen:
        return ShortcutCommand(info.executable)
    return ShortcutCommand(info.executable, (str(info.entry_file),))


def with_extra_args(command: ShortcutCommand, args: Iterable[str]) -> ShortcutCommand:
    return ShortcutCommand(command.target, (*command.arguments, *tuple(args)))


def build_direct_run_shortcut_command(
    info: RuntimeInfo, music_path: str | Path | None = None
) -> ShortcutCommand:
    args: list[str] = ["--direct-run"]
    if music_path:
        args.extend(["--music", str(music_path)])
    return with_extra_args(launcher_base_command(info), args)


def build_relaunch_command(
    info: RuntimeInfo, current_args: Sequence[str]
) -> ShortcutCommand:
    return with_extra_args(launcher_base_command(info), current_args)


def runtime_diagnostic_payload(
    info: RuntimeInfo, music_path: str | Path | None = None
) -> dict[str, object]:
    command = build_direct_run_shortcut_command(info, music_path)
    return {
        "runtime": {
            "sys_executable": str(info.executable),
            "sys_argv0": str(info.argv0),
            "__file__": str(info.entry_file),
            "entry_file": str(info.entry_file),
            "frozen": info.frozen,
            "pyinstaller": info.pyinstaller,
            "nuitka": info.nuitka,
            "meipass": str(info.meipass) if info.meipass else None,
            "compiled_containing_dir": str(info.compiled_containing_dir)
            if info.compiled_containing_dir
            else None,
            "original_argv0": info.original_argv0,
        },
        "shortcut": {
            "target": str(command.target),
            "arguments": command.arguments_text,
            "argument_list": list(command.arguments),
        },
    }


def write_runtime_diagnostic(
    output_path: str | Path, info: RuntimeInfo, music_path: str | Path | None = None
) -> None:
    payload = runtime_diagnostic_payload(info, music_path)
    try:
        from .assets import ensure_assets

        assets = ensure_assets()
        payload["assets"] = {
            "default_image": str(assets.default_image),
            "default_image_exists": assets.default_image.exists(),
            "icon": str(assets.icon),
            "icon_exists": assets.icon.exists(),
            "sound": str(assets.sound),
            "sound_exists": assets.sound.exists(),
            "backup_dir": str(assets.backup_dir),
        }
    except Exception as exc:
        payload["assets"] = {"error": str(exc)}

    Path(output_path).write_text(
        json.dumps(payload, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
