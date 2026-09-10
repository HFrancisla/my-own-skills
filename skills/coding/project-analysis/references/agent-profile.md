# Agent Runtime 分析画像

Agent 是能力画像，可与 Backend、Frontend、CLI、Desktop、Extension、Skill 和 Library/SDK 同时命中。命中后以 `agent/` 为主归属根；对外接缝按根级产物规范写入 `flows/`，不在 Agent 和宿主域复制同一事实。`agent/README.md` 汇总 Runtime 入口、核心状态、内部专题和接缝链接。

本画像分析源码、配置、测试和仓库已有的运行轨迹。运行轨迹用于解释已有行为；本 Skill 不主动运行 Agent、调用模型或调用工具。

## Runtime Loop

**触发**：存在模型请求、消息状态和工具结果之间的迭代控制。

**必答**：任务如何创建和进入循环；模型响应如何解析；工具调用如何回灌；终态、取消、轮次上限、无进展和错误如何判定；同步、流式或后台运行是否共享核心状态机。某类路径不存在时标记 `not-applicable`。

## Context Assembly

**触发**：存在 Prompt/Message Builder、多源上下文注入、Token 计数、历史裁剪或摘要。

**必答**：上下文来源、权威和排序；预算分配；缓存；截断、压缩和恢复；工具结果处理；用户数据与指令的信任区分；超限后的失败路径。

## Tool System and Action Surfaces

**触发**：工具 Schema、注册表、调度器、Shell/浏览器/MCP/自定义动作面或工具结果模型。

**必答**：工具如何发现和暴露给模型；参数和结果契约；并行或串行调度；超时、取消、输出截断和错误回馈；权限、审批、沙箱和审计；工具与 Runtime Loop 的边界。对 Shell、Browser、MCP 等独立动作面，在证据充足时拆分文档。

## Model Provider and Routing

**触发**：多 Provider Adapter、模型选择器、降级、重试、能力协商或计费统计。

**必答**：内部请求模型；Provider 差异如何被 Adapter 吸收；模型选择输入；可重试错误与终止错误；降级对语义、工具和上下文上限的影响。

## Session, State and Memory

**触发**：Session/Run/Thread、Checkpoint、Transcript、短期/长期记忆、恢复或轨迹持久化。

**必答**：核心状态容器与所有权；Run、Session、Message、Event 等概念的区别；写入时机和一致性；恢复、重放、去重和清理；记忆检索如何进入 Context。

## Subagents and Scheduling

**触发**：子 Agent 派生、任务图、队列、并发调度、邮箱或层级资源限制。

**必答**：派生契约和上下文继承；所有权、状态聚合和失败传播；并发上限、取消和资源配额；循环派生或孤儿任务的防御。

## Safety and Governance

**触发**：审批、沙箱、权限策略、秘密处理、输入分类、审计或策略拦截。

**必答**：信任边界；用户、模型、工具和运行环境的权限传递；决策时机；默认策略；审批结果如何绑定到实际操作；失效时状态。

## Observability and Evals

**触发**：Trace/Span、结构化事件、Token/成本/延迟指标、轨迹重放、Eval Case、Judge 或基准数据。

**必答**：事件模型和关联 ID；哪些决策可被观测；敏感数据处理；成本归属；评测输入、判定、可重复性和轨迹重放的真实性。只有仓库已有评测结果时记录结果，不主动执行评测。

## Gateway

**触发**：多平台消息 Adapter、会话路由、富媒体桥接、连接保活或投递保障。

**必答**：平台消息如何归一化；会话键和租户隔离；平台能力差异；重连、去重、顺序和投递语义；入站到 Agent Run 以及出站回复的完整链路。

## Agent 与 Backend 的接缝

当 Agent 作为后端功能存在时，分别分析 Backend 与 Agent Runtime 的内部实现，并由主 Agent 在 `flows/` 整合：

- API/消息如何创建 Agent Run；
- 身份、租户、权限和请求上下文如何传入 Runtime；
- 流式事件、中间状态和终态如何返回调用方；
- Run/Session/Transcript 如何借助后端持久化；
- 后台执行、恢复、取消、限流和计费如何跨越接缝。

## 成文标准

某主题至少拥有独立入口、核心状态/协议、重要边界路径或值得说明的设计取舍之一时，生成独立文档；否则并入 Agent Runtime 总览。同一负责人可为同一知识簇生成多篇文档，但事实只保留在一个主归属域。
