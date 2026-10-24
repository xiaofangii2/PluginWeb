"""按 environment 探测入口脚本并执行。"""
import os
import subprocess
from .config import ENTRY_CANDIDATES, FALLBACK_ENTRIES, RUN_TIMEOUT


def detect_entry(script_dir, environment):
    """返回 (entry_filename, cmd_prefix_list) 或 (None, None)。"""
    candidates = ENTRY_CANDIDATES.get(environment, []) + FALLBACK_ENTRIES
    seen = set()
    for entry in candidates:
        if entry in seen:
            continue
        seen.add(entry)
        if os.path.isfile(os.path.join(script_dir, entry)):
            return entry, build_cmd(entry)
    return None, None


def build_cmd(entry):
    if entry.endswith(".py"):
        return ["python", entry]
    if entry.endswith(".sh"):
        return ["sh", entry]
    if entry.endswith(".jar"):
        return ["java", "-jar", entry]
    if entry.endswith(".class"):
        cls = entry[:-6]
        return ["java", cls]
    if entry.endswith(".php"):
        return ["php", entry]
    return None


def run_plugin(info):
    script_dir = os.path.join(info["path"], "script")
    if not os.path.isdir(script_dir):
        return {"error": "缺少 script 目录"}
    env = info["cfg"].get("environment", "")
    entry, cmd = detect_entry(script_dir, env)
    if not entry:
        return {"error": "未找到入口脚本（main.sh/jar/class/py/php）"}
    if not cmd:
        return {"error": f"无法识别的入口类型: {entry}"}
    try:
        result = subprocess.run(
            cmd, cwd=script_dir, capture_output=True, text=True, timeout=RUN_TIMEOUT
        )
        return {
            "entry": entry,
            "stdout": result.stdout,
            "stderr": result.stderr,
            "returncode": result.returncode,
        }
    except subprocess.TimeoutExpired:
        return {"error": "执行超时"}
    except Exception as e:
        return {"error": str(e)}
