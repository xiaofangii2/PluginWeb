"""Flask 应用与路由。"""
import subprocess
from flask import Flask, request, jsonify, render_template
from .config import RUN_TIMEOUT
from .plugin_loader import scan_plugins, import_plugin
from .plugin_runner import run_plugin

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/plugins")
def api_plugins():
    plugins = scan_plugins()
    items = []
    for pid, info in plugins.items():
        cfg = info["cfg"]
        items.append({
            "id": pid,
            "name": cfg.get("name", pid),
            "version": cfg.get("version", ""),
            "author": cfg.get("author", ""),
            "type": cfg.get("type", ""),
            "environment": cfg.get("environment", ""),
            "rely_on": cfg.get("rely_on", ""),
            "not_compatible": cfg.get("not_compatible", ""),
        })
    return jsonify(items)


@app.route("/api/import", methods=["POST"])
def api_import():
    f = request.files.get("file")
    if not f:
        return jsonify({"ok": False, "msg": "未选择文件"}), 400
    ok, msg = import_plugin(f)
    return jsonify({"ok": ok, "msg": msg}), (200 if ok else 400)


@app.route("/api/run/<pid>", methods=["POST"])
def api_run(pid):
    plugins = scan_plugins()
    if pid not in plugins:
        return jsonify({"error": "插件不存在"}), 404
    return jsonify(run_plugin(plugins[pid]))


@app.route("/api/shell", methods=["POST"])
def api_shell():
    data = request.get_json() or {}
    cmd = data.get("cmd", "")
    if not cmd:
        return jsonify({"error": "空命令"}), 400
    try:
        r = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=RUN_TIMEOUT)
        return jsonify({"stdout": r.stdout, "stderr": r.stderr, "returncode": r.returncode})
    except subprocess.TimeoutExpired:
        return jsonify({"error": "执行超时"}), 500
