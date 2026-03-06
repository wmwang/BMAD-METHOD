---
name: bmad-method-complete
description: Standalone BMAD Method runtime bundled as a single Codex skill. Use when the user wants the full BMAD planning-to-implementation system without installing `_bmad`, references BMAD commands or codes such as `/bmad-help`, `/bmad-bmm-create-prd`, `CP`, `CA`, `DS`, `PM`, asks for BMAD phase routing or party mode, or wants BMAD agents, workflows, quick flow, reviews, PRDs, architecture, epics, stories, sprint planning, or documentation workflows from a pure skill package.
---

# BMAD Method Complete

## Overview

Use this skill as a self-contained BMAD runtime. The bundle includes the BMAD source workflows, agent definitions, core tasks, help catalog, manifests, and runtime indexes inside `references/` so another Codex instance can execute BMAD behavior without a project-local `_bmad` installation.

Start with `references/runtime/capability-map.md`. Use `references/runtime/skill-manifest.json` for exact routing and `references/runtime/path-map.json` whenever a bundled file refers to `_bmad/...` paths.

## Routing Order

1. For general BMAD questions, "what next", workflow sequencing, or `/bmad-help`, load these files first:
   - `references/bmad/core/tasks/help.md`
   - `references/runtime/bmad-help.csv`
   - `references/runtime/workflow-index.md`
2. For agent persona requests, agent menu codes, or named BMAD roles, load these files first:
   - `references/runtime/agent-index.md`
   - the full agent YAML under `references/bmad/<module>/agents/`
3. For user-facing workflows, command aliases, or phase outputs, load these files first:
   - `references/runtime/workflow-index.md`
   - `references/runtime/bmad-help.csv`
   - the target workflow file resolved from the catalog
4. For standalone BMAD review/editorial utilities, load these files first:
   - `references/runtime/task-index.md`
   - the full task file under `references/bmad/core/tasks/`
5. For conceptual BMAD documentation questions, load only the relevant page from:
   - `references/docs/reference/`
   - `references/docs/reference_cn/`

## Path Translation

Treat the current workspace as `{project-root}`. Treat the skill folder as the BMAD resource store.

Apply these translation rules consistently:

- `_bmad/<...>` means the bundled file under `references/bmad/<...>`.
- `{project-root}/_bmad/<...>` also means the bundled file under `references/bmad/<...>` when the path refers to BMAD runtime resources, manifests, tasks, workflows, teams, memory, or agent files.
- `{project-root}` always remains the user's project for outputs, source code, and existing planning artifacts.
- `{installed_path}` means the directory of the currently loaded bundled workflow file.
- Relative references such as `./steps/...`, `./templates/...`, `./checklist.md`, or `./instructions.md` remain relative to the current bundled file.

Use `references/runtime/path-map.json` if an exact translation is needed.

## Synthetic Install State

The pure skill version must not require a literal `_bmad/core/config.yaml` or `_bmad/_config/*.csv` install tree.

When those files are referenced and do not exist in the user project, synthesize them in memory using `references/runtime/defaults.json`:

- `project_name` = basename of `{project-root}` unless the user provides a better name.
- `user_name` = current user if known, otherwise `User`.
- `communication_language` = current conversation language.
- `document_output_language` = `communication_language` unless the user requests another output language.
- `output_folder` = `{project-root}/_bmad-output`.
- `planning_artifacts` = `{project-root}/_bmad-output/planning-artifacts`.
- `implementation_artifacts` = `{project-root}/_bmad-output/implementation-artifacts`.
- `project_knowledge` = `{project-root}/docs`.
- `user_skill_level` = `intermediate` unless the user signals beginner or expert.
- `tool_supports_subagents` = `false` unless the current runtime clearly supports them.
- `tool_supports_agent_teams` = `false` unless the current runtime clearly supports them.

When a workflow expects `_bmad/_config` manifests, use the bundled versions in `references/runtime/`:

