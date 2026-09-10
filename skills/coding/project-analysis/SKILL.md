---
name: project-analysis
description: 对现有代码仓库进行证据驱动的静态系统分析，并将范围、路由、专题和证据产物写入分析目录；适用于接手项目、源码架构拆解、核心机制学习、代码级复现说明或指定机制深度剖析。
disable-model-invocation: true
---

# Project Analysis

本 Skill 的默认模式是静态代码分析：读取仓库中的源码、配置、测试、已有日志和已有实验产物，建立可回溯的架构与机制说明。代码级复现只整理仓库已有的训练配置、参数和执行流程，形成供人执行的复现文档；它不包含环境安装、网络访问、数据或权重下载、训练执行或指标验证。

结果默认写入目标根目录的 `./_项目分析/`；用户指定 `output` 时，所有新增产物都写入该目录。源仓库、既有非 Skill 文件和外部系统保持不变。

## 1. 确定分析契约

从用户请求中确定并记录：

- `target`：目标仓库或子目录；未指定时使用当前工作目录。
- `goals`：`onboarding`、`architecture`、`learning`、`reimplementation`、`reproduction`、`security`、`performance` 或 `extension-development`；默认为 `architecture + learning`。
- `depth`：`survey`、`standard` 或 `deep`；默认为 `standard`。
- `scope`：整仓库、某个可运行系统、包、模块或用户指定机制。
- `output`：用户指定的分析目录；否则为 `<target>/_项目分析/`。

明确路径基准：仓库根、目标根和输出根分别是什么；证据路径默认相对仓库根。将输出目录加入勘探排除集，并识别已有分析产物。用户明确要求生成分析产物时，Skill 才进入写入模式；未知归属的既有文件保持不变。

在输出目录初始化 `analysis-manifest.yaml`、`00-分析范围与路由.md`、`_work/repository-map.md`、`_work/terminology.md` 和 `_work/evidence-ledger.md`。这些文件分别由主 Agent 管理；子 Agent 不直接修改共享工作文件。

完成标准：target、goals、depth、scope、output、路径基准、排除集和写入模式已记录，且初始化文件已经存在。

## 2. 建立仓库地图与路由

完整读取 [references/routing-and-baseline.md](references/routing-and-baseline.md)，然后：

1. 记录 Git revision、工作树状态、适用的仓库指令和目标相对路径。非 Git 仓库使用内容指纹或明确的 `non-git` 标记。
2. 排除输出目录、`.git`、缓存、构建产物、虚拟环境、第三方依赖和生成目录；只有在它们是分析对象时才重新纳入。
3. 识别 Repository 下的 System、Package/Module、Capability 和代表性 Flow，更新 `_work/repository-map.md`。
4. 建立项目术语表，并将证据以结构化条目写入 `_work/evidence-ledger.md`。
5. 根据源码、配置、测试或已有运行产物选择能力画像；为每个选中或跳过的画像记录触发证据和原因。
6. 按证据加载参考：
   - 发现后端、前端、CLI、桌面端、库/SDK、扩展/插件或基础设施入口时，读取 [references/software-profiles.md](references/software-profiles.md)；
   - 发现可训练神经网络、模型构建器、训练入口、数据管线、损失函数或实验配置时，完整读取 [references/deep-learning-profile.md](references/deep-learning-profile.md)；
   - 发现模型调用循环、上下文组装、工具调用、记忆或其他 Agent Runtime 证据时，读取 [references/agent-profile.md](references/agent-profile.md)；
   - 发现 `SKILL.md`、Skill 注册器或技能包时，读取 [references/skill-profile.md](references/skill-profile.md)。

勘探阶段只读取仓库现有内容和已有运行产物。测试、构建、训练、安装依赖、访问网络和下载资源属于本 Skill 之外的单独任务。

完成标准：所有可运行系统和重要包均已归属或标记为范围外；入口、主要依赖、核心链路和画像路由已定位；每个选中或跳过的画像都有可核查理由；输出目录没有被当作项目源码分析。

## 3. 制定产物与分工计划

完整读取 [references/artifacts-and-evidence.md](references/artifacts-and-evidence.md)，为每个选中能力域确定唯一产物根、专题、负责人、依赖和完成标准。

当环境支持子 Agent 且存在两个以上可独立验证的能力域时，完整读取 [references/delegation.md](references/delegation.md)。主 Agent 先完成仓库地图、术语表、证据账本和 manifest，再派发任务。子 Agent 只写入任务契约指定的域目录，返回结构化证据包；主 Agent 统一合并证据账本、处理冲突并写入跨域产物。

小型、高度集中的仓库由当前 Agent 完成。任何两个负责人的最终文档写入范围不得重叠；共享 `_work/` 文件始终由主 Agent 独占写入。

完成标准：manifest 已列出 selected domains、selected topics、依赖、负责人、唯一输出路径、完成标准、跳过项和限制；每个写入路径唯一且可验证。

## 4. 执行专题分析

对每个已选主题：

1. 从入口追踪到状态变更、持久化或外部边界；存在失败、取消、超限或资源释放逻辑时，再追踪一条对应边界路径。代码没有该概念时记录 `not-applicable`，不补造路径。
2. 区分预期架构与实际实现。实现事实优先来自源码、配置、测试和已有日志；作者意图单独标记为 `documented`，推断标记为 `inferred`，无法确认标记为 `unknown`。
3. 将结论写入结构化 evidence ledger，并在专题文档中引用证据 ID；运行证据只能使用仓库已有日志、报告或用户提供的结果。
4. 用项目领域语言解释机制，先更新统一术语，再在各文档复用。
5. 只在图能显著降低理解成本时绘制架构图、时序图、状态图或表格。
6. `reimplementation` 目标下，根据源项目语言和用户意图提供伪代码或可运行蓝图；记录覆盖范围和外部边界，不把蓝图称为已执行实现。
7. `reproduction` 目标下，只整理仓库中的训练入口、数据处理、配置继承、最终参数、执行命令、验证入口和已有指标，形成供人执行的复现说明；缺少外部数据、权重或运行结果时记录前置条件和 `unknown`。

专题完成标准：每个触发问题都有答案、`not-applicable` 或 `unknown`；重要结论有证据 ID；正常路径和相关边界路径已覆盖；没有执行本 Skill 范围外的安装、下载、网络调用或训练。

## 5. 综合与验收

由主 Agent 编写项目总览、跨域端到端链路、全局取舍和风险。总览只摘要并链接专题真实来源，不复制专题的完整内容。`99-证据索引.md` 从 `_work/evidence-ledger.md` 整理生成，不维护第二套独立证据事实。

按 [references/artifacts-and-evidence.md](references/artifacts-and-evidence.md) 验收：检查 manifest、文档链接、证据 ID、术语、重复定义、未声明推断和输出范围；发现冲突时回到原始源码或已有产物核对。

完成标准：

- `README.md`、`analysis-manifest.yaml`、`00-分析范围与路由.md`、`01-项目总览.md` 和 `99-证据索引.md` 存在且相互一致。
- 每个选中能力域均有唯一目录和域级 `README.md`；未命中的能力域没有空目录。
- 每个计划产物均已完成，或在 manifest 中记录可核查的未完成原因。
- 每个重要结论都能通过证据 ID 回溯到 revision、仓库相对路径和 symbol、配置键、测试名、日志条目或文档锚点。
- `unknown`、`not-applicable`、范围限制和未执行的验证均已显式列出。
- 所有新增文件均位于授权的 output 目录，且 output 目录未被当作源码重新分析。
