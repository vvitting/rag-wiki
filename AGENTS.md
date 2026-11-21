# AGENTS.md — RAG Wiki 維護規範

本檔是這個 wiki 的 schema：定義結構、寫作慣例、引用規則與工作流程。
AI agent（Claude Code、Codex 等）在這個 repo 工作時，**每次都必須遵守本檔**。
本檔由使用者與 agent 共同演進；規則要改時，先跟使用者確認，再修改本檔並記錄到 `wiki/log.md`。

設計依據：Karpathy 的 LLM Wiki 構想（https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f）。

---

## 1. 專案目的與讀者

- **主題**：RAG（Retrieval-Augmented Generation，檢索增強生成）。
- **兩個用途**：
  1. 作為素材庫，產生一份給初學者的 HTML 教學簡報（`slides/rag-intro.html`）。
  2. 作為使用者日後自己查資料用的參考庫；說法要能追溯回原文。
- **讀者**：不熟 AI 的大學生。寫作時先假設讀者不知道什麼是 LLM、embedding、vector。

---

## 2. 三層架構與目錄

```
rag-wiki/
├── AGENTS.md          # 本檔（schema）
├── CLAUDE.md          # 只有一行 @AGENTS.md，讓 Claude Code 自動讀到本檔
├── raw/               # 第 1 層：原始來源（PDF）。唯讀，不可修改、改名或刪除
├── wiki/              # 第 2 層：由 agent 撰寫與維護的 Markdown wiki
│   ├── index.md       # 內容目錄（每次 query 先讀這裡）
│   ├── log.md         # 時間序工作紀錄（只能追加）
│   ├── overview.md    # RAG 全貌總覽
│   ├── glossary.md    # 術語表
│   ├── analogies.md   # 生活化比喻
│   ├── sources/       # 每篇 raw 一頁
│   ├── concepts/      # 概念頁
│   ├── methods/       # 方法／系統頁
│   ├── comparisons/   # 比較與綜合頁
│   └── questions/     # 存回 wiki 的問答
├── slides/
│   └── rag-intro.html # 最終簡報
└── tools/
    └── lint.py        # 機械性健康檢查
```

- `raw/` 是唯一的事實來源（source of truth）。
- `wiki/` 完全由 agent 擁有；使用者主要負責閱讀。
- 新增來源時，由使用者把檔案放進 `raw/`，命名格式為 `NN-作者年份-關鍵字.pdf`。

---

## 3. 寫作規範

- **語言**：繁體中文。**專有名詞保留英文**，不翻譯，例如：「把文件切成 chunk，再用 embedding model 轉成 vector」。
  - 例外：`glossary.md` 的每個詞條要附一句白話中文解釋。
- **語氣**：寫給不熟 AI 的大學生看。句子要短，一段只講一件事；第一次出現的專有名詞要連到 `glossary.md` 或對應的概念頁。
- **先講直覺，再講細節**：概念頁的開頭先用 1–2 句白話說明「它是什麼、為什麼需要」，再展開技術細節。
- **改寫，而不是一直往後追加**：新資訊要整合進既有段落，讓頁面保持一份連貫的說明，而不是一串時間序的筆記。
- **先擴充既有頁面，再考慮新增**：建立新頁前，先查 `index.md`，確認沒有主題相同或相近的頁面。

---

## 4. 頁面類型與模板

檔名一律用英文 kebab-case，例如 `concepts/dense-retrieval.md`。來源頁的檔名與 raw 檔名相同（副檔名改成 `.md`），例如 `sources/01-lewis2020-rag.md`。

### 4.1 來源頁 `sources/`（每篇 raw 一頁）

```markdown
---
type: source
title: "論文完整標題"
raw: 01-lewis2020-rag.pdf
authors: [第一作者, ...]
year: 2020
tags: [rag, ...]
sources: [01-lewis2020-rag.pdf]
updated: YYYY-MM-DD
---

# 論文標題（簡稱）

## 一句話摘要
## 這篇想解決什麼問題
## 核心方法
## 關鍵結果（數字務必附出處）
## 限制與後續爭議
## 關鍵圖表說明
## 對初學者的重點
## 相關頁面
```

### 4.2 概念頁 `concepts/`

一個概念一頁，跨論文整合，例如 chunking、embedding、retriever、reranking、hallucination、context window。

段落：`白話說明` → `為什麼重要` → `運作方式` → `各論文怎麼說`（逐篇整理，附引用）→ `常見誤解`（選用）→ `相關頁面`。

### 4.3 方法／系統頁 `methods/`

例如 naive RAG、Self-RAG、GraphRAG、Contextual Retrieval。

段落：`一句話說明` → `跟 naive RAG 的差別` → `運作步驟` → `優點` → `代價與限制` → `出處` → `相關頁面`。

### 4.4 比較與綜合頁 `comparisons/`

