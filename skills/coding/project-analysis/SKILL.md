---
name: project-analysis
description: 对现有代码仓库进行证据驱动的系统分析，根据软件、Agent、Skill、深度学习等实际能力组合路由分析主题，并将总览、专题和证据产物写入项目的 _项目分析 目录。适用于接手项目、源码架构拆解、核心机制学习、模型与训练复现或指定项目深度剖析；不用于仅审查当前代码变更。
disable-model-invocation: true
---

# Project Analysis

将仓库视为多种能力的组合，而不是在互斥的“项目类型”中三选一。公共基线始终执行；专题只在源码、配置、测试或运行行为提供证据时加载。默认将结果写入目标项目根目录的 `./_项目分析/`。

## 1. 确定分析契约

从用户请求中确定：

- `target`：目标仓库或子目录；未指定时使用当前工作目录。
- `goals`：`onboarding`、`architecture`、`learning`、`reimplementation`、`reproduction`、`security`、`performance` 或 `extension-development`；默认为 `architecture + learning`。
- `depth`：`survey`、`standard` 或 `deep`；默认为 `standard`。
- `scope`：整仓库、某个可运行系统、包、模块或用户指定机制。
- `output`：用户未指定时使用 `<target>/_项目分析/`。

对仓库内容使用只读勘探；分析请求只授权写入分析目录。先检查已有分析产物，保留无法确认由本 Skill 管理的文件。

完成标准：目标、目标、深度、范围和输出位置均已确定，且不得为无关的清晰度问题停止勘探。

## 2. 全局勘探

完整读取 [references/routing-and-baseline.md](references/routing-and-baseline.md)，然后：

1. 记录 Git revision、工作树状态和适用的仓库指令。
2. 识别 Repository 下的 System、Package/Module、Capability 和代表性 Flow。
3. 检查 README、构建清单、配置、入口、测试、部署文件和核心源码。
4. 以多标签方式选择能力画像，记录每个选中或跳过决定的证据。
5. 在输出目录创建 `analysis-manifest.yaml`和 `_work/repository-map.md`，作为后续分析的共享上下文。

勘探中发现后端、前端、全栈集成、CLI、桌面端、库/SDK、扩展/插件或基础设施时，读取 [references/software-profiles.md](references/software-profiles.md)。发现可训练神经网络、模型定义、训练入口、数据管线、损失函数或实验配置时，完整读取 [references/deep-learning-profile.md](references/deep-learning-profile.md)。发现模型调用循环、上下文组装、工具调用、记忆或其他 Agent Runtime 证据时，读取 [references/agent-profile.md](references/agent-profile.md)。发现 `SKILL.md`、Skill 注册器或技能包时，读取 [references/skill-profile.md](references/skill-profile.md)。

完成标准：所有可运行系统和重要包均被归属；入口、主要依赖和核心链路已定位；每个选中专题都有触发证据，每个明显但跳过的专题都有原因。

## 3. 制定产物与分工计划

完整读取 [references/artifacts-and-evidence.md](references/artifacts-and-evidence.md)，为每个选中能力域确定唯一产物根，并根据深度和已选主题确定“域级 README + 机制分册 + 跨域 Flow/Quality”产物。文档是阅读边界，不是必然的分工边界；共享同一组核心类型或调用链的主题由同一负责人分析，可生成多篇文档。

当环境支持子 Agent 且仓库存在多个独立能力域时，完整读取 [references/delegation.md](references/delegation.md) 并按其知识边界分工。小型、高度集中的仓库由当前 Agent 完成。

完成标准：`analysis-manifest.yaml` 列出选中能力域及其唯一产物根、专题产物、负责人、依赖、完成标准与跳过项；任何两个负责人的写入范围均不重叠。

## 4. 执行专题分析

对每个已选主题：

1. 从入口追踪到状态变更、持久化或外部边界，同时追踪一条有代表性的失败、取消或超限路径。
2. 区分预期架构与实际实现，根据源码、配置、测试和可重复的运行结果建立结论。
3. 将结论标记为 `verified`、`inferred` 或 `unknown`，并更新 `_work/evidence-ledger.md`。
4. 用项目的领域语言解释机制；先建立统一术语，再在各文档复用。
5. 只在图能显著降低理解成本时绘制架构图、时序图、状态图或表格。
6. `reimplementation` 目标下，根据源项目语言和用户意图选择伪代码或可运行蓝图；记录覆盖范围和外部边界，不将局部复现声称为整个项目的完整还原。

完成标准：每个主题的触发问题均有答案或明确的 `unknown`；核心结论均可回溯到证据；正常路径和重要边界路径均被覆盖。

## 5. 综合与验收

由一个统一负责人编写项目总览、跨域端到端链路、全局取舍和风险。总览摘要并链接分册，不复制分册的完整内容。根据 [references/artifacts-and-evidence.md](references/artifacts-and-evidence.md) 逐项验收，修正术语冲突、重复结论、断链、证据缺口和未声明的推断。

完成标准：

- `README.md`、`analysis-manifest.yaml`、`01-项目总览.md` 和 `99-证据索引.md` 存在并相互一致。
- 每个选中能力域均有唯一目录和域级 `README.md`，未命中的能力域没有占位目录。
- 每个计划产物均已完成，或在 manifest 中记录可核查的未完成原因。
- 每个重要结论都有 revision、相对路径和 symbol/配置键/测试名之一。
- 未知项、范围限制和未执行的验证已显式列出。
- 所有新增文件均位于授权的分析目录。
