---
type: comparison
title: "三種 RAG 典範比較：Naive、Advanced、Modular"
tags: [comparison, paradigm, naive-rag, advanced-rag, modular-rag]
sources: [02-gao2023-survey.pdf]
updated: 2026-11-22
---

# 三種 RAG 典範比較

綜述把 RAG 研究分成三個階段：Naive RAG、Advanced RAG、Modular RAG [02-gao2023-survey.pdf, §II, p.2; Fig.3, p.4]。後兩者都是為了改善 Naive RAG 的特定缺點而發展出來的 [02-gao2023-survey.pdf, §II, p.2]。

| | [Naive RAG](../methods/naive-rag.md) | [Advanced RAG](../methods/advanced-rag.md) | [Modular RAG](../methods/modular-rag.md) |
|---|---|---|---|
| 核心流程 | indexing → retrieval → generation [02-gao2023-survey.pdf, §II-A, p.3] | 和 Naive 相似，前後再加優化 [02-gao2023-survey.pdf, Fig.3, p.4] | 可以新增、替換、重排模組 [02-gao2023-survey.pdf, §II-C, p.5] |
| 結構 | 鏈狀，「Retrieve-Read」[02-gao2023-survey.pdf, §II-A, p.3] | 仍是鏈狀 [02-gao2023-survey.pdf, Fig.3, p.4] | 不限依序；包含 iterative、adaptive 檢索 [02-gao2023-survey.pdf, Fig.3, p.4] |
| 主要改進 | – | pre-retrieval（index、query 優化）與 post-retrieval（rerank、壓縮）[02-gao2023-survey.pdf, §II-B, p.4] | 新模組（Search、Memory、Routing…）與新模式 [02-gao2023-survey.pdf, §II-C, p.4–5] |
| 和 fine-tuning 的結合 | 對模型的修改需求低 [02-gao2023-survey.pdf, Fig.4, p.7] | – | 和 fine-tuning 結合得更多 [02-gao2023-survey.pdf, Fig.4, p.7] |
| 典型例子 | – | LlamaIndex、LangChain、HayStack 的 rerank [02-gao2023-survey.pdf, §II-B, p.4] | RAG-Fusion、Rewrite-Retrieve-Read、FLARE、Self-RAG [02-gao2023-survey.pdf, §II-C, p.4–5] |

## 重點

- 三者是逐步改進的關係，不是互相取代：Modular RAG 仍然建立在 Advanced 和 Naive RAG 的基本原理上 [02-gao2023-survey.pdf, §II-C, p.4]。
- 表中的「–」代表綜述在這個欄位沒有明確整理 [02-gao2023-survey.pdf, §II, p.2–5]。

## 相關頁面

- [Naive RAG](../methods/naive-rag.md)
- [Advanced RAG](../methods/advanced-rag.md)
- [Modular RAG](../methods/modular-rag.md)
- [RAG 演進時間軸](rag-timeline.md)