例如「RAG 進階技巧比較」「RAG 演進時間軸」。以表格為主，**表格的每一格如果有事實或數字，也要附引用**。

### 4.5 問答頁 `questions/`

使用者問過、值得保留的問題。檔名用問題的英文 slug。段落：`問題` → `簡答` → `詳細說明（附引用）` → `相關頁面`。

### 4.6 單一檔案頁

- `glossary.md`：依英文字母排序。每條格式：`- **Term**：一句白話解釋 [raw 檔名, 位置] → [詳見](concepts/xxx.md)`。
- `analogies.md`：每個比喻都要包含 `比喻`、`對應到 RAG 的哪個部分`、`比喻的極限（哪裡不像）`、`對應的技術事實（附引用）`。比喻本身不是事實主張，不需要引用；但「對應的技術事實」一定要引用。
- `overview.md`：RAG 全貌。結構對齊簡報：為什麼需要 → 是什麼 → 怎麼運作 → 進階變體 → 怎麼評估 → 總結。

---

## 5. YAML frontmatter

除了 `index.md`、`log.md`，每頁都要有 frontmatter，必填欄位：

| 欄位        | 說明                                                                                                              |
| ----------- | ----------------------------------------------------------------------------------------------------------------- |
| `type`    | `source` / `concept` / `method` / `comparison` / `question` / `glossary` / `analogy` / `overview` |
| `title`   | 頁面標題                                                                                                          |
| `tags`    | 標籤陣列                                                                                                          |
| `sources` | 本頁引用到的 raw 檔名陣列，例如 `[01-lewis2020-rag.pdf, 02-gao2023-survey.pdf]`                                 |
| `updated` | 最後更新日期 `YYYY-MM-DD`                                                                                       |

來源頁另外加 `raw`、`authors`、`year`。

---

## 6. 連結

- 一律使用**標準 Markdown 相對連結**：`[Chunking](../concepts/chunking.md)`。**不要用** `[[wikilink]]`。這樣 Obsidian 和 VS Code／GitHub 都能點開。
- 每頁結尾都要有 `## 相關頁面` 區塊，至少連到 1 個其他頁面。
- 每頁都必須至少被 1 個其他頁面連到（`index.md` 也算），不能有孤立頁面。
- 提到一個還沒有頁面的重要概念時，先在 `index.md` 的「待建頁面」區塊記下來。

---

## 7. 引用規則（最重要）

- **每個主張都要標出處**，格式：`[raw 檔名, 章節或頁碼]`
  - 章節：`[01-lewis2020-rag.pdf, §3.1]`
  - 頁碼：`[04-liu2023-lost-in-middle.pdf, p.5]`（`p.N` = PDF 檔案的第 N 頁，從 1 開始算，不是論文上印的頁碼）
  - 圖表：`[06-edge2024-graphrag.pdf, Fig.2]`、`[07-es2023-ragas.pdf, Table 1]`
  - 可以合併：`[05-asai2023-self-rag.pdf, §4.2, p.7]`
- **數字一定要附原文出處**：百分比、分數、模型大小、資料集大小、年份比較都算。引用要放在同一句或同一個列表項目裡。
- 引用的位置要指到**實際說出這件事的地方**；不確定時，回去重讀 PDF 確認，不要憑記憶寫。
- **嚴格只用 `raw/`**：不靠常識補寫，不上網找資料。初學者需要、但 raw/ 裡找不到的內容，寫上 `[待補來源]` 標記，並在 `index.md` 的「待補來源」區塊列出。
- 可以直接引用原文的一小段英文（加引號），但以改寫成中文說明為主。

---

## 8. 衝突與更新

新來源推翻、修正或限定了舊說法時：

- **兩邊的說法都保留**，不要直接覆蓋。
- 用下面的格式標註：

```markdown
> ⚠️ **爭議／更新**：[02-gao2023-survey.pdf, §2] 認為……；但 [04-liu2023-lost-in-middle.pdf, §3, p.4] 發現……。
```

- 在相關的概念頁、方法頁都加上這個標註，並在 `log.md` 記錄。

---

## 9. 工作流程

### 9.1 Ingest（一次一篇）

使用者說「ingest 03」或「ingest 下一篇」時：

1. 讀整篇 raw PDF（篇幅長就分段讀），記下章節與頁碼。
2. 建立或更新 `sources/<raw 檔名>.md`。
3. 更新或建立相關的 `concepts/`、`methods/`、`comparisons/` 頁面；先擴充既有頁面，再考慮新增。
4. 更新 `glossary.md`（新術語）、`analogies.md`（適合的比喻）、`overview.md`。
5. 檢查有沒有和既有內容衝突的地方，依第 8 節標註。
6. **更新 `index.md`**。
7. **在 `log.md` 追加一筆**。
8. 執行 `python3 tools/lint.py`，修正所有錯誤（error）。
9. 執行第 9.3 節的語意檢查清單。
10. 回報給使用者一份**變更清單**：新增了哪些頁、修改了哪些頁、新增了哪些 ⚠️ 標註、有哪些 `[待補來源]`。

