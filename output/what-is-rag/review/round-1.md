# ⑦ 忠實度審查 — 第 1 輪（reviewer 模式 B）

- 審查範圍：drafts/ 全部 13 頁；允許讀取：13 頁稿件、引用的 17 個 wiki 頁、sources.md、17 張證據卡
- 核對「實際讀取的檔案」：全部在清單內（有效）
- 判定：嚴重 2（皆在 13）、輕微 11 → 退回 13

## 問題清單

### drafts/13-not-a-silver-bullet.md
1. [嚴重｜講反／無出處] 講稿「這種反而更差的情況，只出現在 20 和 30 份文件設定的最差位置」：closed-book-vs-open-book.md 第 51 行沒有「只」的意思；同頁第 54–63 行還有 05 Table 2 的反例（ChatGPT PubHealth 70.1 → 54.7、TriviaQA 74.3 → 65.7）；overview、naive-rag 的 ⚠️ 都同時列 04 和 05。「只」把「檢索不一定有幫助」的 ⚠️ 縮小成位置效應的特例。建議拿掉「只」、補上 05 的證據。
2. [嚴重｜漏掉 ⚠️，把爭議講成定論] 投影片「資料不是越多越好：取 50 份比 20 份，只多進步約 1%–1.5%」、講稿「但資料不是越多越好」：retriever.md 第 41–42 行、sources/01 第 103–104 行的 ⚠️ 指出「要放多少份文件」各來源說法不一致（01：越多越好；03：20 個最好；04：50 vs 20 只多 1%–1.5%）。稿件把 04 的特定結果當成一般結論；講稿這句掛在 lost-in-the-middle.md 底下，但該頁沒有這句結論，引用錯頁。建議加上「04 的實驗」限定並註明各來源看法不一，改引 overview 或 retriever。（overview.md 第 81 行本身也沒附這個 ⚠️，屬 wiki 層問題，建議交給模式 A。）
3. [輕微｜用詞] 「只要換掉外部資料，就能更新模型的知識」→ 建議「更新 RAG 的知識，不用重新訓練模型」。

### drafts/01-llm-makes-mistakes.md
1. [輕微｜初學者] BART 第一次出現沒有說明，hallucination.md 稱它為「純參數模型」而不是 LLM，聽眾容易把它當成今天的 LLM。

### drafts/02-limits-of-memorizing.md
1. [輕微｜可能無出處] 「模型的知識，大部分是在訓練時背進參數裡的」：「大部分」是加上去的。

### drafts/04-open-book-exam.md
1. [輕微｜初學者] 「44.5 分」「34.5 分」沒說明是 NQ 的 Exact Match。

### drafts/07-one-question-journey.md
1. [輕微｜和前一頁不一致] 原始 RAG「每份文件分別寫再合併」和第 6 頁 Naive RAG「組成一個 prompt」不同，講稿沒有交代。

### drafts/08-chunk-and-embed.md
1. [輕微｜拿掉情境] 「就很難被找到」少了「問『ACME Corp 2023 年 Q2 的營收成長』時」。

### drafts/10-beyond-naive.md
1. [輕微｜講稿和投影片不一致] 講稿「逐步改進」沒有念到投影片上的 ⚠️「不完全等於時間先後」。

### drafts/11-self-rag-and-graphrag.md
1. [輕微｜少了比較對象，漏 ⚠️] 72%–83% 沒說是「對一般 RAG、在全局問題上、由 LLM 評審判定」；rag-evaluation.md 有 LLM 評審可靠度的 ⚠️（但 06 用 GPT-4 並交叉驗證過）。

### drafts/12-evaluate-separately.md
1. [輕微｜擴大範圍] 「RAGAS 這類工具不需要標準答案、拆成小步驟」把 RAGAS 的特點推到其他工具上。
2. [輕微｜漏來源] 講稿沒念到投影片上的 ⚠️，也沒提「LLM 當評審可靠嗎」的 ⚠️ 與「拆成小步驟比較準」的對照。

### drafts/03、05、06、09
沒有發現問題（68%、4%、82 位、626M、11B、21M、100-word 等數字都能在引用的 wiki 頁找到）。

## 統計
- 嚴重：2；輕微：11
- 需要退回的頁面：drafts/13-not-a-silver-bullet.md
