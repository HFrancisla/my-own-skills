# 多 Agent 分析编排

分析按知识边界分工，文档按阅读体验组织。一个负责人可以生成多篇文档；一篇跨域文档由统一负责人整合多方证据。

## 选择执行形态

### 单 Agent

当仓库只有一个主要 System、核心路径高度集中、专题共享同一组类型，且预计只需少量分册时，由当前 Agent 连续完成。

### 能力域并行

当存在两个以上可独立验证的 System 或能力域时，由主 Agent 完成勘探，然后按 Backend、Frontend、Agent Runtime、Deep Learning、Skill/Extension、Infrastructure/Quality 等知识簇派发。这是大型项目的默认形态。

### 二级调研

只有当某能力域自身横跨多个独立包、具有多条复杂链路，或局部源码无法在一个负责人的有效上下文中完整覆盖时，才由能力负责人派生调研 Agent。层级保持为“主 Agent → 能力负责人 → 调研 Agent”，调研 Agent 返回证据包，由能力负责人统一成文。

## 角色

### 主 Agent / Integrator

- 确定分析契约和 revision。
- 建立仓库地图、术语表、manifest 和证据账本。
- 划分不重叠的知识边界与写入路径。
- 整合跨域链路、项目总览、全局取舍和风险。
- 对子 Agent 结论做冲突检查和重要证据抽查。
- 独占根级总览、`flows/` 和跨域 `quality/` 的最终写入；从能力负责人证据中整合接缝，不复制域内分析。

### 能力负责人 / Capability Lead

- 读取共享上下文，然后验证负责范围内的源码。
- 拥有一个知识簇的最终文档，并统一其中的术语和调用链。
- 更新证据账本，显式记录跨域依赖、冲突和未知项。
- 只在本域内存在足够独立的调研分支时派生二级 Agent。
- 独占 manifest 指定的能力域目录，并负责该域 README；域内质量问题留在本域，跨域发现作为证据包交给主 Agent。

### 调研 Agent / Investigator

- 围绕一个机制或局部包定位入口、核心类型、正常和边界路径。
- 返回结构化证据包，不编写与其他负责人重叠的最终文档。
- 对直接结论自行核验原始证据，不把共享摘要当作事实来源。

## 共享上下文包

主 Agent 在派发前提供：

```text
_项目分析/_work/
├── repository-map.md      # System、包、入口和依赖导航
├── terminology.md         # 统一领域语言
├── evidence-ledger.md     # 可复用证据和状态
└── task-contracts/        # 各负责人的任务契约
```

共享上下文是导航索引，不是源码的替代品。

## 任务契约

每个派发任务至少包含：

```yaml
task: <能力域或局部机制>
revision: <git revision>
scope:
  include: [<目录/包/入口>]
  exclude: [<由其他负责人处理的范围>]
questions: [<必须回答的机制问题>]
shared_context: [<repository-map>, <terminology>, <evidence-ledger>]
outputs: [<独占写入路径>]
completion:
  - <正常路径已有证据>
  - <重要边界路径已有证据>
  - <未知项已记录>
```

对 Backend 内的 Agent 功能，将 Backend 与 Agent Runtime 分配给不同能力负责人；跨域契约由主 Agent 整合。Agent Runtime 负责人可为 Context/Memory、Tools/Sandbox、Loop/Scheduling 等局部机制派生调研 Agent，但保留 Agent 专题文档的统一所有权。

深度学习范围较大时，可按“设计与网络实现”和“数据与训练 recipe”拆成调研任务，但由同一 Deep Learning 能力负责人校验模型变体、数据集、配置和指标的一一对应关系，并统一成文。原始源码快照只能有一个写入负责人。

## 证据包

调研 Agent 返回：

```yaml
topic: <topic-id>
entrypoints:
  - path: <relative-path>
    symbol: <symbol>
core_types: [<type>]
verified_findings:
  - claim: <fact>
    evidence: <path + symbol/test/config>
flows:
  - name: <flow>
    kind: normal|failure|cancel|limit
dependencies: [<cross-domain dependency>]
unknowns: [<unresolved question>]
suggested_artifacts: [<optional output split>]
```

## 并发与整合门

- 只并行执行写入路径不重叠、证据范围可独立验证的任务。
- 需要共享类型、契约或上游结论的任务在依赖完成后执行。
- 主 Agent 在所有能力负责人交付后才编写跨域文档和最终总览。
- 冲突结论回到原始证据处解决，并在无法确认时标记 `unknown`。
