# 多 Agent 分析编排

分析按知识边界分工，文档按阅读体验组织。主 Agent 拥有范围、路由、共享账本和跨域结论；子 Agent 只负责独占的域内证据和文档。

## 选择执行形态

### 单 Agent

当仓库只有一个主要 System、核心路径高度集中、专题共享同一组类型，且只需少量分册时，由当前 Agent 连续完成。

### 能力域并行

当存在两个以上可独立验证的 System 或能力域时，由主 Agent 完成勘探，然后按 Backend、Frontend、Agent Runtime、Deep Learning、Skill/Extension、Infrastructure/Quality 等知识簇派发。并行任务必须拥有互不重叠的最终文档写入路径。

### 二级调研

只有当某能力域横跨多个独立包、具有多条复杂链路，或局部源码无法在一个负责人的有效上下文中完整覆盖时，才由能力负责人派生调研 Agent。层级保持为“主 Agent → 能力负责人 → 调研 Agent”，调研 Agent 返回证据包，由能力负责人统一成文。

## 角色

### 主 Agent / Integrator

- 确定分析契约、路径基准和 revision；
- 建立仓库地图、术语表、manifest 和 evidence ledger；
- 划分不重叠的知识边界与写入路径；
- 独占 `_work/`、根级总览、`flows/`、跨域 `quality/` 和最终证据索引；
- 在所有能力负责人交付后整合跨域链路、项目总览、全局取舍和风险；
- 回到原始源码核对冲突结论。

### 能力负责人 / Capability Lead

- 读取共享上下文，然后验证负责范围内的源码、配置和已有产物；
- 拥有一个知识簇的最终文档，并统一其中的术语和调用链；
- 返回结构化证据包，或只写入 manifest 指定的能力域目录；
- 显式记录跨域依赖、冲突、未知项和 `not-applicable`；
- 将跨域发现交给主 Agent，不直接写入 `flows/`、`quality/` 或共享账本。

### 调研 Agent / Investigator

- 围绕一个机制或局部包定位入口、核心类型、正常和边界路径；
- 返回结构化证据包，不编写与其他负责人重叠的最终文档；
- 对直接结论核验原始证据，不把共享摘要当作事实来源。

## 共享上下文

主 Agent 在派发前创建并维护：

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
revision: <git revision or non-git fingerprint>
scope:
  include: [<目录/包/入口>]
  exclude: [<由其他负责人处理的范围>]
questions: [<必须回答的机制问题>]
depends_on: [<task-id>]
shared_context: [<repository-map>, <terminology>, <evidence-ledger>]
outputs: [<独占写入路径>]
completion:
  - <正常路径已有证据>
  - <相关边界路径已有证据或 not-applicable>
  - <未知项已记录>
```

对 Backend 内的 Agent 功能，将 Backend 与 Agent Runtime 分配给不同能力负责人；跨域契约由主 Agent 写入 `flows/`。Agent Runtime 负责人可为 Context/Memory、Tools/Sandbox、Loop/Scheduling 等局部机制派生调研 Agent，但保留 Agent 专题文档的统一所有权。

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
  - id: <local-id>
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

主 Agent 将确认后的 findings 转换为全局 evidence ledger ID。局部 ID 不直接出现在最终索引中。

## 并发与整合门

- 只并行执行最终写入路径不重叠、证据范围可独立验证的任务；
- 需要共享类型、契约或上游结论的任务在依赖完成后执行；
- 子 Agent 不写 `_work/`、根级总览、`flows/`、跨域 `quality/` 或 `99-证据索引.md`；
- 主 Agent 在能力负责人交付后统一合并证据、编写跨域文档和最终总览；
- 冲突结论回到原始证据处解决，无法确认时标记 `unknown`。
