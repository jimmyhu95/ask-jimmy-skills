# Ask Jimmy：本机 ZCode 工程技能组装

更新日期：2026-08-13  
总入口：`/ask-jimmy`（手动触发）  
配置范围：用户级 `~/.zcode/`

---

## 1. 背景

本机日常开发主要是跨仓库、跨服务、带真实验证的工程任务，例如 Reachy Mini 对话应用、MiniCPM Worker、知识库和本地部署。

早期完整启用 Superpowers 后，主 agent 和子 agent 都会被强制流程拖住：

- `using-superpowers` 要求“只要有 1% 相关就必须先调 skill”；
- `brainstorming`、写计划、子 agent、review、验证经常串联成重流程；
- 大量回合花在流程合规上，而不是逼近用户目标；
- 用户需要不断对话催促，才能把结果拉回可验收状态。

Matt Pocock 的技能更轻：先对齐决策，再沉淀规格和工单。但单独使用时，执行、隔离、审查、完成证据和分支收尾不够硬。

因此本机没有二选一，而是做了一套精选组装：

> **Matt 负责把目标锁死；精选 Superpowers 负责把当前这一刀做完并证明做完。**

总路由器命名为 `/ask-jimmy`，避免和 Matt 的 `/ask-matt` 混淆，也不绑定 Superpowers 品牌。

---

## 2. 解决什么问题

| 旧问题 | 组装后的约束 |
|---|---|
| Superpowers 全流程过重 | 不装 `using-superpowers`、`brainstorming` |
| 主/子 agent 重复编排 | 主 agent 写计划，子 agent 只执行当前票 |
| 一次规划全部工单后计划过期 | 只为当前一张票写 `writing-plans` |
| 票写太碎或太晚才拆 | 仅 ≥5 个可独立验收切片才 `to-tickets` |
| 子 agent 说通过就算完成 | 主 agent 必须重跑 `verification-before-completion` |
| 自动吞 backlog | `/ask-jimmy` 做完当前阶段后停止 |

---

## 3. 核心原则

1. **先锁产品边界，再写代码。**
2. **Ticket 写“完成什么”，Plan 写“现在怎么改”。**
3. **一次只做一张票。**
4. **尽早跑真实路径**（浏览器、跨服务、打包），不要拖到最后一轮 E2E。
5. **完成 = 刚跑出来的命令和输出。** 子 agent 口头通过不算。
6. **代码、文档、Todo、git 一起收。**

---

## 4. 角色分工

| 角色 | 做什么 | 不做什么 |
|---|---|---|
| `/ask-jimmy` | 判断当前阶段并路由 | 不写产品代码，不自动跑完全流程 |
| 主 agent | grill、spec、tickets、当前票计划、派工、验收、验证、收尾 | 不默认自己写完全部实现 |
| 实现子 agent | 按当前计划改代码、跑测试、尽早 smoke/E2E | 不扩 scope、不默认 commit、不拿下一张票 |
| 审查 | 当前票完成后审一次 | 不在每个微步骤完整 review |

---

## 5. 标准主链

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
verification-before-completion   主 agent 跑
        ↓
文档 / Todo / git 一次对齐
        ↓
finishing-a-development-branch
        ↓
