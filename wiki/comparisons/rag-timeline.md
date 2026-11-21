---
type: comparison
title: "RAG 演進時間軸"
tags: [comparison, timeline, history]
sources: [01-lewis2020-rag.pdf, 02-gao2023-survey.pdf]
updated: 2026-11-22
---

# RAG 演進時間軸

> 每 ingest 一篇就更新。只列出 raw/ 裡有出處的時間點。

| 時間 | 事件 | 出處 |
|---|---|---|
| Transformer 興起時 | RAG 研究起步，重點是透過預訓練模型（PTM）把額外知識加進 language model | [02-gao2023-survey.pdf, §I, p.1] |
| 2020 | Lewis et al. 提出並命名「retrieval-augmented generation」：DPR 加 BART，端到端訓練 | [01-lewis2020-rag.pdf, §1, p.2]；年份見 [02-gao2023-survey.pdf, Ref.[4], p.17] |
| ChatGPT 出現後 | LLM 展現強大的 in-context learning 能力，RAG 研究轉向在推論階段提供更好的資訊 | [02-gao2023-survey.pdf, §I, p.1] |
| ChatGPT 普及後不久 | Naive RAG（Retrieve-Read）受到重視 | [02-gao2023-survey.pdf, §II-A, p.2–3] |
| 之後 | Advanced RAG、Modular RAG 出現，RAG 也更多地結合 LLM fine-tuning | [02-gao2023-survey.pdf, §I, p.1; §II, p.2] |
| 2023–2024 | Gao et al. 整理 100 多篇研究，發表 RAG 綜述（raw 檔為 2024 年 3 月的 v5） | [02-gao2023-survey.pdf, §I, p.1; p.1] |

> ⚠️ **爭議／更新**：綜述說 Naive RAG 是「最早的方法」[02-gao2023-survey.pdf, §II-A, p.2]，但把它放在 ChatGPT 普及之後；而 RAG 這個名稱在 2020 年就出現了 [01-lewis2020-rag.pdf, §1, p.2]。詳見 [Naive RAG](../methods/naive-rag.md)。

## 相關頁面

- [三種 RAG 典範比較](rag-paradigms.md)
- [原始 RAG](../methods/original-rag.md)
- [RAG 總覽](../overview.md)
