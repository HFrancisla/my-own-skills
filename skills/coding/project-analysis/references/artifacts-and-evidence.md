# 产物与证据规范

## 默认目录

```text
_项目分析/
├── README.md
├── analysis-manifest.yaml
├── 00-分析范围与路由.md
├── 01-项目总览.md
├── backend/                  # 命中 Backend 时
├── frontend/                 # 命中 Frontend 时
├── agent/                    # 命中 Agent Runtime 时
├── deep-learning/            # 命中深度学习时；内部结构见对应画像
├── cli/                      # 命中 CLI 时
├── desktop/                  # 命中 Desktop 时
├── library/                  # 命中 Library / SDK 时
├── extension/                # 命中 Extension / Plugin 时
├── infrastructure/           # 命中 Infrastructure 时
├── skills/                   # 命中 Agent Skill 时
├── flows/                    # 至少跨越两个能力域的端到端链路
├── quality/                  # 跨域测试、安全、性能、可观测性和运营问题
├── 90-风险与改进建议.md     # 风险足以独立成文时
├── 99-证据索引.md
└── _work/
    ├── repository-map.md
    ├── terminology.md
    ├── evidence-ledger.md
    └── task-contracts/        # 仅多 Agent 执行时
```

`README.md`是阅读入口；`01-项目总览.md`是结论地图；能力域、Flow 和 Quality 分册是详细内容的单一真实来源。只为命中的能力域创建目录，不生成空目录或占位文件。

## 产物归属

目录表达知识所有权：

1. 只涉及一个能力域的架构、状态、协议、机制、域内链路和质量问题，写入该能力域目录。
2. 一条链路实际跨越两个以上能力域时，写入 `flows/`；Flow 解释交接顺序、数据和失败传播，并链接各域内部机制，不复制其详细实现。
3. Full-stack Integration、Agent 与 Backend 接缝等关系型主题归 `flows/`，不创建 `fullstack/` 或其他接缝目录。
4. 测试、安全、性能或可观测性只影响一个域时写入该域；比较多个域或描述全局治理时写入 `quality/`。
5. 项目级拓扑、全局依赖方向和跨域取舍由 `01-项目总览.md` 综合，不另设会与能力域重复的根级 `architecture/`。

每个选中能力域至少生成 `<domain>/README.md`，包含范围、所属 System/Package、入口、核心机制、域内文档导航、入站/出站契约、证据状态和未知项。一个画像覆盖多个独立 System 时，在画像目录下按稳定的 System ID 建子目录，由画像 README 汇总；单一 System 不增加这一层。

能力域内先按机制成文。只有同一机制簇已有多个独立文档时才增加子目录，避免为一篇文档制造一层目录。深度学习画像的固定分层遵循 [deep-learning-profile.md](deep-learning-profile.md)。

## Manifest

`analysis-manifest.yaml` 至少包含：

```yaml
schema_version: 1
target:
  root: .
  revision: <git revision or non-git marker>
  scope: <repository|system|package|module|mechanism>
request:
  goals: [architecture, learning]
  depth: standard
detected_units:
  - id: <stable-id>
    kind: <system/package/capability>
    evidence: [<relative path or symbol>]
selected_domains:
  - id: <backend|frontend|agent|deep-learning|cli|desktop|library|extension|infrastructure|skills>
    systems: [<system-id>]
    reason: <trigger evidence>
    owner: <agent or current>
    root: <domain-directory>/
selected_topics:
  - id: <topic-id>
    domain: <domain-id|cross-domain|quality>
    reason: <trigger evidence>
    owner: <agent or current>
    outputs: [<relative analysis path>]
skipped_topics:
  - id: <topic-id>
    reason: <verifiable reason>
artifacts:
  - path: <relative analysis path>
    status: planned|in-progress|complete|blocked
limitations: []
```

## 总览与分册

### README

包含分析对象、revision、goal/depth、一句话定位、建议阅读路径和所有产物链接。

### 项目总览

包含：

1. 项目定位与边界。
2. Repository/System/Package/Capability 全景。
3. 一至三条核心链路。
4. 核心领域语言和状态。
5. 重要设计取舍。
6. 高优先级风险与未知项。
7. 对各分册的摘要和链接。

### 专题分册

每篇分册按问题自然组织，但必须表达：

- 范围、触发证据和未覆盖范围。
- 入口、核心类型/契约和依赖。
- 正常路径和至少一条重要边界路径。
- 设计意图、获得的性质和付出的代价。
- 已验证、推断和未知结论。
- 与其他专题的契约和链接。

能力域 README 负责本域导航与综合，专题分册负责一个机制的详细分析。深度学习专题的网络源码快照与训练复现字段遵循 [deep-learning-profile.md](deep-learning-profile.md)，不以普通专题分册的摘要粒度替代完整实现和最终生效参数。

一个主题合并还是拆分，由独立入口、状态、协议、失败语义和设计取舍决定，不由预设文档数量决定。

## 证据

每条重要结论标记：

- `verified`：由源码、配置、测试或可重复运行结果直接支持。
- `inferred`：由多项证据支持，但项目未直接表达该结论。
- `unknown`：当前范围、权限或环境无法确认。

证据键格式：

```text
<revision>:<relative-path>:<symbol|config-key|test-name>[:line]
```

行号是导航信息；revision、相对路径和 symbol/配置键/测试名共同提供稳定锺点。运行证据同时记录命令、环境、退出状态和与结论相关的输出摘要。

`99-证据索引.md` 使用如下字段：

| ID | Status | Claim | Evidence | Used by |
|---|---|---|---|---|
| E-001 | verified | <claim> | <evidence key> | <document links> |

## 评估与建议

把实现事实、设计解释和改进建议分开。数字评分只在用户给出量表或不同项目需要用同一量表比较时使用；否则使用严重度、影响、证据状态和置信度，避免伪精确的总分。

## 验收清单

- Manifest 中每个 selected topic 均有完成产物或明确限制。
- Manifest 中每个 selected domain 均有唯一产物根和域级 README；未命中的画像没有占位目录。
- README、总览、分册、manifest 和证据索引的名称与链接一致。
- 项目术语在所有文档中含义一致。
- 跨域文档串联了各域交界处的实际契约。
- 域内事实只在所属域详细定义，Flow 和 Quality 通过链接引用，没有复制形成第二真实来源。
- 无重要结论仅依赖 README 或二手摘要而未检查实现。
- 推断、未知项和未执行的验证均已显式表达。
- 图表节省了理解成本，且与正文叙述一致。
- 已有的非管理文件和项目源码保持未受影响。
