# BMad Method — Pure Skill Edition 使用手冊

> **版本**: Pure Skill Edition (無需安裝器)
> **適用**: Claude Code 任何專案

---

## 目錄

1. [什麼是 BMad Method](#1-什麼是-bmad-method)
2. [如何安裝這個 Skill](#2-如何安裝這個-skill)
3. [快速開始](#3-快速開始)
4. [配置設定](#4-配置設定)
5. [Agent 陣容（9位專家）](#5-agent-陣容9位專家)
6. [完整 Workflow 列表](#6-完整-workflow-列表)
7. [Core Tasks（核心任務）](#7-core-tasks核心任務)
8. [完整指令參考表](#8-完整指令參考表)
9. [BMAD 開發生命週期](#9-bmad-開發生命週期)
10. [Quick Flow 快速通道](#10-quick-flow-快速通道)
11. [Party Mode 多 Agent 協作](#11-party-mode-多-agent-協作)
12. [輸出檔案結構](#12-輸出檔案結構)
13. [使用情境範例](#13-使用情境範例)
14. [常見問題](#14-常見問題)

---

## 1. 什麼是 BMad Method

**BMad Method (BMAD)** 是一個 AI 驅動的敏捷軟體開發框架，透過 9 位專業 AI Agent 陪伴你走過完整的產品開發生命週期：

```
構想 → 研究 → PRD → 架構 → Epics → Sprint 規劃 → 開發 → 測試 → 文件
```

**Pure Skill Edition** 的特點：
- ✅ **零安裝** — 不需執行安裝程式，不需要 `_bmad/` 目錄
- ✅ **完全自包含** — 所有邏輯內嵌在 skill 中
- ✅ **可攜帶** — 複製 skill 資料夾到任何專案即可使用
- ✅ **完整功能** — 涵蓋所有 9 個 Agent、所有 Workflows、所有 Core Tasks

---

## 2. 如何安裝這個 Skill

### 方法 A：直接複製（最簡單）

將以下資料夾複製到你的專案：

```
你的專案/
└── .claude/
    └── skills/
        └── bmad-method/          ← 複製這整個資料夾
            ├── SKILL.md
            ├── MANUAL.md
            └── prompts/
                └── instructions.md
```

### 方法 B：從 BMAD-METHOD 儲存庫取得

```bash
# 複製 skill 資料夾到你的專案
cp -r /path/to/BMAD-METHOD/.claude/skills/bmad-method \
      your-project/.claude/skills/
```

### 驗證安裝

在 Claude Code 中輸入 `/bmad`，應該看到 BMad Master 的歡迎畫面。

---

## 3. 快速開始

### 啟動 BMAD

在 Claude Code 中輸入任一觸發詞：

```
/bmad
bmad
start bmad
use bmad
```

### 選擇 Agent

BMAD 啟動後會顯示 Agent 選單：

```
═══════════════════════════════════════════
  BMad Method — Agent Roster
═══════════════════════════════════════════
[BM] 🧙  BMad Master     — 幫助、導航、任意任務
[MA] 📊  Mary            — 商業分析師：研究與探索
[PM] 📋  John            — 產品經理：PRD 與需求
[AR] 🏗️  Winston         — 架構師：技術設計決策
[SM] 🏃  Bob             — Scrum Master：Sprint 規劃
[DV] 💻  Amelia          — 開發者：Story 實作 (TDD)
[UX] 🎨  Sally           — UX 設計師：使用者體驗
[QA] 🧪  Quinn           — QA 工程師：測試自動化
[QF] 🚀  Barry           — Quick Flow：快速 Spec 與開發
[TW] 📚  Paige           — 技術寫作：文件製作
═══════════════════════════════════════════
```

輸入代碼（如 `PM`）或模糊搜尋（如 `architect`、`developer`）來選擇 Agent。

---

## 4. 配置設定

### 自動設定

第一次使用時，BMAD 會使用預設值並可自動建立 `.bmad-config.yaml`。

### 手動建立設定檔

在專案根目錄建立 `.bmad-config.yaml`：

```yaml
# BMad Method 設定檔

# 專案資訊
project_name: "我的專案"
user_name: "你的名字"

# 輸出目錄（相對於專案根目錄）
output_folder: "docs"
planning_artifacts: "docs/planning"         # PRD、架構、Epics 存放位置
implementation_artifacts: "docs/stories"    # Sprint 計劃、Story 存放位置

# 語言設定
communication_language: "繁體中文"          # Agent 對話語言
document_output_language: "繁體中文"        # 輸出文件語言

# 使用者技能等級（影響解說詳細程度）
# beginner | intermediate | expert
user_skill_level: "intermediate"
```

### 設定說明

| 設定項 | 說明 | 預設值 |
|--------|------|--------|
| `project_name` | 專案名稱 | "My Project" |
| `user_name` | 你的名字（Agent 稱呼你） | "User" |
| `output_folder` | 輸出根目錄 | "docs" |
| `planning_artifacts` | 規劃文件目錄 | "docs" |
| `implementation_artifacts` | 實作文件目錄 | "docs/stories" |
| `communication_language` | 對話語言 | "English" |
| `document_output_language` | 文件語言 | "English" |
| `user_skill_level` | 技能等級 | "intermediate" |

---

## 5. Agent 陣容（9位專家）

### 🧙 BMad Master [BM]

**職責：** 總指揮。導航、幫助、任意任務執行。

**特色：**
- 可執行任何任務，無需切換 Agent
- 提供 `/bmad-help` 智慧建議
- 協調 Party Mode 多 Agent 討論
- 列出所有可用 workflows 和 tasks

**觸發方式：** 輸入 `BM`、`bmad master`、或直接 `/bmad`

---

### 📊 Mary — Business Analyst [MA]

**職責：** 研究與探索、把模糊想法轉化為具體需求。

**個性：** 像尋寶探險家一樣充滿熱情，用精準的分析讓洞見如同探索般令人興奮。

**最擅長：**
- 腦力激盪（支援 10+ 種技法）
- 市場研究與競爭分析
- 產品簡報撰寫
- 既有專案文件化

**指令：**
| 代碼 | 指令 | 說明 |
|------|------|------|
| `BP` | Brainstorm Project | 專家引導腦力激盪，產出報告 |
| `MR` | Market Research | 市場分析、競爭格局、趨勢 |
| `DR` | Domain Research | 產業領域深入研究 |
| `TR` | Technical Research | 技術可行性、架構選項 |
| `CB` | Create Brief | 從想法到產品執行摘要 |
| `DP` | Document Project | 分析既有專案，產出完整文件 |

---

### 📋 John — Product Manager [PM]

**職責：** 需求定義、PRD 撰寫、Epic/Story 規劃。

**個性：** 像偵探一樣不停問「為什麼？」直接、以數據為準，剔除廢話找到真正重要的事。

**最擅長：**
- 透過訪談（非填表格）建立 PRD
- 把 PRD 轉化為可實作的 Epics & Stories
- 確保所有文件對齊再開發

**指令：**
| 代碼 | 指令 | 說明 |
|------|------|------|
| `CP` | Create PRD | 從零建立產品需求文件 |
| `VP` | Validate PRD | 審查 PRD 完整性與品質 |
| `EP` | Edit PRD | 修改既有 PRD |
| `CE` | Create Epics & Stories | 將 PRD 分解為 Epics 和 Stories |
| `IR` | Implementation Readiness | 開發前文件對齊檢查 |
| `CC` | Course Correction | 開發中途重大變更管理 |

---

### 🏗️ Winston — Architect [AR]

**職責：** 技術架構設計，確保 AI Agent 實作一致性。

**個性：** 冷靜務實，在「能做什麼」和「應該做什麼」之間取得平衡。

**最擅長：**
- 架構決策記錄（ADR）
- 技術選型與評估
- 為開發 Agent 提供明確的實作指南

**指令：**
| 代碼 | 指令 | 說明 |
|------|------|------|
| `CA` | Create Architecture | 協作式技術架構設計 |
| `IR` | Implementation Readiness | 技術可行性確認 |

---

### 🏃 Bob — Scrum Master [SM]

**職責：** Sprint 規劃、Story 準備、敏捷儀式。

**個性：** 精準、條列式思考。每個字都有目的，對模糊零容忍。

**最擅長：**
- 將 Epics 轉化為追蹤用 Sprint Status 檔案
- 為每個 Story 準備完整的實作上下文
- 管理 Epic 回顧

**指令：**
| 代碼 | 指令 | 說明 |
|------|------|------|
| `SP` | Sprint Planning | 從 Epics 產生 Sprint 追蹤檔 |
| `SS` | Sprint Status | 查看目前 Sprint 進度 |
| `CS` | Create Story | 準備單一 Story 的完整實作上下文 |
| `VS` | Validate Story | 開發前 Story 品質檢查 |
| `ER` | Epic Retrospective | Epic 完成後的回顧會議 |
| `CC` | Course Correction | 開發中途重大變更管理 |

---

### 💻 Amelia — Developer [DV]

**職責：** Story 實作，嚴格遵循 TDD 紅綠重構循環。

**個性：** 極度簡潔。說的都是檔案路徑和 AC 編號，每句話都可引用。絕不廢話。

**鐵則：**
- 先寫失敗的測試（Red），再實作（Green），再重構（Refactor）
- 永遠不謊稱測試通過
- 不完成就不停下來

**指令：**
| 代碼 | 指令 | 說明 |
|------|------|------|
| `DS` | Dev Story | 實作下一個或指定的 Story |
| `CR` | Code Review | 對實作進行對抗性程式碼審查 |

---

### 🎨 Sally — UX Designer [UX]

**職責：** 使用者體驗設計規格。

**個性：** 用文字作畫，充滿同理心的倡導者。平衡創意與邊界案例。

**指令：**
| 代碼 | 指令 | 說明 |
|------|------|------|
| `CU` | Create UX Design | 建立完整 UX 設計規格文件 |

---

### 🧪 Quinn — QA Engineer [QA]

**職責：** 測試策略與自動化測試生成。

**個性：** 務實。「先出貨再迭代」心態。聚焦在真正能抓到 bug 的覆蓋率。

**指令：**
| 代碼 | 指令 | 說明 |
|------|------|------|
| `QG` | Generate E2E Tests | 生成端到端測試套件 |
| `QR` | QA Review | 審查測試覆蓋率與品質 |

---

### 🚀 Barry — Quick Flow Solo Dev [QF]

**職責：** 快速通道——跳過繁文縟節，直接規格化並實作。

**個性：** 直接、自信、以實作為核心。直奔重點。

**指令：**
| 代碼 | 指令 | 說明 |
|------|------|------|
| `QS` | Quick Spec | 快速產生實作就緒的技術規格 |
| `QD` | Quick Dev | 從規格或描述直接實作 |
| `QQ` | Quick Dev New (Preview) | 先預覽實作計劃，確認後再執行 |
| `CR` | Code Review | 程式碼審查 |

---

### 📚 Paige — Technical Writer [TW]

**職責：** 技術文件製作、圖表生成、文件品質管理。

**個性：** 像教朋友一樣耐心解說，用比喻讓複雜事物變簡單，相信圖勝千言。

**指令：**
| 代碼 | 指令 | 說明 |
|------|------|------|
| `DP` | Document Project | 分析既有專案，產出完整文件集 |
| `WD` | Write Document | 多輪對話產出任何文件 |
| `US` | Update Standards | 更新文件寫作標準 |
| `MG` | Mermaid Generate | 從描述生成 Mermaid 圖表 |
| `VD` | Validate Documentation | 驗證文件品質與準確性 |
| `EC` | Explain Concept | 為複雜概念建立清晰解說 |

---

## 6. 完整 Workflow 列表

### 第一階段：分析（Analysis）

| Workflow | 代碼 | Agent | 說明 | 輸出 |
|----------|------|-------|------|------|
| Brainstorm Project | `BP` | Mary | 腦力激盪引導（10+ 技法） | `brainstorm-report.md` |
| Market Research | `MR` | Mary | 市場分析、競爭格局 | `market-research.md` |
| Domain Research | `DR` | Mary | 產業領域深入研究 | `domain-research.md` |
| Technical Research | `TR` | Mary | 技術可行性評估 | `technical-research.md` |
| Create Product Brief | `CB` | Mary | 產品執行摘要 | `product-brief.md` |
| Document Project | `DP` | Mary/Paige | 現有專案文件化 | `project-context.md` + docs |

### 第二階段：規劃（Planning）

| Workflow | 代碼 | Agent | 說明 | 輸出 |
|----------|------|-------|------|------|
| Create PRD | `CP` | John | 透過訪談建立產品需求文件 | `prd.md` |
| Validate PRD | `VP` | John | PRD 完整性與品質審查 | 審查報告 |
| Edit PRD | `EP` | John | 修改既有 PRD | 更新版 `prd.md` |
| Create UX Design | `CU` | Sally | UX 設計規格 | `ux-design.md` |

### 第三階段：解決方案（Solutioning）

| Workflow | 代碼 | Agent | 說明 | 輸出 |
|----------|------|-------|------|------|
| Create Architecture | `CA` | Winston | 技術架構決策（含 ADR） | `architecture.md` |
| Create Epics & Stories | `CE` | John | PRD → Epics & Stories | `epics.md` |
| Implementation Readiness | `IR` | John/Winston | 開發前文件對齊檢查 | 就緒報告 |

### 第四階段：實作（Implementation）

| Workflow | 代碼 | Agent | 說明 | 輸出 |
|----------|------|-------|------|------|
| Sprint Planning | `SP` | Bob | Epics → Sprint 追蹤 | `sprint-status.yaml` |
| Sprint Status | `SS` | Bob | 查看 Sprint 進度 | 進度報告 |
| Create Story | `CS` | Bob | 準備 Story 實作上下文 | `{story-key}.md` |
| Validate Story | `VS` | Bob | Story 品質檢查 | 驗證報告 |
| Dev Story | `DS` | Amelia | TDD 實作 Story | 程式碼 + 測試 |
| Code Review | `CR` | Amelia/Barry | 對抗性程式碼審查 | 審查報告 |
| QA Automation Tests | `QG` | Quinn | 生成 E2E 測試 | 測試檔案 |
| Epic Retrospective | `ER` | Bob | Epic 完成後回顧 | `epic-N-retrospective.md` |
| Course Correction | `CC` | John/Bob | 開發中途重大變更 | 修正計劃 |

### 快速通道（Quick Flow，可隨時使用）

| Workflow | 代碼 | Agent | 說明 | 輸出 |
|----------|------|-------|------|------|
| Quick Spec | `QS` | Barry | 快速技術規格 | `tech-spec.md` |
| Quick Dev | `QD` | Barry | 從規格直接實作 | 程式碼 + 測試 |
| Quick Dev Preview | `QQ` | Barry | 先預覽計劃再實作 | 計劃 + 程式碼 |

### 文件工具（隨時可用）

| Workflow | 代碼 | Agent | 說明 | 輸出 |
|----------|------|-------|------|------|
| Generate Project Context | `GPC` | BMad Master | 自動生成 project-context.md | `project-context.md` |
| Write Document | `WD` | Paige | 撰寫任何文件 | 指定文件 |
| Mermaid Generate | `MG` | Paige | 生成 Mermaid 圖表 | Mermaid 程式碼 |
| Validate Documentation | `VD` | Paige | 文件品質審查 | 審查報告 |
| Explain Concept | `EC` | Paige | 技術概念解說 | 解說文件 |
| Index Docs | `ID` | BMad Master | 生成文件索引 | `index.md` |
| Shard Document | `SD` | BMad Master | 大文件分割成小檔案 | 分割後的檔案集 |

---

## 7. Core Tasks（核心任務）

Core Tasks 是可以在任何時候、從任何 Agent 呼叫的獨立任務，透過 BMad Master `[BM]` 存取。

### Party Mode [PM-PARTY]

**說明：** 讓多個 Agent 同時討論一個問題，集合不同視角做出更好的決策。

**使用場景：**
- 所有 Agent 審查 PRD → 從分析師、PM、架構師、開發者視角找問題
- 多角度評估技術選型
- 回顧會議

**啟動：** `party mode — [描述要討論的議題]`

**範例：**
```
party mode — all agents review the PRD and identify concerns from their perspective
```

---

### 對抗性審查工具

| 任務 | 代碼 | 說明 |
|------|------|------|
| Adversarial Review | `AR-REVIEW` | 假設一切都有問題，找出所有缺陷 |
| Edge Case Hunter | `ECH` | 系統性列舉所有未處理的邊界案例 |

**Adversarial Review 適用於：**
- PRD（找未考慮到的情況）
- 架構文件（找技術風險）
- Story（找需求漏洞）
- 程式碼（找 bug 和安全問題）

**Edge Case Hunter 適用於：**
- 演算法和業務邏輯
- API 端點
- 工作流程規格

---

### 文件品質工具

| 任務 | 代碼 | 說明 |
|------|------|------|
| Editorial Review Prose | `EP-PROSE` | 用詞、句子結構、清晰度審查 |
| Editorial Review Structure | `EP-STRUCT` | 結構、組織、完整性審查 |
| Index Docs | `ID` | 為資料夾生成文件索引 |
| Shard Document | `SD` | 將大文件分割成較小的檔案 |

---

## 8. 完整指令參考表

### 快速查找

輸入格式：`[Agent代碼] [Workflow代碼]`

範例：
- `PM CP` → John 建立 PRD
- `SM SP` → Bob 執行 Sprint 規劃
- `DV DS` → Amelia 實作 Story
- `QF QS` → Barry 快速規格化

### 所有指令一覽

```
AGENT     CODE  WORKFLOW / TASK
────────────────────────────────────────────────────────
BMad Master [BM]
          LT    列出所有任務
          LW    列出所有 Workflows
          LA    列出所有 Agents
          HE    幫助和建議
          GPC   生成 Project Context
          PM-PARTY  Party Mode（多 Agent 討論）
          AR-REVIEW Adversarial Review（對抗性審查）
          ECH   Edge Case Hunter（邊界案例獵人）
          EP-PROSE  Editorial Review - Prose
          EP-STRUCT Editorial Review - Structure
          ID    Index Docs（文件索引）
          SD    Shard Document（文件分割）

Mary - Analyst [MA]
          BP    Brainstorm Project
          MR    Market Research
          DR    Domain Research
          TR    Technical Research
          CB    Create Product Brief
          DP    Document Project

John - PM [PM]
          CP    Create PRD
          VP    Validate PRD
          EP    Edit PRD
          CE    Create Epics & Stories
          IR    Implementation Readiness
          CC    Course Correction

Winston - Architect [AR]
          CA    Create Architecture
          IR    Implementation Readiness

Bob - Scrum Master [SM]
          SP    Sprint Planning
          SS    Sprint Status
          CS    Create Story
          VS    Validate Story
          ER    Epic Retrospective
          CC    Course Correction

Amelia - Developer [DV]
          DS    Dev Story
          CR    Code Review

Sally - UX Designer [UX]
          CU    Create UX Design

Quinn - QA [QA]
          QG    Generate E2E Tests
          QR    QA Review

Barry - Quick Flow [QF]
          QS    Quick Spec
          QD    Quick Dev
          QQ    Quick Dev New (Preview)
          CR    Code Review

Paige - Tech Writer [TW]
          DP    Document Project
          WD    Write Document
          US    Update Standards
          MG    Mermaid Generate
          VD    Validate Documentation
          EC    Explain Concept
```

---

## 9. BMAD 開發生命週期

### 完整開發流程（從零開始的新產品）

```
┌─────────────────────────────────────────────────────────┐
│                    第一階段：分析                         │
│                                                         │
│  Mary [BP] → 腦力激盪                                    │
│  Mary [CB] → 產品執行摘要                                 │
│  Mary [MR] → 市場研究（可選）                             │
│  Mary [DR] → 領域研究（可選）                             │
│  Mary [TR] → 技術研究（可選）                             │
└─────────────────────────┬───────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────┐
│                    第二階段：規劃                         │
│                                                         │
│  John [CP] → 建立 PRD                                   │
│  John [VP] → 驗證 PRD                                   │
│  Sally [CU] → UX 設計（有 UI 時）                        │
└─────────────────────────┬───────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────┐
│                   第三階段：解決方案                      │
│                                                         │
│  Winston [CA] → 技術架構                                 │
│  John [CE]    → 建立 Epics & Stories                    │
│  John [IR]    → 實作就緒確認                             │
└─────────────────────────┬───────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────┐
│                   第四階段：實作                         │
│                                                         │
│  Bob [SP]     → Sprint 規劃                             │
│    ↓（每個 Story 重複以下流程）                           │
│  Bob [CS]     → 準備 Story                              │
│  Bob [VS]     → 驗證 Story                              │
│  Amelia [DS]  → 實作 Story (TDD)                        │
│  Amelia [CR]  → 程式碼審查                               │
│    ↓（Epic 完成後）                                      │
│  Bob [ER]     → Epic 回顧                               │
└─────────────────────────────────────────────────────────┘
```

### 各階段輸出文件

```
docs/planning/
├── brainstorm-report.md       ← Mary [BP]
├── product-brief.md           ← Mary [CB]
├── market-research.md         ← Mary [MR]
├── prd.md                     ← John [CP]
├── ux-design.md               ← Sally [CU]
├── architecture.md            ← Winston [CA]
├── epics.md                   ← John [CE]
└── project-context.md         ← Mary [DP] / Auto [GPC]

docs/stories/
├── sprint-status.yaml         ← Bob [SP]
├── 1-1-user-auth.md           ← Bob [CS]
├── 1-2-profile-page.md        ← Bob [CS]
└── ...
```

---

## 10. Quick Flow 快速通道

適合：已充分了解需求的小功能、bug 修復、技術重構。

```
┌─────────────────────────────────────────────────────────┐
│                    Quick Flow 流程                       │
│                                                         │
│  Barry [QS]   → 快速技術規格（5-10分鐘）                  │
│  Barry [QD]   → 直接實作（從規格或描述）                   │
│  Amelia [CR]  → 程式碼審查                               │
└─────────────────────────────────────────────────────────┘
```

### 何時使用 Quick Flow

✅ **適合 Quick Flow：**
- 需求清楚的小功能
- Bug 修復
- 技術重構
- 獨立的 API 端點
- 設定或環境變更

❌ **不適合 Quick Flow（使用完整流程）：**
- 全新產品
- 需要市場驗證的功能
- 涉及多個系統的大型架構變更
- 需要 UX 設計的功能

---

## 11. Party Mode 多 Agent 協作

Party Mode 讓多個 Agent 同時討論一個議題，模擬真實團隊討論。

### 啟動方式

```
party mode — [描述議題]
```

### 使用範例

**PRD 全面審查：**
```
party mode — all agents review the PRD and give their perspective on potential issues
```
結果：Mary 從用戶研究角度、John 從需求完整性、Winston 從技術可行性、Amelia 從實作難度分別提出意見。

**技術選型評估：**
```
party mode — evaluate between React and Vue for our frontend, agents debate pros and cons
```

**Epic 規劃：**
```
party mode — review the epics and stories, identify missing stories or ordering issues
```

### Party Mode 輸出

- 每個 Agent 的立場和理由
- 共識點
- 分歧點（含各方理由）
- BMad Master 綜合建議
- 行動項目

---

## 12. 輸出檔案結構

BMAD 生成的所有文件組織如下：

```
{your-project}/
├── .bmad-config.yaml            ← BMAD 設定（自動生成）
│
├── docs/planning/               ← 規劃文件（planning_artifacts）
│   ├── brainstorm-report.md
│   ├── product-brief.md
│   ├── market-research.md
│   ├── domain-research.md
│   ├── technical-research.md
│   ├── prd.md
│   ├── ux-design.md
│   ├── architecture.md
│   ├── epics.md
│   ├── project-context.md
│   └── epic-N-retrospective.md
│
└── docs/stories/                ← 實作文件（implementation_artifacts）
    ├── sprint-status.yaml
    ├── 1-1-{story-slug}.md
    ├── 1-2-{story-slug}.md
    └── ...
```

### Story 檔案結構

每個 Story 檔案（如 `1-1-user-auth.md`）包含：

```markdown
---
story_key: "1-1-user-authentication"
title: "User Authentication"
epic: 1
status: "ready-for-dev"           ← not-started | ready-for-dev | in-progress | review | done | blocked
---

## Story
As a [persona], I want to [action], so that [outcome].

## Acceptance Criteria
- [ ] AC1: Given... When... Then...

## Tasks / Subtasks
- [ ] Task 1: Write tests for...
  - [ ] Write failing test
  - [ ] Implement
  - [ ] Verify passes

## Dev Notes
[架構上下文、技術指引]

## Dev Agent Record
[Amelia 填寫的實作記錄]

## File List
[所有修改的檔案]
```

### Sprint Status 狀態機

```
not-started → ready-for-dev → in-progress → review → done
                                   ↑                   |
                              blocked ←────────────────┘
                              (有問題時)
```

---

## 13. 使用情境範例

### 情境 A：從零開始的新 SaaS 產品

```
1. /bmad → 選 [MA] Mary
2. MA > BP  → 腦力激盪：「我想做一個 X 平台」
3. MA > CB  → 把想法整理成產品執行摘要
4. MA > MR  → 市場研究：競爭對手和目標用戶
5. → 切換到 [PM] John
6. PM > CP  → 建立完整 PRD（透過訪談）
7. → 切換到 [AR] Winston
8. AR > CA  → 技術架構設計
9. → 切換到 [UX] Sally
10. UX > CU → UX 設計規格
11. → 切換到 [PM] John
12. PM > CE → 建立 Epics & Stories
13. PM > IR → 確認所有文件對齊
14. → 切換到 [SM] Bob
15. SM > SP → 生成 Sprint 計劃
16. SM > CS → 準備第一個 Story
17. → 切換到 [DV] Amelia
18. DV > DS → 實作 Story（自動 TDD）
19. DV > CR → 程式碼審查
20. 重複步驟 16-19 直到所有 Story 完成
```

---

### 情境 B：快速功能開發

```
1. /bmad → 選 [QF] Barry
2. QF > QS → 「我需要一個 JWT 認證的 API 端點」
3. （Barry 快速產生技術規格）
4. QF > QD → 直接從規格實作
5. DV > CR → Amelia 進行程式碼審查（建議用不同 LLM）
```

---

### 情境 C：既有專案文件化

```
1. /bmad → 選 [MA] Mary
2. MA > DP → 分析現有程式碼庫
3. （生成 project-context.md、架構圖等）
4. 或：選 [TW] Paige
5. TW > DP → 更詳盡的技術文件
6. TW > MG → 生成架構圖（Mermaid）
```

---

### 情境 D：多角度 PRD 審查

```
1. /bmad → 選 [BM] BMad Master
2. BM > party mode — all agents review the PRD
3. （所有 Agent 從各自角度提出問題和建議）
4. 切換到 [PM] John
5. PM > EP → 根據反饋修改 PRD
```

---

### 情境 E：程式碼品質審查

```
1. /bmad → 選 [DV] Amelia
2. DV > CR → 對特定 Story 實作進行對抗性審查
3. 或：選 [BM] BMad Master
4. BM > AR-REVIEW → 對抗性審查任何文件或程式碼
5. BM > ECH → 邊界案例獵人
```

---

## 14. 常見問題

### Q: 我不知道從哪裡開始？

輸入 `/bmad-help [你的情況描述]`，BMad Master 會根據你的情況推薦下一步。

例如：
```
/bmad-help 我有一個 app 的想法，不知道從哪裡開始
/bmad-help 我有 PRD 了，接下來要做什麼？
/bmad-help 我的 Sprint 卡住了，有個 Story 需要重大修改
```

---

### Q: 可以跳過某些階段嗎？

可以。BMAD 是靈活的：
- 有清楚需求？跳到第二階段 → John [CP]
- 已有 PRD？跳到架構 → Winston [CA]
- 小功能？直接用 Quick Flow → Barry [QS/QD]

---

### Q: 輸出語言如何設定為中文？

在 `.bmad-config.yaml` 中設定：
```yaml
communication_language: "繁體中文"
document_output_language: "繁體中文"
```

---

### Q: Dev Story 可以自動執行嗎？

可以。Amelia [DS] 會：
1. 自動找到下一個 `ready-for-dev` 的 Story
2. 連續執行所有 Tasks（TDD 循環）
3. 不會因為「進度里程碑」停下來
4. 只有在遇到真正的問題（HALT 條件）才會停止

---

### Q: Code Review 建議用不同的 LLM？

是的。為了最佳效果，程式碼審查建議使用與實作時不同的 LLM 或新的 context window，這樣可以避免審查者對自己的工作有盲點。

---

### Q: 如何管理多個 Epic？

使用 Bob [SS] Sprint Status 指令隨時查看所有 Epics 和 Stories 的進度。
`sprint-status.yaml` 是追蹤整個專案進度的主文件。

---

### Q: Party Mode 和普通 Agent 切換有什麼差別？

- **切換 Agent**：一次只有一個 Agent 活躍，用它的視角回答
- **Party Mode**：多個 Agent 同時討論，你可以看到不同專業視角的辯論和對話

---

## 附錄：BMAD 設計原則

1. **Context Engineering**：每個階段的輸出都是下一階段的輸入，建立完整的上下文鏈
2. **Scale-Adaptive**：根據專案規模自動調整規劃深度
3. **Sequential Enforcement**：步驟必須按順序執行，不允許跳步
4. **User Gates**：每個重要決策點都需要用戶確認
5. **Append-Only Documents**：文件只增不減，保留完整歷史
6. **TDD First**：先寫失敗的測試，再實作（Red-Green-Refactor）
7. **No Time Estimates**：專注於「做什麼」而非「需要多久」

---

*BMad Method Pure Skill Edition — 讓 AI 成為你整個開發團隊*
