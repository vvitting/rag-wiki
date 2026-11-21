---
description: 主題 → 教學 HTML 簡報（只用 wiki/ 內容的 graph workflow，含關卡、審查、渲染檢查）
argument-hint: <主題>
---

# /topic-slides $ARGUMENTS

把主題「$ARGUMENTS」做成一份給不熟 AI 的大學生看的教學 HTML 簡報。依序執行節點 ⓪–⑩，**不得跳過節點，不得改變順序**。

## 總則

- **唯一的內容來源是 `wiki/`。** 不讀 `raw/`、不上網、不用自己的背景知識補內容。wiki 沒有的，就是缺口。
- **所有產出放在 `output/<slug>/`。** slug 是主題的英文 kebab-case（例如「Chunking 策略」→ `chunking-strategy`）。⑩ 之外不修改 `output/<slug>/` 以外的任何檔案；`wiki/`、`raw/`、`slides/` 一律不動。
- **狀態一律用 `scripts/wf_state.py` 記錄**，不要靠記憶計算輪數：
  - 每個節點每一輪結束都執行 `python3 scripts/wf_state.py log <slug> --node N --result R --detail "檢查結果" [--reason "退回原因"] [--change "修改內容"] [--pages "03,05"]`。
  - R：關卡用 `pass`／`fail`，其他節點用 `done`，停下來等使用者用 `wait`，中止用 `stop`。
  - `log` 的結束碼是 3 時，代表**全域停止條件**觸發（某個關卡退回累計超過 3 輪），立刻跳到「停止程序」。
- **每完成一個節點（含每一輪退回重做）就 commit 一次**：
  ```bash
  git add output/<slug>/ && git commit -m "topic-slides(<slug>): ③ 證據卡 — 6 張"
  ```
  - 只 add `output/<slug>/`（⑩ 另外加 `wiki/log.md`），不要 add 其他檔案。
  - 重做的輪次在訊息後加 `（第 N 輪）`；退回的輪次寫 `↩️ 退回：原因摘要`。
  - commit 失敗（例如沒有變更）就記在該輪的 `--detail`，繼續流程。
- **關卡（⓪②⑤⑥⑦⑨）退回累計超過 3 輪 → 停止。** 由 `wf_state.py log` 計算，第 4 次 `fail` 時回傳結束碼 3。
- **停止程序**：
  1. `python3 scripts/wf_state.py report <slug>`
  2. 在 report.md 的 `<!-- manual -->` 之後補上「補充說明」：卡在哪裡、每一輪的問題、可能的解法、需要使用者決定什麼。
  3. commit，然後把問題摘要回報給使用者，**結束本次執行**。
- **等待程序（② 缺口、⑤ 確認大綱）**：記一筆 `--result wait`、commit、回報使用者，**結束本次執行**。使用者回覆後，會再執行 `/topic-slides <主題>`（或直接回覆），從 state.json 記錄的節點接續。

## 開始：建立或接續

1. 決定 slug，執行 `python3 scripts/wf_state.py init <slug> --topic "$ARGUMENTS"`。
2. 輸出 `NEW` → 從 ⓪ 開始。
3. 輸出 `RESUME` → 讀 state.json 與 rounds.jsonl：
   - `status` 是 `stopped` → 不自動重跑。告訴使用者停止原因，問要怎麼處理。
   - `status` 是 `waiting` → 依使用者的回覆從該節點接續（見 ② 和 ⑤）。
   - `status` 是 `done` → 告訴使用者已完成，問是否要重新產生；要重做就先用 `set --status running --node 0`。

---

## ⓪ Wiki lint 關卡

1. 執行 `python3 tools/lint.py`，把完整輸出寫到 `output/<slug>/lint.md` 的「機械性檢查」段。
2. 呼叫 `reviewer` subagent（模式 A）：
   - 「允許讀取的檔案」= `wiki/` 下所有 `.md`（用 `ls`／`find` 列出完整路徑後逐一列給它）。
   - 把 AGENTS.md §9.3 的語意檢查清單原文貼進任務中。
   - 核對它回報的「實際讀取的檔案」；讀了清單外的檔案，這一輪無效，重新呼叫。
