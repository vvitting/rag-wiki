# 大綱：RAG 是什麼？（共 12 頁，約 15 分鐘）

> 讀者：不熟 AI 的大學生。每頁約 1–1.5 分鐘。比喻來自 `cards/analogies.md`。
> 依 issues.md：不使用 V2-05（PopQA 消融數字）、V2-09（35%–49%）；RAGAS 的一致度只引用帶「WikiEval」限定的句子（V2-01）；Self-RAG 不使用「勝過更大模型」的結論（E03 ⚠️）。

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
- 閉書考 vs 開書考的比喻（和它的極限）；NQ 上 RAG-Sequence（626M 參數）44.5 勝過 T5-11B（11B 參數）34.5。
- 證據卡：cards/analogies.md、cards/comparisons--closed-book-vs-open-book.md
- 圖：無

### 05｜知識過時了？換一本新版課本就好
- 換 index 就能更新知識：2016／2018 年的 index 各自答對 70%／68%，年份對不上時只剩 12%／4%。
- 證據卡：cards/analogies.md、cards/concepts--parametric-vs-non-parametric-memory.md
- 圖：無

## 怎麼運作

### 06｜三個步驟：建索引、找資料、寫答案
- Indexing → Retrieval → Generation；用「圖書館員＋作家」比喻 retriever 和 generator。
- 證據卡：cards/overview.md、cards/methods--naive-rag.md、cards/analogies.md
- 圖：要。文件 → 切塊與向量 → 找出相關段落 → LLM 寫答案

### 07｜先切塊，再把意思轉成向量
- 為什麼要切塊（context 有限制）、通常切多大；embedding 把文字的意思變成一串數字；切塊的副作用是 chunk 失去上下文。
- 證據卡：cards/concepts--chunking.md、cards/concepts--embedding.md
- 圖：無

### 08｜找資料：用意思找，也用字找
- Retriever 的角色；embedding 擅長語意但會漏掉「TS-999」這種精確字串，BM25 補上；兩者一起用比較好（館員的比喻）。
- 證據卡：cards/concepts--retriever.md、cards/concepts--embedding.md、cards/analogies.md
- 圖：無

## 進階變體

### 09｜基本版不夠用：Naive → Advanced → Modular
- Naive RAG 的缺點（找不準、寫錯、答不了全局問題）→ 綜述的三種典範；⚠️「階段」是分類方式，不完全等於時間先後。
- 證據卡：cards/methods--naive-rag.md、cards/comparisons--rag-paradigms.md、cards/overview.md
- 圖：無

### 10｜兩個例子：Self-RAG 與 GraphRAG
- Self-RAG：自己決定要不要查、為自己打分數（寫作文就不用查）。GraphRAG：用「找一句話 vs 寫讀書報告」比喻全局問題；全局方法在 Podcast 上的全面性勝率 72%–83%；代價是建 index 很貴。
- 證據卡：cards/methods--self-rag.md、cards/methods--graphrag.md、cards/analogies.md、cards/concepts--retriever.md
- 圖：無

## 怎麼評估

### 11｜評估要分開看：找得好不好、寫得好不好
- 兩個目標、三個品質分數（用「改開書考的考卷」比喻）；RAGAS 不需要標準答案，faithfulness 在 WikiEval 上和人類判斷的一致度 0.95；但 faithfulness 高不代表答案對。
- 證據卡：cards/concepts--rag-evaluation.md、cards/concepts--ragas.md、cards/analogies.md、cards/concepts--hallucination.md
- 圖：無

## 總結

### 12｜重點回顧：RAG 有用，但不是萬靈丹
- RAG = 先查再寫，換 index 就能更新知識；但檢索不一定有幫助（答案放在中間時 53.8% 低於不給文件的 56.1%）、外部資料本身也可能有錯、用了 RAG 仍可能講錯。
- 證據卡：cards/overview.md、cards/comparisons--closed-book-vs-open-book.md、cards/concepts--hallucination.md、cards/methods--naive-rag.md
- 圖：無
