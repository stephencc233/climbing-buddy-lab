"""入口层（占位）：产品形态未定，本文件可整体替换。

依赖规则：入口层可以导入核心层和存储层；核心层、存储层不得导入入口层。
"""

import os
from pathlib import Path

from rich.console import Console
from rich.table import Table

from climbing_buddy_lab.core import send_rate
from climbing_buddy_lab.storage import load_records

# 配置只从环境变量读取，代码不关心变量从哪来。
# 本地开发用 `uv run --env-file .env ...` 注入，变量说明见 .env.example
DATA_FILE_ENV = "CLIMBING_BUDDY_DATA_FILE"
DEFAULT_DATA_FILE = "data/records.json"


def data_file() -> Path:
    """记录文件路径：环境变量优先；未设置或为空时用默认值（相对当前目录）。"""
    return Path(os.environ.get(DATA_FILE_ENV) or DEFAULT_DATA_FILE)


def format_send_rate(rate: float | None, dimension: str) -> str:
    """完攀率的显示文字：百分比保留 1 位小数；无数据时显示提示文字（AC3.2）。

    dimension 是筛选维度：“难度”“类型”或“角度”。
    """
    if rate is None:
        return f"本周未进行该{dimension}攀爬"
    return f"{rate:.1%}"


def main() -> None:
    path = data_file()
    records = load_records(path)

    console = Console()  # rich 的输出对象，负责颜色和宽字符对齐
    table = Table(title="攀岩训练伙伴 · 原型 v0")  # 带标题的表格
    table.add_column("指标")
    table.add_column("数值", justify="right")  # 数字列右对齐
    table.add_row("数据文件", str(path))
    table.add_row("记录条数", str(len(records)))
    table.add_row("示例完攀率", format_send_rate(send_rate(3, 5), "难度"))
    console.print(table)
