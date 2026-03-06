#!/usr/bin/env python3
from __future__ import annotations

import csv
import json
import re
import shutil
from datetime import datetime, timezone
from pathlib import Path

SKILL_DIR = Path(__file__).resolve().parents[1]
REPO_ROOT = SKILL_DIR.parent.parent
REFERENCES_DIR = SKILL_DIR / 'references'
BUNDLE_DIR = REFERENCES_DIR / 'bmad'
RUNTIME_DIR = REFERENCES_DIR / 'runtime'
DOCS_DIR = REFERENCES_DIR / 'docs'

SOURCE_TREES = [
    (REPO_ROOT / 'src' / 'core', BUNDLE_DIR / 'core'),
    (REPO_ROOT / 'src' / 'bmm', BUNDLE_DIR / 'bmm'),
    (REPO_ROOT / 'src' / 'utility', BUNDLE_DIR / 'utility'),
    (REPO_ROOT / 'docs' / 'reference', DOCS_DIR / 'reference'),
    (REPO_ROOT / 'docs_cn' / 'reference', DOCS_DIR / 'reference_cn'),
]

HELP_SOURCES = [
    ('core', REPO_ROOT / 'src' / 'core' / 'module-help.csv'),
    ('bmm', REPO_ROOT / 'src' / 'bmm' / 'module-help.csv'),
]

DEFAULT_CONFIG = {
    'project_name': '{project-root basename}',
    'user_name': 'User',
    'communication_language': '{current conversation language}',
    'document_output_language': '{communication_language unless explicitly overridden}',
    'output_folder': '{project-root}/_bmad-output',
    'tool_supports_subagents': False,
    'tool_supports_agent_teams': False,
    'user_skill_level': 'intermediate',
    'planning_artifacts': '{project-root}/_bmad-output/planning-artifacts',
    'implementation_artifacts': '{project-root}/_bmad-output/implementation-artifacts',
    'project_knowledge': '{project-root}/docs',
}

HELP_HEADER = [
    'module',
    'phase',
    'name',
    'code',
    'sequence',
    'workflow-file',
    'command',
    'required',
    'agent-name',
    'agent-command',
    'agent-display-name',
    'agent-title',
    'options',
    'description',
    'output-location',
    'outputs',
]


def read_text(path: Path) -> str:
    return path.read_text(encoding='utf-8')


def write_text(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding='utf-8')


def clean_dir(path: Path) -> None:
    if path.exists():
        shutil.rmtree(path)
    path.mkdir(parents=True, exist_ok=True)


def copy_tree(src: Path, dst: Path) -> None:
    if not src.exists():
        return
    shutil.copytree(src, dst, dirs_exist_ok=True)


def unquote(value: str) -> str:
    value = value.strip()
    if not value:
        return ''
    if value[0] == value[-1] and value[0] in {'"', "'"}:
        return value[1:-1]
    return value


def extract_section(lines: list[str], section_name: str, section_indent: int = 2) -> list[str]:
    target = ' ' * section_indent + f'{section_name}:'
    start = None
    for index, line in enumerate(lines):
        if line.startswith(target):
            start = index + 1
            break
    if start is None:
        return []

    collected: list[str] = []
    next_section_pattern = re.compile(rf'^\s{{{section_indent}}}[A-Za-z0-9_-]+:\s*$')
    for line in lines[start:]:
        if next_section_pattern.match(line):
            break
        collected.append(line)
    return collected


def parse_key_block(block_lines: list[str], indent: int = 4) -> dict[str, str]:
    result: dict[str, str] = {}
    index = 0
    indent_prefix = ' ' * indent
    while index < len(block_lines):
        line = block_lines[index]
        if not line.startswith(indent_prefix):
            index += 1
            continue

        stripped = line[indent:]
        if ':' not in stripped:
            index += 1
            continue

        key, raw_value = stripped.split(':', 1)
        key = key.strip()
        raw_value = raw_value.strip()
        if raw_value == '|':
            index += 1
            chunks: list[str] = []
            multiline_prefix = ' ' * (indent + 2)
            while index < len(block_lines):
                candidate = block_lines[index]
                if candidate.startswith(indent_prefix) and not candidate.startswith(multiline_prefix):
                    break
                if candidate.startswith(multiline_prefix):
                    chunks.append(candidate[indent + 2 :])
                elif candidate.strip() == '':
                    chunks.append('')
                else:
                    break
                index += 1
            result[key] = '\n'.join(chunks).rstrip()
            continue

        result[key] = unquote(raw_value)
        index += 1

    return result


