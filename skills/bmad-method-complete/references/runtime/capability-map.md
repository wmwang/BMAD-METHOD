# Capability Map

This bundle is a self-contained BMAD runtime for Codex skills.

- Agents: 10
- Standalone tasks: 7
- Help catalog rows: 40
- Core routing file: `references/runtime/bmad-help.csv`
- Core executor: `references/bmad/core/tasks/workflow.xml`
- Party mode: `references/bmad/core/workflows/party-mode/workflow.md`

## Phase Coverage

- `1-analysis`: 5
- `2-planning`: 4
- `3-solutioning`: 3
- `4-implementation`: 8
- `anytime`: 20

## Synthetic Config Defaults

- `project_name` = `{project-root basename}`
- `user_name` = `User`
- `communication_language` = `{current conversation language}`
- `document_output_language` = `{communication_language unless explicitly overridden}`
- `output_folder` = `{project-root}/_bmad-output`
- `tool_supports_subagents` = `False`
- `tool_supports_agent_teams` = `False`
- `user_skill_level` = `intermediate`
- `planning_artifacts` = `{project-root}/_bmad-output/planning-artifacts`
- `implementation_artifacts` = `{project-root}/_bmad-output/implementation-artifacts`
- `project_knowledge` = `{project-root}/docs`

## Path Translation

- `_bmad/<...>` -> `references/bmad/<...>`
- `{project-root}/_bmad/<...>` -> `references/bmad/<...>` for bundled resources
- `{project-root}` remains the user workspace for outputs and working files
- `_bmad/_config/*.csv` -> `references/runtime/*.csv`
- `_bmad/core/config.yaml` -> `references/runtime/defaults.json`

Use `references/runtime/skill-manifest.json` for exact machine-readable routing.
