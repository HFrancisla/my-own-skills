# Agent Runtime 分析画像

Agent 是能力画像，可与 Backend、Frontend、CLI、Desktop、Extension、Skill 和 Library/SDK 同时命中。命中后以 Agent 为主知识域；`artifacts` 模式使用 `agent/` 作为产物根，并将对外接缝写入 `flows/`，不在 Agent 和宿主域复制同一事实。`agent/README.md` 汇总 Runtime 入口、核心状态、最低能力覆盖、内部专题和接缝链接；`inline` 模式给出等价结构。

本画像分析源码、配置、测试和仓库已有的运行轨迹。运行轨迹用于解释已有行为；本 Skill 不主动运行 Agent、调用模型或调用工具。

## 分析边界与覆盖规则

Agent Runtime 是模型请求、上下文、工具、状态和执行控制形成的运行闭环；Harness 是承载该闭环并提供模型、工具、会话、安全和运营能力的宿主。项目可以采用不同边界和名称，分析时以实际所有权和调用关系为准，不把这一区分强加给源码。

命中 Agent 画像后，先建立项目自己的核心概念表，至少辨析 `Agent`、`Task`、`Run`、`Session`、`Thread`、`Turn`、`Message`、`Event`、`Tool Call`、`Approval`、`Checkpoint` 和 `Memory`。项目没有某个概念时记录 `not-applicable`；名称不同但语义相同时使用项目术语并注明映射；无法从现有证据确认时记录 `unknown`。

`artifacts` 模式下，`agent/README.md` 必须包含“最低能力覆盖表”；`inline` 模式在最终回答中给出等价表。逐项列出以下能力的结论状态、证据 ID 和主归属文档或结论段：

| 能力 | 最低检查范围 |
|---|---|
| System Prompt | 指令来源、优先级、组装、版本和信任边界 |
| Tools | 发现、Schema、暴露、调度和结果回灌 |
| Agentic Loop | 进入、迭代、终态、错误、流式和后台路径 |
| Translation Layer | 内部规范模型与 Provider、工具、宿主协议转换 |
| Context Management | 来源、顺序、预算、缓存、裁剪和失败路径 |
| Memory | 写入、检索、注入、隔离、更新和删除 |
| Session State | Run/Session/Thread 状态、持久化、恢复和清理 |
| Permissions | 主体、资源、动作、作用域、继承和执行时校验 |
| Approvals | 请求、绑定、决定、有效期、恢复和审计 |
| Sandboxing | 进程、文件、网络、环境、资源和产物边界 |
| Retry | 错误分类、退避、预算、幂等和副作用防重 |
| Timeout | 分层时限、deadline 传播、到期状态和资源回收 |
| Observability | Event、Log、Trace、Metric、关联 ID 和脱敏 |
| Cost Accounting | 用量、价格、归属、预算、重试和子任务成本 |
| Compaction | 触发、保留规则、摘要、恢复和信息损失 |
| Interrupts | 取消、暂停、steering、信号传播、终止和恢复 |
| Human-in-the-loop | 澄清、审批、修改、拒绝、接管和继续执行 |
| Trust, Secrets and Input Safety | 输入信任分类、秘密最小暴露、注入防护和输出脱敏 |

覆盖表建议使用 `能力 | 结论状态 | 结论摘要 | 证据 ID | 主归属文档` 五列；结论状态沿用 evidence ledger 的 `verified`、`documented`、`inferred`、`unknown` 和 `not-applicable`。`documented` 只表示项目材料声明了该能力，不证明实现存在。

最低覆盖不等于固定文档数量。规划阶段先建立全部覆盖项、负责人和候选结论落点，再依据初始证据决定专题边界；执行中填充结论，并随新证据调整合并或拆分。`survey` 可在域级 README 或 inline 结果中合并回答；`standard` 和 `deep` 根据独立入口、状态、协议、失败语义和设计取舍拆分专题。能力存在但本次范围未深入时不得写成 `not-applicable`，应记录已知证据、范围限制和 `unknown`。

## System Prompt and Instruction Model

**触发**：存在任何发送给模型的 system/developer instruction、Prompt 模板、策略文本、项目指令、用户偏好或动态规则注入。

