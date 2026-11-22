# 相關 wiki 頁：RAG 是什麼？

- wiki/overview.md — 全貌頁，結構和簡報的六段完全對齊（為什麼需要 → 總結），是整份簡報的骨架
- wiki/concepts/hallucination.md — 為什麼需要：LLM 會講錯卻像真的；RAG 想減少它，但有 ⚠️ 不一定有效
- wiki/concepts/parametric-vs-non-parametric-memory.md — 是什麼：RAG 結合「背的知識」和「翻的資料」；換 index 就能更新知識（70%／68% vs 12%／4%）
- wiki/comparisons/closed-book-vs-open-book.md — 是什麼＋總結：閉書考 vs 開書考的成績；開書考不一定比較好（56.1% vs 53.8%）
- wiki/analogies.md — 全段：開書考、圖書館員＋作家、換新版課本、讀長文只記頭尾、改開書考的考卷等比喻
- wiki/methods/naive-rag.md — 怎麼運作：indexing → retrieval → generation 三步；缺點；⚠️ 不一定勝過不檢索
- wiki/concepts/chunking.md — 怎麼運作：為什麼要把文件切塊、切多大、切塊會失去上下文
- wiki/concepts/embedding.md — 怎麼運作：把文字的意思轉成向量，用相似度找資料
- wiki/concepts/retriever.md — 怎麼運作：retriever 怎麼找資料；embedding vs BM25；只找得到局部
- wiki/comparisons/rag-paradigms.md — 進階變體：Naive → Advanced → Modular 三種典範的對照
- wiki/methods/self-rag.md — 進階變體：讓模型自己決定要不要查、為自己打分數；⚠️ 原文結論與 Table 2 不一致
- wiki/methods/graphrag.md — 進階變體：回答「整批資料的主題是什麼」這類全局問題
- wiki/concepts/rag-evaluation.md — 怎麼評估：找得好不好 vs 寫得好不好、三個品質分數、LLM 當評審的可靠度
- wiki/concepts/ragas.md — 怎麼評估：不需要標準答案的自動評估，和人類判斷的一致度（0.95／0.78／0.70）
- wiki/sources/01-lewis2020-rag.md — 怎麼運作（走一遍）：Fig.1「Define "middle ear"」從輸入到輸出的 6 個步驟（⑤ 退回後補進 wiki）
- wiki/sources/05-asai2023-self-rag.md — 怎麼運作（走一遍）＋進階變體：Fig.1「How did US states get their names?」一般 RAG vs Self-RAG 的逐步對照（⑤ 退回後補進 wiki）
- wiki/concepts/lost-in-the-middle.md — 總結：答案放在中間最容易被忽略（U 形曲線），說明「位置也有影響」

## 看過但沒選的頁

- wiki/glossary.md — 121 條詞條，範圍太大；投影片需要的白話定義，上面各頁的「白話說明」已經足夠
- wiki/concepts/generator.md — overview 和 naive-rag 已經講清楚 generator 的角色；細節（BART、extractive vs generative）超出入門範圍
- wiki/methods/original-rag.md — 原始 RAG 的架構細節（marginalize、RAG-Sequence／Token）對初學者太深；需要的「2020 年提出」「和 Naive RAG 的差別」在 overview、naive-rag 已有
- wiki/methods/advanced-rag.md、wiki/methods/modular-rag.md — rag-paradigms 的對照表已涵蓋入門需要的部分
- wiki/methods/contextual-retrieval.md、wiki/concepts/reranking.md、wiki/concepts/query-optimization.md — 個別進階技巧；「RAG 是什麼」只需要用 rag-paradigms 帶過，overview 也有一句摘要
- wiki/concepts/context-window.md — 文件數量的六種說法；入門需要的「20 份 vs 50 份」在 overview 已有
- wiki/comparisons/rag-techniques.md — 技巧比較表，適合「進階技巧」主題，不適合入門
- wiki/comparisons/rag-vs-fine-tuning.md — 和 fine-tuning 的比較是另一個主題；需要的「帶教科書 vs 內化」比喻已在 analogies
- wiki/comparisons/rag-timeline.md — 演進史，入門只需要「2020 年提出」這一點，overview 已有
- wiki/sources/ 下其餘 5 個來源頁（02、03、04、06、07）— 逐篇摘要；同樣的內容已整合在上面的概念頁、方法頁

## 缺口

- **為什麼需要**：無。
- **是什麼**：無。
- **怎麼運作**：~~wiki 沒有完整走一遍的例子~~ → 已補（⑤ 第 1 次退回後，依使用者批准把 01、05 的 Fig.1 逐步例子補進 sources/01、sources/05）。仍然沒有的是「切塊」這一步的具體例子：兩個 Fig.1 都從「已經建好的 index」開始，沒有示範文件怎麼被切成 chunk。
- **進階變體**：無。
- **怎麼評估**：無。
- **總結**：wiki 沒有實際的應用場景或產品案例（例如客服、企業內部文件問答）；raw/ 的 7 篇都是研究論文或技術文章，沒有這類內容。
