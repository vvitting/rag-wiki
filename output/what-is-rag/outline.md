# 大綱：RAG 是什麼？（共 13 頁，約 15 分鐘）

> 讀者：不熟 AI 的大學生。每頁約 1 分鐘。比喻來自 `cards/analogies.md`。
> **投影片放白話結論，模型名稱和精確分數放講稿**（⑤ 第 1 次退回的意見）。
> 依 issues.md：不使用 V2-05（PopQA 消融數字）、V2-09（35%–49%）、V2-26（2%）、V2-32／V2-33（lost-in-the-middle 第 17、42 行）；不用 MIPS 這個詞（V2-24）；Self-RAG 不使用「勝過更大模型」的結論（E03 ⚠️）。
>
> **相較於第 1 版的修改**（⑤ 第 1 次退回）：新增 07「走一遍：一個問題的旅程」；04 投影片改成白話比較，模型與分數移到講稿，保留 open-domain QA 限定；05 只留一組數字（68% vs 4%）；12 不放 0.95，重點放在分開評估；13 寫明 53.8% < 56.1% 的條件，並帶出 Lost in the Middle。

## 為什麼需要

### 01｜LLM 很強，但會一本正經地講錯
- LLM 有三個主要問題：hallucination、知識過時、無法追溯出處。用 BART 把「中耳」講錯的例子說明什麼是 hallucination。
- 證據卡：cards/overview.md、cards/concepts--hallucination.md
- 圖：無

### 02｜只靠「背」的知識，有兩個天生限制
- 知識存在參數裡：不知道訓練之後發生的事、記不住冷門知識；很難更新，也說不出出處。
- 證據卡：cards/overview.md、cards/concepts--parametric-vs-non-parametric-memory.md
- 圖：無

## 是什麼

### 03｜RAG：先查資料，再回答
- 定義：先從外部知識庫找出相關資料，再根據資料回答；結合「背的知識」和「翻的資料」兩種記憶；名稱來自 2020 年 Lewis et al. 的論文。
- 證據卡：cards/overview.md、cards/concepts--parametric-vs-non-parametric-memory.md
- 圖：無

### 04｜比喻：從閉書考變成開書考
- 投影片：閉書考 vs 開書考的比喻（和它的極限）；白話比較：**在 open-domain QA 上**，參數少很多的開書考模型，可以勝過參數多很多的閉書考模型。
- 講稿：模型名稱與分數（RAG-Sequence 626M 參數、NQ 44.5；T5-11B 11B 參數、34.5）。
- 證據卡：cards/analogies.md、cards/comparisons--closed-book-vs-open-book.md
- 圖：無

### 05｜知識過時了？換一本新版課本就好
- 換 index 就能更新知識。只用一組數字：換成 2018 年版的 index，答對 2018 年的世界領袖 68%；用 2016 年版的 index 問 2018 年的領袖，只剩 4%。
- 證據卡：cards/analogies.md、cards/concepts--parametric-vs-non-parametric-memory.md
- 圖：無

## 怎麼運作

### 06｜三個步驟：建索引、找資料、寫答案
- Indexing → Retrieval → Generation；用「圖書館員＋作家」比喻 retriever 和 generator。
- 證據卡：cards/overview.md、cards/methods--naive-rag.md、cards/analogies.md
- 圖：要。文件 → 切塊與向量 → 找出相關段落 → LLM 寫答案

### 07｜走一遍：一個問題的旅程（新增）
- 跟著原始 RAG 論文 Fig.1 的例子走一遍：問題「Define "middle ear"」→ 轉成向量 → 從 Wikipedia 的 index 找出最相關的幾份文件 → 依每份文件寫答案再合併 → 輸出「中耳包含鼓室和三塊聽小骨」。對照：不查資料的 BART 把中耳講錯。
- 講稿：每一步對應 06 的哪一個步驟。
- 證據卡：cards/sources--01-lewis2020-rag.md、cards/concepts--hallucination.md
- 圖：要。問題 → 轉成向量 → 找出相關文件 → 寫出答案

### 08｜先切塊，再把意思轉成向量
- 為什麼要切塊（context 有限制）、通常切多大；embedding 把文字的意思變成一串數字；切塊的副作用是 chunk 失去上下文。
- 證據卡：cards/concepts--chunking.md、cards/concepts--embedding.md
- 圖：無

### 09｜找資料：用意思找，也用字找
- Retriever 的角色；embedding 擅長語意但會漏掉「TS-999」這種精確字串，BM25 補上；兩者一起用比較好（館員的比喻）。
- 證據卡：cards/concepts--retriever.md、cards/concepts--embedding.md、cards/analogies.md
- 圖：無

## 進階變體

### 10｜基本版不夠用：Naive → Advanced → Modular
- Naive RAG 的缺點（找不準、寫錯、答不了全局問題）→ 綜述的三種典範；⚠️「階段」是分類方式，不完全等於時間先後。
- 證據卡：cards/methods--naive-rag.md、cards/comparisons--rag-paradigms.md、cards/overview.md
- 圖：無

### 11｜兩個例子：Self-RAG 與 GraphRAG
- Self-RAG：同一個問題「美國各州的名字怎麼來的？」，一般 RAG 寫出和文件不一致的答案；Self-RAG 先判斷要不要查、為每段打分數、挑出有根據的那段（寫作文就不用查）。GraphRAG：用「找一句話 vs 寫讀書報告」比喻全局問題；代價是建 index 很貴。
- 講稿：GraphRAG 等全局方法在 Podcast 資料上的全面性勝率 72%–83%。
- 證據卡：cards/sources--05-asai2023-self-rag.md、cards/methods--self-rag.md、cards/methods--graphrag.md、cards/analogies.md、cards/concepts--retriever.md
- 圖：無

## 怎麼評估

### 12｜評估要分開看：找得好不好、寫得好不好
- 投影片重點：「找資料」（retrieval quality）和「寫答案」（generation quality）分開評估；三個品質分數各看一件事（用「改開書考的考卷」比喻）。不放 0.95。
- 講稿：RAGAS 不需要標準答案、拆成小步驟讓 LLM 評分；faithfulness 高也不代表答案對。
- 證據卡：cards/concepts--rag-evaluation.md、cards/concepts--ragas.md、cards/analogies.md
- 圖：無

## 總結

### 13｜重點回顧：RAG 有用，但不是萬靈丹
- RAG = 先查再寫，換 index 就能更新知識。
- 資料不是越多越好，位置也有影響（Lost in the Middle）：**GPT-3.5-Turbo、20 份文件、答案放在中間（第 10 份）時，準確率 53.8%，低於完全不給文件的 56.1%**；這種「反而更差」只出現在 20、30 份文件設定的最差位置。答案在開頭時是 75.8%。取 50 份和取 20 份相比，只多進步約 1%–1.5%。
- 外部資料本身也可能有錯；用了 RAG 仍可能講錯。
- 證據卡：cards/overview.md、cards/comparisons--closed-book-vs-open-book.md、cards/concepts--lost-in-the-middle.md、cards/concepts--hallucination.md、cards/analogies.md
- 圖：無
