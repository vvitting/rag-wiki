---
type: comparison
title: "RAG 演進時間軸"
tags: [comparison, timeline, history]
sources: [01-lewis2020-rag.pdf, 02-gao2023-survey.pdf, 03-anthropic-contextual-retrieval.pdf, 04-liu2023-lost-in-middle.pdf, 05-asai2023-self-rag.pdf, 06-edge2024-graphrag.pdf, 07-es2023-ragas.pdf]
updated: 2026-11-22
---

# RAG 演進時間軸

> 每 ingest 一篇就更新。只列出 raw/ 裡有出處的時間點。

| 時間 | 事件 | 出處 |
|---|---|---|
| Transformer 興起時 | RAG 研究起步，重點是透過預訓練模型（PTM）把額外知識加進 language model | [02-gao2023-survey.pdf, §I, p.1] |
| 2020 | Lewis et al. 提出並命名「retrieval-augmented generation」：DPR 加 BART，端到端訓練 | [01-lewis2020-rag.pdf, §1, p.2]；年份見 [02-gao2023-survey.pdf, Ref. 4, p.17] |
| ChatGPT 出現後 | LLM 展現強大的 in-context learning 能力，RAG 研究轉向在推論階段提供更好的資訊 | [02-gao2023-survey.pdf, §I, p.1] |
| ChatGPT 普及後不久 | Naive RAG（Retrieve-Read）受到重視 | [02-gao2023-survey.pdf, §II-A, p.2–3] |
| 之後 | Advanced RAG、Modular RAG 出現，RAG 也更多地結合 LLM fine-tuning | [02-gao2023-survey.pdf, §I, p.1; §II, p.2] |
| 2023 | Liu et al. 發表〈Lost in the Middle〉：LLM 對 context 中間的資訊用得最差，支援長 context 的模型也一樣（raw 檔為 2023 年 11 月的 v3） | [04-liu2023-lost-in-middle.pdf, Abstract, p.1; p.1] |
| 2023 | Es et al. 發表 RAGAS：不需要標準答案、由 LLM 計算的 RAG 評估指標（02 引用時標為 2023 年的 arXiv 預印本；raw 檔為 2025 年 4 月的 v2） | [02-gao2023-survey.pdf, Ref. 164, p.20] [07-es2023-ragas.pdf, p.1] |
| 2023 年 10 月 | Asai et al. 發表 Self-RAG：讓模型自己決定何時檢索，並用 reflection tokens 自我評分（raw 檔為 v1 預印本） | [05-asai2023-self-rag.pdf, p.1] |
| 2023–2024 | Gao et al. 整理 100 多篇研究，發表 RAG 綜述（raw 檔為 2024 年 3 月的 v5） | [02-gao2023-survey.pdf, §I, p.1; p.1]；年份見 [06-edge2024-graphrag.pdf, References, p.13] |
| 2024 年 9 月 19 日 | Anthropic 發表 Contextual Retrieval，並說小型知識庫可以直接放進 prompt | [03-anthropic-contextual-retrieval.pdf, p.1–2] |
| 2025 年 2 月 19 日（raw 版本） | Edge et al.（Microsoft）發表 GraphRAG：用 LLM 建 knowledge graph 和社群摘要，回答全局問題。raw 檔是 arXiv:2404.16130 的 v2 預印本；raw 中沒有寫第一版的日期，所以這裡依 raw 版本的日期排序 | [06-edge2024-graphrag.pdf, p.1] |

> ⚠️ **爭議／更新**：綜述說 Naive RAG 是「最早的方法」[02-gao2023-survey.pdf, §II-A, p.2]，但把它放在 ChatGPT 普及之後；而 RAG 這個名稱在 2020 年就出現了 [01-lewis2020-rag.pdf, §1, p.2] [02-gao2023-survey.pdf, Ref. 4, p.17]。詳見 [Naive RAG](../methods/naive-rag.md)。

## 相關頁面

- [三種 RAG 典範比較](rag-paradigms.md)
- [原始 RAG](../methods/original-rag.md)
- [RAG 總覽](../overview.md)
- [術語表](../glossary.md)
