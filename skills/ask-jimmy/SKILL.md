---
name: ask-jimmy
description: 本机工程总路由。用户输入 /ask-jimmy，或要求按本机工程流程推进、不知道下一步该 grill / spec / tickets / 写计划 / 派子 agent 时使用。只做状态判断和路由，不写产品代码，不自动吞 backlog。
disable-model-invocation: true
---

# Ask Jimmy

本机总路由器。判断当前处于哪一阶段，然后调用对应技能。不要自己写产品代码，不要一次做完全部 tickets。

## 硬规则

- 一次只处理当前一张票，完成后停止。
- Ticket 写「完成什么」；`writing-plans` 写「现在怎么改」。
- 默认执行器：`subagent-driven-development`（一张票一个实现子 agent）。
- 备用执行器：`executing-plans`（子 agent 跑偏 / 共享协议很脆 / 用户要求主 agent 自己改）。
- TDD 只用 Matt `tdd`。
- 不要启用或调用 `using-superpowers`、`brainstorming`、Superpowers `test-driven-development`。
- 主 agent 必须自己跑 `verification-before-completion`；不算子 agent 口头通过。

## 路由

1. 只有模糊想法：用户选择 `/grill-with-docs`（有代码库）或 `/grill-me`。
2. 决策未清：继续 `/grilling`。
3. 决策已清且需要跨会话：`/to-spec`。
4. 可独立验收切片 **≥5**：`/to-tickets`。不到 5 个则不拆，直接为这一份工作写 `writing-plans`。
5. 已有当前票：主 agent 读最新代码 → `writing-plans`（只规划这一张）→ 需要隔离才 `using-git-worktrees` → `subagent-driven-development`。
6. 复杂/偶发/时序 bug：`systematic-debugging`。普通 bug：`diagnosing-bugs`。不要两个同时跑。
7. 实现已完成：`requesting-code-review` → 有意见才 `receiving-code-review` → `verification-before-completion` → 文档/Todo/git 对齐 → `finishing-a-development-branch`。

## 主链

```text
grill-with-docs 或 grill-me
        ↓
决策清楚？  否 → grilling
        ↓ 是
to-spec                 跨会话才写
        ↓
to-tickets              ≥5 个可独立验收切片才拆
        ↓
主 agent 只拿当前一张票
        ↓
主 agent：读最新代码
        ↓
主 agent：writing-plans
        ↓
using-git-worktrees       需要隔离才建
        ↓
subagent-driven-development
        └── 一张票一个实现子 agent
        ↓
主 agent：核对 diff + 重跑关键验证
        ↓
requesting-code-review
        ↓
有意见 → receiving-code-review → 子 agent 修 → 主 agent 再验
        ↓
verification-before-completion
        ↓
finishing-a-development-branch
        ↓
停。下一张票再重复
```
