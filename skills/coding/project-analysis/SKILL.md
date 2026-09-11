---
name: project-analysis
description: 对现有代码仓库进行证据驱动的静态系统分析，并将范围、路由、专题和证据产物写入分析目录；适用于接手项目、源码架构拆解、核心机制学习、代码级复现说明或指定机制深度剖析。
disable-model-invocation: true
---

# Project Analysis

本 Skill 默认进行静态代码分析：读取仓库中的源码、配置、测试、已有日志和已有实验产物，建立可回溯的架构与机制说明。代码级复现只整理仓库已有的训练配置、参数和执行流程，形成供人执行的复现文档；它不包含环境安装、网络访问、数据或权重下载、训练执行或指标验证。

默认使用 `artifacts` 模式，结果写入目标根目录的 `./_项目分析/`；用户指定 `output` 时写入该目录。只有用户明确要求不写文件时才使用 `inline` 模式。源仓库、既有非 Skill 文件和外部系统保持不变。

## 1. 确定契约并加载公共规范

从用户请求中确定：

- `target`：目标仓库或子目录；未指定时使用当前工作目录。
- `goals`：`onboarding`、`architecture`、`learning`、`reimplementation`、`reproduction`、`security`、`performance` 或 `extension-development`；默认为 `architecture + learning`。
- `depth`：`survey`、`standard` 或 `deep`；默认为 `standard`。
- `scope`：整仓库、某个可运行系统、包、模块或用户指定机制。
- `write_mode`：`artifacts` 或 `inline`；默认为 `artifacts`。
- `output`：用户指定的分析目录；否则为 `<target>/_项目分析/`。`inline` 模式只记录路径基准，不创建目录。

明确仓库根、目标根、输出根和证据路径基准，将输出目录加入勘探排除集。若 `artifacts` 模式的 output 已存在，先读取既有 manifest 和文件归属：目标与路径基准兼容时按既有 ID 续作并执行必要 schema 迁移；没有可识别 manifest、目标不一致或文件归属不明时，在写入前要求用户指定新的 output。任何情况下都不以“初始化”为由覆盖未知归属文件。

在创建或更新任何分析产物前，完整读取：

- [references/routing-and-baseline.md](references/routing-and-baseline.md)：仓库层级、分析目标、深度和公共必答问题；
- [references/artifacts-and-evidence.md](references/artifacts-and-evidence.md)：产物归属、Manifest、证据状态和验收规范。

随后在写入 output 前读取并记录所有适用于 target 和 output 的仓库指令，并固定源码基线：Git 仓库记录 commit、原始工作树状态和排除 output 后的 diff hash；该 hash 覆盖 staged/unstaged diff 以及未跟踪源文件的路径与内容摘要。非 Git 仓库对目标内容生成排除 output 的内容指纹。后续证据都引用这一本次分析基线，避免 Skill 自己生成的文件污染 revision 或 dirty 状态。

`artifacts` 模式按产物规范初始化 draft 状态的 `analysis-manifest.yaml`、`00-分析范围与路由.md`、`_work/repository-map.md`、`_work/terminology.md` 和 `_work/evidence-ledger.md`。`inline` 模式在当前工作上下文中维护同等的契约、路由、术语和证据结构，不执行文件存在性验收。

完成标准：分析契约、路径基准、排除集、适用仓库指令和写入模式均已确定；公共规范已完整读取；写入前源码基线已固定；`artifacts` 模式的初始产物存在，或 `inline` 模式的等价工作状态已建立。

## 2. 建立仓库地图并选择画像

1. 使用第 1 阶段固定的 revision、原始工作树状态、内容指纹和适用仓库指令，记录目标相对路径并开始勘探。
2. 排除输出目录、`.git`、缓存、构建产物、虚拟环境、第三方依赖和生成目录；只有在它们是分析对象时才重新纳入。
3. 识别 Repository 下的 System、Package/Module、Capability 和代表性 Flow，建立仓库地图和项目术语表。
4. 根据源码、配置、测试或已有运行产物选择能力画像；为每个选中或跳过的画像保留触发证据和理由。
5. 按证据加载画像参考：
   - 发现后端、前端、CLI、桌面端、库/SDK、扩展/插件或基础设施入口时，完整读取 [references/software-profiles.md](references/software-profiles.md)；
   - 发现可训练神经网络、模型构建器、训练入口、数据管线、损失函数或实验配置时，完整读取 [references/deep-learning-profile.md](references/deep-learning-profile.md)；
   - 发现模型调用循环、上下文组装、工具调用、记忆或其他 Agent Runtime 证据时，完整读取 [references/agent-profile.md](references/agent-profile.md)；
   - 发现 `SKILL.md`、Skill 注册器或技能包时，完整读取 [references/skill-profile.md](references/skill-profile.md)。
6. 更新公共基线答案、仓库地图、术语、初始证据和画像路由；`artifacts` 模式写入对应 `_work/` 文件、范围文档和 manifest，`inline` 模式更新等价工作状态。

勘探阶段只读取仓库现有内容和已有运行产物。测试、构建、训练、安装依赖、访问网络和下载资源属于本 Skill 之外的单独任务。

完成标准：范围内所有可运行 System 和重要 Package/Module 均已归属或标记为范围外；入口、主要依赖、代表性链路和画像路由已定位；每个画像选择都有可核查理由；输出目录没有被当作项目源码分析。

## 3. 建立覆盖计划并确定执行形态

