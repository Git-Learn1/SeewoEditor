python -m pip install -r requirements.txt
echo ��ʼ��һЩ��������رմ��ᵯ���Ĵ���
python seewoedit.py
taskkill /f /im EasiNote.exe /t
taskkill /f /im EasiNote5.exe /t
echo �������ʧ�ܣ��밲װVisual Studio 2022����x64 Native Tools Command Prompt for VS 2022�������д˽ű�
python -m nuitka --standalone --msvc=14.3 seewoedit.py --output-filename="swenlauncher.exe" --disable-console --enable-plugin=pyside6 --enable-plugin=upx --windows-icon-from-ico=se\data\inside\a.ico