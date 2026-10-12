"""核心层：纯逻辑，不做任何 I/O（不读写文件、不 print、不 input）。"""


def send_rate(sent_routes: int, logged_routes: int) -> float | None:
    """完攀率（按线算）= 完攀线路条数 / 记录线路条数，返回 0–1 的比例。

    口径见 docs/requirements.md 第 4 节；百分比格式化和提示文字由入口层负责。
    约定见 ADR 0003：
    - 没有记录（logged_routes == 0）返回 None，表示“无数据”，不是 0%；
    - 计数为负数或 sent_routes > logged_routes 时抛 ValueError（程序错误）。
    """
    if sent_routes < 0 or logged_routes < 0:
        raise ValueError(f"计数不能为负数：sent={sent_routes}, logged={logged_routes}")
    if sent_routes > logged_routes:
        raise ValueError(
            f"完攀条数不能多于记录条数：sent={sent_routes}, logged={logged_routes}"
        )
    if logged_routes == 0:
        return None
    return sent_routes / logged_routes
