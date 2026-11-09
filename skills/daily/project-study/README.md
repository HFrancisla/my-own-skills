# Project Study

面向真实代码仓库的**导师带读型** Agent Skill：先建立最小代码地图与知识依赖，带学习者逐段阅读一条真实功能链路，再逐步练习、独立验收和复习。**Agent 已读懂不等于学习者学会。**

本 Skill 由用户显式调用（`disable-model-invocation: true`；`agents/openai.yaml` 禁止隐式调用）。

## 典型使用

首次学习陌生项目：

> 用 project-study 学习当前项目。我不了解这个项目，请先找一个真实最小入口，讲必要概念、展示源码并带我追踪一次函数调用；每次只看一个片段，理解后再继续。

继续学习：

> 使用 project-study 恢复上次进度，从实际带读到的位置继续。先讲解下一小段，不要直接把 Agent 已调查过的整条链当成我的学习成果。

已有基础，主动加快：

> 这部分我已经理解。跳过基础示范，给我一个刚学过片段的局部练习，然后用源码核对。

复习：

> 用 project-study 检查已完成单元的到期复习。先让我回忆，再核对源码。

## 导师带读的颗粒度

以 `this.session.prompt(userInput)` 为例：Agent 应先从**实际目标仓库**打开包含该调用的上下文，解释 `userInput` 和 `session`，再打开下一跳源码进行示范。完成带读、学习者准备好练习后，才让其尝试独立解释整条链路。示例符号不代表任何仓库已经被验证。

## 记录位置

首次保存前需要用户授权。默认建议目标项目根目录 `.project-learning/`，也可指定项目外目录：

- `overview.md`：项目代码地图和知识地图
- `roadmap.md`：Uxx 单元、证据和复习计划
- `progress.md`：唯一续学指针（包括实际带读位置）
- `sessions/YYYY-MM-DD.md`：每次真实学习、回忆与实验记录
- `notes/topic.md`：可选的专题笔记

复习建议不会自动触发提醒；实际运行代码、修改文件、clone 或安装依赖均需先获授权。旧笔记缺新增字段可直接续学。

## 结构与维护

- `SKILL.md`：分支入口、共通约束
- `references/learning-workflow.md`：**唯一**的教学阶段、状态与复习规则
- `references/code-analysis.md`：按需进行源码研究
- `references/artifact-templates.md`：仅在保存/更新时读取
- `agents/openai.yaml`：展示信息与隐式调用开关

该 Skill 不依赖数据库或后台脚本，旨在学习已有项目而不是自动开发新功能。
