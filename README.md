# Ask Jimmy Skills

本机 ZCode 工程技能组装：`/ask-jimmy` 做手动总路由，Matt 负责对齐与切片，精选 Superpowers 负责执行、审查和验证。

完整背景、优势和实现说明见 [docs-ask-jimmy.md](docs-ask-jimmy.md)。

## 原则

- 主 agent 写当前票计划，子 agent 按计划实现，主 agent 验收。
- 一次只处理一张票，完成后停止。
- `to-tickets` 仅在 ≥5 个可独立验收切片时拆。
- TDD 只用 Matt `tdd`。
- 不启用 `using-superpowers` 或 `brainstorming`。

## 安装到 ZCode

```bash
mkdir -p ~/.zcode/skills
cp -a skills/* ~/.zcode/skills/
cp AGENTS.md ~/.zcode/AGENTS.md
```

重启 ZCode 后输入：

```text
/ask-jimmy
```

## 主链

```text
/ask-jimmy
        ↓
grill-with-docs 或 grill-me
        ↓
to-spec                 跨会话才写
        ↓
to-tickets              ≥5 个可独立验收切片才拆
        ↓
主 agent：writing-plans
        ↓
subagent-driven-development
        ↓
requesting-code-review
        ↓
verification-before-completion
        ↓
finishing-a-development-branch
```

## 验证

```bash
python3 -m unittest tests/test_skill_assembly.py -v
```

`CONFIG` 检查读取本机 `~/.zcode/cli/config.json`，用于确认 Superpowers 插件未启用。
