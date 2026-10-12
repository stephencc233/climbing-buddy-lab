# CLAUDE.md

## 项目背景

攀岩训练伙伴的**原型仓库**：记录室内攀岩训练、按周统计完攀率。同时用于学习 Git / GitHub 全流程，会做实验和事故演练；正式版另建仓库 `climbing-buddy`。产品形态（命令行 / 网页）尚未确定。

语言：文档和代码注释用中文；提交信息用英文 Conventional Commits，格式 `type: 描述`（冒号后有空格），如 `feat: read data file path from environment variable`。

## 工作约定

- 这是学习仓库：修改前先说明计划，等我确认后再动手；一次只改一件事，不要顺手重构。
- 改动走分支 → PR，不直接提交到 main；PR 用 merge commit 合并。
- 提交前四项检查都要通过：`uv run ruff check`、`uv run ruff format --check`、`uv run pyright`、`uv run pytest`。
- `git commit` 会触发 pre-commit（`.pre-commit-config.yaml`）；钩子失败时修正后重新提交，不用 `--no-verify` 绕过。
- 公开仓库：不读取、不提交 `.env` 和 `data/`，任何文件里都不写密钥。

## 常用命令

环境：Windows + PowerShell 7，uv 和 Python 3.14 都由 Scoop 管理。

```powershell
uv sync                                     # 按 uv.lock 建 .venv 并装全部依赖（含 dev 组）
uv run climbing-buddy-lab                   # 运行入口
uv run --env-file .env climbing-buddy-lab   # 读取本地 .env 后运行（先 Copy-Item .env.example .env）
uv run pytest                               # 全部测试
uv run pytest tests/test_core.py::test_send_rate_counts_routes   # 单个测试
uv run pytest --cov --cov-report=term-missing   # 测试 + 覆盖率（范围见 [tool.coverage]，不设门槛）
uv run ruff check                           # lint（Ruff 默认规则集，不写 select）
uv run ruff format                          # 格式化（改写文件）
uv run ruff format --check                  # 只检查不改（验收和 CI 用这条）
uv run pyright                              # 类型检查（standard 模式，范围见 [tool.pyright]）
uv run pre-commit install                   # 启用提交前钩子（每个克隆一次）
uv run pre-commit run --all-files           # 对全部文件运行钩子
```

## 架构

`src/` 布局，包为 `climbing_buddy_lab`，三层结构，**依赖只能从上往下**，核心层和存储层不得导入入口层：

- `entry.py` 入口层：占位实现，产品形态定下后可整体替换；负责读取配置、调用其他层、所有输出与格式化（rich）。
- `core.py` 核心层：纯逻辑，**不做任何 I/O**（不读写文件、不 print、不 input）；统计口径以 `docs/requirements.md` 第 4 节为准（完攀率按“线”计）。
- `storage.py` 存储层：只负责 JSON 读写，不做统计；格式与写入方式见 ADR 0001。

配置只通过环境变量传入，不在代码中写死；新增变量要同步更新 `.env.example` 和 README 的变量表。

核心层统计函数的约定（ADR 0003）：分母为 0 返回 `None`（“无数据”，不是 0%），负数或 `sent > logged` 等非法计数抛 `ValueError`；提示文字由入口层的 `format_send_rate` 生成。

## 需求与决策文档

- `docs/requirements.md`：需求、术语约定和验收标准 AC*；测试注释或参数化 id 中引用对应的 AC 编号（如 `# 对应 AC2.1`、`id="AC2.1-3of4"`）。
- `docs/adr/`：架构决策记录。改动涉及已有决策时先读相关 ADR；新的重要决策另写 ADR。

## 依赖与工具约束（ADR 0002）

- 依赖只能用 `uv add` / `uv remove` 修改，禁止 `uv pip install`；不执行 `uv self update`、`uv python install`（由 Scoop 管理）。
- `pyproject.toml`、`uv.lock`、`.python-version` 必须一起提交；`uv.lock` 不手改，冲突时任取一边再 `uv lock`。
- 升级 uv 小版本时，同一 PR 内同步改 `uv_build` 上限并 `uv lock`；升级 Ruff、pyright 各自单独提 PR（`uv lock --upgrade-package <包名>`）。
- pre-commit 里的 Ruff、pyright 是本地钩子（`uv run --locked`），版本只由 `uv.lock` 决定，不要改成远程钩子另记版本。
- 换行统一 LF（`.gitattributes`、`.editorconfig`、Ruff format 一致），`.bat` / `.cmd` 除外。
