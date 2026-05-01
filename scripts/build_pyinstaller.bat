@echo off
setlocal
pushd "%~dp0\.."
set "PYINSTALLER_UPX_ARGS="
where upx >nul 2>nul
if errorlevel 1 (
  echo UPX not found; building without UPX.
  set "PYINSTALLER_UPX_ARGS=--noupx"
) else (
  echo UPX found; PyInstaller will use UPX where supported.
)
python -m PyInstaller ^
  --noconfirm ^
  --clean ^
  %PYINSTALLER_UPX_ARGS% ^
  --onefile ^
  --windowed ^
  --name swenIauncher ^
  --icon src\seewo_editor\resources\default_seewo_icon.ico ^
  --add-data "src\seewo_editor\resources;seewo_editor\resources" ^
  --uac-admin ^
  src\main.py
popd
