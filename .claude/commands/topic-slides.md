---
description: 主題 → 教學 HTML 簡報（只用 wiki/ 內容的 graph workflow v2，含關卡、相關頁語意檢查、審查、渲染檢查）
argument-hint: <主題>
---

# /topic-slides $ARGUMENTS

把主題「$ARGUMENTS」做成一份給不熟 AI 的大學生看的教學 HTML 簡報。依序執行節點 ⓪ ① ② ②b ③ ④ ⑤ ⑥ ⑦ ⑧ ⑨ ⑩，**不得跳過節點，不得改變順序**。

本檔是 **workflow v2**，流程圖見 `README.md`「Workflow v2」。和 v1 的差別：⓪ 只做機械檢查；wiki 的語意檢查移到 ②b，只看和主題相關的頁面；嚴重度規則寫死；問題登記在 `issues.md`。

## 總則

- **簡報內容唯一的來源是 `wiki/`。** 不上網、不用自己的背景知識補內容。wiki 沒有的，就是缺口。
  - 例外 1：②b 的 reviewer 可以讀相關頁對應的 `raw-text/`，用來核對 wiki 頁是否忠於原文。`raw/` 的 PDF 一律不讀。
  - 例外 2：②b 發現嚴重問題時，可以修改**和主題相關的 wiki 頁**，但必須依 AGENTS.md 的規則（引用、⚠️ 格式等），並記到 `wiki/log.md`、`issues.md`。
- **所有產出放在 `output/<slug>/`。** slug 是主題的英文 kebab-case（例如「Chunking 策略」→ `chunking-strategy`）。除了 ②b 的修正和 ⑩ 的 `wiki/log.md`，不修改 `output/<slug>/` 以外的任何檔案；`raw/`、`raw-text/`、`slides/` 一律不動。
- **嚴重度規則（v2，寫死，所有 reviewer 呼叫都要貼進任務中）**：
  - **嚴重**只有兩種：
    1. 數字或結論和引用的 raw 原文不符，或講反了；
    2. 和 wiki 另一頁直接矛盾，而且沒有 ⚠️ 標註。
  - 無法確定的一律列為**輕微**。
  - 已登記在 `issues.md` 的問題，嚴重度不得改變；reviewer 只回報新問題，以及舊問題是否仍然存在。
- **問題追蹤**：`output/<slug>/issues.md` 給每個 wiki 問題固定編號、類別、嚴重度和狀態（待修／已修／不修並寫理由）。新問題接續編號，不重新編號；狀態改變時直接改該列。
- **狀態一律用 `scripts/wf_state.py` 記錄**，不要靠記憶計算輪數：
  - 每個節點每一輪結束都執行 `python3 scripts/wf_state.py log <slug> --node N --result R --detail "檢查結果" [--reason "退回原因"] [--change "修改內容"] [--pages "03,05"]`。
  - 節點編號 N：`0` `1` `2` `2b` `3` `4` `5` `6` `7` `8` `9` `10`。
  - R：關卡用 `pass`／`fail`，其他節點用 `done`，停下來等使用者用 `wait`，中止用 `stop`。
  - `log` 的結束碼是 3 時，代表**停止條件**觸發（某個關卡退回超過上限），立刻跳到「停止程序」。
- **每完成一個節點（含每一輪退回重做）就 commit 一次**：
  ```bash
  git add output/<slug>/ && git commit -m "topic-slides(<slug>): ③ 證據卡 — 6 張"
  ```
  - 只 add `output/<slug>/`；②b 的修正另外加上改到的 `wiki/` 檔案，⑩ 另外加 `wiki/log.md`。不要 add 其他檔案。
  - 重做的輪次在訊息後加 `（第 N 輪）`；退回的輪次寫 `↩️ 退回：原因摘要`。
  - commit 失敗（例如沒有變更）就記在該輪的 `--detail`，繼續流程。
- **關卡與退回上限**（由 `wf_state.py log` 計算，超過上限回傳結束碼 3）：

  | 關卡 | 上限 | 退回到 |
  |---|---|---|
  | ⓪ lint | 3 | 停下來，依 Wiki 維護流程修正後重跑 ⓪ |
  | ② 覆蓋率 | 3 | 停下來等使用者補來源，補完後重跑 ⓪ |
  | ②b 相關頁語意檢查 | 2 | 只修相關 wiki 頁，再跑 ②b |
  | ⑤ 大綱確認 | 3 | 結構問題 → ④；缺主題 → ① |
  | ⑥ 逐頁稿（check_sources 小 loop） | 2 | 只修出錯的頁，重跑 check_sources |
  | ⑦ 忠實度審查 | 3 | 只把出錯的頁退回 ⑥ |
  | ⑨ 渲染檢查 | 3 | 溢出的頁退回 ⑥ 縮短 |

