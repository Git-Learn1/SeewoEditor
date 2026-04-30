@echo off
setlocal
pushd "%~dp0\.."
python -m nuitka ^
  --mode=onefile ^
  --assume-yes-for-downloads ^
  --msvc=latest ^
  --enable-plugin=pyside6 ^
  --include-package-data=seewo_editor.resources ^
  --windows-console-mode=disable ^
  --windows-icon-from-ico=src\seewo_editor\resources\default_seewo_icon.ico ^
  --windows-uac-admin ^
  --output-dir=dist\nuitka-onefile ^
  --output-filename=swenIauncher.exe ^
  src\main.py
popd
