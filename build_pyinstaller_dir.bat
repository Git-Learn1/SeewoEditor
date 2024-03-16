python -m pip install -r requirements.txt
echo 初始化一些东西，请关闭待会弹出的窗口
python seewoedit.py
taskkill /f /im EasiNote.exe /t
taskkill /f /im EasiNote5.exe /t
python -m PyInstaller -w seewoedit.py -i se\data\inside\a.ico
move dist\seewoedit\seewoedit.exe dist\seewoedit\swenlauncher.exe