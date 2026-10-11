"""入口层（占位）：产品形态未定，本文件可整体替换。

依赖规则：入口层可以导入核心层和存储层；核心层、存储层不得导入入口层。
"""

from climbing_buddy_lab.core import send_rate


def main() -> None:
    print("攀岩训练伙伴 · 原型 v0")
    print(f"示例完攀率：{send_rate(3, 5):.1%}")
