"""Observable assembly of Matt + Superpowers skills for this machine.

Seam: ~/.zcode/skills/<name>/SKILL.md and ~/.zcode/cli/config.json.
Tests describe what an agent session must be able to discover, not how
individual paragraphs are worded internally beyond required contracts.
"""

from __future__ import annotations

import json
import unittest
from pathlib import Path

SKILLS = Path(__file__).resolve().parents[1] / "skills"
CONFIG = Path.home() / ".zcode/cli/config.json"

MATT_REQUIRED = {
    "grill-with-docs",
    "grill-me",
    "grilling",
    "to-spec",
    "to-tickets",
    "tdd",
    "domain-modeling",
    "diagnosing-bugs",
    "ask-jimmy",
}

SUPERPOWERS_REQUIRED = {
    "writing-plans",
    "using-git-worktrees",
    "executing-plans",
    "subagent-driven-development",
    "requesting-code-review",
    "receiving-code-review",
    "verification-before-completion",
    "finishing-a-development-branch",
    "systematic-debugging",
    "dispatching-parallel-agents",
}

FORBIDDEN_SKILLS = {
    "using-superpowers",
    "brainstorming",
    "test-driven-development",
    "ask-matt",
    "implement",
}


def skill_text(name: str) -> str:
    return (SKILLS / name / "SKILL.md").read_text(encoding="utf-8")


def has_skill(name: str) -> bool:
    return (SKILLS / name / "SKILL.md").is_file()


class SkillPresenceTests(unittest.TestCase):
    def test_required_matt_skills_are_installed(self) -> None:
        missing = sorted(name for name in MATT_REQUIRED if not has_skill(name))
        self.assertEqual(missing, [])

    def test_required_superpowers_skills_are_installed(self) -> None:
        missing = sorted(name for name in SUPERPOWERS_REQUIRED if not has_skill(name))
        self.assertEqual(missing, [])

    def test_forbidden_superpowers_skills_are_not_installed(self) -> None:
        present = sorted(name for name in FORBIDDEN_SKILLS if has_skill(name))
        self.assertEqual(present, [])

    def test_zcode_plugin_config_does_not_enable_superpowers_plugin(self) -> None:
        data = json.loads(CONFIG.read_text(encoding="utf-8"))
        enabled = data.get("plugins", {}).get("enabledPlugins", {})
        superpowers_keys = [key for key in enabled if "superpower" in key.lower()]
        self.assertEqual(superpowers_keys, [])


class ArchitectureContractTests(unittest.TestCase):
    def test_to_tickets_requires_five_independent_slices(self) -> None:
        text = skill_text("to-tickets")
        self.assertIn("≥5", text)
        self.assertIn("可独立验收", text)

    def test_to_tickets_does_not_write_implementation_steps(self) -> None:
        text = skill_text("to-tickets")
        self.assertIn("不要写具体文件路径", text)
        self.assertIn("Definition of Ready", text)

    def test_writing_plans_is_main_agent_current_ticket_only(self) -> None:
        text = skill_text("writing-plans")
        self.assertIn("主 agent", text)
        self.assertIn("当前一张票", text)
        self.assertIn("不要一次规划全部", text)

    def test_subagent_driven_development_is_one_ticket_one_subagent(self) -> None:
        text = skill_text("subagent-driven-development")
        self.assertIn("一张票", text)
        self.assertIn("一个实现子 agent", text)
        self.assertIn("不要自动连跑全 backlog", text)

    def test_executing_plans_is_fallback_not_default(self) -> None:
        text = skill_text("executing-plans")
        self.assertIn("备用", text)
        self.assertIn("子 agent 跑偏", text)

    def test_ask_jimmy_is_manual_router(self) -> None:
        text = skill_text("ask-jimmy")
        self.assertIn("disable-model-invocation: true", text)
        self.assertIn("writing-plans", text)
        self.assertIn("subagent-driven-development", text)
        self.assertIn("verification-before-completion", text)
        self.assertIn("一张票", text)
        self.assertNotIn("/implement", text)
        self.assertNotIn("ask-matt", text)

    def test_dispatching_parallel_agents_is_investigation_only(self) -> None:
        text = skill_text("dispatching-parallel-agents")
        self.assertIn("调查", text)
        self.assertIn("不要默认并行写代码", text)

    def test_verification_must_be_run_by_main_agent(self) -> None:
        text = skill_text("verification-before-completion")
        self.assertIn("主 agent", text)
        self.assertIn("不算子 agent 口头通过", text)


if __name__ == "__main__":
    unittest.main()
