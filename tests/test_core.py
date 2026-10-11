from climbing_buddy_lab.core import send_rate


def test_send_rate_counts_routes() -> None:
    # 对应 AC2.1：4 条 V4 记录，其中 3 条完攀 → 75.0%
    assert send_rate(3, 4) == 0.75
