#!/usr/bin/env bash
# PluginWeb 启动脚本（Linux / termux / macOS）
set -e
cd "$(dirname "$0")"

ENV_DIR="server-env"
PY="${PYTHON:-python3}"
if ! command -v "$PY" >/dev/null 2>&1; then
  PY=python
fi

echo "======================================"
echo "  PluginWeb 启动"
echo "======================================"

if [ ! -d "$ENV_DIR" ]; then
  echo "[1/3] 未找到虚拟环境，创建 $ENV_DIR ..."
  "$PY" -m venv "$ENV_DIR"
else
  echo "[1/3] 使用现有虚拟环境 $ENV_DIR"
fi

# shellcheck disable=SC1091
source "$ENV_DIR/bin/activate"

if ! python -c "import flask" >/dev/null 2>&1; then
  echo "[2/3] 安装依赖..."
  pip install --upgrade pip >/dev/null
  pip install -r requirements.txt
else
  echo "[2/3] 依赖已就绪"
fi

echo "[3/3] 启动服务..."
echo
exec python run.py