def parse_menu_block(block_lines: list[str]) -> list[dict[str, str]]:
    entries: list[dict[str, str]] = []
    current: dict[str, str] | None = None

    for line in block_lines:
        if line.startswith('    - '):
            if current:
                entries.append(current)
            current = {}
            stripped = line[6:]
            if ':' in stripped:
                key, raw_value = stripped.split(':', 1)
                current[key.strip()] = unquote(raw_value.strip())
            continue

        if current is None:
            continue

        if line.startswith('      ') and ':' in line[6:]:
            key, raw_value = line[6:].split(':', 1)
            current[key.strip()] = unquote(raw_value.strip())
            continue

    if current:
        entries.append(current)
    return entries


def parse_agent_file(path: Path, module: str) -> dict[str, object]:
    lines = read_text(path).splitlines()
    metadata = parse_key_block(extract_section(lines, 'metadata'))
    persona = parse_key_block(extract_section(lines, 'persona'))
    menu = parse_menu_block(extract_section(lines, 'menu'))

    relative_agent_path = path.relative_to(REPO_ROOT / 'src' / module)
    install_path = f'_bmad/{module}/{relative_agent_path.as_posix()}'

    return {
        'name': path.name.replace('.agent.yaml', ''),
        'displayName': metadata.get('name', path.name.replace('.agent.yaml', '')),
        'title': metadata.get('title', ''),
        'icon': metadata.get('icon', ''),
        'capabilities': metadata.get('capabilities', ''),
        'role': persona.get('role', ''),
        'identity': persona.get('identity', ''),
        'communicationStyle': persona.get('communication_style', ''),
        'principles': persona.get('principles', ''),
        'module': module,
        'path': install_path,
        'sourcePath': str(path.relative_to(REPO_ROOT).as_posix()),
        'menu': menu,
    }


def extract_frontmatter(content: str) -> dict[str, str]:
    match = re.match(r'^---\n([\s\S]*?)\n---\n?', content)
    if not match:
        return {}
    result: dict[str, str] = {}
    for line in match.group(1).splitlines():
        if ':' not in line:
            continue
        key, raw_value = line.split(':', 1)
        result[key.strip()] = unquote(raw_value.strip())
    return result


def parse_task_file(path: Path) -> dict[str, object] | None:
    content = read_text(path)
    if 'internal="true"' in content:
        return None

    name = path.stem
    display_name = name
    description = ''
    standalone = True

    if path.suffix == '.md':
        frontmatter = extract_frontmatter(content)
        display_name = frontmatter.get('name', name)
        description = frontmatter.get('description', '')
        standalone_value = frontmatter.get('standalone', 'true').lower()
        standalone = standalone_value != 'false'
    else:
        name_match = re.search(r'<task[^>]+name="([^"]+)"', content)
        objective_match = re.search(r'<objective>([\s\S]*?)</objective>', content)
        standalone_false_match = re.search(r'<task[^>]+standalone="false"', content)
        display_name = name_match.group(1).strip() if name_match else name
        description = objective_match.group(1).strip() if objective_match else ''
        standalone = standalone_false_match is None

    if not standalone:
        return None

    return {
        'name': name,
        'displayName': display_name,
        'description': re.sub(r'\s+', ' ', description).strip(),
        'module': 'core',
        'path': f'_bmad/core/tasks/{path.name}',
        'sourcePath': str(path.relative_to(REPO_ROOT).as_posix()),
        'standalone': True,
    }


