"""核心层 send_rate 的测试。

输入来自 scratch/repro_send_rate.py 和 docs/requirements.md 的验收标准（AC）。
"""

import pytest

from climbing_buddy_lab.core import send_rate


@pytest.mark.parametrize(
    ("sent", "logged", "expected"),
    [
        pytest.param(3, 4, 0.75, id="AC2.1-3of4"),
        pytest.param(2, 3, 0.667, id="AC2.3-2of3"),
        pytest.param(2, 5, 0.4, id="AC3.1-2of5"),
        pytest.param(1, 1, 1.0, id="AC3.3-1of1"),
        pytest.param(5, 5, 1.0, id="repro-all-sent"),
        pytest.param(0, 2, 0.0, id="repro-none-sent"),  # 有记录但没完攀：0% 是合法结果
        pytest.param(1, 3, 0.333, id="repro-1of3"),
    ],
)
def test_send_rate_counts_routes(sent: int, logged: int, expected: float) -> None:
    # 需求只要求百分比保留 1 位小数，比例精确到 0.0005（= 0.05%）即可；
    # 2/3 这类循环小数不能用 ==，也不要在测试里写 2 / 3（那是把被测公式抄一遍）
    assert send_rate(sent, logged) == pytest.approx(expected, abs=5e-4)
