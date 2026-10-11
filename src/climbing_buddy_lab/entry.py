"""入口层（占位）：产品形态未定，本文件可整体替换。

依赖规则：入口层可以导入核心层和存储层；核心层、存储层不得导入入口层。
"""

from rich.console import Console
from rich.table import Table

from climbing_buddy_lab.core import send_rate


def main() -> None:
    console = Console()                                # rich 的输出对象，负责颜色和宽字符对齐
    table = Table(title="攀岩训练伙伴 · 原型 v0")      # 带标题的表格
    table.add_column("指标")
    table.add_column("数值", justify="right")          # 数字列右对齐
    table.add_row("示例完攀率", f"{send_rate(3, 5):.1%}")
    console.print(table)
