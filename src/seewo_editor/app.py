from __future__ import annotations

import ctypes
import sys
from pathlib import Path

from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import QApplication, QFileDialog, QMessageBox

from .assets import BuiltinAssets, backup_default_resources, ensure_assets
from .constants import (
    DEFAULT_MUSIC_LABEL,
    IMAGE_FILTER,
    MUSIC_FILTER,
    SEEWO_PROGRAM_FILTER,
    SHORTCUT_NAME,
)
from .file_ops import replace_images, restore_images
from .launcher import play_music, start_program, stop_seewo_process
from .runtime import (
    RuntimeInfo,
    ShortcutCommand,
    build_direct_run_shortcut_command,
    build_relaunch_command,
    current_runtime_info,
    write_runtime_diagnostic,
)
from .seewo import SeewoPaths, detect_seewo_paths
from .shortcut import create_shortcut, move_existing_shortcuts
from .ui import SEMain


class MainWindow(SEMain):
    def __init__(self, runtime_info: RuntimeInfo, music_path: str | None = None) -> None:
        super().__init__()
        self.runtime_info = runtime_info
        self.assets: BuiltinAssets = ensure_assets()
        self.paths: SeewoPaths = detect_seewo_paths()
        self.selected_image_path = self.assets.default_image
        self.music_path = music_path or ""

        self.btn_user_path.clicked.connect(self.choose_user_path)
        self.btn_path.clicked.connect(self.choose_path)
        self.btn_seewo_path.clicked.connect(self.choose_seewo_path)
        self.btn_music_path.clicked.connect(self.choose_music_path)
        self.btn_choose.clicked.connect(self.choose_pic)
        self.btn_use_default.clicked.connect(self.use_default_pic)
        self.btn_replace.clicked.connect(self.replace_pic)
        self.btn_lnk.clicked.connect(self.create_music_shortcut)
        self.btn_fix.clicked.connect(self.fix_seewo)
        self.btn_start.clicked.connect(self.start_seewo)

        self.populate_detected_paths()
        self.use_default_pic()
        if self.music_path:
            self.label_music_path.setText(self.music_path)

    def populate_detected_paths(self) -> None:
        if self.paths.system_image:
            self.label_path.setText(str(self.paths.system_image))
            backup_default_resources(self.paths.system_image, self.assets)
        if self.paths.launcher:
            self.label_seewo_path.setText(str(self.paths.launcher))
        self.label_user_path.setText(str(self.paths.user_image))
        if not self.paths.found_install:
            QMessageBox.warning(
                self,
                "警告",
                "未找到希沃安装！请自行选择系统希沃图片路径和程序路径，需要管理员权限进行替换或还原操作。",
            )

    def ensure_admin(self) -> None:
        if ctypes.windll.shell32.IsUserAnAdmin():
            return
        QMessageBox.warning(self, "警告", "将请求管理员权限")
        command = build_relaunch_command(self.runtime_info, sys.argv[1:])
        ctypes.windll.shell32.ShellExecuteW(
            None,
            "runas",
            str(command.target),
            command.arguments_text,
            None,
            1,
        )
        sys.exit(1)

    def choose_path(self) -> None:
        file_name, _ = QFileDialog.getOpenFileName(self, "选择图片", "", IMAGE_FILTER)
        if file_name:
            self.label_path.setText(file_name)

    def choose_pic(self) -> None:
        file_name, _ = QFileDialog.getOpenFileName(self, "选择图片", "", IMAGE_FILTER)
        if file_name:
            self.selected_image_path = Path(file_name)
            self.label_img.setPixmap(QPixmap(file_name))

    def choose_user_path(self) -> None:
        file_name, _ = QFileDialog.getOpenFileName(self, "选择图片", "", IMAGE_FILTER)
        if file_name:
            self.label_user_path.setText(file_name)

    def choose_seewo_path(self) -> None:
        file_name, _ = QFileDialog.getOpenFileName(
            self, "选择希沃软件位置(swenlauncher.exe)", "", SEEWO_PROGRAM_FILTER
        )
        if file_name:
            self.label_seewo_path.setText(file_name)

    def choose_music_path(self) -> None:
        file_name, _ = QFileDialog.getOpenFileName(self, "选择音乐", "", MUSIC_FILTER)
        if file_name:
            self.music_path = file_name
            self.label_music_path.setText(file_name)

    def use_default_pic(self) -> None:
        self.selected_image_path = self.assets.default_image
        self.label_img.setPixmap(QPixmap(str(self.selected_image_path)))

    def replace_pic(self) -> None:
        QMessageBox.warning(
            self,
            "警告",
            "原图片将备份到 SeewoEditor 的备份目录，如有重复文件将会覆盖！需要管理员权限执行此操作。",
        )
        self.ensure_admin()
        try:
            replace_images(
                self.label_path.text(),
                self.label_user_path.text(),
                self.selected_image_path,
                self.assets.backup_dir,
            )
        except Exception as exc:
            QMessageBox.critical(self, "错误", str(exc))
            return
        QMessageBox.information(self, "提示", "替换成功！")

    def _selected_music_path(self) -> str | None:
        if self.label_music_path.text() in ("", DEFAULT_MUSIC_LABEL):
            return None
        return self.music_path or self.label_music_path.text()

    def create_music_shortcut(self) -> None:
        QMessageBox.warning(self, "警告", "原快捷方式将被移动到临时目录，如需恢复请从开始菜单重新复制一个至桌面。")
        self.ensure_admin()
        command = build_direct_run_shortcut_command(
            self.runtime_info, self._selected_music_path()
        )
        move_existing_shortcuts(self.paths.shortcut_desktop)
        create_shortcut(
            self.paths.current_user_desktop / SHORTCUT_NAME,
            command,
            self.assets.icon,
        )
        QMessageBox.information(self, "提示", "替换成功！")

    def fix_seewo(self) -> None:
        QMessageBox.warning(self, "警告", "这将使图片和桌面快捷方式恢复至原来的情况！")
        self.ensure_admin()
        try:
            restore_images(
                self.label_path.text(),
                self.label_user_path.text(),
                self.assets.original_backup,
            )
            launcher = Path(self.label_seewo_path.text())
            if not launcher.exists():
                raise FileNotFoundError(f"希沃程序不存在：{launcher}")
            move_existing_shortcuts(self.paths.shortcut_desktop)
            create_shortcut(
                self.paths.current_user_desktop / SHORTCUT_NAME,
                ShortcutCommand(launcher),
                self.assets.icon,
            )
        except Exception as exc:
            QMessageBox.critical(self, "错误", str(exc))
            return
        QMessageBox.information(self, "提示", "修复成功！")

    def start_seewo(self) -> None:
        try:
            stop_seewo_process()
            start_program(self.label_seewo_path.text())
            play_music(self.music_path or self.assets.sound)
        except Exception as exc:
            QMessageBox.critical(self, "错误", str(exc))


def _value_after(argv: list[str], option: str) -> str | None:
    if option not in argv:
        return None
    index = argv.index(option)
    if index + 1 >= len(argv):
        return None
    return argv[index + 1]


def main(entry_file: str | Path | None = None, argv: list[str] | None = None) -> int:
    argv = list(sys.argv[1:] if argv is None else argv)
    entry = Path(entry_file) if entry_file is not None else Path(__file__)
    runtime_info = current_runtime_info(entry)

    diagnose_path = _value_after(argv, "--diagnose-runtime")
    if diagnose_path:
        write_runtime_diagnostic(
            diagnose_path,
            runtime_info,
            _value_after(argv, "--music"),
        )
        return 0

    app = QApplication(sys.argv)
    window = MainWindow(runtime_info, _value_after(argv, "--music"))

    if "--direct-run" in argv:
        window.start_seewo()
        return 0
    if "--quick-fix" in argv:
        window.fix_seewo()
        return 0
    if "--replace-pic" in argv:
        window.replace_pic()
        return 0
    if "--replace-shortcut" in argv:
        window.create_music_shortcut()
        return 0

    window.show()
    return app.exec()