預設順序照檔名 01 → 07。每篇處理完直接寫入，不用每篇都先停下來等使用者確認；使用者再看變更清單抽查。

### 9.2 Query

1. 先讀 `index.md`，找出相關頁面。
2. 讀那些頁面；必要時回到 raw PDF 核對。
3. 回答時附上 wiki 頁面連結與 raw 引用。
4. 如果答案值得保留（使用者要求，或明顯有重複查詢的價值），存成 `questions/` 頁面，並更新 `index.md`、`log.md`。

### 9.3 Lint（兩層，在每次 ingest 完和產生簡報前各跑一次）

**機械性檢查**：執行 `python3 tools/lint.py`，它會檢查：

- 壞掉的連結（連到不存在的檔案）
- 孤立頁面（沒有其他頁面連進來）
- frontmatter 缺少或必填欄位不完整
- 引用到不存在的 raw 檔名
- 含數字卻沒附引用的段落（error）
- 沒附引用的內文段落（warning）
- 簡報規格（第 10 節）

**語意檢查清單**（由 agent 人工檢查）：

- [ ] 不同頁面之間有沒有互相矛盾、但還沒加 ⚠️ 標註的說法？
- [ ] 有沒有被較新來源取代、但沒有標註的舊說法？
- [ ] 有沒有被提到好幾次、卻還沒有獨立頁面的概念？
- [ ] 有沒有內容重疊、應該合併的頁面？
- [ ] 引用的章節／頁碼是不是真的有這個說法？（每次抽查至少 3 處）
- [ ] 不熟 AI 的大學生讀得懂嗎？專有名詞第一次出現時有連結嗎？
- [ ] `[待補來源]` 清單是否最新？

Lint 結果追加到 `log.md`。

### 9.4 產生簡報

1. 先跑一次完整 lint（9.3）。
2. 以 `overview.md` 為骨架，從各頁取材。
3. 依第 10 節規格產生 `slides/rag-intro.html`。
4. 跑 `python3 tools/lint.py` 確認簡報規格。
5. 在 `log.md` 記錄。

---

## 10. 簡報規格（`slides/rag-intro.html`）

- **完全自包含的單一 HTML 檔**：CSS 和 JS 全部內嵌。**不使用 reveal.js 或任何框架、CDN、外部字型或外部圖片**。
- 每張投影片是一個 `<section class="slide">`，固定 **16:9**，依視窗大小等比例縮放。
- **方向鍵**（← →，也支援 PageUp/PageDown、空白鍵）翻頁；`F` 鍵切換全螢幕；`N` 鍵切換顯示講者備註。
- **張數 8–15 張**（目標約 12 張），約 15 分鐘。
- **結構**：為什麼需要 → 是什麼 → 怎麼運作 → 進階變體 → 怎麼評估 → 總結。
- **內容呈現**：以文字重點為主；內嵌 SVG 圖只在關鍵處少量使用（例如 RAG 流程圖）。多用 `analogies.md` 裡的比喻。
- **講者備註**：每張都要有 `<aside class="notes">…</aside>`，內容是可以直接照著念的講稿。
- **引用 footer**：每張底部都要有 `<footer class="refs">`，列出這張用到的 wiki 頁面路徑，例如 `wiki/concepts/chunking.md`。
- 簡報裡的事實都必須來自 wiki，不能有 wiki 裡沒有的新主張。

---

## 11. `index.md` 與 `log.md` 格式

### index.md

依類別分區，每頁一行：

```markdown
- [頁面標題](concepts/chunking.md) — 一行摘要（sources: 3, updated: 2026-11-22）
```

固定的區塊：總覽、來源、概念、方法、比較與綜合、問答、工具頁（glossary／analogies）、待建頁面、待補來源。

### log.md

只能往後追加，最新的放最下面。每筆用固定前綴，方便用 `grep "^## \[" wiki/log.md | tail -5` 查：

```markdown
## [YYYY-MM-DD] ingest | 01-lewis2020-rag.pdf
- 新增：…
- 修改：…
- ⚠️ 新標註：…
- 待補來源：…
- lint：0 error, N warning
```

動作類型：`setup`、`ingest`、`query`、`lint`、`slides`、`schema`（修改本檔）。

---

## 12. 禁止事項

- ❌ 修改、改名、刪除 `raw/` 裡的任何檔案。
- ❌ 寫沒有出處的事實主張或數字；找不到出處就寫 `[待補來源]`。
- ❌ 使用 raw/ 以外的知識來源（包括網路搜尋）。
- ❌ 用新說法直接覆蓋舊說法、卻沒有加 ⚠️ 標註。
- ❌ 使用 `[[wikilink]]` 語法。
- ❌ 讓簡報依賴任何外部資源。
- ❌ 跳過 `index.md`、`log.md` 的更新。
