---
type: concept
title: "Reranking（重新排序）"
tags: [concept, reranking, post-retrieval]
sources: [02-gao2023-survey.pdf, 01-lewis2020-rag.pdf]
updated: 2026-11-22
---

# Reranking

## 白話說明

[Retriever](retriever.md) 先粗略找出一批候選文件，reranking 再把它們重新排序，讓最相關的排在前面，同時篩掉不相關的 [02-gao2023-survey.pdf, §IV-A, p.10]。

## 為什麼重要

- Reranking 有兩個作用：一是「強化」，把最相關的結果排在前面；二是「過濾」，減少要交給 LLM 的文件數量 [02-gao2023-survey.pdf, §IV-A, p.10]。
- 它是 [Advanced RAG](../methods/advanced-rag.md) 在 post-retrieval 階段的關鍵策略 [02-gao2023-survey.pdf, §II-B, p.4]。

## 運作方式

- **規則式**：依照預先定義的指標排序，例如 Diversity、Relevance、MRR [02-gao2023-survey.pdf, §IV-A, p.10]。
- **模型式**：使用 BERT 系列的 encoder-decoder 模型（例如 SpanBERT）、專門的 reranking 模型（例如 Cohere rerank、bge-reranker-large），或一般的 LLM（例如 GPT）[02-gao2023-survey.pdf, §IV-A, p.10]。
- **放在哪裡**：有一種策略是把最相關的內容移到 prompt 的頭尾 [02-gao2023-survey.pdf, §II-B, p.4]。原因可參考 [Context window](context-window.md) 頁的「Lost in the middle」。

## 各論文怎麼說

- **[02-gao2023-survey.pdf](../sources/02-gao2023-survey.md)**：把 reranking 列為 post-retrieval 的主要方法之一，另一個是 context 壓縮 [02-gao2023-survey.pdf, §II-B, p.4]。
- **[01-lewis2020-rag.pdf](../sources/01-lewis2020-rag.md)**：當時表現最好的 DPR QA 系統用 BERT cross-encoder 來 re-rank 文件，RAG 沒有用，表現仍然勝過它 [01-lewis2020-rag.pdf, §4.1, p.5]。

> ⚠️ **爭議／更新**：[01-lewis2020-rag.pdf, §4.1, p.5] 認為，要達到當時的最佳表現，re-ranker 不是必要的；但 [02-gao2023-survey.pdf, §II-B, p.4] 把 reranking 視為 Advanced RAG 的關鍵策略。兩者的情境不同：前者是在 open-domain QA 上端到端訓練的 BART 模型，後者是以 LLM 為核心的 RAG 系統。

## 相關頁面

- [Advanced RAG](../methods/advanced-rag.md)
- [Context window](context-window.md)
- [Retriever](retriever.md)
- [術語表](../glossary.md)
