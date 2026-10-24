# XfPluginWeb

一个带 Web 界面的可扩展插件运行环境。插件以 .xfpe / .xfpn（Zip）形式导入，
可在 shell / Python / JAVA 环境下运行脚本。启动时进行依赖与冲突校验，
不满足则直接中止启动。

## 特性
- 多任务栏 Web 界面：插件管理、导入、运行、Shell 终端
- 插件包：.xfpe / .xfpn（本质 Zip），data 下对应 xfpe.cfg / xfpn.cfg
- 依赖与不兼容校验：rely_on / not_compatible，格式 ID+版本，逗号分隔，* 表示任意版本
- 启动校验失败即报错并中止，不启动 Web 服务
- 自动打开浏览器，默认端口 8888

## 安装（termux / Linux）
1. 创建虚拟环境：python -m venv server-env
2. 激活：source server-env/bin/activate
3. 安装依赖：pip install -r requirements.txt
4. 启动：python run.py

## 插件开发
详见 docs/PLUGIN_FORMAT.md。要点：
- 包结构：assets/、script/、data/（含 xfpe.cfg 或 xfpn.cfg）
- script 入口约定 main.py / main.sh / main.jar，由 environment 决定
- 配置字段：author、id、version、name、type、not_compatible、environment、rely_on

## 许可证
本项目采用 CC BY-NC-SA 4.0。修改后必须以同样方式开放，且不得用于商业用途。
详见 LICENSE。
