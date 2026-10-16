"""存储层的测试：全部使用临时目录（tmp_path），不碰真实的 data/。"""

import json
from pathlib import Path
from typing import Any

import pytest

from climbing_buddy_lab.storage import load_records, save_records


@pytest.fixture
def sample_records() -> list[dict[str, Any]]:
    """两条示例记录；字段对应 AC1.1（日期、难度、类型多选、角度、尝试次数、是否完攀）。"""
    return [
        {
            "date": "2026-10-09",
            "grade": "V4",
            "types": ["指力"],
            "angle": "小仰角",
            "attempts": 3,
            "sent": True,
        },
        {
            "date": "2026-10-09",
            "grade": "V5",
            "types": ["动态", "协调"],
            "angle": "大仰角",
            "attempts": 1,
            "sent": False,
        },
    ]


@pytest.fixture
def records_file(tmp_path: Path) -> Path:
    """记录文件的路径（文件还不存在）；放在子目录里，顺便检验“目录不存在时自动创建”。"""
    return tmp_path / "data" / "records.json"


def test_load_returns_empty_list_when_file_missing(records_file: Path) -> None:
    assert load_records(records_file) == []


def test_saved_records_survive_reload(
    records_file: Path, sample_records: list[dict[str, Any]]
) -> None:
    # 对应 AC1.5：保存后重新读取（模拟重启程序），记录仍在且字段不变
    save_records(records_file, sample_records)
    assert load_records(records_file) == sample_records


def test_save_writes_schema_version_and_keeps_chinese_readable(
    records_file: Path, sample_records: list[dict[str, Any]]
) -> None:
    save_records(records_file, sample_records)
    text = records_file.read_text(encoding="utf-8")
    assert json.loads(text)["schema_version"] == 1  # 字面量：常量被误改时这里会失败
    assert "指力" in text  # ensure_ascii=False：中文不被转义成 \uXXXX，便于直接查看


def test_save_replaces_whole_file_and_leaves_no_temp_file(
    records_file: Path, sample_records: list[dict[str, Any]]
) -> None:
    save_records(records_file, sample_records)
    save_records(records_file, sample_records[:1])
    assert load_records(records_file) == sample_records[:1]
    assert [p.name for p in records_file.parent.iterdir()] == ["records.json"]


@pytest.mark.parametrize(
    "payload",
    [
        pytest.param({"records": []}, id="missing"),
        pytest.param({"schema_version": 0, "records": []}, id="older-0"),
        pytest.param({"schema_version": 999, "records": []}, id="newer-999"),
        pytest.param({"schema_version": "1", "records": []}, id="string-1"),
    ],
)
def test_load_rejects_unsupported_schema_version(
    records_file: Path, payload: dict[str, Any]
) -> None:
    # 只认当前版本：缺字段、旧版本、新版本、类型不对都要报错，而不是静默读入
    records_file.parent.mkdir(parents=True)
    records_file.write_text(json.dumps(payload), encoding="utf-8")
    with pytest.raises(ValueError, match="schema_version"):
        load_records(records_file)


def test_failed_replace_keeps_old_file_and_removes_temp(
    records_file: Path,
    sample_records: list[dict[str, Any]],
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    # 覆盖率报告指出的漏测路径（storage.py 的 except 分支）：用 monkeypatch 注入故障。
    # 对应 Windows 上目标文件被占用时 os.replace 抛 PermissionError 的技术债
    save_records(records_file, sample_records)

    def fail_replace(src: object, dst: object) -> None:
        raise PermissionError("模拟：目标文件被其他程序占用")

    monkeypatch.setattr("climbing_buddy_lab.storage.os.replace", fail_replace)
    with pytest.raises(PermissionError):
        save_records(records_file, sample_records[:1])

    assert load_records(records_file) == sample_records  # 旧数据完好
    assert [p.name for p in records_file.parent.iterdir()] == ["records.json"]
