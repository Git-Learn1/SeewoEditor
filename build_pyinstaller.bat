python -m pip install -r requirements.txt
echo 初始化一些东西，请关闭待会弹出的窗口
python seewoedit.py
python -m PyInstaller -F -w --uac-admin seewoedit.py --disable-console --enable-plugin=pyside6 --enable-plugin=upx -i %appdata%\a.ico
move dist\seewoedit.exe swenlauncher.exe