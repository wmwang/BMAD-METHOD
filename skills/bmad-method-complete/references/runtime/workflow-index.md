# Workflow Index

Total user-facing workflows: 28

| phase | code | workflow | command alias | agent | outputs |
| --- | --- | --- | --- | --- | --- |
| 1-analysis | BP | Brainstorm Project | bmad-brainstorming | analyst | brainstorming session |
| 1-analysis | MR | Market Research | bmad-bmm-market-research | analyst | research documents |
| 1-analysis | DR | Domain Research | bmad-bmm-domain-research | analyst | research documents |
| 1-analysis | TR | Technical Research | bmad-bmm-technical-research | analyst | research documents |
| 1-analysis | CB | Create Brief | bmad-bmm-create-product-brief | analyst | product brief |
| 2-planning | CP | Create PRD | bmad-bmm-create-prd | pm | prd |
| 2-planning | VP | Validate PRD | bmad-bmm-validate-prd | pm | prd validation report |
| 2-planning | EP | Edit PRD | bmad-bmm-edit-prd | pm | updated prd |
| 2-planning | CU | Create UX | bmad-bmm-create-ux-design | ux-designer | ux design |
| 3-solutioning | CA | Create Architecture | bmad-bmm-create-architecture | architect | architecture |
| 3-solutioning | CE | Create Epics and Stories | bmad-bmm-create-epics-and-stories | pm | epics and stories |
| 3-solutioning | IR | Check Implementation Readiness | bmad-bmm-check-implementation-readiness | architect | readiness report |
| 4-implementation | SP | Sprint Planning | bmad-bmm-sprint-planning | sm | sprint status |
| 4-implementation | SS | Sprint Status | bmad-bmm-sprint-status | sm |  |
| 4-implementation | CS | Create Story | bmad-bmm-create-story | sm | story |
| 4-implementation | VS | Validate Story | bmad-bmm-create-story | sm | story validation report |
| 4-implementation | DS | Dev Story | bmad-bmm-dev-story | dev |  |
| 4-implementation | QA | QA Automation Test | bmad-bmm-qa-automate | qa | test suite |
| 4-implementation | CR | Code Review | bmad-bmm-code-review | dev |  |
| 4-implementation | ER | Retrospective | bmad-bmm-retrospective | sm | retrospective |
| anytime | DP | Document Project | bmad-bmm-document-project | analyst | * |
| anytime | GPC | Generate Project Context | bmad-bmm-generate-project-context | analyst | project context |
| anytime | QS | Quick Spec | bmad-bmm-quick-spec | quick-flow-solo-dev | tech spec |
| anytime | QD | Quick Dev | bmad-bmm-quick-dev | quick-flow-solo-dev |  |
| anytime | QQ | Quick Dev New Preview | bmad-bmm-quick-dev-new-preview | quick-flow-solo-dev | tech spec implementation |
| anytime | CC | Correct Course | bmad-bmm-correct-course | sm | change proposal |
| anytime | BSP | Brainstorming | bmad-brainstorming | analyst |  |
| anytime | PM | Party Mode | bmad-party-mode | party-mode facilitator |  |

Resolve each `workflow-file` through `references/runtime/path-map.json` or the prefix rules in `SKILL.md`.