**必答**：指令来自代码、配置、组织策略、用户、工作区、Skill 还是运行时状态；各来源的权威、顺序、覆盖和冲突规则；何时组装、是否版本化或缓存；模型、模式和任务是否选择不同模板；外部文件、网页、工具结果等不可信数据如何与指令分隔；最终 Prompt 如何被观测、脱敏和测试。区分稳定指令、动态上下文和普通用户数据，不把所有 Prompt 内容统称为 Context。

## Context Management and Compaction

**触发**：存在 Message/Prompt Builder、多源上下文注入、Token 计数、历史裁剪、工具结果压缩或摘要。

**必答**：上下文来源、所有权、信任级别、排序和去重；不同来源的 Token 预算和保留优先级；模型窗口和缓存如何影响组装；工具结果、附件和多模态内容如何进入上下文；截断、折叠、摘要和 Compaction 的触发阈值、保留不变量及信息损失；压缩结果如何持久化、恢复和再次压缩；超限、计数失败或摘要失败时的终态。明确 System Prompt、Session State 和 Memory 进入 Context 的接缝，但不复制其内部事实。

## Runtime / Agentic Loop

**触发**：存在模型请求、消息状态、工具结果或其他动作之间的迭代控制。

**必答**：任务如何创建、校验并进入循环；每轮的输入状态、模型调用、响应解析、动作派发和 Observation 回灌顺序；结构化输出、工具调用和普通文本如何决定下一步；成功、失败、取消、暂停、轮次上限、预算上限、无进展和协议错误如何形成终态；同步、流式、后台和恢复路径是否共享一个状态机；循环退出后如何提交状态、产物和最终响应。只有源码明确采用 ReAct 时才使用该名称，不要求或推断隐藏思维过程。

## Translation Layer and Model Providers

**触发**：存在 Provider Adapter、内部消息模型、协议转换、模型路由、能力协商、流式事件归一化或降级。

**必答**：Runtime 的规范请求、响应和事件模型是什么；角色、文本、多模态 Content Block、Tool Schema、Tool Call ID、Tool Result、Finish Reason、Usage、Error 和流式 Delta 如何双向转换；未知字段、顺序、关联 ID 和 Provider 扩展如何保留；哪些转换有损以及如何报告；模型能力、上下文上限和工具能力如何协商；路由输入、Fallback 条件及降级对语义的影响；Provider 的认证、传输和 SDK 生命周期位于何处。将协议转换与业务决策分开描述。

## Tool System and Action Surfaces

**触发**：存在工具 Schema、注册表、调度器、Tool Host、Shell、Browser、MCP、自定义动作面或工具结果模型。

**必答**：工具如何发现、注册、命名、去重、启用并暴露给模型；参数 Schema 和返回契约如何校验、转换和版本化；调用 ID 如何关联请求、执行和结果；工具串行、并行和有副作用调用如何排序；输出如何流式返回、截断、持久化和回灌；错误如何归一化并反馈给模型；权限、审批、沙箱、超时、重试和取消分别在哪个边界执行；Runtime Loop 与 Tool Runtime 如何交换状态。Shell、Browser、MCP、代码执行器和其他动作面仅在证据充足时拆分文档。

## Session State, Checkpoints and Transcript

**触发**：存在 Session/Run/Thread、事件流、Checkpoint、Transcript、恢复、分支或轨迹持久化。

**必答**：核心状态容器、标识符、不变量和所有者；Task、Run、Session、Thread、Turn、Message、Event 和 Artifact 的实际区别；状态写入时机、事务边界、并发控制和一致性；事件日志、快照、Checkpoint 与 Transcript 的关系；恢复、重放、Fork、去重、幂等和部分写入处理；配置、模型、权限和审批决定是否随 Run 固化；终态后的保留、清理和数据生命周期。不要把可观测日志自动视为可恢复状态。

## Memory

**触发**：存在超出当前 Context 或 Run 生命周期的事实、偏好、经验、摘要、索引或检索存储。

**必答**：工作记忆、会话记忆和长期记忆如何定义；谁在何时依据什么规则写入；来源、租户、用户和 Session 如何隔离；关键词、向量、图或其他检索如何召回并排序；Memory 如何进入 Context；冲突、过期、污染和提示注入如何处理；用户如何查看、更正、删除或禁用记忆；写入失败、检索失败和无结果的行为。项目只有会话历史或 Checkpoint 时，不将其误称为长期记忆。

## Reliability: Retry, Timeout and Interrupts