def load_help_rows() -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    for module_name, csv_path in HELP_SOURCES:
        with csv_path.open(newline='', encoding='utf-8') as handle:
            reader = csv.DictReader(handle)
            for row in reader:
                if not any((value or '').strip() for value in row.values()):
                    continue
                normalized = {key.strip(): (value or '').strip() for key, value in row.items() if key is not None}
                if not normalized.get('module') and module_name != 'core':
                    normalized['module'] = module_name
                rows.append(normalized)
    return rows


def escape_csv(value: object) -> str:
    text = '' if value is None else str(value)
    return '"' + text.replace('"', '""') + '"'


def write_csv(path: Path, header: list[str], rows: list[list[object]]) -> None:
    lines = [','.join(header)]
    lines.extend(','.join(escape_csv(value) for value in row) for row in rows)
    write_text(path, '\n'.join(lines) + '\n')


def build_path_map(copied_files: list[Path]) -> dict[str, str]:
    path_map: dict[str, str] = {}
    for copied_file in copied_files:
        relative = copied_file.relative_to(BUNDLE_DIR)
        original = f'_bmad/{relative.as_posix()}'
        skill_relative = f'references/bmad/{relative.as_posix()}'
        path_map[original] = skill_relative
        path_map[original.replace('_bmad/', 'bmad/', 1)] = skill_relative
        path_map[f'{{project-root}}/{original}'] = skill_relative

    runtime_aliases = {
        '_bmad/_config/bmad-help.csv': 'references/runtime/bmad-help.csv',
        '_bmad/_config/agent-manifest.csv': 'references/runtime/agent-manifest.csv',
        '_bmad/_config/workflow-manifest.csv': 'references/runtime/workflow-manifest.csv',
        '_bmad/_config/task-manifest.csv': 'references/runtime/task-manifest.csv',
        '_bmad/core/config.yaml': 'references/runtime/defaults.json',
        '_bmad/_memory/tech-writer-sidecar/documentation-standards.md': 'references/bmad/bmm/agents/tech-writer/tech-writer-sidecar/documentation-standards.md',
    }
    for original, skill_relative in runtime_aliases.items():
        path_map[original] = skill_relative
        path_map[f'{{project-root}}/{original}'] = skill_relative
    return path_map


def list_copied_files(root: Path) -> list[Path]:
    return sorted(path for path in root.rglob('*') if path.is_file())


def markdown_table(headers: list[str], rows: list[list[str]]) -> str:
    lines = ['| ' + ' | '.join(headers) + ' |', '| ' + ' | '.join(['---'] * len(headers)) + ' |']
    for row in rows:
        lines.append('| ' + ' | '.join(row) + ' |')
    return '\n'.join(lines)


def generate_agent_index(agents: list[dict[str, object]]) -> str:
    rows = []
    for agent in agents:
        triggers = ', '.join(entry.get('trigger', '') for entry in agent['menu'][:4] if entry.get('trigger'))
        rows.append([
            str(agent['name']),
            str(agent['displayName']),
            str(agent['title']),
            str(agent['module']),
            triggers or '-',
        ])

    body = [
        '# Agent Index',
        '',
        f'Total agents: {len(agents)}',
        '',
        markdown_table(['agent key', 'persona', 'title', 'module', 'menu triggers'], rows),
        '',
        'Use the bundled agent YAML under `references/bmad/<module>/agents/` for the full persona and menu.',
    ]
    return '\n'.join(body) + '\n'


def generate_workflow_index(help_rows: list[dict[str, str]]) -> str:
    workflow_rows = []
    for row in help_rows:
        workflow_file = row.get('workflow-file', '')
        if '/workflows/' not in workflow_file:
            continue
        workflow_rows.append([
            row.get('phase', 'anytime') or 'anytime',
            row.get('code', ''),
            row.get('name', ''),
            row.get('command', ''),
            row.get('agent-name', ''),
            row.get('outputs', ''),
        ])

    body = [
        '# Workflow Index',
        '',
        f'Total user-facing workflows: {len(workflow_rows)}',
        '',
        markdown_table(['phase', 'code', 'workflow', 'command alias', 'agent', 'outputs'], workflow_rows),
        '',
        'Resolve each `workflow-file` through `references/runtime/path-map.json` or the prefix rules in `SKILL.md`.',
    ]
    return '\n'.join(body) + '\n'


