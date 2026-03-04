# BMAD-METHOD × Cline 相容性研究報告

> 研究日期：2026-03-04
> 研究分支：`claude/research-cline-compatibility-FcTrg`

---

## 摘要

**結論：完全可行，且已有基礎整合。**

BMAD-METHOD 目前已支援 Cline，並透過 `.clinerules/workflows/` 目錄安裝 workflow 指令。整合品質屬「初步可用」等級，有具體的改進空間，特別是在 agent 呼叫機制與原生 Cline workflow 格式對接上。

---

## 一、BMAD-METHOD 現況

### 系統架構

BMAD-METHOD 是一套 AI 驅動的敏捷開發框架，包含：

| 元件 | 說明 |
|------|------|
| **9 個專業 Agent** | PM（John）、Architect（Winston）、Dev（Amelia）等，各有 YAML 定義的 persona |
| **33+ Workflows** | 涵蓋 4 個開發階段：分析 → 規劃 → 架構 → 實作 |
| **CLI 安裝器** | `npx bmad-method install` 自動根據 IDE 產生對應設定檔 |
| **模組系統** | core + bmm + 外部官方模組（測試、遊戲開發等） |

### 已支援的平台

```yaml
# tools/platform-codes.yaml 節錄
claude-code:   preferred: true   # 主力平台
cursor:        preferred: true   # 第二推薦
cline:         preferred: false  # 已支援，但非首選
roo:           preferred: false  # Cline 分支，也支援
windsurf:      preferred: false  # 共用同一套 template
```

---

## 二、現有 Cline 整合狀態

### 安裝設定

```yaml
# tools/cli/installers/lib/ide/platform-codes.yaml
cline:
  name: "Cline"
  preferred: false
  category: ide
  description: "AI coding assistant"
  installer:
    target_dir: .clinerules/workflows   # 安裝位置
    template_type: windsurf             # 使用 windsurf 的模板格式
```

### 產生的 Workflow 格式

安裝後，每個 workflow 會在 `.clinerules/workflows/` 下產生一個 `.md` 檔：

```markdown
---
description: '{{description}}'
auto_execution_mode: "iterate"
---

# {{name}}

Read the entire workflow file at {project-root}/_bmad/{{workflow_path}}

Follow all instructions in the workflow file exactly as written.
```

### 目前的限制

1. **Agent 指令缺失**：只安裝了 workflows，沒有安裝 agents。Cline 沒有像 Claude Code 的 `/command` 系統可以切換 agent persona。
2. **使用 windsurf 模板**：windsurf 格式有 `auto_execution_mode: "iterate"` 等欄位，但這是否為 Cline 原生支援的格式需要確認。
3. **`.clinerules` 的定位問題**：`.clinerules/workflows/` 是自訂目錄，Cline 的 workflow slash command 機制讀取的路徑需要驗證。

---

## 三、Cline 原生能力分析

### 可以利用的功能

| Cline 功能 | BMAD 對應使用方式 |
|-----------|----------------|
| `.clinerules` 設定檔 | 放入 agent persona 指令、專案規則 |
| `.clinerules/` 目錄 | 分多個 `.md` 檔管理不同 agent 的規則 |
| Slash command workflows | 觸發 BMAD workflow（目前安裝到 `.clinerules/workflows/`） |
| MCP 整合 | 擴充 BMAD 工具能力（如資料庫、外部 API） |
| 大型 context window（1M tokens） | 支援 BMAD 的長文件處理（PRD、架構文件等） |
| 人工審核每個動作 | 與 BMAD 的 human-in-the-loop 哲學完全一致 |

### Cline 的限制

| 限制 | 影響程度 | 說明 |
|------|---------|------|
| 無原生 multi-agent 切換 | ⚠️ 中 | BMAD 的 agent persona 切換需改用 `.clinerules` 注入 |
| VS Code 限定 | ℹ️ 低 | 不影響功能，但非 VS Code 使用者無法用 |
| 300KB 單檔限制 | ⚠️ 低-中 | 大型 workflow 步驟檔需注意大小 |
| 速度較慢（約 90s/task） | ℹ️ 低 | 與 BMAD 慢工出細活的風格匹配 |

---

## 四、可行性評估

### ✅ 高度可行的使用場景

