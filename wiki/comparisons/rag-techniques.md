---
type: comparison
title: "RAG 進階技巧比較"
tags: [comparison, techniques, advanced-rag]
sources: [02-gao2023-survey.pdf, 03-anthropic-contextual-retrieval.pdf]
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
| Reranking | post-retrieval | 初步檢索回傳太多、品質不一的 chunk [03-anthropic-contextual-retrieval.pdf, p.9] | 和上一列合用時，失敗率總共降低 67% [03-anthropic-contextual-retrieval.pdf, p.10] | [Reranking](../concepts/reranking.md) |
| Context 壓縮 | post-retrieval | context 太長，雜訊太多 [02-gao2023-survey.pdf, §IV-A, p.10] | 無 [02-gao2023-survey.pdf, §IV-A, p.10] | [Context window](../concepts/context-window.md) |
| Iterative／recursive／adaptive retrieval | 整個流程 | 只檢索一次，不夠應付需要多步推理的問題 [02-gao2023-survey.pdf, §V, p.10] | 無 [02-gao2023-survey.pdf, §V, p.10–12] | [Modular RAG](../methods/modular-rag.md) |

## 重點

- Contextual Retrieval、BM25、reranking 的好處可以疊加 [03-anthropic-contextual-retrieval.pdf, p.11]。
- 目前 raw/ 裡，只有 03 對這些技巧提供了量化比較；而且它衡量的是檢索失敗率，不是最終答案的品質 [03-anthropic-contextual-retrieval.pdf, p.7]。

## 相關頁面

- [Advanced RAG](../methods/advanced-rag.md)
- [Modular RAG](../methods/modular-rag.md)
- [Contextual Retrieval](../methods/contextual-retrieval.md)
- [三種 RAG 典範比較](rag-paradigms.md)