3. reviewer 的輸出寫到 lint.md 的「語意檢查」段。
4. 判定：
   - **通過** = lint.py 0 error，且 reviewer 沒有「嚴重」問題。warning 和「輕微」問題寫進 `--detail`，不阻擋。
   - **未通過** → `log --node 0 --result fail`，commit，然後**停止，不得進入 ①**。回報使用者要先修哪些 wiki 頁（修 wiki 是另一個任務，依 AGENTS.md 進行，不在這個 workflow 裡做）。使用者修好後重新執行會再跑一次 ⓪；超過 3 輪就觸發停止程序。
5. 通過 → `log --node 0 --result pass`，commit。

## ① 檢索

1. 讀 `wiki/index.md`，依主題挑出候選頁；逐頁讀候選頁，並順著「相關頁面」連結擴展一層。
2. 寫 `output/<slug>/sources.md`：
   ```markdown
   # 相關 wiki 頁：<主題>

   - wiki/concepts/chunking.md — 和主題的關係（一句話）
   - wiki/methods/naive-rag.md — …

   ## 看過但沒選的頁
   - wiki/xxx.md — 沒選的原因

   ## 缺口
   - 主題需要、但 wiki 中找不到的內容（沒有就寫「無」）
   ```
   - 相關頁一行一頁，路徑從 `wiki/` 開始。不能列 `wiki/index.md`、`wiki/log.md`。
   - 六段教學結構（為什麼需要→是什麼→怎麼運作→進階變體→怎麼評估→總結）都要想過，每段找不到材料就寫進「缺口」。
3. `log --node 1 --result done`，commit。

## ② 覆蓋率關卡

1. 執行 `python3 scripts/check_coverage.py output/<slug>`。
2. **結束碼 0** → `log --node 2 --result pass`，commit，進入 ③。
3. **結束碼 1** → `log --node 2 --result fail`（若結束碼為 3 → 停止程序），commit，然後**停下來等使用者**：
   - 列出腳本的錯誤，以及 sources.md 的「缺口」。
   - 建議可以補的來源：先查 `raw/` 的檔名清單（只看檔名，**不讀內容**），說明哪一篇 raw 的 ingest 可能補得到；不然就描述需要哪一類的新來源（例如「一篇比較 chunk 大小的實驗論文」）。**不得上網搜尋、不得自行 ingest。**
   - `log --node 2 --result wait`，commit，結束本次執行。
4. 使用者回覆後：
   - 「已補資料」→ 回到 ① 重新檢索。
   - 「縮小主題／改主題」→ 依指示改 sources.md 或回到 ①。
   - 「停止」→ 停止程序。

## ③ 證據卡

每個相關頁一張卡：`output/<slug>/cards/<目錄>--<檔名>.md`（例如 `wiki/concepts/chunking.md` → `cards/concepts--chunking.md`）。

```markdown
---
page: wiki/concepts/chunking.md
---
# 證據卡：Chunking

## 重點摘錄
> （逐字複製 wiki 頁的一行或一段連續文字，包含原本的 [raw.pdf, p.N] 引用）

## 數字
> （含數字的原句，逐字複製整句）

## ⚠️ 爭議
> （這頁和主題有關的 ⚠️ 標註，逐字複製；沒有就省略這一段）

## 可以用在
- 大綱的哪一段（這一段是你的說明，可以不是原文）
```

- 只有 `> ` 開頭的行算摘錄，**必須逐字出現在該 wiki 頁**。不可改寫、不可合併兩句、不可用「……」省略中間文字。要省略就拆成兩行摘錄。
- 每個要在簡報中使用的數字，都要有一行含該數字的原句。
- 寫完執行 `python3 scripts/check_coverage.py output/<slug> --cards`，修到結束碼 0。
- `log --node 3 --result done --detail "N 張卡"`，commit。

## ④ 大綱

寫 `output/<slug>/outline.md`：