1. 将所有适用的公共基线问题和已选画像必答问题纳入覆盖清单，记录预期证据、主归属域和候选结论落点。命中 Agent 画像时，同时纳入最低能力覆盖表和实际执行边界的横切控制矩阵。
2. 判断是否需要委派。环境支持子 Agent，且存在两个以上可独立验证的 System、能力域或专题，或者单一能力域超出一个负责人的合理上下文范围时，完整读取 [references/delegation.md](references/delegation.md)；环境不支持或范围高度集中时由当前 Agent 连续完成。
3. 确定任务依赖和执行形态，再为每个必答项指定唯一负责人；根据独立入口、核心状态、协议、失败语义和设计取舍决定专题合并或拆分。`artifacts` 模式分配互不重叠的最终写入路径，`inline` 模式分配互不重叠的结论段；需要 Capability Lead 成文时，由主 Agent 同时预分配不重叠的全局 evidence ID 命名空间。
4. `artifacts` 模式将 selected/skipped domains、selected/skipped topics、负责人、依赖、artifact ID、完成条件和限制写入 manifest，并把计划产物置为 `planned`；`inline` 模式维护相同计划但不创建文件。
5. 需要派发时，主 Agent 先完成仓库地图、术语、初始证据和任务契约；`artifacts` 模式同时完成 manifest 和 `_work/task-contracts/`，且共享 `_work/` 文件始终由主 Agent 独占写入。

完成标准：每个公共或画像必答项均有唯一负责人和结论落点；`artifacts` 模式的每个写入路径只有一个负责人，`inline` 模式的结论段没有责任重叠；manifest 或等价计划完整描述范围、依赖、产物或结论段、状态、完成条件、跳过项和限制。

## 4. 执行专题分析

开始一个 domain、topic 或 artifact 时，将其状态由 `planned` 更新为 `in-progress`；完成后更新为 `complete`，无法完成时使用 `blocked` 并记录 `status_reason`。取证后确认 topic 或 artifact 不适用时使用 `not-applicable` 并记录证据；被证伪的 domain 移入 skipped domains，不创建空域目录。专题合并、拆分、跳过或更换负责人时，先更新 manifest 或等价计划，再调整产物。

对每个已选主题：

1. 从入口追踪到状态变更、持久化或外部边界；对实际存在的失败、取消、超限或资源释放逻辑，至少再追踪一条代表性边界路径。代码没有该概念时记录 `not-applicable`，不补造路径。
2. 区分预期架构与实际实现。实现事实优先来自源码、配置、测试和已有日志；作者意图标记为 `documented`，推断标记为 `inferred`，无法确认标记为 `unknown`。
3. 将重要结论写入结构化 evidence ledger 或 `inline` 等价证据集，并在专题文档或结论段中引用证据 ID。Capability Lead 使用任务契约预分配的全局 evidence ID；Investigator 返回局部 ID，由其上级在成文前核验并映射。主 Agent 最终校验证据 ID 唯一性并合并证据。
4. 用项目领域语言解释机制，先更新统一术语，再在各结论中复用。同一事实只保留一个主归属域；跨域交接在 `artifacts` 模式写入 `flows/`，在 `inline` 模式写入对应综合段。
5. 只在图能显著降低理解成本时绘制架构图、时序图、状态图或表格。
6. `reimplementation` 目标下，根据源项目语言和用户意图提供伪代码或可运行蓝图；记录覆盖范围和外部边界，不把蓝图称为已执行实现。
7. `reproduction` 目标只增强对仓库现有训练/实验证据的搜索和整理。证据足够时形成供人执行的复现说明；证据不足时记录 `blocked`、前置条件和 `unknown`，不生成臆测的训练流程或占位专题。

命中 Agent 画像时，逐项更新最低能力覆盖表和横切控制矩阵；证据改变专题边界时同步更新计划。运行证据只能使用仓库已有日志、报告或用户提供的结果。

专题完成标准：每个负责的公共或画像必答问题都有答案、`not-applicable` 或 `unknown`；重要结论有证据 ID；正常路径和适用的边界路径已覆盖；状态和实际产物一致；没有执行本 Skill 范围外的安装、下载、网络调用、训练或评测。

## 5. 综合、验收并交付

主 Agent 在所有负责人交付并完成证据合并后处理冲突，编写跨域端到端链路、项目总览、全局取舍和风险。总览只摘要并链接专题的事实来源，不复制专题全文。交付前再次检查排除 output 后的源码 revision 和工作树指纹；若相对第 1 阶段发生漂移，重新核验受影响证据，无法重核时在 limitations 中记录漂移范围。

`artifacts` 模式生成或更新 `README.md`、`01-项目总览.md` 和由 `_work/evidence-ledger.md` 派生的 `99-证据索引.md`，随后按产物规范验收并固化 manifest。`inline` 模式按同一证据状态和内容标准直接交付结果，不生成这些文件。

完成标准：

- 每个适用的公共基线问题和每个已选画像的必答问题均有证据支持的答案、`unknown` 或 `not-applicable`。
- 每个 selected domain 均为 `complete`，或者以 `blocked` 记录可核查原因；每个 selected topic 均为 `complete`，或者以 `blocked`/`not-applicable` 记录可核查原因；`artifacts` 模式下每个 artifact 也满足同一终态要求。不存在遗留的 `planned` 或 `in-progress`。
- 每个重要结论都能回溯到 revision、仓库相对路径和 symbol、配置键、测试名、已有日志条目、文档锚点或用户提供材料。
- 术语、链接、产物归属和状态相互一致；推断、未知项、范围限制和未执行验证均已显式列出。
- `artifacts` 模式的 README、范围路由、总览、manifest、专题和证据索引相互一致，所有新增文件均位于授权的 output，且 output 未被重新分析。
- `inline` 模式已给出范围、revision、核心结论、证据引用、未知项和未执行验证，不要求文件存在。
