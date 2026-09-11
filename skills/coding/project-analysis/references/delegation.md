# 多 Agent 分析编排

分析按知识边界分工，产物按阅读体验组织。主 Agent 拥有范围、路由、共享证据和跨域结论；子 Agent 只负责独占的域内证据，并在 `artifacts` 模式按任务契约编写域内文档。

## 选择执行形态

### 单 Agent

当仓库只有一个主要 System、核心路径高度集中、专题共享同一组类型，且只需少量分册时，由当前 Agent 连续完成。

### 任务并行

当存在两个以上可独立验证的 System、能力域或专题时，由主 Agent 完成勘探和覆盖清单，再按知识簇派发，例如 Backend、Frontend、Agent Runtime、Deep Learning、Skill/Extension、Infrastructure/Quality。并行任务必须拥有互不重叠的证据范围；`artifacts` 模式下还必须拥有互不重叠的最终文档写入路径。

### 二级调研

只有当某能力域横跨多个独立包、具有多条复杂链路，或局部源码无法在一个负责人的有效上下文中完整覆盖时，才由能力负责人派生调研 Agent。层级保持为“主 Agent → 能力负责人 → 调研 Agent”，调研 Agent 返回证据包，由能力负责人统一成文。

## 角色

### 主 Agent / Integrator

- 确定分析契约、路径基准和 revision；
- 建立仓库地图、术语表、manifest/evidence ledger 或 inline 等价工作状态；
- 划分不重叠的知识边界；为 Capability Lead 预分配唯一 evidence ID 命名空间，`artifacts` 模式同时分配唯一写入路径；
- `artifacts` 模式独占 `_work/`、根级总览、`flows/`、跨域 `quality/` 和最终证据索引；`inline` 模式独占对应综合结论；
- 在所有能力负责人交付后整合跨域链路、项目总览、全局取舍和风险；
- 回到原始源码核对冲突结论。

### 能力负责人 / Capability Lead

- 读取共享上下文，然后验证负责范围内的源码、配置和已有产物；
- 拥有一个知识簇的结论并统一其中的术语和调用链；`artifacts` 模式按任务契约拥有对应最终文档；
- 始终返回结构化证据包；任务契约分配了最终文档时，同时只写入指定的能力域路径；
- 显式记录跨域依赖、冲突、未知项和 `not-applicable`；
- 将跨域发现交给主 Agent，不直接写入 `flows/`、`quality/` 或共享账本。

### 调研 Agent / Investigator

- 围绕一个机制或局部包定位入口、核心类型、正常和边界路径；
- 返回结构化证据包，不编写与其他负责人重叠的最终文档；
- 对直接结论核验原始证据，不把共享摘要当作事实来源。

## 共享上下文

主 Agent 在派发前创建并维护共享上下文。`artifacts` 模式使用以下文件；`inline` 模式将同等内容作为只读快照放入任务契约，不创建 `_work/`：

```text
<output>/_work/
├── repository-map.md      # System、包、入口和依赖导航
├── terminology.md         # 统一领域语言
├── evidence-ledger.md     # 唯一证据事实来源
└── task-contracts/        # 各负责人的任务契约
```

共享上下文对负责人只读。子 Agent 通过证据包返回新增事实；主 Agent 负责合并、去重和冲突处理，避免多个 Agent 同时修改同一文件。

## 任务契约

每个派发任务至少包含：

```yaml
task: <能力域或局部机制>
role: capability-lead|investigator
revision: <git revision or non-git fingerprint>
scope:
  include: [<目录/包/入口>]
  exclude: [<由其他负责人处理的范围>]
questions: [<必须回答的机制问题>]
depends_on: [<task-id>]
shared_context: [<repository-map>, <terminology>, <evidence-ledger>]
evidence_ids: <Capability Lead 的全局 ID 命名空间；Investigator 使用 local>
outputs: [<artifacts 模式下 Capability Lead 的独占路径；inline 或 Investigator 使用 []>]
completion:
  - <正常路径已有证据>
  - <相关边界路径已有证据或 not-applicable>
  - <负责的画像必答项已有结论和证据>
  - <结构化证据包已返回>
  - <未知项已记录>
```

对 Backend 内的 Agent 功能，将 Backend 与 Agent Runtime 分配给不同能力负责人；跨域契约由主 Agent 统一整合，`artifacts` 模式写入 `flows/`。Agent Runtime 负责人先拥有最低能力覆盖表和横切控制矩阵，再按 Instruction/Context、Loop/Translation/Provider、Tools/Governance、State/Memory、Reliability/Observability、Subagents/Scheduling 等证据簇派生调研 Agent，并保留 Agent 结论的统一所有权。每个调研任务明确负责的最低能力项，汇总后不得出现无人覆盖项。

深度学习范围较大时，可按“设计与网络实现”和“训练配置与复现说明”拆成调研任务。后者只分析仓库已有代码、配置、日志和文档，返回供人执行的流程说明；不下载资源、不安装依赖、不运行训练。模型源码引用或用户明确要求的源码快照只能有一个写入负责人。

## 证据包

调研 Agent 返回：

```yaml
topic: <topic-id>
entrypoints:
  - path: <relative-path>
    symbol: <symbol>
core_types: [<type>]
findings:
  - id: <Capability Lead 使用预分配全局 ID；Investigator 使用 local-id>
    status: verified|documented|inferred|unknown|not-applicable
    kind: source|config|test|existing-log|document
    claim: <fact or documented claim>
    evidence: <path + symbol/test/config/log anchor>
flows:
  - name: <flow>
    kind: normal|failure|cancel|limit|not-applicable
dependencies: [<cross-domain dependency>]
unknowns: [<unresolved question>]
suggested_artifacts: [<optional output split>]
```

Capability Lead 使用任务契约预分配的全局 evidence ID，并在证据包和最终文档中保持一致。Investigator 使用局部 ID，由直接上级核验并在成文前映射到对应 Lead 的全局命名空间；主 Agent 最终检查 ID 唯一性并合并 evidence ledger。

## 并发与整合门

- 只并行执行证据范围可独立验证的任务；`artifacts` 模式还要求最终写入路径不重叠；
- 需要共享类型、契约或上游结论的任务在依赖完成后执行；
- Capability Lead 和 Investigator 都必须返回证据包；前者使用预分配的全局 evidence ID 并只写任务契约分配的最终文档，后者使用局部 ID且不写最终文档；
- 子 Agent 不写 `_work/`、根级总览、`flows/`、跨域 `quality/` 或 `99-证据索引.md`；
- 主 Agent 在能力负责人交付后统一合并证据、编写跨域文档和最终总览；
- 冲突结论回到原始证据处解决，无法确认时标记 `unknown`。