```markdown
# 大綱：<主題>（共 N 頁，約 M 分鐘）

## 為什麼需要
### 01｜投影片標題
- 要講的重點（一兩句）
- 證據卡：cards/concepts--chunking.md、cards/…
- 圖：（要不要放流程圖；大多數頁不需要）

## 是什麼
### 02｜…
…（依序：為什麼需要 → 是什麼 → 怎麼運作 → 進階變體 → 怎麼評估 → 總結）
```

- 共 **8–15 頁**，六段都要有，每段至少 1 頁。
- 每頁都要指明用哪幾張證據卡；用不到卡的內容不能放進大綱。
- 多用 `wiki/analogies.md` 的比喻：比喻頁要列在 sources.md 並做成卡片，才能使用。
- `log --node 4 --result done --detail "N 頁"`，commit。

## ⑤ 等使用者確認大綱

1. 把大綱的摘要（每頁標題、用到的卡）給使用者看，請使用者回覆「確認」或「退回：意見」。
2. `log --node 5 --result wait`，commit，**結束本次執行**。
3. 使用者回覆後：
   - **「確認」** → `log --node 5 --result pass`，commit，進入 ⑥。
   - **「退回」** → `log --node 5 --result fail --reason "使用者意見"`（結束碼 3 → 停止程序）：
     - 意見是結構、順序、刪減、強調 → 修改 outline.md（④），`log --node 4 --result done --change "改了什麼"`，commit，回到 ⑤。
     - 意見是缺內容 → 回到 ① 補檢索，再依序經過 ②③④⑤。

## ⑥ 逐頁稿

每頁一個檔案：`output/<slug>/drafts/NN-英文-slug.md`（從 01 連號）。**格式必須完全符合下面的規格**，因為 check_sources.py 和 render_deck.py 都依這個格式解析：

```markdown
---
slide: 3
section: 怎麼運作
title: 先切塊，再轉成向量
---
## 投影片
- 文件會先切成小段，叫做 **chunk**〔wiki/concepts/chunking.md〕
- 每個 chunk 再用 embedding model 轉成向量〔wiki/methods/naive-rag.md〕

## 圖
文件 → chunk → 向量 → 資料庫〔wiki/methods/naive-rag.md〕

## 講稿
我們先看資料是怎麼存進去的〔wiki/methods/naive-rag.md〕。系統會把文件切成一小段一小段〔wiki/concepts/chunking.md〕。
```

規格：
- `section` 只能是：為什麼需要／是什麼／怎麼運作／進階變體／怎麼評估／總結，而且整份稿件要照這個順序、六段都有。
- 引用標記是全形括號 `〔wiki/路徑.md〕`，一個括號放一頁；要引用兩頁就寫兩個括號。
- **投影片每個項目、流程圖、講稿每一句都要有引用**；引用要放在句號**之前**。標題不放引用。
- 只能引用 sources.md 列出的頁；內容必須來自對應的證據卡。
- **每個數字都必須出現在同一行（同一句）所引用的 wiki 頁中。** 數字用阿拉伯數字，寫法和 wiki 頁一致（例如 wiki 寫 `49%`，稿件就寫 `49%`）。
- **講稿 2–4 句**，口語、可以直接照著念。
- `## 圖` 可省略；要放就只放一行，2–5 個節點用 `→` 分隔，每個節點 ≤ 12 字。整份簡報只在關鍵處放 1–3 張圖。
- 份量：投影片項目建議 3–5 條、每條 ≤ 40 字（⑨ 會實際檢查溢出）。可以用 `**粗體**` 強調專有名詞。

完成後執行 `python3 scripts/check_sources.py output/<slug>`：
- **結束碼 0** → `log --node 6 --result pass --detail "N 頁"`，commit，進入 ⑦。
- **結束碼 1** → `log --node 6 --result fail --detail "腳本錯誤摘要" --pages "出錯的頁"`（結束碼 3 → 停止程序），只修改出錯的頁，`--change` 記錄改了什麼，commit，重跑腳本。

