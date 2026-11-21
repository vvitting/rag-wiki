---
type: concept
title: "Reranking（重新排序）"
tags: [concept, reranking, post-retrieval]
sources: [02-gao2023-survey.pdf, 01-lewis2020-rag.pdf, 03-anthropic-contextual-retrieval.pdf, 04-liu2023-lost-in-middle.pdf]
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
- **放在哪裡**：有一種策略是把最相關的內容移到 prompt 的頭尾 [02-gao2023-survey.pdf, §II-B, p.4]；04 則建議推向 context 的開頭 [04-liu2023-lost-in-middle.pdf, §5, p.10]。原因見 [Lost in the middle](lost-in-the-middle.md)。

### 實際流程（以 03 為例）

1. 先做初步檢索，取出可能相關的 chunk（03 取前 150 個）[03-anthropic-contextual-retrieval.pdf, p.9]。
2. 把這些 chunk 和使用者的問題一起交給 reranking model [03-anthropic-contextual-retrieval.pdf, p.9]。
3. Reranking model 依照相關性和重要性為每個 chunk 打分數，選出 top-K（03 選 20 個）[03-anthropic-contextual-retrieval.pdf, p.9]。
4. 把這 top-K 個 chunk 當作 context 交給模型產生答案 [03-anthropic-contextual-retrieval.pdf, p.9]。

03 用的是 Cohere reranker [03-anthropic-contextual-retrieval.pdf, p.10]。

### 成本與延遲的取捨

- **好處**：模型要處理的資訊變少，所以回答更好，成本和延遲也會降低 [03-anthropic-contextual-retrieval.pdf, p.9]。
- **代價**：reranking 在執行時多了一個步驟，即使 reranker 是平行為所有 chunk 打分數，還是一定會增加一點延遲 [03-anthropic-contextual-retrieval.pdf, p.10]。
- **取捨**：rerank 越多 chunk 表現越好，rerank 越少則延遲和成本越低；作者建議依自己的使用情境實驗 [03-anthropic-contextual-retrieval.pdf, p.10]。

## 各論文怎麼說

- **[02-gao2023-survey.pdf](../sources/02-gao2023-survey.md)**：把 reranking 列為 post-retrieval 的主要方法之一，另一個是 context 壓縮 [02-gao2023-survey.pdf, §II-B, p.4]。
- **[01-lewis2020-rag.pdf](../sources/01-lewis2020-rag.md)**：當時表現最好的 DPR QA 系統用 BERT cross-encoder 來 re-rank 文件，RAG 沒有用，表現仍然勝過它 [01-lewis2020-rag.pdf, §4.1, p.5]。

- **[03-anthropic-contextual-retrieval.pdf](../sources/03-anthropic-contextual-retrieval.md)**：在 Contextual Embeddings 加 Contextual BM25 之上再做 reranking，檢索失敗率從 2.9% 降到 1.9%；和基準（5.7%）相比，總共降低 67% [03-anthropic-contextual-retrieval.pdf, p.7, p.10]。結論是有 reranking 比沒有好 [03-anthropic-contextual-retrieval.pdf, p.11]。

- **[04-liu2023-lost-in-middle.pdf](../sources/04-liu2023-lost-in-middle.md)**：LLM 最會利用 context 開頭和結尾的資訊，所以建議 rerank 時把相關資訊推向 context 的開頭 [04-liu2023-lost-in-middle.pdf, §5, p.10]。在 20 份文件中，答案在第 1 份時，GPT-3.5-Turbo 的準確率是 75.8%；在第 10 份時只有 53.8% [04-liu2023-lost-in-middle.pdf, Table 6, p.18]。

> ⚠️ **爭議／更新**：[01-lewis2020-rag.pdf, §4.1, p.5] 認為，要達到當時的最佳表現，re-ranker 不是必要的；但 [02-gao2023-survey.pdf, §II-B, p.4] 把 reranking 視為 Advanced RAG 的關鍵策略，[03-anthropic-contextual-retrieval.pdf, p.10–11] 的實驗顯示 reranking 能進一步降低檢索失敗率，[04-liu2023-lost-in-middle.pdf, §5, p.10] 也建議用 reranking 來應對位置效應。
> 情境不同：01 是在 open-domain QA 上端到端訓練的 BART 模型，每份文件分別交給 generator 再加權合併 [01-lewis2020-rag.pdf, §2.1, p.3]，所以沒有「文件排在 prompt 哪個位置」的問題；02、03、04 談的則是把多份文件串成一個 prompt 交給 LLM 的情境 [02-gao2023-survey.pdf, §II-A, p.3; 04-liu2023-lost-in-middle.pdf, §5, p.9]。在這種情境下，reranking 的價值已經有 03（檢索失敗率）和 04（位置效應）兩方面的證據 [03-anthropic-contextual-retrieval.pdf, p.10; 04-liu2023-lost-in-middle.pdf, §2.3, p.5]。

## 相關頁面

- [Advanced RAG](../methods/advanced-rag.md)
- [Contextual Retrieval](../methods/contextual-retrieval.md)
- [Lost in the middle](lost-in-the-middle.md)
- [Context window](context-window.md)
- [Retriever](retriever.md)
- [術語表](../glossary.md)
