"""启动入口：校验插件，通过则启动 Web 服务。"""
import sys
import logging
from pluginweb.config import HOST, PORT
from pluginweb.plugin_loader import scan_plugins, validate_plugins

C_RESET = "\033[0m"
C_GREEN = "\033[32m"
C_RED = "\033[31m"
C_YELLOW = "\033[33m"
C_CYAN = "\033[36m"
C_GRAY = "\033[90m"
C_BOLD = "\033[1m"

TAG = f"{C_CYAN}{C_BOLD}[PluginWeb]{C_RESET}"


def main():
    plugins = scan_plugins()
    print(f"{TAG} 已加载插件: {C_GREEN}{len(plugins)}{C_RESET}")

    errors = validate_plugins(plugins)
    if errors:
        for e in errors:
            print(f"{TAG} {C_RED}{e}{C_RESET}")
        print(f"{TAG} {C_YELLOW}校验未通过，服务未启动。{C_RESET}")
        sys.exit(1)

    # 关闭 Flask/Werkzeug 默认日志与启动横幅
    logging.getLogger("werkzeug").setLevel(logging.ERROR)
    import flask.cli
    flask.cli.show_server_banner = lambda *args, **kwargs: None

    from pluginweb.app import app

    url = f"http://{HOST}:{PORT}/"
    print()
    print(f"  {C_GREEN}{C_BOLD}PluginWeb 服务已启动{C_RESET}")
    print(f"  {C_GRAY}地址:{C_RESET} {C_CYAN}{url}{C_RESET}")
    print(f"  {C_GRAY}按 Ctrl+C 停止服务{C_RESET}")
    print()

    app.run(host=HOST, port=PORT, debug=False, use_reloader=False)


if __name__ == "__main__":
    main()
