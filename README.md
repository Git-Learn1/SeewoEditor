# SeewoEditor

一个用于替换希沃白板启动图片，并可通过桌面快捷方式播放启动音乐的小工具。

> 这是一个旧个人项目的维护性重构版本。当前重点是清理代码结构、修复明显问题，并恢复 PyInstaller / Nuitka 两套打包流程。

## 功能

- 替换系统启动图片和用户 Banner 图片。
- 备份并还原原始图片。
- 创建带 `--direct-run` 参数的桌面快捷方式，用于启动希沃并播放音乐。
- 支持自定义启动音乐。
- 提供运行时诊断参数，用于验证打包后快捷方式目标路径。

## 运行

```powershell
pip install -r requirements.txt
python src\main.py
```

命令行入口保持兼容：

```powershell
python src\main.py --direct-run
python src\main.py --quick-fix
python src\main.py --replace-pic
python src\main.py --replace-shortcut
python src\main.py --direct-run --music "D:\Music\start.mp3"
```

## 打包

所有脚本都应从仓库根目录或 `scripts` 目录运行。Nuitka 需要可用的 Visual Studio 2022 / MSVC 编译环境；首次运行会自动下载 Dependency Walker 到 Nuitka 的用户缓存。

```powershell
scripts\build_pyinstaller.bat
scripts\build_pyinstaller_dir.bat
scripts\build_nuitka.bat
scripts\build_nuitka_dir.bat
```

产物说明：

- PyInstaller 单文件：`dist\swenIauncher.exe`
- PyInstaller 目录版：`dist\swenIauncher\swenIauncher.exe`
- Nuitka 单文件：`dist\nuitka-onefile\swenIauncher.exe`
- Nuitka 目录版：`dist\nuitka-standalone\main.dist\swenIauncher.exe`

GitHub Actions 会在每次 push 时构建上述四种产物：

- Actions artifacts 使用 commit SHA 命名，便于按 commit 找回产物。
- 同一批产物也会发布到 `nightly build` prerelease，release tag 为 `nightly-build`。
- Nightly release 会随新 commit 移动并覆盖旧资产，只保留最新构建。

## 打包路径验证

创建快捷方式时不再直接使用旧代码里的 `sys.argv[0]`。

- PyInstaller frozen 环境使用 `sys.executable`，因为它指向用户实际启动的 exe。
- Nuitka 环境使用 `sys.argv[0]`，避免 onefile 模式把临时解包路径写入快捷方式。
- 源码运行时使用 Python 解释器作为 TargetPath，并把 `src\main.py` 放入 Arguments。

可用隐藏诊断参数输出实际运行时信息：

```powershell
dist\swenIauncher.exe --diagnose-runtime runtime.json
```

诊断文件会包含 `sys.executable`、`sys.argv[0]`、`__file__` 相关推导结果和最终快捷方式 TargetPath / Arguments。
同时会检查内置图片、图标、音频是否能从打包资源落盘。

## 测试

```powershell
python -m compileall src
python -m unittest discover
```

## 说明

项目仅面向 Windows。替换系统图片、还原和创建公共桌面快捷方式可能需要管理员权限。
