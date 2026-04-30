from __future__ import annotations

import subprocess
from pathlib import Path

from pydub import AudioSegment
from pydub.playback import play


def stop_seewo_process() -> None:
    subprocess.run(
        ["taskkill", "/f", "/im", "EasiNote.exe", "/t"],
        check=False,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )


def start_program(program_path: str | Path) -> None:
    program = Path(program_path)
    if not program.exists():
        raise FileNotFoundError(f"希沃程序不存在：{program}")
    subprocess.Popen([str(program)])


def play_music(music_path: str | Path) -> None:
    music = Path(music_path)
    if not music.exists():
        raise FileNotFoundError(f"音乐文件不存在：{music}")
    audio = AudioSegment.from_file(str(music), format=music.suffix.lstrip("."))
    play(audio)
