"""存储层：记录的 JSON 读写，只负责保存和读取，不做统计（见 ADR 0001）。"""

import json
import os
import tempfile
from pathlib import Path
from typing import Any

SCHEMA_VERSION = 1


def load_records(path: Path) -> list[dict[str, Any]]:
    """读取全部记录；文件不存在时返回空列表。"""
    if not path.exists():
        return []
    data = json.loads(path.read_text(encoding="utf-8"))
    version = data.get("schema_version")
    if version != SCHEMA_VERSION:
        raise ValueError(f"不支持的 schema_version：{version!r}")
    return data["records"]


def save_records(path: Path, records: list[dict[str, Any]]) -> None:
    """整体重写记录文件：先写同目录临时文件，再用 os.replace 替换原文件。"""
    path.parent.mkdir(parents=True, exist_ok=True)
    payload = {"schema_version": SCHEMA_VERSION, "records": records}
    # 临时文件放在同一目录，保证与目标在同一文件系统，os.replace 才不会失败
    fd, tmp_name = tempfile.mkstemp(dir=path.parent, prefix=f".{path.name}.", suffix=".tmp")
    tmp = Path(tmp_name)
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as f:
            json.dump(payload, f, ensure_ascii=False, indent=2)
            f.flush()
            os.fsync(f.fileno())  # 先落盘，再替换
        os.replace(tmp, path)
    except BaseException:
        tmp.unlink(missing_ok=True)
        raise