**触发**：任一模型、工具、存储、队列、子 Agent、Gateway 或宿主边界存在失败、等待、取消或资源上限。

**必答 Retry**：每个边界如何区分可重试、不可重试和结果未知；最大次数、退避、Jitter、Retry-After 和总重试预算；重试由哪一层拥有；幂等键、调用 ID、事务或补偿如何阻止重复副作用；模型 Fallback 是否属于重试以及是否改变语义；重试成本如何归属。

**必答 Timeout**：Run、Turn、模型、工具、审批等待、子 Agent 和外部连接有哪些独立 timeout；相对 timeout 如何转换并受上层 deadline 限制；排队、流式读取和重试是否计入；到期时如何取消下游、回收进程和连接、保存部分状态并形成终态。

**必答 Interrupts**：用户取消、暂停、修改方向或 steering，以及系统关闭、配额耗尽、父任务取消和 Provider 断流如何进入 Runtime；信号如何穿过 Loop、流、工具、子 Agent 和沙箱；优雅停止与强制终止的边界；竞态和迟到结果如何处理；暂停后能否恢复、从哪个 Checkpoint 恢复。明确区分 cancel、pause、interrupt 和 timeout 的状态语义。

为存在的执行边界建立横切控制矩阵，至少包含 `model`、`tool`、`persistence`、`subagent`、`gateway/transport` 和 `overall run`，列出 retry owner、timeout/deadline、interrupt propagation、idempotency、terminal state 和证据；不存在的边界标记 `not-applicable`。

## Permissions, Approvals and Human-in-the-loop

**触发**：存在身份、权限策略、能力授予、审批、人工输入、暂停恢复、策略拦截或审计。

**必答 Permissions**：用户、服务、Agent、模型、工具和运行环境分别是什么主体；资源与动作如何表达；权限从入口到 Runtime、工具和子任务如何传递、收窄和撤销；默认策略、作用域、租户隔离及检查时机；策略缺失、不可用或判断失败时的行为。区分“模型看得到工具”和“运行时允许执行工具”。

**必答 Approvals**：什么动作需要批准；审批请求是否绑定规范化后的具体参数、资源、主体、Run 和策略版本；批准、拒绝、修改、过期和撤销如何表示；一次性与持续授权的作用域；批准后执行前是否重新校验；挂起、恢复、竞态和审计如何处理。不能只检查模型生成的展示文本。

**必答 Human-in-the-loop**：除审批外，系统在何处请求澄清、计划确认、参数修改、结果复核、人工接管或方向调整；人工输入如何关联当前状态并防止迟到响应污染新状态；等待期间资源是否释放；恢复后从哪个步骤继续；无交互通道时如何降级或终止。

## Trust, Secrets and Input Safety

**触发**：存在外部文件、网页、消息、检索结果或工具输出等不可信输入，或者 Runtime 可接触凭据、Token、用户隐私和其他敏感数据。

**必答**：输入如何按来源和信任级别分类，数据与指令如何分隔；间接 Prompt Injection、工具描述污染、Memory 污染和跨会话数据泄漏如何防御；秘密从哪里加载、哪些组件可见、是否进入模型上下文、工具参数、日志、Trace、Transcript、Checkpoint 或 Artifact；输出、错误和遥测如何脱敏；网络与工具出口如何限制敏感数据外传；租户隔离、保留、删除和策略失效时的行为。区分输入过滤、权限决策、沙箱隔离和输出脱敏各自能够保证的边界，不把字符串过滤描述为完整的注入防御。

## Sandboxing and Isolation

**触发**：存在命令、代码、浏览器、插件或其他不可信执行环境。

**必答**：隔离单元是进程、容器、虚拟机、远程沙箱还是策略代理；文件系统、工作区、网络、进程、系统调用、环境变量、凭据、CPU、内存、磁盘和时间如何限制；沙箱策略与 Permissions/Approvals 如何组合；宿主与沙箱之间如何传输输入、流式输出和产物；复用、快照、销毁和异常清理语义；逃逸面、宿主守护进程和未隔离动作面。没有执行隔离时明确记录信任假设和风险。

## Observability and Cost Accounting

**触发**：存在 Event、Log、Trace/Span、Metric、审计、状态通知、Token/成本/延迟指标或预算控制。

