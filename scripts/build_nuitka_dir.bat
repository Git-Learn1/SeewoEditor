@echo off
setlocal
pushd "%~dp0\.."
set "NUITKA_UPX_ARGS="
where upx >nul 2>nul
if errorlevel 1 (
  echo UPX not found; building without UPX.
) else (
  echo UPX found; enabling Nuitka UPX plugin.
  set "NUITKA_UPX_ARGS=--enable-plugin=upx"
)
python -m nuitka ^
  --mode=standalone ^
  --assume-yes-for-downloads ^
  --msvc=latest ^
  --enable-plugin=pyside6 ^
  %NUITKA_UPX_ARGS% ^
  --include-package-data=seewo_editor.resources ^
  --windows-console-mode=disable ^
  --windows-icon-from-ico=src\seewo_editor\resources\default_seewo_icon.ico ^
  --windows-uac-admin ^
  --output-dir=dist\nuitka-standalone ^
  --output-filename=swenIauncher.exe ^
  src\main.py
popd