- `bmad-help.csv`
- `agent-manifest.csv`
- `workflow-manifest.csv`
- `task-manifest.csv`

Do not require the user to install `_bmad`. Keep this synthetic state in memory unless the user explicitly asks to materialize BMAD scaffolding in the project.

## Agent Execution

When an agent is selected:

1. Load the full agent YAML, not a snippet.
2. Adopt the persona, communication style, principles, critical actions, and menu.
3. Treat menu triggers, fuzzy matches, short codes, and slash-command strings as equivalent aliases.
4. If the chosen menu item points to a workflow, route into the workflow execution process below.
5. If the chosen menu item is an `action`, perform that action directly while staying faithful to the agent persona.

Special cases:

- `tech-writer` actions rely on bundled memory at `references/bmad/bmm/agents/tech-writer/tech-writer-sidecar/documentation-standards.md`.
- `bmad-master` uses bundled manifests to list workflows and tasks.
- `party-mode` uses `references/runtime/agent-manifest.csv` plus the bundled party-mode workflow.

## Workflow Execution

When a user-facing BMAD workflow is chosen:

1. Resolve the workflow from `references/runtime/bmad-help.csv` or `references/runtime/skill-manifest.json`.
2. Load the full target workflow file.
3. If the workflow says it is governed by `core/tasks/workflow.xml`, load `references/bmad/core/tasks/workflow.xml` first and follow it exactly.
4. Load every referenced steps file, instructions file, checklist, template, validation file, or data file completely when the workflow requires it.
5. Obey step order, optional-step prompts, `template-output` pauses, party-mode branches, and `#yolo` semantics exactly as described.
6. Save workflow outputs into the user workspace, not inside the skill bundle.
7. Reuse existing project artifacts when the workflow's file discovery expects them.

Output rule:

- Default output paths should follow the synthetic config values above.
- If the user already has a better existing artifact layout, honor it and keep the workflow consistent.

## Help And Sequencing

For `/bmad-help` behavior, do not improvise the sequence model. Use the bundled help catalog and the actual BMAD help task.

Minimum files to load:

- `references/bmad/core/tasks/help.md`
- `references/runtime/bmad-help.csv`
- `references/runtime/agent-manifest.csv`

Use the catalog to determine:

- current phase
- next optional workflows
- next required workflow
- command aliases
- agent load instructions
- likely output locations

## Party Mode

For party mode, load these files:

- `references/bmad/core/workflows/party-mode/workflow.md`
- `references/bmad/core/workflows/party-mode/steps/step-01-agent-loading.md`
- `references/bmad/core/workflows/party-mode/steps/step-02-discussion-orchestration.md`
- `references/bmad/core/workflows/party-mode/steps/step-03-graceful-exit.md`
- `references/runtime/agent-manifest.csv`

Use the manifest to select relevant agents, preserve their personalities, and facilitate a multi-agent discussion. If the user explicitly exits party mode, stop the multi-agent orchestration cleanly.

## Standalone Tasks

Use bundled core tasks directly when the user requests review, sharding, indexing, or editorial work outside a larger BMAD workflow.

Key tasks live in `references/bmad/core/tasks/` and are indexed by `references/runtime/task-index.md`.

## Reference Discipline

Keep context small:

- Start with the runtime indexes in `references/runtime/`.
- Load only the single workflow, agent, task, or doc page needed for the current request.
- Do not bulk-load the whole bundle.
- Prefer machine-readable `references/runtime/skill-manifest.json` for exact lookups and markdown indexes for quick human scanning.

## Functional Equivalence Target

This skill is intended to reproduce the BMAD feature surface through one standalone skill bundle:

- BMAD help and next-step routing
- agent personas and menus
- analysis, planning, solutioning, and implementation workflows
- quick-spec and quick-dev flows
- party mode
- core standalone review/editorial utilities
- documentation-oriented tech-writer actions

Literal IDE slash-command UI is not part of the skill runtime. Treat slash-command text, short codes, and natural-language requests as aliases that route into the same bundled BMAD resources.