def generate_task_index(tasks: list[dict[str, object]]) -> str:
    rows = [[str(task['name']), str(task['displayName']), str(task['description'])] for task in tasks]
    body = [
        '# Task Index',
        '',
        f'Total standalone tasks: {len(tasks)}',
        '',
        markdown_table(['task key', 'display name', 'description'], rows),
    ]
    return '\n'.join(body) + '\n'


def generate_capability_map(help_rows: list[dict[str, str]], agents: list[dict[str, object]], tasks: list[dict[str, object]]) -> str:
    phase_counts: dict[str, int] = {}
    for row in help_rows:
        phase = row.get('phase', 'anytime') or 'anytime'
        phase_counts[phase] = phase_counts.get(phase, 0) + 1

    bullets = '\n'.join(f'- `{phase}`: {count}' for phase, count in sorted(phase_counts.items()))
    body = [
        '# Capability Map',
        '',
        'This bundle is a self-contained BMAD runtime for Codex skills.',
        '',
        f'- Agents: {len(agents)}',
        f'- Standalone tasks: {len(tasks)}',
        f'- Help catalog rows: {len(help_rows)}',
        '- Core routing file: `references/runtime/bmad-help.csv`',
        '- Core executor: `references/bmad/core/tasks/workflow.xml`',
        '- Party mode: `references/bmad/core/workflows/party-mode/workflow.md`',
        '',
        '## Phase Coverage',
        '',
        bullets,
        '',
        '## Synthetic Config Defaults',
        '',
        *[f'- `{key}` = `{value}`' for key, value in DEFAULT_CONFIG.items()],
        '',
        '## Path Translation',
        '',
        '- `_bmad/<...>` -> `references/bmad/<...>`',
        '- `{project-root}/_bmad/<...>` -> `references/bmad/<...>` for bundled resources',
        '- `{project-root}` remains the user workspace for outputs and working files',
        '- `_bmad/_config/*.csv` -> `references/runtime/*.csv`',
        '- `_bmad/core/config.yaml` -> `references/runtime/defaults.json`',
        '',
        'Use `references/runtime/skill-manifest.json` for exact machine-readable routing.',
    ]
    return '\n'.join(body) + '\n'


