"""全局配置常量。"""
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PLUGINS_DIR = os.path.join(BASE_DIR, "plugins")
HOST = "127.0.0.1"
PORT = 8888

# 入口脚本探测顺序（按 environment 分组）
ENTRY_CANDIDATES = {
    "Python": ["main.py"],
    "shell": ["main.sh"],
    "JAVA": ["main.jar", "main.class"],
    "PHP": ["main.php"],
}
# 兜底：environment 未匹配时按此顺序找任意入口
FALLBACK_ENTRIES = ["main.sh", "main.jar", "main.class", "main.py", "main.php"]

RUN_TIMEOUT = 30