- **停止程序**：
  1. `python3 scripts/wf_state.py report <slug>`
  2. 在 report.md 的 `<!-- manual -->` 之後補上「補充說明」：卡在哪裡、每一輪的問題、可能的解法、需要使用者決定什麼。
  3. commit，然後把問題摘要回報給使用者，**結束本次執行**。
- **等待程序（⓪ lint 失敗、② 缺口、⑤ 確認大綱）**：記一筆 `--result wait`、commit、回報使用者，**結束本次執行**。使用者回覆後，會再執行 `/topic-slides <主題>`（或直接回覆），從 state.json 記錄的節點接續。
- **report.md 的開頭區塊**：`<!-- preamble -->` 和 `<!-- /preamble -->` 之間的內容（例如前一次執行的摘要），`wf_state.py report` 重新產生時會保留，不要刪除。

## 開始：建立或接續

1. 決定 slug，執行 `python3 scripts/wf_state.py init <slug> --topic "$ARGUMENTS"`。
2. 輸出 `NEW` → 從 ⓪ 開始。
3. 輸出 `RESUME` → 讀 state.json 與 rounds.jsonl：
   - `status` 是 `stopped` → 不自動重跑。告訴使用者停止原因，問要怎麼處理。
   - `status` 是 `waiting` → 依使用者的回覆從該節點接續（見 ⓪、② 和 ⑤）。
   - `status` 是 `done` → 告訴使用者已完成，問是否要重新產生；要重做就先用 `set --status running --node 0`。

---

## ⓪ lint 關卡（只做機械檢查）

1. 執行 `python3 tools/lint.py`，把完整輸出寫到 `output/<slug>/lint.md`。**不呼叫 reviewer**；wiki 的語意檢查在 ②b 進行，而且只看相關頁。
2. 判定：
   - **通過** = 0 error。warning 寫進 `--detail`，不阻擋。→ `log --node 0 --result pass`，commit，進入 ①。
   - **未通過** → `log --node 0 --result fail`（結束碼 3 → 停止程序），commit，然後**停下來，不得進入 ①**：
     - 回報 lint.py 的錯誤，以及要修哪些 wiki 頁。修正依 AGENTS.md §9.3 的 Wiki 維護流程進行，不在這個 workflow 裡做。
     - `log --node 0 --result wait`，commit，結束本次執行。使用者修好後重新執行，會再跑一次 ⓪。

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
   - 相關頁一行一頁，路徑從 `wiki/` 開始，**全部放在第一個 `## ` 標題之前**（腳本只讀到第一個 `## ` 為止，之後的段落不算相關頁）。不能列 `wiki/index.md`、`wiki/log.md`。
   - 六段教學結構（為什麼需要→是什麼→怎麼運作→進階變體→怎麼評估→總結）都要想過，每段找不到材料就寫進「缺口」。
3. `log --node 1 --result done`，commit。

## ② 覆蓋率關卡

1. 執行 `python3 scripts/check_coverage.py output/<slug>`。
2. **結束碼 0** → `log --node 2 --result pass`，commit，進入 ②b。
3. **結束碼 1** → `log --node 2 --result fail`（若結束碼為 3 → 停止程序），commit，然後**停下來等使用者**：
   - 列出腳本的錯誤，以及 sources.md 的「缺口」。
   - 建議可以補的來源：先查 `raw/` 的檔名清單（只看檔名，**不讀內容**），說明哪一篇 raw 的 ingest 可能補得到；不然就描述需要哪一類的新來源（例如「一篇比較 chunk 大小的實驗論文」）。**不得上網搜尋、不得自行 ingest。**
   - `log --node 2 --result wait`，commit，結束本次執行。
4. 使用者回覆後：
   - 「已補資料」（新來源已放進 `raw/`、已產生 `raw-text/`、已依 AGENTS.md ingest）→ 回到 **⓪** 重跑。
   - 「縮小主題／改主題」→ 依指示改 sources.md 或回到 ①。
   - 「停止」→ 停止程序。

## ②b 相關頁語意檢查（最多 2 輪）

只檢查 sources.md 列出的頁面，不檢查整個 wiki。

