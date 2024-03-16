python -m pip install -r requirements.txt
echo 初始化一些东西，请关闭待会弹出的窗口
python seewoedit.py
taskkill /f /im EasiNote.exe /t
taskkill /f /im EasiNote5.exe /t
echo 如果编译失败，请安装Visual Studio 2022并打开x64 Native Tools Command Prompt for VS 2022，后运行此脚本
python -m nuitka --standalone --msvc=14.3 seewoedit.py --output-filename="swenlauncher.exe" --disable-console --enable-plugin=pyside6 --enable-plugin=upx --windows-icon-from-ico=se\data\inside\a.ico