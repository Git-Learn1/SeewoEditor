python -m pip install -r requirements.txt
echo ��ʼ��һЩ��������رմ��ᵯ���Ĵ���
python seewoedit.py
taskkill /f /im EasiNote.exe /t
taskkill /f /im EasiNote5.exe /t
python -m PyInstaller -w seewoedit.py -i se\data\inside\a.ico
move dist\seewoedit\seewoedit.exe dist\seewoedit\swenlauncher.exe