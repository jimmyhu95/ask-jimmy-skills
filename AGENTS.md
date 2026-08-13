# 本机工程技能组装

默认：**主 agent 写当前票计划，子 agent 按计划实现，主 agent 验收。**

总入口：`/ask-jimmy`（手动）。不要启用 `using-superpowers` 或 `brainstorming`。TDD 只用 Matt `tdd`。

## 主链

```text
/ask-jimmy
        ↓
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
主 agent：writing-plans   ← 只规划这一张
        ↓
using-git-worktrees       需要隔离才建
        ↓
subagent-driven-development
   └── 一张票一个实现子 agent
   └── TDD + 相关测试 + 尽早 smoke/E2E
        ↓
主 agent：核对 diff + 重跑关键验证
        ↓
requesting-code-review
        ↓
有意见 → receiving-code-review → 子 agent 修 → 主 agent 再验
        ↓
verification-before-completion   主 agent 跑，不算子 agent 口头通过
        ↓
文档 / Todo / git 一次对齐
        ↓
finishing-a-development-branch
        ↓
停。下一张票再重复
```

## 执行器

- 默认：`subagent-driven-development`，一张票一个实现子 agent。
- `executing-plans` 仅备用（子 agent 跑偏 / 共享协议很脆 / 用户要求主 agent 自己改）。
- 不要自动连跑全 backlog。
- `dispatching-parallel-agents`：只并行调查，不要默认并行写代码。

## 小改 / 难 bug

- 小改：说清 → 改 → 测 → verification。
- 难 bug：`systematic-debugging`。普通 bug：`diagnosing-bugs`。不要两个同时跑。
