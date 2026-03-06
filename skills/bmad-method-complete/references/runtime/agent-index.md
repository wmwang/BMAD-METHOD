# Agent Index

Total agents: 10

| agent key | persona | title | module | menu triggers |
| --- | --- | --- | --- | --- |
| bmad-master | BMad Master | BMad Master Executor, Knowledge Custodian, and Workflow Orchestrator | core | LT or fuzzy match on list-tasks, LW or fuzzy match on list-workflows |
| analyst | Mary | Business Analyst | bmm | BP or fuzzy match on brainstorm-project, MR or fuzzy match on market-research, DR or fuzzy match on domain-research, TR or fuzzy match on technical-research |
| architect | Winston | Architect | bmm | CA or fuzzy match on create-architecture, IR or fuzzy match on implementation-readiness |
| dev | Amelia | Developer Agent | bmm | DS or fuzzy match on dev-story, CR or fuzzy match on code-review |
| pm | John | Product Manager | bmm | CP or fuzzy match on create-prd, VP or fuzzy match on validate-prd, EP or fuzzy match on edit-prd, CE or fuzzy match on epics-stories |
| qa | Quinn | QA Engineer | bmm | QA or fuzzy match on qa-automate |
| quick-flow-solo-dev | Barry | Quick Flow Solo Dev | bmm | QS or fuzzy match on quick-spec, QD or fuzzy match on quick-dev, QQ or fuzzy match on quick-dev-new-preview, CR or fuzzy match on code-review |
| sm | Bob | Scrum Master | bmm | SP or fuzzy match on sprint-planning, CS or fuzzy match on create-story, ER or fuzzy match on epic-retrospective, CC or fuzzy match on correct-course |
| tech-writer | Paige | Technical Writer | bmm | DP or fuzzy match on document-project, WD or fuzzy match on write-document, US or fuzzy match on update-standards, MG or fuzzy match on mermaid-gen |
| ux-designer | Sally | UX Designer | bmm | CU or fuzzy match on ux-design |

Use the bundled agent YAML under `references/bmad/<module>/agents/` for the full persona and menu.
