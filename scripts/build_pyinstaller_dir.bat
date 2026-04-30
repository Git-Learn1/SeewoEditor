@echo off
setlocal
pushd "%~dp0\.."
python -m PyInstaller ^
  --noconfirm ^
  --clean ^
  --noupx ^
  --onedir ^
  --windowed ^
  --name swenIauncher ^
  --icon src\seewo_editor\resources\default_seewo_icon.ico ^
  --add-data "src\seewo_editor\resources;seewo_editor\resources" ^
  --uac-admin ^
  src\main.py
popd
