# 产物与证据规范

## 默认目录

```text
_项目分析/
├── README.md
├── analysis-manifest.yaml
├── 00-分析范围与路由.md
├── 01-项目总览.md
├── architecture/             # 按需
├── flows/                    # 按需
├── capabilities/             # 按需
├── quality/                  # 按需
├── 90-风险与改进建议.md     # 风险足以独立成文时
├── 99-证据索引.md
└── _work/
    ├── repository-map.md
    ├── terminology.md
    ├── evidence-ledger.md
    └── task-contracts/        # 仅多 Agent 执行时
```

`README.md`是阅读入口；`01-项目总览.md`是结论地图；分册是详细内容的单一真实来源。不为没有实质内容的目录或预设主题创建空文件。

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
selected_topics:
  - id: <topic-id>
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
- README、总览、分册、manifest 和证据索引的名称与链接一致。
- 项目术语在所有文档中含义一致。
- 跨域文档串联了各域交界处的实际契约。
- 无重要结论仅依赖 README 或二手摘要而未检查实现。
- 推断、未知项和未执行的验证均已显式表达。
- 图表节省了理解成本，且与正文叙述一致。
- 已有的非管理文件和项目源码保持未受影响。
