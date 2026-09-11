# 产物、Manifest 与证据

本文件是 `artifacts` 模式下产物归属、manifest 和证据账本的唯一规范。能力画像只补充域内问题，不重新定义根级目录、状态或证据字段。`inline` 模式不创建这些文件，但沿用本文件的证据状态、归属和内容标准。

## 默认目录

以下目录只在 `artifacts` 模式创建：

```text
<output>/
├── README.md                      # 阅读入口和产物导航
├── analysis-manifest.yaml         # 范围、路由、负责人和状态
├── 00-分析范围与路由.md           # 本次分析契约和选择理由
├── 01-项目总览.md                 # 项目级结论地图
├── backend/                       # 命中 Backend 时
├── frontend/                      # 命中 Frontend 时
├── agent/                         # 命中 Agent Runtime 时
├── deep-learning/                 # 命中深度学习时
├── cli/                           # 命中 CLI 时
├── desktop/                       # 命中 Desktop 时
├── library/                       # 命中 Library / SDK 时
├── extension/                     # 命中 Extension / Plugin 时
├── infrastructure/                # 命中 Infrastructure 时
├── skills/                        # 命中 Agent Skill 时
├── flows/                         # 跨越至少两个能力域时
├── quality/                       # 跨域质量、治理或运营问题
├── 90-风险与改进建议.md           # 风险需要独立成文时
├── 99-证据索引.md                 # evidence ledger 的阅读视图
└── _work/
    ├── repository-map.md
    ├── terminology.md
    ├── evidence-ledger.md
    └── task-contracts/             # 仅多 Agent 执行时
```

只创建实际命中的能力域和实际需要的文件。`README.md` 是阅读入口，`00-分析范围与路由.md` 记录输入契约和路由决定，`01-项目总览.md` 汇总项目结论，域级文档保存域内事实，`99-证据索引.md` 由 `_work/evidence-ledger.md` 整理而来。

## 产物归属

目录表达知识所有权：

1. 只涉及一个能力域的架构、状态、协议、机制、域内链路和质量问题，写入该能力域目录。
2. 一条链路实际跨越两个以上能力域时，写入 `flows/`；Flow 解释交接顺序、数据和失败传播，并链接各域内部机制。
3. Full-stack Integration、Agent 与 Backend 接缝等关系型主题归 `flows/`，不创建 `fullstack/` 或其他接缝目录。
4. 测试、安全、性能、可观测性或运营问题只影响一个域时写入该域；比较多个域或描述全局治理时写入 `quality/`。
5. 项目级拓扑、全局依赖方向和跨域取舍由 `01-项目总览.md` 综合，不另设根级 `architecture/`。
6. 同一文件同时属于多个画像时，manifest 指定一个主归属域；其他画像只通过链接引用。跨域行为写入 Flow，不复制第二份事实。

每个选中能力域至少生成 `<domain>/README.md`，包含范围、所属 System/Package、入口、核心机制、域内文档导航、入站/出站契约、证据状态和未知项。一个画像覆盖多个独立 System 时，在画像目录下按稳定 System ID 建子目录，由画像 README 汇总；单一 System 不增加这一层。

## Manifest

`analysis-manifest.yaml` 使用 schema version 3。路径均相对 `target.path_base`，除非字段明确标记为绝对路径。继续已有 schema version 2 分析时，先保留现有 ID 和路径，将 domain/topic 状态补为 `planned` 或其实际状态，再升级到 version 3。

```yaml
schema_version: 3
target:
  repository_root: .
  target_root: <target-relative path>
  path_base: repository_root
  output_root: <output-relative path or absolute path>
  revision:
    kind: git|non-git
    commit: <commit or null>
    worktree: clean|dirty|unknown
    diff_hash: <hash excluding output or null>
request:
  goals: [architecture, learning]
  depth: standard
  scope: <repository|system|package|module|mechanism>
  write_mode: artifacts
selected_domains:
  - id: <backend|frontend|agent|deep-learning|cli|desktop|library|extension|infrastructure|skills>
    systems: [<system-id>]
    trigger_evidence: [E-001]
    reason: <why selected>
    owner: <agent or current; null until stage 3>
    root: <domain-directory>/
    status: planned|in-progress|complete|blocked
    status_reason: null # required for blocked
    completion: [<checkable condition>]
skipped_domains:
  - id: <domain-id>
    reason: <verifiable reason>
selected_topics:
  - id: <topic-id>
    domain: <domain-id|cross-domain|quality>
    trigger_evidence: [E-002]
    depends_on: [<topic-id>]
    owner: <agent or current>
    outputs: [A-001] # blocked/not-applicable topics may use []
    status: planned|in-progress|complete|blocked|not-applicable
    status_reason: null # required for blocked or not-applicable
    completion: [<checkable condition>]
skipped_topics:
  - id: <topic-id>
    reason: <verifiable reason>
artifacts:
  - id: A-001
    path: <relative analysis path>
    owner: <agent or current>
    status: planned|in-progress|complete|blocked|not-applicable
    status_reason: null # required for blocked or not-applicable
limitations: []
```

`selected_topics.outputs` 只引用 artifact ID；产物路径和状态只在 `artifacts` 中维护。Domain 和 topic 的状态描述分析工作，artifact 的状态描述文件交付，三者不得相互代替。`00-分析范围与路由.md` 应解释用户请求、范围、排除项、选中画像和跳过理由，避免与 manifest 重复保存不同版本的事实。