**必答 Observability**：事件模型、时间和关联 ID 如何连接 Session、Run、Turn、模型、工具、审批和子任务；输入、决策、状态转移、重试、超时、中断和终态中哪些可观测；同步、流式和后台状态如何暴露；日志、Trace、Metric、Transcript 和审计记录的职责边界；采样、缓冲、丢失、导出、保留和敏感数据脱敏；运行状态能否支持故障定位而不泄露秘密或隐藏推理。

**必答 Cost Accounting**：输入、输出、缓存、推理、多模态和工具等用量从何处取得；价格表、币种和模型版本如何绑定；重试、Fallback、并行分支和子 Agent 成本如何归属到用户、租户、Session 和 Run；预估与实收如何区分；Provider 缺失或迟到 Usage 如何处理；预算在调用前、流式中和调用后如何执行；超限如何中断并形成可解释终态。只有延迟或 Token 指标时，不宣称实现了成本核算。

## Subagents and Scheduling

**触发**：存在子 Agent 派生、任务图、队列、并发调度、邮箱、Worker 或层级资源限制。

**必答**：派生契约、上下文和权限继承；父子身份、状态所有权、通信和结果聚合；队列、公平性、并发上限、背压和资源配额；失败、重试、超时和取消如何传播；成本如何汇总；循环派生、深度膨胀、孤儿任务和迟到结果如何防御。普通后台任务不自动视为子 Agent。

## Evals and Replay

**触发**：存在 Eval Case、Benchmark、Judge、模拟 Provider/Tool、轨迹重放或回归数据。

**必答**：评测输入、环境、模型和工具版本如何固定；成功判定、Judge 和容差；非确定性、污染和重复运行如何处理；Replay 是重新执行副作用、模拟结果还是仅重建视图；录制轨迹是否足以复现关键决策；评测覆盖哪些 Runtime 路径。只有仓库已有结果时记录结果，不主动执行评测。

## Gateway

**触发**：存在多平台消息 Adapter、会话路由、富媒体桥接、连接保活或投递保障。

**必答**：平台消息如何转换为 Runtime 的规范输入和输出；会话键、身份、租户与权限如何映射；平台能力和格式差异如何协商或降级；重连、超时、重试、去重、顺序和投递语义；Webhook、轮询和长连接的生命周期；入站消息到 Agent Run 以及出站回复的完整链路。Gateway 的协议归一化归 Gateway，模型 Provider 的消息转换归 Translation Layer。

## Agent 与宿主域的接缝

Agent 作为后端、CLI、桌面端、IDE 扩展或消息服务中的能力时，分别分析宿主域与 Agent Runtime 的内部实现，并由主 Agent 在 `flows/` 整合：

- 外部输入如何创建、恢复、查询、暂停和取消 Agent Run；
- 身份、租户、权限、配置和请求上下文如何传入 Runtime；
- 流式事件、中间状态、审批请求、成本和终态如何返回调用方；
- Session、Transcript、Checkpoint、Memory 和 Artifact 由谁持久化；
- 后台执行、限流、背压、重试、超时和资源清理如何跨越接缝；
- Translation Layer 在宿主 API、Runtime 规范模型和外部 Provider 之间由谁拥有。

## 成文与验收

- 规划阶段建立最低能力覆盖项、负责人和候选结论落点；执行中填充答案，并依据证据调整专题边界。缺少实现是分析结论，不生成空专题。
- 每个选中主题从入口追踪一条正常路径，并对实际存在的 failure、retry、timeout、interrupt、approval 或 recovery 路径至少追踪一条代表性边界路径。
- 关键结论落入 evidence ledger；源码事实、文档意图、推断、未知和不适用分别使用既定状态。
- 原始源码摘录保持原样；解释写在摘录外。逻辑蓝图仅在 `reimplementation` 目标或确实降低理解成本时生成，并保持源项目的并发、类型和状态语义。
- 源码锚点以 revision、仓库相对路径和 symbol/test/config key 为主，行号只作辅助，不使用浮动行号代替稳定锚点。
- 图只在能澄清状态、时序、信任边界或数据流时绘制；图中的节点必须能回到正文和证据。
- 验收时确认最低能力覆盖表中的全部能力均有证据支持的答案、`not-applicable` 或 `unknown`，横切控制矩阵覆盖所有实际执行边界，且同一事实只有一个主归属文档。