**從 ⑦ 或 ⑨ 退回時**：只重寫被退回的頁（其他頁的檔案不得變動），重跑 check_sources.py，`log --node 6 ... --pages "03,07" --change "改了什麼"`，commit，再回到 ⑦（只審被重寫的頁）。

## ⑦ 忠實度審查

1. 呼叫 `reviewer` subagent（模式 B）。「允許讀取的檔案」**只有**：
   - `output/<slug>/drafts/` 下要審的稿件（第一輪是全部；退回後只給重寫的頁）
   - 這些稿件 `〔〕` 中引用到的 wiki 頁（用 `grep -oh '〔wiki/[^〕]*〕' drafts/*.md | sort -u` 列出）
   - `output/<slug>/sources.md` 與 `output/<slug>/cards/` 下的所有卡片（用來檢查漏掉的重要來源）
   - 在任務中逐一列出完整路徑，並說明是模式 B。
2. 核對 reviewer 的「實際讀取的檔案」；讀了清單外的檔案，這一輪無效，重新呼叫。
3. 把 reviewer 的完整輸出存到 `output/<slug>/review/round-N.md`。
4. 判定：
   - 輸出 `PASS`，或只有「輕微」問題 → `log --node 7 --result pass`（輕微問題寫進 `--detail`），commit，進入 ⑧。
   - 有「嚴重」問題，或「漏來源」被判為重要 → `log --node 7 --result fail --reason "問題摘要" --pages "出錯的頁"`（結束碼 3 → 停止程序），commit，**只把出錯的那幾頁**退回 ⑥ 重寫。

## ⑧ 渲染

1. 執行 `python3 scripts/render_deck.py output/<slug>`，產生 `output/<slug>/deck.html`。
2. **不得手動編輯 deck.html，也不得更改任何文字。** 渲染的結果不對，要改的是稿件（回到 ⑥）或 render_deck.py（改腳本要先問使用者）。
3. `log --node 8 --result done`，commit。

## ⑨ 渲染檢查

1. 執行 `python3 scripts/check_render.py output/<slug>`（會把截圖存到 `screenshots/`）。
2. **結束碼 0** → `log --node 9 --result pass`，commit，進入 ⑩。
3. **結束碼 1**：
   - 溢出 → `log --node 9 --result fail --reason "第 N 頁溢出：…" --pages "N"`（結束碼 3 → 停止程序），commit，把溢出的頁退回 ⑥ **縮短**（刪掉次要的項目、拆短句子；不能換掉事實），再依序經過 ⑥ 檢查 → ⑦（只審該頁）→ ⑧ → ⑨。
   - 文字不一致、缺 notes／refs、外部資源 → 這是渲染腳本的問題，不是稿件的問題：停止程序，在 report.md 說明。
4. 結束碼 2（環境問題，例如沒裝 Playwright）→ 停止程序，告訴使用者要裝什麼。

## ⑩ 交件

1. `python3 scripts/wf_state.py set <slug> --status done --node 10`。
2. `python3 scripts/wf_state.py report <slug>` 產生 report.md，然後在 `<!-- manual -->` 之後補上「補充說明」：
   - 每次退回的根本原因與教訓
   - reviewer 提出、但判為輕微而沒有修的問題
   - sources.md 的「缺口」（簡報沒涵蓋到的部分）
3. 在 `wiki/log.md` 末尾追加一筆（AGENTS.md §9.4）：
   ```markdown
   ## [YYYY-MM-DD] slides | topic-slides：<主題>
   - 產出：output/<slug>/deck.html（N 頁）
   - 使用的 wiki 頁：N 頁（見 output/<slug>/sources.md）
   - 退回：⓪ x、② x、⑤ x、⑥ x、⑦ x、⑨ x 輪
   ```
4. `log --node 10 --result done`，再跑一次 `report`（讓這筆紀錄也進報告），然後 `git add output/<slug>/ wiki/log.md` 並 commit。
5. 回報使用者：deck.html 的路徑、頁數、各關卡退回輪數、還沒解決的問題。
