<!--
标题：Conventional Commits 格式 `type: 描述`（冒号后有空格）。squash 合并时，标题就是 main 上的提交信息。
HTML 注释不会显示在 PR 页面上，可以保留。不适用的清单项整行删除，并在最后一节说明原因。
-->

## 关联 Issue

Closes #

<!-- 只有合并进默认分支 main 时 Closes 才生效；一个 Issue 写一行。只关联、不关闭时用 Refs #N -->

## 改了什么、为什么

-

## 怎么验证的

<!-- 命令与结果；修 bug 写清“先红后绿”的测试名 -->

-

## 自查清单（C3）

范围
- [ ] 只做关联 Issue 的一件事，没有顺手重构或无关的格式化
- [ ] diff 里没有调试代码、临时文件、`scratch/` 内容

正确性与测试
- [ ] 改动涉及的 AC 都有测试覆盖，期望值写字面量（不引用被测模块的常量）
- [ ] 边界情况已考虑：空数据、0、非法输入
- [ ] 修 bug：有先失败、修复后通过的测试

设计
- [ ] 分层不破：核心层无 I/O；核心层和存储层不导入入口层；rich 只在入口层
- [ ] 涉及已有决策的已对照 ADR；新的重要决策已写 ADR

安全与配置
- [ ] 没有密钥、`.env`、真实训练数据
- [ ] 新增配置只走环境变量，并同步更新 `.env.example` 和 README 变量表

依赖与文档
- [ ] 依赖只用 `uv add` / `uv remove` 修改，`pyproject.toml` 与 `uv.lock` 一起提交
- [ ] 命令或约定有变化时，README / CLAUDE.md / docs 已同步

检查
- [ ] 本地四项检查通过：`ruff check`、`ruff format --check`、`pyright`、`pytest`
- [ ] 已用 Claude Code 按 C3 审查 diff（E3 P16），每条结论已判定：采纳 / 推迟 / 不采纳

## 不适用项与遗留

-
