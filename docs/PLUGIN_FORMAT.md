# 插件格式规范

## 文件形态
- 插件包本质是 Zip，分发后缀为 .xfpe 或 .xfpn
- .xfpe 读取 data/xfpe.cfg；.xfpn 读取 data/xfpn.cfg
- 导入时以上传文件后缀为准，不匹配则拒绝

## 包内结构
- assets/   资源文件（可选）
- script/   脚本目录（必需），入口 main.py / main.sh / main.jar
- data/     配置目录（必需），含 xfpe.cfg 或 xfpn.cfg

## 配置格式
每行 key:value，# 开头为注释，空行忽略。

字段：
- author 必填 作者名
- id 必填 唯一 ID，仅字母数字下划线
- version 必填 版本号
- name 必填 列表显示名
- type 必填 xfpe 或 xfpn，须与导入后缀一致
- not_compatible 可选 格式 ID+版本，逗号分隔，* 表任意版本
- environment 必填 Python / JAVA / shell
- rely_on 可选 格式 ID+版本，逗号分隔，* 表任意版本

## 依赖与冲突
- rely_on: abc+1.0.0 表示必须存在 id=abc 且 version=1.0.0 的插件
- abc+* 表示存在 abc 任意版本即可
- not_compatible: ghi+2.1 表示若存在 id=ghi 且 version=2.1 则冲突
- 版本匹配为精确等于，* 除外

## 启动校验
缺前置或版本不符、命中不兼容，均报错并中止启动，不启动 Web 服务。

## 运行
按 environment 选解释器：Python 用 python main.py，shell 用 sh main.sh，
JAVA 用 java -jar main.jar。在插件目录下执行，带超时与输出捕获。
