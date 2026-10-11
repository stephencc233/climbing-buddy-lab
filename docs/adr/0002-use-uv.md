# ADR 0002：选择 uv 管理依赖

- 状态：提议中
- 日期：2026-10-10

## 背景
<由 Stephen 填写：为什么现在必须决定？引用触发它的需求或计划；列出影响选择的约束>

## 可选方案
1. venv + pip + requirements.txt：标准库自带、已经掌握；没有原生锁文件，`pip freeze` 只是当前环境的快照，跨平台不可靠
2. pip + pip-tools（pip-compile）：在 pip 之上补锁文件；需要两个工具配合，不管理 Python 版本
3. Poetry：成熟，有自己的 `poetry.lock`，2.x 支持标准 `[project]` 表；依赖解析较慢，不管理 Python 版本
4. PDM：对 PEP 标准跟进积极；社区规模较小
5. uv：一个工具完成虚拟环境、依赖、锁文件、Python 版本、构建；速度快；仍是 0.x 版本
6. conda：能管理非 Python 的二进制依赖；对纯 Python 项目过重

## 决定
<由 Stephen 填写> uv

## 理由
<由 Stephen 填写>

## 后果
- 好处：<由 Stephen 填写>
- 代价 / 风险（Claude 补充，应对措施由 Stephen 取舍）：
  1. 0.x 版本，小版本也可能有破坏性变更。实例：0.13.0（2026-10-09）把默认 Python 从 3.14 改为 3.15。
     - 可选应对：提交 `.python-version`（已做）；在 `[tool.uv]` 中用 `required-version` 限定 uv 版本范围
  2. `uv.lock` 是 uv 专有格式，换工具时不能直接复用。
     - 可选应对：需要时用 `uv export --format pylock.toml`（PEP 751 标准格式）或 `--format requirements.txt` 导出
  3. 构建后端版本有上限：`uv_build>=0.13.0,<0.14.0`，uv 升到 0.14 时需要同步修改 `[build-system]`。
     - 可选应对：升级 uv 时一起改上限；或换成 hatchling 等通用构建后端
  4. 厂商与治理：Astral 于 2026-03 宣布被 OpenAI 收购；uv 仍以 MIT / Apache-2.0 开源，风险在于产品路线变化。
     - 可选应对：项目元数据遵循 PEP 621 标准，迁移成本主要集中在锁文件和命令
  5. 通过 Scoop 安装时 `uv self update` 被禁用；Scoop 清单会修改 PATH（加入 uv 的 python 与 tools shims）。
     - 可选应对：升级只用 `scoop update uv`；Python 解释器继续由 Scoop 管理，不执行 `uv python install`
  6. 协作者和 CI 都必须安装 uv。
     - 可选应对：README 写明前置条件；M6 的 CI 使用官方 `astral-sh/setup-uv`
  7. 学习风险：只会 uv 命令，不理解背后的 venv / pip。
     - 可选应对：维护 uv 与 venv / pip 的命令对照表（Obsidian B8《uv 使用指南》）
- 约束：<由 Stephen 填写>
- 复审时机：<由 Stephen 填写>
