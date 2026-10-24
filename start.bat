@echo off
REM PluginWeb 启动脚本（Windows）
setlocal
cd /d "%~dp0"

set ENV_DIR=server-env

echo ======================================
echo   PluginWeb 启动
echo ======================================

if not exist "%ENV_DIR%" (
  echo [1/3] 未找到虚拟环境，创建 %ENV_DIR% ...
  python -m venv "%ENV_DIR%"
  if errorlevel 1 (
    echo [错误] 创建虚拟环境失败，请确认已安装 Python 并加入 PATH。
    pause
    exit /b 1
  )
) else (
  echo [1/3] 使用现有虚拟环境 %ENV_DIR%
)

call "%ENV_DIR%\Scripts\activate.bat"

python -c "import flask" >nul 2>&1
if errorlevel 1 (
  echo [2/3] 安装依赖...
  python -m pip install --upgrade pip >nul
  python -m pip install -r requirements.txt
  if errorlevel 1 (
    echo [错误] 依赖安装失败。
    pause
    exit /b 1
  )
) else (
  echo [2/3] 依赖已就绪
)

echo [3/3] 启动服务...
echo.
python run.py

echo.
echo [PluginWeb] 服务已退出。
pause
endlocal
