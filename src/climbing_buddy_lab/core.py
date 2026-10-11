"""核心层：纯逻辑，不做任何 I/O（不读写文件、不 print、不 input）。"""


def send_rate(sent_routes: int, logged_routes: int) -> float:
    """完攀率（按线算）= 完攀线路条数 / 记录线路条数，返回 0–1 的比例。

    口径见 docs/requirements.md 第 4 节；百分比格式化由入口层负责。
    已知问题：logged_routes 为 0 时抛 ZeroDivisionError，留给 M4 用测试复现并修复。
    """
    return sent_routes / logged_routes
