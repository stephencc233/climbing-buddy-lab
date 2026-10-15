# 攀岩训练伙伴（原型）

记录室内攀岩训练数据、按周统计完攀率的工具（产品形态待定：命令行或网页）。

> 这是**原型仓库**，用于学习 Git / GitHub 全流程，会做各种实验和事故演练。正式版另建仓库 `climbing-buddy`。

## 运行

前置：已安装 [uv](https://docs.astral.sh/uv/)（Python 3.14 由 `.python-version` 指定）。

```powershell
uv sync                    # 按 uv.lock 创建 .venv 并安装全部依赖（含开发依赖）
uv run climbing-buddy-lab  # 运行入口命令
uv run pytest              # 运行测试
```

## 参与开发

克隆后先启用提交前检查（每个克隆做一次）：

```powershell
uv run pre-commit install         # 之后 git commit 时自动运行检查（Ruff 查暂存的 .py 文件，pyright 查整个项目），配置见 .pre-commit-config.yaml
uv run pre-commit run --all-files # 手动对全部文件运行一遍
```

推送前用 VS Code 任务“检查：全部（提交前）”做一次全量检查（ruff check、ruff format --check、pyright、pytest）。

## 配置

配置只通过环境变量传入，代码里不写死。变量清单和说明见 `.env.example`。

```powershell
Copy-Item .env.example .env                  # 本地配置文件，已被 .gitignore 忽略
uv run --env-file .env climbing-buddy-lab    # 由 uv 读取 .env，注入环境变量后再运行
```

| 变量 | 作用 | 默认值 |
| --- | --- | --- |
| `CLIMBING_BUDDY_DATA_FILE` | 训练记录 JSON 文件路径 | `data/records.json` |

## 目录结构

```text
src/climbing_buddy_lab/
├── entry.py      入口层（占位，形态待定，可整体替换）
├── core.py       核心层：纯逻辑，无 I/O
└── storage.py    存储层：JSON 文件读写（见 ADR 0001）
tests/            测试
docs/             需求文档与 ADR
data/             本地训练数据（不进仓库）
```

依赖方向：入口层 → 核心层 / 存储层；核心层和存储层不得导入入口层。

## 许可证（MIT）

MIT
