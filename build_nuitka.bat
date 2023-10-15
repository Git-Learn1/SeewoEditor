python -m pip install -r requirements.txt
echo 初始化一些东西，请关闭待会弹出的窗口
python seewoedit.py
python -m nuitka --onefile --windows-uac-admin seewoedit.py --output-filename="swenlauncher.exe" --disable-console --enable-plugin=pyside6 --enable-plugin=upx --windows-icon-from-ico=%appdata%\a.ico