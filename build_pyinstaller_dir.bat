python -m pip install -r requirements.txt
echo 初始化一些东西，请关闭待会弹出的窗口
python seewoedit.py
python -m PyInstaller -w --uac-admin seewoedit.py -i %appdata%\a.ico