@echo off
setlocal enabledelayedexpansion
chcp 65001 >nul

set "BASE_DIR=%~dp0"
set "PYTHON_EXE=%BASE_DIR%python\pythonw.exe"
set "SCRIPT=%BASE_DIR%gui_ytdlp.py"
set "BIN_DIR=%BASE_DIR%bin"

title yt-dlp 万能下载工具

if not exist "%PYTHON_EXE%" (
    echo.
    echo [错误] 找不到内置 Python: %PYTHON_EXE%
    echo 请确认 python 文件夹是否存在
    echo.
    pause
    exit /b 1
)

if not exist "%BIN_DIR%\yt-dlp.exe" (
    echo.
    echo [警告] 缺少核心文件：bin\yt-dlp.exe
    echo 下载功能将无法正常工作
    echo.
)

echo 正在启动图形界面...
echo 当前目录：%BASE_DIR%

start "" /b "%PYTHON_EXE%" "%SCRIPT%"

exit