## 状态与文件生命周期

主 Agent 按统一顺序维护状态：

1. **初始化**：第 1 阶段先读取适用于 target/output 的仓库指令，并固定排除 output 后的源码 revision、原始工作树状态和 diff hash 或内容指纹，再创建 draft manifest、范围文档和 `_work/` 文件；尚未发现的 domain、topic 和 artifact 不创建占位项。Git `diff_hash` 覆盖 staged/unstaged diff 以及未跟踪源文件的路径与内容摘要。
2. **路由**：第 2 阶段写入 revision、仓库地图、术语、初始证据以及 selected/skipped domains；domain 负责人此时可以暂为 `null`。
3. **规划**：第 3 阶段写入 selected/skipped topics、负责人、依赖、artifact 和完成条件；计划执行的项状态为 `planned`。
4. **执行**：开始时置为 `in-progress`；完成时置为 `complete`；无法继续时置为 `blocked` 并记录 `status_reason`；取证确认 topic 或 artifact 不适用时置为 `not-applicable` 并关联证据。被证伪的 domain 从 `selected_domains` 移入 `skipped_domains`，不保留空域目录。合并、拆分、跳过或改派时先更新 manifest，再改变文件。
5. **固化**：第 5 阶段生成 README、总览和证据索引，解决状态与文件差异，并复核排除 output 后的源码是否相对初始基线漂移；最终不得遗留 `planned` 或 `in-progress`。

`00-分析范围与路由.md` 随契约和路由决定更新；`repository-map.md`、`terminology.md` 和 `evidence-ledger.md` 在勘探与执行期间增量更新；README、项目总览和证据索引在综合阶段生成或固化。已有 output 先读取 manifest 和文件归属：目标与路径基准兼容时保留既有 ID 并续作；没有可识别 manifest、目标不一致或归属不明时停止写入并要求新的 output，不覆盖既有文件。

## 文档要求

### README

包含分析对象、revision、goal/depth、一句话定位、建议阅读路径和所有产物链接。

### 项目总览

包含项目定位与边界、Repository/System/Package/Capability 全景、一至三条核心链路、核心领域语言和状态、重要设计取舍、高优先级风险与未知项，以及各分册的摘要和链接。

### 专题分册

每篇分册必须表达：

- 范围、触发证据和未覆盖范围；
- 入口、核心类型/契约和依赖；
- 正常路径和适用的边界路径；没有该类边界时标记 `not-applicable`；
- 设计意图、获得的性质和付出的代价；
- `verified`、`documented`、`inferred` 和 `unknown` 结论；
- 与其他专题的契约和链接。

一个主题合并还是拆分，由独立入口、状态、协议、失败语义和设计取舍决定，不由预设文档数量决定。

## 证据账本

`_work/evidence-ledger.md` 是分析期间唯一的证据事实来源。每条重要结论使用结构化条目：

| ID | Status | Kind | Claim | Revision | Path | Anchor | Used by |
|---|---|---|---|---|---|---|---|
| E-001 | verified | source | <claim> | <revision> | <relative path> | <symbol> | <document links> |

Evidence ID 在一次分析内必须唯一且稳定。单 Agent 可使用 `E-001` 递增；多 Agent 由主 Agent 在规划阶段为 Capability Lead 预分配命名空间，例如 `E-AGENT-001`。Investigator 的局部 ID 不进入最终文档或索引。

状态含义：

- `verified`：源码、配置、测试或仓库已有日志/报告直接支持；
- `documented`：README、注释、论文或用户提供材料明确表达，但不单独证明实现行为；
- `inferred`：由多项证据推导，项目没有直接表达；
- `unknown`：当前范围、权限或已有材料无法确认；
- `not-applicable`：该问题在目标项目或当前范围中不存在。

`Kind` 至少区分 `source`、`config`、`test`、`existing-log`、`document` 和 `user-provided`。运行证据只记录已有命令、环境、退出状态和输出摘要，不代表本 Skill 已执行该命令。

证据路径相对 `target.path_base`。`99-证据索引.md` 是账本的阅读视图，不得在其中创建与账本冲突的第二份事实。

## 评估与建议

把实现事实、设计解释和改进建议分开。数字评分只在用户给出量表或需要跨项目比较时使用；否则使用严重度、影响、证据状态和置信度，避免伪精确总分。

## 验收清单

- 每个适用的公共基线问题和每个 selected profile 的必答问题都有答案、`unknown` 或 `not-applicable`。
- Manifest 中每个 selected domain 都是 `complete` 或以 `blocked` 记录可核查原因；每个 selected topic 和 artifact 都是 `complete`，或以 `blocked`/`not-applicable` 记录可核查原因；不存在遗留的 `planned` 或 `in-progress`。
- 每个 selected domain 都有唯一产物根和域级 README；未命中的画像没有空目录。
- README、范围路由、总览、manifest、专题和证据索引的名称与链接一致；排除 output 后的源码基线没有未处理漂移。
- 项目术语在所有文档中含义一致，主归属域明确。
- 跨域文档串联实际契约，域内事实只在所属域定义。
- 重要结论没有只依赖二手摘要；作者意图、推断、未知项和未执行验证均已标记。
- 图表节省理解成本，且与正文一致。
- 所有新增文件位于 output 目录；output 目录、缓存和生成物未被重新当作源码分析。