def main() -> None:
    clean_dir(BUNDLE_DIR)
    clean_dir(RUNTIME_DIR)
    clean_dir(DOCS_DIR)

    for src, dst in SOURCE_TREES:
        copy_tree(src, dst)

    package_json = json.loads(read_text(REPO_ROOT / 'package.json'))

    agents = []
    for module in ('core', 'bmm'):
        for agent_file in sorted((REPO_ROOT / 'src' / module / 'agents').rglob('*.agent.yaml')):
            agents.append(parse_agent_file(agent_file, module))

    tasks = []
    for task_file in sorted((REPO_ROOT / 'src' / 'core' / 'tasks').iterdir()):
        if not task_file.is_file() or task_file.suffix not in {'.md', '.xml'}:
            continue
        task = parse_task_file(task_file)
        if task:
            tasks.append(task)

    agents_by_name = {str(agent['name']): agent for agent in agents}

    raw_help_rows = load_help_rows()
    help_rows: list[dict[str, str]] = []
    for row in raw_help_rows:
        agent_name = row.get('agent', '').strip()
        agent = agents_by_name.get(agent_name)
        help_rows.append({
            'module': row.get('module', ''),
            'phase': row.get('phase', ''),
            'name': row.get('name', ''),
            'code': row.get('code', ''),
            'sequence': row.get('sequence', ''),
            'workflow-file': row.get('workflow-file', ''),
            'command': row.get('command', ''),
            'required': row.get('required', 'false') or 'false',
            'agent-name': agent_name,
            'agent-command': f"bmad:{agent['module']}:agent:{agent_name}" if agent else '',
            'agent-display-name': str(agent['displayName']) if agent else '',
            'agent-title': (f"{agent['icon']} {agent['title']}".strip() if agent else '').strip(),
            'options': row.get('options', ''),
            'description': row.get('description', ''),
            'output-location': row.get('output-location', ''),
            'outputs': row.get('outputs', ''),
        })

    help_rows.sort(key=lambda row: ((row.get('module', '') or '').lower(), row.get('phase', ''), int(row.get('sequence', '') or 0)))

    agent_manifest_rows = [
        [
            agent['name'],
            agent['displayName'],
            agent['title'],
            agent['icon'],
            agent['capabilities'],
            agent['role'],
            agent['identity'],
            agent['communicationStyle'],
            agent['principles'],
            agent['module'],
            agent['path'],
        ]
        for agent in agents
    ]
    write_csv(
        RUNTIME_DIR / 'agent-manifest.csv',
        ['name', 'displayName', 'title', 'icon', 'capabilities', 'role', 'identity', 'communicationStyle', 'principles', 'module', 'path'],
        agent_manifest_rows,
    )

    workflow_manifest_rows = []
    seen_workflows: set[tuple[str, str]] = set()
    for row in help_rows:
        workflow_file = row.get('workflow-file', '')
        key = (row.get('module', ''), workflow_file)
        if '/workflows/' not in workflow_file or key in seen_workflows:
            continue
        seen_workflows.add(key)
        workflow_manifest_rows.append([
            row.get('name', ''),
            row.get('description', ''),
            row.get('module', ''),
            workflow_file,
        ])
    write_csv(RUNTIME_DIR / 'workflow-manifest.csv', ['name', 'description', 'module', 'path'], workflow_manifest_rows)

    task_manifest_rows = [
        [task['name'], task['displayName'], task['description'], task['module'], task['path'], 'true'] for task in tasks
    ]
    write_csv(RUNTIME_DIR / 'task-manifest.csv', ['name', 'displayName', 'description', 'module', 'path', 'standalone'], task_manifest_rows)

    help_csv_rows = [
        [row[column] for column in HELP_HEADER] for row in help_rows
    ]
    write_csv(RUNTIME_DIR / 'bmad-help.csv', HELP_HEADER, help_csv_rows)

    copied_files = list_copied_files(BUNDLE_DIR)
    path_map = build_path_map(copied_files)
    write_text(RUNTIME_DIR / 'path-map.json', json.dumps(path_map, indent=2, ensure_ascii=False) + '\n')
    write_text(RUNTIME_DIR / 'defaults.json', json.dumps(DEFAULT_CONFIG, indent=2, ensure_ascii=False) + '\n')

    manifest = {
        'skill': 'bmad-method-complete',
        'generatedAt': datetime.now(timezone.utc).isoformat(),
        'sourceVersion': package_json.get('version', ''),
        'sourceRepo': package_json.get('repository', {}).get('url', ''),
        'copiedRoots': [str(dst.relative_to(SKILL_DIR).as_posix()) for _, dst in SOURCE_TREES],
        'counts': {
            'agents': len(agents),
            'standaloneTasks': len(tasks),
            'helpRows': len(help_rows),
            'bundledFiles': len(copied_files),
        },
        'syntheticConfigDefaults': DEFAULT_CONFIG,
        'pathPrefixes': {
            '_bmad/': 'references/bmad/',
            '{project-root}/_bmad/': 'references/bmad/',
        },
        'agents': agents,
        'standaloneTasks': tasks,
        'helpCatalog': help_rows,
    }
    write_text(RUNTIME_DIR / 'skill-manifest.json', json.dumps(manifest, indent=2, ensure_ascii=False) + '\n')

    write_text(RUNTIME_DIR / 'agent-index.md', generate_agent_index(agents))
    write_text(RUNTIME_DIR / 'workflow-index.md', generate_workflow_index(help_rows))
    write_text(RUNTIME_DIR / 'task-index.md', generate_task_index(tasks))
    write_text(RUNTIME_DIR / 'capability-map.md', generate_capability_map(help_rows, agents, tasks))

    print(f'Bundled {len(copied_files)} files, {len(agents)} agents, {len(tasks)} tasks, {len(help_rows)} help rows into {SKILL_DIR}')


if __name__ == '__main__':
    main()
