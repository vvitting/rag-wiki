---
type: method
title: "Contextual Retrieval"
tags: [method, contextual-retrieval, contextual-embeddings, contextual-bm25, preprocessing]
sources: [03-anthropic-contextual-retrieval.pdf, 02-gao2023-survey.pdf]
updated: 2026-11-22
---

# Contextual Retrieval

## 一句話說明

建 index 之前，先用 LLM 為每個 [chunk](../concepts/chunking.md) 寫一段簡短的背景說明，貼在 chunk 前面，讓它不再缺少上下文 [03-anthropic-contextual-retrieval.pdf, p.5]。

## 跟 naive RAG 的差別

- [Naive RAG](naive-rag.md) 是直接把切好的 chunk 轉成 embedding [02-gao2023-survey.pdf, §II-A, p.3]；Contextual Retrieval 則是先補上說明，再轉成 embedding、建 BM25 index [03-anthropic-contextual-retrieval.pdf, p.5]。
- 它是一種前處理（preprocessing）技術，用來提升檢索準確度 [03-anthropic-contextual-retrieval.pdf, p.6]。
- 依 02 的分類，「提升被 index 內容的品質」屬於 [Advanced RAG](advanced-rag.md) 的 pre-retrieval 優化 [02-gao2023-survey.pdf, §II-B, p.4]。

## 運作步驟

1. 把文件切成 chunk [03-anthropic-contextual-retrieval.pdf, p.6]。
2. 對每個 chunk，把**整份文件**和**這個 chunk** 一起交給 Claude 3 Haiku，請它寫一段簡短的說明，交代這個 chunk 在整份文件中的位置 [03-anthropic-contextual-retrieval.pdf, p.5–6]。
3. 把產生的說明（通常 50–100 tokens）貼在 chunk 前面 [03-anthropic-contextual-retrieval.pdf, p.6]。
4. 用這個「加了說明的 chunk」建立 embedding（Contextual Embeddings）和 BM25 index（Contextual BM25）[03-anthropic-contextual-retrieval.pdf, p.5–6]。
5. 查詢時，同時用 embedding 和 BM25 檢索，再用 rank fusion 合併結果 [03-anthropic-contextual-retrieval.pdf, p.3]。
6. （選用）先取 top 150，再用 reranker 挑出 top 20 交給模型 [03-anthropic-contextual-retrieval.pdf, p.9]。

### 轉換範例

| | 內容 | 出處 |
|---|---|---|
| 原始 chunk | "The company's revenue grew by 3% over the previous quarter." | [03-anthropic-contextual-retrieval.pdf, p.4–5] |
| 加上說明後 | 開頭多了「This chunk is from an SEC filing on ACME Corp's performance…」（原文在列印時被截斷） | [03-anthropic-contextual-retrieval.pdf, p.5] |

## 優點

- 檢索失敗率從 5.7% 降到 2.9%，相對降低 49% [03-anthropic-contextual-retrieval.pdf, p.7]。
- 再加上 reranking，失敗率降到 1.9%，相對降低 67% [03-anthropic-contextual-retrieval.pdf, p.10]。
- 在測試過的每一種 embedding 和資料來源組合中都有提升 [03-anthropic-contextual-retrieval.pdf, p.7]。
- 搭配 prompt caching，前處理成本約為每百萬文件 tokens 1.02 美元 [03-anthropic-contextual-retrieval.pdf, p.7]。

## 代價與限制

- 前處理時，每個 chunk 都要呼叫一次 LLM；作者說，手動標註成千上萬個 chunk 工作量太大，所以才交給 Claude [03-anthropic-contextual-retrieval.pdf, p.5]。
- 成本數字建立在 prompt caching 之上：作者說，是 Claude 的 prompt caching 讓 Contextual Retrieval 能以低成本實現 [03-anthropic-contextual-retrieval.pdf, p.6]。
- 效果會受 chunk 大小、切分邊界、chunk 重疊程度影響 [03-anthropic-contextual-retrieval.pdf, p.8]。
- 有些 embedding model 受益比較多；作者發現 Gemini 和 Voyage 特別有效 [03-anthropic-contextual-retrieval.pdf, p.8]。
- 針對特定領域客製化 prompt，可能效果更好；例如把只在其他文件中定義的關鍵術語整理成詞彙表，一起放進 prompt [03-anthropic-contextual-retrieval.pdf, p.8]。
- 作者提醒，一定要做評估（always run evals）[03-anthropic-contextual-retrieval.pdf, p.9]。

## 和其他「補上下文」方法的比較

- **加上通用的文件摘要**：作者實驗後發現提升非常有限 [03-anthropic-contextual-retrieval.pdf, p.5]。
- **以摘要為基礎的 indexing**：作者評估後發現表現很差 [03-anthropic-contextual-retrieval.pdf, p.5]。
- **Hypothetical document embedding（HyDE）**：作者也列為過去的方法之一，並說它和 Contextual Retrieval 不同 [03-anthropic-contextual-retrieval.pdf, p.5]。HyDE 的做法見 [Query 優化](../concepts/query-optimization.md)。

## 出處

- [03-anthropic-contextual-retrieval.pdf](../sources/03-anthropic-contextual-retrieval.md)

## 相關頁面

- [Chunking](../concepts/chunking.md)
- [Retriever](../concepts/retriever.md)
- [Reranking](../concepts/reranking.md)
- [Advanced RAG](advanced-rag.md)
- [RAG 進階技巧比較](../comparisons/rag-techniques.md)
