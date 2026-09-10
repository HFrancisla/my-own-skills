# 软件项目能力画像

一个仓库可同时命中多个画像。目录或项目名称只是线索；入口、依赖、配置、契约、测试或已有运行产物才是触发证据。没有匹配画像时使用公共基线，并在 manifest 中记录 `unprofiled` 或范围外原因。

选中的 Backend、Frontend、CLI、Desktop、Library/SDK、Extension/Plugin 和 Infrastructure 分别以 `backend/`、`frontend/`、`cli/`、`desktop/`、`library/`、`extension/` 和 `infrastructure/` 为产物根。域内事实只在主归属域定义，跨域关系写入 `flows/`，全局治理写入 `quality/`。

## Backend

**触发**：HTTP/RPC 路由、消息消费者、定时任务、服务入口、数据库或服务端身份认证。

**覆盖**：请求接入、校验、认证、授权、错误映射、应用/领域逻辑与基础设施接缝、事务、幂等、并发控制、队列、重试、一致性、Schema、迁移、索引、缓存、数据生命周期，以及同步请求和异步任务的故障路径。

## Frontend

**触发**：浏览器入口、页面路由、UI 组件树、客户端状态、样式或前端构建工具。

**覆盖**：页面和导航模型、组件职责与状态所有权、服务端数据/本地状态/表单/缓存同步、API Client、错误/空/加载状态、实时更新、权限呈现、构建分包、资源加载、性能和可访问性。

## Full-stack Integration

**触发**：Backend 和 Frontend 同时存在，并通过 API、BFF、生成客户端、WebSocket/SSE 或共享 Schema 协作。

**覆盖**：前后端契约的权威来源、版本兼容、身份传递、错误映射、实时事件、本地开发拓扑和一条跨端链路。

**产物**：写入 `flows/`，分别链接 `frontend/` 与 `backend/` 的内部实现；不创建 `fullstack/` 目录。

## CLI

**触发**：命令注册、参数解析、终端 I/O 或可发布命令入口。

**覆盖**：命令树、参数与配置优先级、交互/非交互模式、stdout/stderr/退出码契约、中断和批处理安全性。

## Desktop

**触发**：桌面主进程、窗口生命周期、本地 IPC、系统菜单、文件协议或打包签名配置。

**覆盖**：主/渲染进程边界、IPC 协议、本地权限、文件系统与自动更新、平台差异、打包发布和崩溃恢复。

## Library / SDK

**触发**：公共导出、发布包配置、用户可调用接口、多后端 Adapter 或兼容性测试。

**覆盖**：公开接口与不变条件、默认值、错误契约、扩展接缝、版本与迁移、平台支持、打包以及调用方示例。以调用方需要学习的界面而非内部文件数量衡量复杂度。

## Extension / Plugin

**触发**：Manifest、Host SDK、激活钩子、贡献点、插件发现或动态加载。

**覆盖**：宿主契约、发现/激活/停用/卸载生命周期、能力声明、隔离与权限、版本兼容、扩展间冲突和调试发布。Skill 若有独立指令契约，同时加载 Skill 画像；同一实现的主归属由 manifest 指定。

## Infrastructure

**触发**：容器、Kubernetes、Terraform、CI/CD、服务编排或环境提升配置是项目的实质部分。

**覆盖**：环境拓扑、资源与秘密、健康检查、扩缩容、发布/回滚、数据迁移顺序、故障域和可观测性。

## 合并规则

- Full-stack 是 Backend + Frontend + Integration 的关系型主题，不替换前两者；
- Agent、Skill 或 Extension 可与 Backend、Frontend、CLI、Desktop、Library/SDK 或 Infrastructure 同时选中；
- 同一条主链路跨多个画像时，各画像负责局部机制，由主 Agent 编写端到端文档；
- 一个主题证据较少时并入总览；拥有独立入口、状态、协议或重要取舍时再独立成文；
- 画像只描述仓库已有实现。命令、脚本和配置作为分析对象记录，不因画像命中而自动执行。
