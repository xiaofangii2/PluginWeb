"""插件扫描、配置解析、依赖与冲突校验。"""
import os
import zipfile
import shutil
from .config import PLUGINS_DIR

CFG_BY_SUFFIX = {".xfpe": "xfpe.cfg", ".xfpn": "xfpn.cfg"}


def parse_cfg(path):
    """解析 key:value 配置，返回 dict。"""
    data = {}
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            if ":" not in line:
                continue
            k, v = line.split(":", 1)
            data[k.strip()] = v.strip()
    return data


def parse_pairs(value):
    """把 'id+ver,id2+*' 解析为 [(id, ver), ...]。"""
    pairs = []
    if not value:
        return pairs
    for item in value.split(","):
        item = item.strip()
        if not item or "+" not in item:
            continue
        pid, ver = item.rsplit("+", 1)
        pairs.append((pid.strip(), ver.strip()))
    return pairs


def scan_plugins():
    """扫描 plugins 目录，返回 {id: {cfg, path}}。"""
    result = {}
    if not os.path.isdir(PLUGINS_DIR):
        return result
    for name in os.listdir(PLUGINS_DIR):
        pdir = os.path.join(PLUGINS_DIR, name)
        if not os.path.isdir(pdir):
            continue
        for cfg_name in ("xfpe.cfg", "xfpn.cfg"):
            cfg_path = os.path.join(pdir, "data", cfg_name)
            if os.path.isfile(cfg_path):
                cfg = parse_cfg(cfg_path)
                pid = cfg.get("id", name)
                result[pid] = {"cfg": cfg, "path": pdir}
                break
    return result


def validate_plugins(plugins):
    """校验依赖与不兼容，返回错误信息列表。"""
    errors = []
    for pid, info in plugins.items():
        cfg = info["cfg"]
        name = cfg.get("name", pid)
        for dep_id, dep_ver in parse_pairs(cfg.get("rely_on", "")):
            dep = plugins.get(dep_id)
            if not dep:
                errors.append(
                    f"插件 '{name}'({pid}) 需要前置插件 '{dep_id}' 的版本 {dep_ver}，当前未找到或版本不符。启动中止。"
                )
                continue
            actual = dep["cfg"].get("version", "")
            if dep_ver != "*" and actual != dep_ver:
                errors.append(
                    f"插件 '{name}'({pid}) 需要前置插件 '{dep_id}' 的版本 {dep_ver}，当前版本 {actual} 不符。启动中止。"
                )
        for nc_id, nc_ver in parse_pairs(cfg.get("not_compatible", "")):
            other = plugins.get(nc_id)
            if not other:
                continue
            actual = other["cfg"].get("version", "")
            if nc_ver == "*" or actual == nc_ver:
                errors.append(
                    f"插件 '{name}'({pid}) 与 '{nc_id}' 的版本 {actual} 不兼容。启动中止。"
                )
    return errors


def import_plugin(file_storage):
    """导入上传的 .xfpe/.xfpn，解压到 plugins/<id>/。返回 (ok, msg)。"""
    filename = file_storage.filename or ""
    ext = os.path.splitext(filename)[1].lower()
    if ext not in CFG_BY_SUFFIX:
        return False, "仅支持 .xfpe / .xfpn 文件"
    cfg_name = CFG_BY_SUFFIX[ext]
    tmp_dir = os.path.join(PLUGINS_DIR, "__tmp_import__")
    if os.path.isdir(tmp_dir):
        shutil.rmtree(tmp_dir)
    os.makedirs(tmp_dir, exist_ok=True)
    zip_path = os.path.join(tmp_dir, "pkg.zip")
    file_storage.save(zip_path)
    try:
        with zipfile.ZipFile(zip_path) as zf:
            zf.extractall(tmp_dir)
    except zipfile.BadZipFile:
        shutil.rmtree(tmp_dir, ignore_errors=True)
        return False, "不是有效的 Zip 包"
    cfg_path = os.path.join(tmp_dir, "data", cfg_name)
    if not os.path.isfile(cfg_path):
        shutil.rmtree(tmp_dir, ignore_errors=True)
        return False, f"包内缺少 data/{cfg_name}"
    cfg = parse_cfg(cfg_path)
    pid = cfg.get("id")
    if not pid:
        shutil.rmtree(tmp_dir, ignore_errors=True)
        return False, "配置缺少 id"
    if cfg.get("type", ext[1:]) != ext[1:]:
        shutil.rmtree(tmp_dir, ignore_errors=True)
        return False, "type 与文件后缀不一致"
    target = os.path.join(PLUGINS_DIR, pid)
    if os.path.isdir(target):
        shutil.rmtree(target)
    os.replace(tmp_dir, target)
    return True, f"插件 {pid} 导入成功"
