# -*- coding: utf-8 -*-

import ctypes
import sys
import winreg
import shutil
import os
import stat
import pyaudio
import subprocess
from win32com.client import Dispatch
from pydub import AudioSegment
from pydub.playback import play
from data import pil_img, fix_pil_img, icon_path, sound
from ui_seewoedit import SEMain
from PySide6.QtWidgets import QMessageBox, QFileDialog, QApplication
from PySide6.QtGui import QPixmap


INK = "希沃白板 5.lnk"
EXT = "图片文件(*.png)"


class MainWindow(SEMain):
    def __init__(self):
        super().__init__()
        self.btn_user_path.clicked.connect(self.choose_user_path)
        self.btn_path.clicked.connect(self.choose_path)
        self.btn_seewo_path.clicked.connect(self.choose_seewo_path)
        self.btn_music_path.clicked.connect(self.choose_music_path)
        self.btn_choose.clicked.connect(self.choose_pic)
        self.btn_use_default.clicked.connect(self.use_default_pic)
        self.btn_replace.clicked.connect(self.replace_pic)
        self.btn_lnk.clicked.connect(self.create_shortcut)
        self.btn_fix.clicked.connect(self.fix_seewo)
        self.btn_start.clicked.connect(self.start_seewo)
        
        self.music_path = ""
        if "--music" in sys.argv:
            self.music_path = sys.argv[-1]
            self.label_music_path.setText(sys.argv[-1])
        
        self.find_seewo()
        self.use_default_pic()
        
    def get_admin(self):
        if not ctypes.windll.shell32.IsUserAnAdmin():
            QMessageBox.warning(self, "警告", "将请求管理员权限")
            ctypes.windll.shell32.ShellExecuteW(
                None, "runas", sys.executable, __file__)

    def find_seewo(self):
        try:
            reg = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE,
                                 r"SOFTWARE\Wow6432Node\Seewo\EasiNote5")
            reg2 = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, 
                                  r"SOFTWARE\classes\easinote")
            path_t = winreg.QueryValueEx(reg, "VersionPath")[0]
            self.seewo_program_dir = os.path.dirname(path_t)
            path = os.path.join(path_t, r"Main\Assets\SplashScreen.png")
            path2 = os.path.join(path_t, r"Main\Resources\Startup\SplashScreen.png")
            self.seewo_path = winreg.QueryValueEx(reg2, "URL Protocol")[0]
            if os.path.exists(path):
                self.label_path.setText(path)
            elif os.path.exists(path2):
                self.label_path.setText(path2)
            self.label_seewo_path.setText(self.seewo_path)
            reg.Close()
        except FileNotFoundError:
            QMessageBox.warning(self, "警告", "未找到希沃安装！请自行选择系统希沃图片路径，需要管理员权限进行下一步操作")
            if not ctypes.windll.shell32.IsUserAnAdmin():
                self.get_admin()
            pgdir = "programfiles(x86)" if "PROGRAMFILES(X86)" in [i.upper() for i in os.environ] else "programfiles"
            self.seewo_program_dir = os.path.join(os.getenv(pgdir), r"Seewo\EasiNote5") # type: ignore
            if not os.path.exists(self.seewo_program_dir):
                os.makedirs(self.seewo_program_dir)
            self.seewo_path = os.path.join(self.seewo_program_dir, r"swenlauncher\swenlauncher.exe")
        path = os.path.join(os.getenv("APPDATA"), r"Seewo\EasiNote5\Resources\Banner") # type: ignore
        if not os.path.exists(path):
            os.makedirs(path)
        path += "\\Banner.png"
        self.label_user_path.setText(path)
        self.desktop_path_cu = winreg.QueryValueEx(winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer\Shell Folders"), "DESKTOP")[0]
        self.desktop_path = winreg.QueryValueEx(winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer\Shell Folders"), "COMMON DESKTOP")[0]
        if not os.path.exists(os.path.join(self.desktop_path, INK)) and  not os.path.exists(os.path.join(self.desktop_path, "希沃白板.lnk")):
            self.desktop_path = self.desktop_path_cu
        
    def choose_path(self):
        file_name, _ = QFileDialog.getOpenFileName(
            self, "选择图片", "", EXT)
        if file_name:
            self.label_path.setText(file_name)

    def choose_pic(self):
        self.file_name, _ = QFileDialog.getOpenFileName(
            self, "选择图片", "", EXT)
        if self.file_name:
            self.label_img.setPixmap(QPixmap(self.file_name))
            
    def choose_user_path(self):
        file_name, _ = QFileDialog.getOpenFileName(
            self, "选择图片", "", EXT)
        if self.file_name:
            self.label_user_path.setText(file_name)

    def choose_seewo_path(self):
        file_name, _ = QFileDialog.getOpenFileName(
            self, "选择希沃软件位置(swenlauncher.exe)", "", "应用程序(swenlauncher.exe)")
        if self.file_name:
            self.label_user_path.setText(file_name)

    def choose_music_path(self):
        file_name, _ = QFileDialog.getOpenFileName(
            self, "选择音乐", "", "音乐文件(*.wav *.mp3)")
        if self.file_name:
            self.music_path = file_name
            self.label_music_path.setText(file_name)

    def use_default_pic(self):
        self.file_name = os.path.join(os.getenv("TEMP"), "t.png") # type: ignore
        pil_img.save(self.file_name)
        self.label_img.setPixmap(QPixmap(self.file_name))
        self.file_name_fix = os.path.join(os.getenv("TEMP"), "f.png") # type: ignore
        fix_pil_img.save(self.file_name_fix)

    def replace_pic(self):
        QMessageBox.warning(
            self, "警告", "原图片将备份为 xxx.bak ，如有重复文件将会覆盖！需要管理员权限执行此操作")
        self.get_admin()
        os.chmod(self.label_path.text(), stat.S_IWRITE)
        os.chmod(self.label_user_path.text(), stat.S_IWRITE)
        shutil.copy(self.label_path.text(), self.label_path.text() + ".bak")
        shutil.copy(self.file_name, self.label_path.text())
        shutil.copy(self.label_user_path.text(), self.label_user_path.text() + ".bak")
        shutil.copy(self.file_name, self.label_user_path.text())
        os.chmod(self.label_path.text(), stat.S_IREAD)
        os.chmod(self.label_user_path.text(), stat.S_IREAD)
        QMessageBox.information(self, "提示", "替换成功！")
    
    def create_shortcut(self):
        QMessageBox.warning(self, "警告", "原快捷方式将被删除，如需恢复请从开始菜单重新复制一个至桌面")
        self.get_admin()
        try:
            shutil.move(os.path.join(self.desktop_path, INK), os.path.join(os.getenv("TEMP"), INK)) # type: ignore
        except (OSError):
            pass
        shell = Dispatch("WScript.Shell")
        shortcut = shell.CreateShortcut(os.path.join(self.desktop_path_cu, INK))
        # 我说我是希沃白板你信吗
        shortcut.TargetPath = sys.argv[0]
        if self.label_music_path.text() == "（可选）自定义音乐" or self.label_music_path.text() == "":
            shortcut.Arguments = "--direct-run"
        else:
            shortcut.Arguments = "--direct-run" + f" --music {self.music_path}"
        shortcut.IconLocation = icon_path
        shortcut.Save()
        QMessageBox.information(self, "提示", "替换成功！")

    def fix_seewo(self):
        QMessageBox.warning(self, "警告", "这将使一切恢复至原来的情况！")
        self.get_admin()
        os.chmod(self.label_path.text(), stat.S_IWRITE)
        os.chmod(self.label_user_path.text(), stat.S_IWRITE)
        shutil.copy(self.label_path.text(), self.label_path.text() + ".bak")
        shutil.copy(self.file_name_fix, self.label_path.text())
        shutil.copy(self.label_user_path.text(), self.label_user_path.text() + ".bak")
        shutil.copy(self.file_name_fix, self.label_user_path.text())
        try:
            shutil.move(os.path.join(self.desktop_path, INK), os.path.join(os.getenv("TEMP"), INK)) # type: ignore
        except (OSError):
            pass
        shell = Dispatch("WScript.Shell")
        shortcut = shell.CreateShortcut(os.path.join(self.desktop_path_cu, INK))
        shortcut.TargetPath = self.seewo_path
        shortcut.IconLocation = icon_path
        shortcut.Save()
        QMessageBox.information(self, "提示", "修复成功！")
        
    def start_seewo(self):
        os.system("taskkill /f /im EasiNote.exe /t")
        subprocess.call(self.seewo_path)
        if not self.music_path:
            p = pyaudio.PyAudio()
            stream = p.open(format=p.get_format_from_width(2), channels=2, rate=44100, output=True)
            stream.write(sound)
            stream.stop_stream()
            stream.close()
            p.terminate()
        else:
            audio = AudioSegment.from_file(self.music_path, format=self.music_path.split(".")[-1])
            play(audio)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    if "--direct-run" in sys.argv:
        window.start_seewo()
        sys.exit(0)
    if "--quick-fix" in sys.argv:
        window.fix_seewo()
        sys.exit(0)
    if "--replace-pic" in sys.argv:
        window.replace_pic()
        sys.exit(0)
    if "--replace-shortcut" in sys.argv:
        window.create_shortcut()
        sys.exit(0)
    window.show()
    sys.exit(app.exec())