1. **完整 Workflow 執行**：`npx bmad-method install` 後，Cline 可讀取安裝在 `.clinerules/workflows/` 的工作流程，執行 PRD 創建、架構設計、sprint 規劃等任務。

2. **Agent Persona 注入**：透過 `.clinerules` 主檔案或目錄中的 `.md` 檔，將 agent 的 persona（如 PM John、Architect Winston）的角色定義注入 Cline 的 system prompt。

3. **文件導向工作**：BMAD 的 append-only document building 模式與 Cline 的 approve-before-execute 工作流完美搭配。

4. **MCP 工具擴充**：BMAD 的 task tool 系統可透過 MCP server 整合到 Cline 中。

### ⚠️ 需要調整的地方

1. **Agent 切換機制**：Claude Code 用 `/` slash command 切換 agent，Cline 目前不支援原生 agent 切換。解決方案：
   - 在 `.clinerules/` 目錄下為每個 agent 建立獨立規則檔（如 `.clinerules/agent-pm.md`）
   - 用戶手動指示 Cline「現在扮演 PM John 角色」
   - 等待 Cline 的 role-based system 功能（已在規劃中）

2. **Workflow 格式驗證**：需確認 `auto_execution_mode: "iterate"` 是否為 Cline 支援的 frontmatter 欄位，否則可能需要新增 `cline` 專屬 template type。

3. **Slash Command 路徑**：需確認 Cline 是否將 `.clinerules/workflows/*.md` 自動識別為 slash commands，還是需要不同目錄結構。

---

## 五、建議行動方案

### 短期（立即可做）

```bash
# 1. 安裝 BMAD 到 Cline 專案
npx bmad-method install
# 選擇 Cline 平台

# 2. 手動在 .clinerules 加入 agent persona 規則
# 例如在 .clinerules/agents.md 中描述各 agent 角色
```

### 中期（改善整合品質）

1. **新增 Cline 專屬 template type**：從 `windsurf` 分離，建立 `cline` 專屬格式
2. **增加 agent 安裝**：在 Cline 的安裝目標中加入 agent 指令檔
3. **驗證 slash command 路徑**：測試 `.clinerules/workflows/` 是否正確觸發

### 長期（等待 Cline 功能成熟）

1. **採用 Cline role-based system**：當 Cline 推出正式的 agent roles 功能後，可直接對應 BMAD agent 定義
2. **MCP 工具整合**：將 BMAD tasks 封裝為 MCP tools，讓 Cline 可呼叫

---

## 六、技術風險評估

| 風險 | 機率 | 影響 | 緩解方案 |
|------|------|------|---------|
| Cline workflow 格式不相容 | 中 | 中 | 新增 cline 專屬 template |
| Agent persona 切換體驗差 | 高 | 中 | 用 `.clinerules` 文件注入 |
| 大型工作流在 Cline 中執行緩慢 | 中 | 低 | 分拆 workflow 步驟 |
| Cline API 費用較高 | 中 | 低 | 使用便宜模型搭配 BMAD |

---

## 七、結論

BMAD-METHOD 用於 Cline **技術上完全可行**，且已有基礎整合。

主要優勢在於：
- Cline 的 `.clinerules` 機制與 BMAD 的 workflow/agent 系統有良好的對應關係
- 兩者的 human-in-the-loop 哲學高度一致
- Cline 的大型 context window 足以支援 BMAD 的長文件導向工作

主要挑戰在於：
- Agent persona 切換需要變通方案（`.clinerules` 注入而非 slash command 切換）
- 現有整合使用 windsurf template，可能需要 Cline 專屬格式優化

**推薦**：可以立即使用現有整合，同時評估是否值得投資建立更完善的 Cline 原生整合（新增 `cline` template type + agent 安裝支援）。

---

## 參考資料

- [Cline 官方文件 - clinerules](https://docs.cline.bot/features/cline-rules)
- [Cline GitHub](https://github.com/cline/cline)
- [BMAD-METHOD platform-codes.yaml](../tools/cli/installers/lib/ide/platform-codes.yaml)
- [GitHub Issue #643: Update BMAD Cline integration to use workflows instead of clinerules](https://github.com/bmad-code-org/BMAD-METHOD/issues/643)