1. **準備 issues.md**：`output/<slug>/issues.md` 不存在時，建立一份空的總表（欄位：編號、類別、問題、頁面、嚴重度、出現輪次、狀態）。已經存在就沿用，不要重新編號。
2. **列出允許讀取的檔案**，每個都寫完整路徑：
   - sources.md 列出的每一個 wiki 頁；
   - 這些頁面 frontmatter `sources` 中每個 raw 檔對應的 `raw-text/<同檔名>.md`（例如 `05-asai2023-self-rag.pdf` → `raw-text/05-asai2023-self-rag.md`）。可以用：
     ```bash
     grep -h '^sources:' $(sed '/^## /q' output/<slug>/sources.md | grep -oE 'wiki/[^ )]+\.md' | sort -u) \
       | grep -oE '[0-9]{2}-[a-z0-9-]+\.pdf' | sort -u | sed 's#^#raw-text/#; s#\.pdf$#.md#'
     ```
   - `output/<slug>/issues.md`。
3. 呼叫 `reviewer` subagent（**模式 A**），任務中要包含：
   - 允許讀取的檔案清單；
   - 「總則」中的**嚴重度規則**原文；
   - 檢查重點：數字和結論是否忠於 `raw-text/` 的原文、有沒有拿掉限定條件、這些頁之間有沒有未標註的矛盾、⚠️ 是否同步、初學者讀不讀得懂；
   - 要求它對 issues.md 中「待修」的每一條回報「仍然存在／已解決」，新問題另外列出，而且不得改變已登記問題的嚴重度。
4. 核對 reviewer 的「實際讀取的檔案」；讀了清單外的檔案，這一輪無效，重新呼叫。
5. 把 reviewer 的完整輸出存到 `output/<slug>/review/semantic-round-N.md`。
6. **登記到 issues.md**：新問題接續編號、照 reviewer 給的嚴重度登記為「待修」；舊問題依回報更新狀態。嚴重度以 issues.md 為準；reviewer 改了已登記問題的嚴重度時，以 issues.md 為準，並記在 `--detail`。
7. 判定：
   - **沒有「待修」的嚴重問題** → `log --node 2b --result pass --detail "新問題：嚴重 0、輕微 M；輕微問題見 issues.md"`，commit，進入 ③。輕微問題不阻擋；決定不修的，在 issues.md 寫理由。
   - **有「待修」的嚴重問題** → `log --node 2b --result fail --reason "問題編號與摘要" --pages "wiki 頁"`（結束碼 3 → 停止程序：「②b 超過 2 輪，交給使用者決定」），commit，然後修正：
     - **只修 sources.md 中的相關 wiki 頁**，依 AGENTS.md 的規則；同一類的問題一次修完（例如同主題的 ⚠️ 全部同步），不要只修單一條目。
     - 需要核對原文時，讀對應的 `raw-text/`；引用仍然寫原始 PDF 的檔名和頁碼。
     - 跑 `python3 tools/lint.py`，必須 0 error。
     - 更新 issues.md 的狀態（已修／不修並寫理由）；在 `wiki/log.md` 追加一筆 `lint` 紀錄；有需要就更新 `wiki/index.md`。
     - `git add output/<slug>/ <改到的 wiki 檔案>`，commit（訊息寫 `topic-slides(<slug>): ②b 修正 wiki — 問題編號`），然後回到 ②b 步驟 2 重新檢查。

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
     - 意見是缺內容 → 回到 ① 補檢索，再依序經過 ② ②b ③ ④ ⑤。

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
- **結束碼 1** → `log --node 6 --result fail --detail "腳本錯誤摘要" --pages "出錯的頁"`（結束碼 3 → 停止程序：小 loop 最多 2 輪），只修改出錯的頁，`--change` 記錄改了什麼，commit，重跑腳本。

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
   - reviewer 提出、但判為輕微而沒有修的問題（列出 issues.md 的編號）
   - sources.md 的「缺口」（簡報沒涵蓋到的部分）
3. 在 `wiki/log.md` 末尾追加一筆（AGENTS.md §9.4）：
   ```markdown
   ## [YYYY-MM-DD] slides | topic-slides：<主題>
   - 產出：output/<slug>/deck.html（N 頁）
   - 使用的 wiki 頁：N 頁（見 output/<slug>/sources.md）
   - 退回：⓪ x、② x、②b x、⑤ x、⑥ x、⑦ x、⑨ x 輪
   - issues.md：新登記 x 條（嚴重 x、輕微 x），已修 x 條
   ```
4. `log --node 10 --result done`，再跑一次 `report`（讓這筆紀錄也進報告），然後 `git add output/<slug>/ wiki/log.md` 並 commit。
5. 回報使用者：deck.html 的路徑、頁數、各關卡退回輪數、還沒解決的問題。
