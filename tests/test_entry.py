"""入口层的测试：显示文字（format_send_rate）、配置读取（data_file）、整体运行（main）。"""

import json
import re
from pathlib import Path

import pytest

from climbing_buddy_lab import entry


@pytest.mark.parametrize(
    ("rate", "dimension", "shown"),
    [
        pytest.param(0.75, "难度", "75.0%", id="AC2.1"),
        pytest.param(2 / 3, "难度", "66.7%", id="AC2.3-round"),
        pytest.param(0.0, "类型", "0.0%", id="zero-is-shown"),
        pytest.param(None, "类型", "本周未进行该类型攀爬", id="AC3.2-empty"),
        pytest.param(None, "角度", "本周未进行该角度攀爬", id="empty-angle"),
    ],
)
def test_format_send_rate(rate: float | None, dimension: str, shown: str) -> None:
    # 这里比较的是显示文字，所以可以用 ==：“保留 1 位小数”在这一层才真正被检验
    assert entry.format_send_rate(rate, dimension) == shown


def test_data_file_reads_env_var(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv(entry.DATA_FILE_ENV, "custom/records.json")
    assert entry.data_file() == Path("custom/records.json")


@pytest.mark.parametrize("value", [None, ""], ids=["unset", "empty"])
def test_data_file_falls_back_to_default(
    monkeypatch: pytest.MonkeyPatch, value: str | None
) -> None:
    # 不管运行测试的进程里有没有 .env 注入的值（测试面板会注入），都先清掉再设
    monkeypatch.delenv(entry.DATA_FILE_ENV, raising=False)
    if value is not None:
        monkeypatch.setenv(entry.DATA_FILE_ENV, value)
    assert entry.data_file() == Path(entry.DEFAULT_DATA_FILE)


def test_main_shows_record_count(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    # 集成测试：入口层 + 存储层 + 核心层一起跑，用临时数据文件，不碰真实的 data/
    data = tmp_path / "records.json"
    payload = {"schema_version": 1, "records": [{"grade": "V4"}, {"grade": "V5"}]}
    data.write_text(json.dumps(payload), encoding="utf-8")
    monkeypatch.setenv(entry.DATA_FILE_ENV, str(data))

    entry.main()

    lines = capsys.readouterr().out.splitlines()
    # 按“行”断言：整段输出里含有 "2" 不算数（临时目录路径里也可能有 2）。
    # \W 匹配表格边框（│ 或 |）和空格，中文属于 \w
    count_row = next(line for line in lines if "记录条数" in line)
    rate_row = next(line for line in lines if "示例完攀率" in line)
    assert re.fullmatch(r"\W*记录条数\W+2\W*", count_row)
    assert re.fullmatch(r"\W*示例完攀率\W+60\.0%\W*", rate_row)  # send_rate(3, 5)
