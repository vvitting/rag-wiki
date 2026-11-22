---
type: method
title: "Advanced RAG"
tags: [method, rag, advanced-rag, paradigm, pre-retrieval, post-retrieval]
sources: [02-gao2023-survey.pdf, 03-anthropic-contextual-retrieval.pdf, 01-lewis2020-rag.pdf, 04-liu2023-lost-in-middle.pdf]
updated: 2026-11-22
---

# Advanced RAG

## 一句話說明

在 [Naive RAG](naive-rag.md) 的流程前後各加一道優化：檢索前（pre-retrieval）先改善 index 和問題，檢索後（post-retrieval）再整理找到的內容 [02-gao2023-survey.pdf, §II-B, p.3]。

## 跟 naive RAG 的差別

- 主要目標是提升檢索品質 [02-gao2023-survey.pdf, §II-B, p.3]。
- 整體流程仍和 Naive RAG 相似，還是一條鏈狀的結構 [02-gao2023-survey.pdf, Fig.3, p.4]。

## 運作步驟

### Pre-retrieval：檢索前

- **優化 index**：目標是提升被 index 的內容品質；策略包括調整資料粒度、優化 index 結構、加入 metadata、alignment 優化、混合檢索 [02-gao2023-survey.pdf, §II-B, p.4]。
- **改善 indexing 的手法**：sliding window、更細的切分、加入 metadata [02-gao2023-survey.pdf, §II-B, p.3]。詳見 [Chunking](../concepts/chunking.md)。
- **實例：[Contextual Retrieval](contextual-retrieval.md)**：在建 index 前為每個 chunk 補上說明，提升被 index 內容的品質 [03-anthropic-contextual-retrieval.pdf, p.5–6]。03 本身沒有使用「Advanced RAG」這個詞，這裡是依 02 的分類歸入 [02-gao2023-survey.pdf, §II-B, p.4]。
- **優化 query**：讓使用者的問題更清楚、更適合檢索；常見方法有 query rewriting、query transformation、query expansion [02-gao2023-survey.pdf, §II-B, p.4]。詳見 [Query 優化](../concepts/query-optimization.md)。

### Post-retrieval：檢索後

- 主要方法是把 chunk [rerank](../concepts/reranking.md)，以及壓縮 context [02-gao2023-survey.pdf, §II-B, p.4]。
- 一個關鍵策略是 rerank，把最相關的內容移到 prompt 的頭尾；LlamaIndex、LangChain、HayStack 等框架都有實作 [02-gao2023-survey.pdf, §II-B, p.4]。
- **實測**：03 在 Contextual Retrieval 之上再加 reranking，檢索失敗率降到 1.9% [03-anthropic-contextual-retrieval.pdf, p.10]。
- 把所有相關文件一股腦丟給 LLM，可能造成資訊過載，讓不相關的內容稀釋掉關鍵細節 [02-gao2023-survey.pdf, §II-B, p.4]。
- 所以 post-retrieval 著重在挑出必要資訊、強調關鍵段落、縮短要處理的 context [02-gao2023-survey.pdf, §II-B, p.4]。

## 優點

- 針對 Naive RAG 的特定缺點提出改善 [02-gao2023-survey.pdf, §II-B, p.3]。

## 代價與限制

- 流程仍是鏈狀的，不像 [Modular RAG](modular-rag.md) 那樣可以彈性重組 [02-gao2023-survey.pdf, Fig.3, p.4]。

> ⚠️ **爭議／更新**：[01-lewis2020-rag.pdf, §4.1, p.5] 認為，要達到當時的最佳表現，re-ranker 不是必要的；但 [02-gao2023-survey.pdf, §II-B, p.4] 把 reranking 視為 Advanced RAG 的關鍵策略，[03-anthropic-contextual-retrieval.pdf, p.10–11] 的實驗顯示 reranking 能進一步降低檢索失敗率，[04-liu2023-lost-in-middle.pdf, §5, p.10] 也建議用 reranking 來應對位置效應。
> 情境不同：01 是每份文件分別交給 generator 再加權合併 [01-lewis2020-rag.pdf, §2.1, p.3]，所以沒有「文件排在 prompt 哪個位置」的問題；02、03、04 談的則是把多份文件串成一個 prompt 交給 LLM 的情境 [02-gao2023-survey.pdf, §II-A, p.3] [04-liu2023-lost-in-middle.pdf, §5, p.9]。詳見 [Reranking](../concepts/reranking.md)。

## 出處

- [02-gao2023-survey.pdf](../sources/02-gao2023-survey.md)
- [03-anthropic-contextual-retrieval.pdf](../sources/03-anthropic-contextual-retrieval.md)
- [01-lewis2020-rag.pdf](../sources/01-lewis2020-rag.md)
- [04-liu2023-lost-in-middle.pdf](../sources/04-liu2023-lost-in-middle.md)

## 相關頁面

- [Naive RAG](naive-rag.md)
- [Modular RAG](modular-rag.md)
- [Contextual Retrieval](contextual-retrieval.md)
- [三種 RAG 典範比較](../comparisons/rag-paradigms.md)
- [RAG 進階技巧比較](../comparisons/rag-techniques.md)
- [術語表](../glossary.md)