停。下一张票再重复
```

### 小改

```text
说清 → 改 → 测 → verification
```

### 难 bug

```text
systematic-debugging → 回归测试 → 最小修复 → review → verification
```

普通 bug 用 `diagnosing-bugs`。不要和 `systematic-debugging` 同时跑。

---

## 6. 执行器怎么选

一次只选一个。

| 情况 | 用 |
|---|---|
| 默认：当前票已有计划 | `subagent-driven-development` |
| 子 agent 跑偏 / 共享协议很脆 / 用户要求主 agent 自己改 | `executing-plans` |
| 互不影响的调查 | `dispatching-parallel-agents` |

禁止串联：

```text
writing-plans → executing-plans → 再 SDD
```

禁止：

```text
所有票一次写完计划 → 并行改共享协议或同一份文档
```

---

## 7. 优势

### 比完整 Superpowers 轻

- 没有“1% 相关就必须先调 skill”；
- 没有强制 brainstorm；
- 不默认创建 worktree；
- 不自动处理全部 backlog。

### 比单独 Matt 更完整

- 有隔离工作区；
- 有子 agent 执行契约；
- 有审查闭环；
- 有完成前证据闸门；
- 有分支收尾。

### 更适合强模型

模型已经能写代码后，瓶颈变成：

- 目标是否对准；
- 跨会话决策会不会丢；
- 当前这一刀是否可验收。

`/ask-jimmy` 把注意力压在这三件事上。

---

## 8. 本机怎么实现

### 8.1 总入口

文件：

```text
~/.zcode/skills/ask-jimmy/SKILL.md
```

关键属性：

```yaml
name: ask-jimmy
disable-model-invocation: true
```

它只做状态判断和路由：

- 模糊想法 → grill
- 决策未清 → grilling
- 跨会话 → to-spec
- ≥5 个独立验收切片 → to-tickets
- 已有当前票 → writing-plans → SDD
- 复杂 bug → systematic-debugging
- 实现完成 → review → verify → finish

### 8.2 全局默认指令

文件：

```text
~/.zcode/AGENTS.md
```

把主链、执行器和禁止项写成所有工作区的默认规则。

### 8.3 已安装技能

**Matt（对齐 / 切片 / TDD）**

```text
grill-with-docs
grill-me
grilling
to-spec
to-tickets
tdd
domain-modeling
diagnosing-bugs
```

**精选 Superpowers（执行 / 审查 / 验证）**

```text
writing-plans
using-git-worktrees
subagent-driven-development
executing-plans
requesting-code-review
receiving-code-review
verification-before-completion
finishing-a-development-branch
systematic-debugging
dispatching-parallel-agents
```

这些 Superpowers 技能以用户级 skill 安装，**没有启用完整 Superpowers 插件**。

### 8.4 已删除或禁止

```text
ask-matt
implement
execute-ticket
using-superpowers
brainstorming
test-driven-development
```

`implement` 没有改名为第四个执行器。实现职责并入 `subagent-driven-development`。

### 8.5 关键契约

`to-tickets`：

- 仅 ≥5 个可独立验收切片才拆；
- 不写具体文件路径和实现步骤；
- 必须达到 Definition of Ready。

`writing-plans`：

- 主 agent 技能；
- 只规划当前一张票；
- 计划写完后交给 SDD。

`subagent-driven-development`：

- 一张票一个实现子 agent；
- 不自动连跑 backlog；
- 子 agent 默认不 commit。

`verification-before-completion`：

- 主 agent 自己跑命令；
- 不算子 agent 口头通过。

### 8.6 汇装测试

测试文件：

```text
~/.zcode/workspace/default/tests/test_skill_assembly.py
```

覆盖：

- 必装技能存在；
- 禁止技能不存在；
- Superpowers 插件未启用；
- `/ask-jimmy` 是手动路由器；
- 一票一子 agent；
- `executing-plans` 仅备用。

最近验证：

```text
python3 -m unittest ~/.zcode/workspace/default/tests/test_skill_assembly.py -v
Ran 12 tests
OK
```

### 8.7 子 agent 默认模型

文件：

```text
~/.zcode/v2/agents-state.json
```

当前覆盖：

| Agent | 模型 | 思维等级 |
|---|---|---|
| `general-purpose` | 东京 / `grok-4.6` | `high` |
| `Explore` | 东京 / `grok-4.6` | `high` |

模型 ID：

```text
custom:68638758-1ba8-4dd5-bebe-4576abc00019:grok-4.6
```

运行时已验证：

- `general-purpose` 实际 snapshot 为 `grok-4.6 / high`；
- `Explore` 实际 snapshot 为 `grok-4.6 / high`；
- Explore 仍只读：Bash、Glob、Grep、Read、WebFetch、WebSearch、TodoWrite。

修改该配置后，通常需要重启 ZCode，否则当前会话会继续使用缓存的旧 profile。

---

## 9. 日常怎么用

### 只有想法

```text
/ask-jimmy

我想给当前项目增加多租户权限，但租户隔离和角色继承还没定。
```

### 已有工单

```text
/ask-jimmy

处理当前 ticket：<链接或文件路径>
```

### 已有计划，进入实现

```text
/ask-jimmy

当前票已有计划：<计划路径>，进入实现阶段。
```

### 复杂 bug

```text
/ask-jimmy

结账流程偶发重复扣款，原因未知，需要定位并修复。
```

注意：`/ask-jimmy` 是路由器，不是“一次调用后从第一步机械跑到最后一步”的脚本。它会跳过不适用的阶段，并在当前票完成后停止。

---

## 10. 文件清单

| 路径 | 作用 |
|---|---|
| `~/.zcode/skills/ask-jimmy/SKILL.md` | 总路由 |
| `~/.zcode/AGENTS.md` | 全局默认流程 |
| `~/.zcode/skills/` | 用户级精选技能 |
| `~/.zcode/workspace/default/tests/test_skill_assembly.py` | 组装回归测试 |
| `~/.zcode/v2/agents-state.json` | 内置子 agent 模型覆盖 |
| `~/.zcode/cli/config.json` | 插件启用状态（不含 Superpowers 插件） |

---

## 11. 一句话

**`/ask-jimmy` 判断现在该做什么；主 agent 把当前这一刀计划清楚；`grok-4.6 / high` 子 agent 按计划实现；主 agent 用新鲜验证证据收尾。**
