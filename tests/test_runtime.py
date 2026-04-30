import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from seewo_editor.runtime import (  # noqa: E402
    RuntimeInfo,
    build_direct_run_shortcut_command,
    build_relaunch_command,
)


class RuntimeCommandTests(unittest.TestCase):
    def test_source_shortcut_uses_python_with_entry_script(self):
        info = RuntimeInfo(
            executable=Path(r"C:\Python312\python.exe"),
            argv0=Path(r"D:\repo\src\main.py"),
            entry_file=Path(r"D:\repo\src\main.py"),
        )

        command = build_direct_run_shortcut_command(info)

        self.assertEqual(command.target, Path(r"C:\Python312\python.exe"))
        self.assertEqual(
            command.arguments,
            (r"D:\repo\src\main.py", "--direct-run"),
        )

    def test_pyinstaller_shortcut_uses_sys_executable(self):
        info = RuntimeInfo(
            executable=Path(r"D:\dist\swenIauncher.exe"),
            argv0=Path(r".\swenIauncher.exe"),
            entry_file=Path(r"C:\Temp\_MEI12345\main.py"),
            frozen=True,
            pyinstaller=True,
            meipass=Path(r"C:\Temp\_MEI12345"),
        )

        command = build_direct_run_shortcut_command(info, r"D:\Music\start sound.mp3")

        self.assertEqual(command.target, Path(r"D:\dist\swenIauncher.exe"))
        self.assertEqual(
            command.arguments,
            ("--direct-run", "--music", r"D:\Music\start sound.mp3"),
        )
        self.assertIn('"D:\\Music\\start sound.mp3"', command.arguments_text)

    def test_nuitka_onefile_shortcut_uses_original_argv0(self):
        info = RuntimeInfo(
            executable=Path(r"C:\Users\me\AppData\Local\Temp\onefile_1\swenIauncher.exe"),
            argv0=Path(r"D:\dist\swenIauncher.exe"),
            entry_file=Path(r"C:\Users\me\AppData\Local\Temp\onefile_1\main.py"),
            nuitka=True,
        )

        command = build_direct_run_shortcut_command(info)

        self.assertEqual(command.target, Path(r"D:\dist\swenIauncher.exe"))
        self.assertNotIn("onefile_1", str(command.target))

    def test_nuitka_standalone_shortcut_uses_argv0(self):
        info = RuntimeInfo(
            executable=Path(r"D:\dist\main.dist\swenIauncher.exe"),
            argv0=Path(r"D:\dist\main.dist\swenIauncher.exe"),
            entry_file=Path(r"D:\dist\main.dist\main.py"),
            nuitka=True,
        )

        command = build_direct_run_shortcut_command(info)

        self.assertEqual(command.target, Path(r"D:\dist\main.dist\swenIauncher.exe"))

    def test_relaunch_preserves_args(self):
        info = RuntimeInfo(
            executable=Path(r"C:\Python312\python.exe"),
            argv0=Path(r"D:\repo\src\main.py"),
            entry_file=Path(r"D:\repo\src\main.py"),
        )

        command = build_relaunch_command(info, ["--replace-shortcut", "--music", "a b.mp3"])

        self.assertEqual(
            command.arguments,
            (r"D:\repo\src\main.py", "--replace-shortcut", "--music", "a b.mp3"),
        )


if __name__ == "__main__":
    unittest.main()
