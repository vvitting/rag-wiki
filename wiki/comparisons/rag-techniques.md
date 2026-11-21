---
type: comparison
title: "RAG 進階技巧比較"
tags: [comparison, techniques, advanced-rag]
sources: [02-gao2023-survey.pdf, 03-anthropic-contextual-retrieval.pdf, 04-liu2023-lost-in-middle.pdf, 05-asai2023-self-rag.pdf, 06-edge2024-graphrag.pdf]
updated: 2026-11-22
---

# RAG 進階技巧比較

> 每 ingest 一篇就更新。「階段」依 [02-gao2023-survey.pdf, §II-B, p.4] 的 pre-retrieval／post-retrieval 分類。

| 技巧 | 階段 | 解決什麼問題 | raw/ 裡有沒有實測數字 | 頁面 |
|---|---|---|---|---|
| Query rewrite／expansion | pre-retrieval | 使用者的原始問題不清楚，或不適合拿去檢索 [02-gao2023-survey.pdf, §III-C, p.8] | 只有質性描述 [02-gao2023-survey.pdf, §III-C, p.9] | [Query 優化](../concepts/query-optimization.md) |
| HyDE | pre-retrieval | 讓比對變成「答案和答案」，而不是「問題和答案」[02-gao2023-survey.pdf, §III-C, p.9] | 無 [02-gao2023-survey.pdf, §III-C, p.9] | [Query 優化](../concepts/query-optimization.md) |
| Small2Big／metadata | pre-retrieval（index） | 兼顧檢索精度和 context 完整度；縮小搜尋範圍 [02-gao2023-survey.pdf, §III-B, p.8] | 無 [02-gao2023-survey.pdf, §III-B, p.8] | [Chunking](../concepts/chunking.md) |
| Contextual Retrieval | pre-retrieval（index） | chunk 缺少上下文，所以找不到 [03-anthropic-contextual-retrieval.pdf, p.4] | 檢索失敗率降低 35%（只加 embedding）到 49%（再加 BM25）[03-anthropic-contextual-retrieval.pdf, p.7] | [Contextual Retrieval](../methods/contextual-retrieval.md) |
| Hybrid retrieval（embedding + BM25） | retrieval | embedding 會漏掉精確字串，例如錯誤碼 [03-anthropic-contextual-retrieval.pdf, p.3] | 結論是比只用 embedding 好 [03-anthropic-contextual-retrieval.pdf, p.11] | [Retriever](../concepts/retriever.md) |
| Reranking | post-retrieval | 初步檢索回傳太多、品質不一的 chunk [03-anthropic-contextual-retrieval.pdf, p.9]；中間的資訊容易被忽略 [04-liu2023-lost-in-middle.pdf, §5, p.10] | 在 Contextual Embeddings + Contextual BM25 之上再加 reranking，失敗率從 5.7% 降到 1.9%，總共降低 67% [03-anthropic-contextual-retrieval.pdf, p.7, p.10]；04 顯示答案在第 1 份和第 10 份的準確率差 22 個百分點（75.8% vs 53.8%），但沒有直接測 reranker [04-liu2023-lost-in-middle.pdf, Table 6, p.18] | [Reranking](../concepts/reranking.md) |
| Ranked list truncation（少取幾份） | post-retrieval | 文件多了，效益小、成本高 [04-liu2023-lost-in-middle.pdf, §5, p.10] | 50 份 vs 20 份只多約 1%–1.5% [04-liu2023-lost-in-middle.pdf, §5, p.10] | [Context window](../concepts/context-window.md) |
| Query-aware contextualization（問題放在文件前後） | prompt 排版 | decoder-only 模型讀文件時還看不到問題 [04-liu2023-lost-in-middle.pdf, §4.2, p.7–8] | key-value 檢索幾乎變成完美，多文件問答幾乎沒有變化 [04-liu2023-lost-in-middle.pdf, §4.2, p.8] | [Lost in the middle](../concepts/lost-in-the-middle.md) |
| Context 壓縮 | post-retrieval | context 太長，雜訊太多 [02-gao2023-survey.pdf, §IV-A, p.10] | 無 [02-gao2023-survey.pdf, §IV-A, p.10] | [Context window](../concepts/context-window.md) |
| Iterative／recursive／adaptive retrieval | 整個流程 | 只檢索一次，不夠應付需要多步推理的問題 [02-gao2023-survey.pdf, §V, p.10] | 02 沒有提供（Self-RAG 的數字見下一列）[02-gao2023-survey.pdf, §V, p.10–12] | [Modular RAG](../methods/modular-rag.md) |
| GraphRAG（knowledge graph＋社群摘要） | index＋整個流程 | 一般 RAG 回答不了需要理解整批資料的全局問題 [06-edge2024-graphrag.pdf, Abstract, p.1] | 全局問題的全面性勝率 72%–83%、多樣性勝率 62%–82%（LLM 評審）[06-edge2024-graphrag.pdf, §5.1, p.9]；但答案較不直接 [06-edge2024-graphrag.pdf, §5.1, p.9] | [GraphRAG](../methods/graphrag.md) |
| Self-RAG（adaptive retrieval＋自我評分） | 整個流程（需要訓練） | 不管需不需要都檢索；生成後不檢查品質 [05-asai2023-self-rag.pdf, §1, p.1–2] | 7B 模型的 PopQA 54.9、PubHealth 72.4，都高於加上檢索的 Llama2-7B（38.2、30.0）[05-asai2023-self-rag.pdf, Table 2, p.8] | [Self-RAG](../methods/self-rag.md) |

## 重點

- Contextual Retrieval、BM25、reranking 的好處可以疊加 [03-anthropic-contextual-retrieval.pdf, p.11]。
- 目前 raw/ 裡，03 對檢索技巧提供了量化比較，但它衡量的是檢索失敗率，不是最終答案的品質 [03-anthropic-contextual-retrieval.pdf, p.7]。
- 04 則從「答案準確率」的角度，說明為什麼文件的順序和數量很重要 [04-liu2023-lost-in-middle.pdf, §2.3, p.5; §5, p.10]。

## 相關頁面

- [Advanced RAG](../methods/advanced-rag.md)
- [Modular RAG](../methods/modular-rag.md)
- [Contextual Retrieval](../methods/contextual-retrieval.md)
- [三種 RAG 典範比較](rag-paradigms.md)
- [術語表](../glossary.md)
