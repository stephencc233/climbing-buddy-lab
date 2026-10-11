# ADR 0002：选择 uv 管理依赖

- 状态：已采纳
- 日期：2026-10-11
- 执笔：Claude 起草，Stephen 审阅（计划中的“结论由本人独立写”本次未执行）

## 背景
M3 的验收要求“在新目录克隆仓库后，`uv sync` + `uv run` 一条命令就能运行”，也就是任何机器上都能装出**完全相同**的环境。lab 之前只有一个 `main.py`，没有依赖清单，也没有锁文件。现在要开始引入第三方包（M4 的 pytest，U05 的 Ruff），必须先确定依赖管理方式。

影响选择的约束：

- 本机环境是 Windows 10、PowerShell 7、Scoop；Python 3.14 由 Scoop 管理（决策 2026-10-05）。
- 仓库是公开的；M6 要用 GitHub Actions 在 Linux 上跑 CI，所以锁文件必须**跨平台**可复现。
- 学习目标要求理解底层原理（venv / pip），不能只会用工具。
- 依赖管理方式在 2026-10-05 已经选定为 uv（计划书 4.2），本 ADR 补记当时的理由，并记录引入时（uv 0.13.0）核实到的风险。

## 可选方案
1. venv + pip + requirements.txt：标准库自带、已经掌握；没有原生锁文件，`pip freeze` 只是当前环境的快照，跨平台不可靠
2. pip + pip-tools（pip-compile）：在 pip 之上补锁文件；需要两个工具配合，不管理 Python 版本
3. Poetry：成熟，有自己的 `poetry.lock`，2.x 支持标准 `[project]` 表；依赖解析较慢，不管理 Python 版本
4. PDM：对 PEP 标准跟进积极；社区规模较小
5. uv：一个工具完成虚拟环境、依赖、锁文件、Python 版本、构建；速度快；仍是 0.x 版本
6. conda：能管理非 Python 的二进制依赖；对纯 Python 项目过重

## 决定
采用 uv（0.13.x，通过 Scoop 安装）管理虚拟环境、依赖、锁文件和构建，构建后端使用 `uv_build`。Python 解释器仍由 Scoop 提供，项目用 `.python-version` 固定为 3.14。

## 理由
1. **原生的跨平台锁文件**：`uv.lock` 记录的是在所有平台上的解析结果。例如 pytest 依赖的 colorama 被标注为 `sys_platform == 'win32'`，Windows 上会安装，Linux CI 上会跳过。这直接满足“克隆后一条命令复现”的验收要求。方案 1 做不到；方案 2 能锁版本，但一次只能为一个平台生成锁文件。
2. **一个工具覆盖全流程**：建环境、增删依赖、锁定、运行、构建都在 uv 里完成，不必像方案 2 那样拼两个工具，也比方案 3、4 多了管理 Python 版本的能力。学习阶段少一个工具，就少一份配置和一类故障。
3. **迁移成本低**：项目元数据用的是标准格式（PEP 621 的 `[project]`、PEP 735 的 `[dependency-groups]`），锁文件也能用 `uv export` 导出成标准格式（已实测）。将来换工具时，主要改的只是命令。
4. **CI 有官方支持**：M6 用的 `astral-sh/setup-uv` 由官方维护，内置缓存，并且会读取 `pyproject.toml` 中的 `required-version` 来决定安装哪个 uv 版本，本地和 CI 能自动对齐。
5. **不牺牲原理学习**：uv 的底层仍然是 venv 结构加标准安装，命令可以和 venv / pip 一一对照（B8《uv 使用指南》第 3 节）。
6. 速度快（官方宣称比 pip 快 10–100 倍）。这一条是次要理由，lab 的依赖很少。

不选其他方案的原因：方案 1、2 不满足跨平台锁定；方案 3 解析慢、不管 Python 版本，和 Scoop + uv 的组合相比没有额外收益；方案 4 社区规模较小，遇到问题时可参考的资料更少；方案 6 对纯 Python 项目来说过重。

## 后果
- 好处：
  - 克隆后 `uv sync` 一条命令就能复现环境（已在模拟克隆中验证）；`.venv` 删掉后可随时重建。
  - 运行依赖和开发依赖分开管理；`uv run` 不需要激活环境，也不会忘记同步。
  - 本地和 CI 使用同一套命令（`uv sync --locked`、`uv run pytest`）。
- 代价 / 风险及应对（✅ 采纳，⏸ 只记录、暂不行动）：
  1. 0.x 版本，小版本也可能有破坏性变更。实例：0.13.0（2026-10-09）把默认 Python 从 3.14 改为 3.15。
     - ✅ 提交 `.python-version`（3.14）。
     - ✅ 在 `[tool.uv]` 中设置 `required-version = ">=0.13.0"`，只设下限：版本过旧的 uv 会直接报错，而不是悄悄生成格式不同的锁文件；setup-uv 也会按它选版本。
     - ⏸ 不设上限：uv 小版本发布频繁，设上限的话每次升级都要改配置，学习阶段的维护成本大于收益。改为升级前先读 Release Notes 里的 Breaking changes。
  2. `uv.lock` 是 uv 专有格式。
     - ⏸ 需要时用 `uv export --format pylock.toml`（PEP 751）或 `--format requirements.txt` 导出；现在不提交导出文件，避免出现两份“真相”。
  3. 构建后端有版本上限：`uv_build>=0.13.0,<0.14.0`。
     - ✅ uv 升级小版本时，同一个 PR 里同步修改这个上限，并执行 `uv lock`。暂时不换成 hatchling。
  4. 厂商与治理：Astral 于 2026-03 宣布被 OpenAI 收购；uv 仍以 MIT / Apache-2.0 开源。
     - ⏸ 接受。依靠理由 3（标准格式）控制迁移成本；如出现许可证变更，触发复审。
  5. Scoop 安装方式下 `uv self update` 被禁用（uv 报版本不符时提示的 `uv self update` 在本机不可用）；Scoop 清单会修改 PATH。
     - ✅ 升级只用 `scoop update uv`；解释器继续由 Scoop 管理，不执行 `uv python install`。
  6. 协作者和 CI 都必须安装 uv。
     - ✅ README 写明前置条件（已写）；M6 的 CI 使用 `astral-sh/setup-uv`。
  7. 学习风险：只会 uv 命令，不懂背后的 venv / pip。
     - ✅ 维护 Obsidian B8《uv 使用指南》中的命令对照表。
- 约束（写 ADR 时暴露出的隐含约束）：
  - `pyproject.toml`、`uv.lock`、`.python-version` 必须一起提交；改了依赖但没提交锁文件，CI 的 `--locked` 会失败。
  - 依赖只能通过 `uv add` / `uv remove` 修改；禁止在项目里使用 `uv pip install`。
  - `uv.lock` 不手改；合并冲突时先接受任意一边，再执行 `uv lock` 重新生成。
- 复审时机：
  - uv 发布 1.0，或某个小版本的 Breaking changes 影响到本项目时；
  - uv 的许可证或开源状态发生变化时；
  - 第二部分 P4 搭建正式仓库 `climbing-buddy` 时，复核是否沿用；
  - 出现 uv 无法解析或安装的必需依赖时。
