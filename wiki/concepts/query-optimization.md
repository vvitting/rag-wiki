---
type: concept
title: "Query 優化（改寫、擴展、路由）"
tags: [concept, query, pre-retrieval, hyde, query-rewriting]
sources: [02-gao2023-survey.pdf]
updated: 2026-11-22
---

# Query 優化

## 白話說明

使用者的問題常常不夠清楚，也不適合直接拿去檢索。Query 優化就是在檢索之前，先把問題「修整」一下，讓 [retriever](retriever.md) 更容易找到對的資料 [02-gao2023-survey.pdf, §II-B, p.4]。

## 為什麼重要

- Naive RAG 的主要問題之一，就是直接用使用者的原始問題去檢索；但要把問題寫得精確很難，寫得不好的問題會讓檢索效果變差 [02-gao2023-survey.pdf, §III-C, p.8]。
- 語言本身也有歧義。例如在法律情境中，「LLM」可能指 large language model，也可能指法學碩士（Master of Laws）[02-gao2023-survey.pdf, §III-C, p.8]。

## 運作方式

### 1. Query expansion：把一個問題擴展成多個

- **Multi-Query**：用 LLM 把問題擴展成多個查詢，再平行執行 [02-gao2023-survey.pdf, §III-C, p.8]。
- **Sub-Query**：把複雜的問題拆成一連串較簡單的子問題 [02-gao2023-survey.pdf, §III-C, p.8]。
- **Chain-of-Verification（CoVe）**：讓 LLM 驗證擴展後的查詢，以減少 hallucination [02-gao2023-survey.pdf, §III-C, p.8]。

### 2. Query transformation：改用轉換後的問題去檢索

- **Query Rewrite**：讓 LLM 或專門的小模型（例如 RRR）改寫問題 [02-gao2023-survey.pdf, §III-C, p.9]。
- **實際案例**：淘寶的 BEQUE 改寫方法提升了長尾查詢的 recall [02-gao2023-survey.pdf, §III-C, p.9]。
- **HyDE**：先讓 LLM 寫一份「假設的答案文件」，再用它去找相似的真實文件；比對的是「答案和答案」的相似度，而不是「問題和答案」[02-gao2023-survey.pdf, §III-C, p.9]。
- **Step-back Prompting**：把原始問題抽象成一個更高層次的問題，兩個問題都拿去檢索 [02-gao2023-survey.pdf, §III-C, p.9]。

### 3. Query routing：把不同的問題送往不同的流程

- **Metadata Router/Filter**：從問題中抽出關鍵字，再用 chunk 的 metadata 過濾，縮小搜尋範圍 [02-gao2023-survey.pdf, §III-C, p.9]。
- **Semantic Router**：依照問題的語意資訊來決定路徑；也可以和 metadata 路由混合使用 [02-gao2023-survey.pdf, §III-C, p.9]。

## 各論文怎麼說

- **[02-gao2023-survey.pdf](../sources/02-gao2023-survey.md)**：把 query 優化歸在 [Advanced RAG](../methods/advanced-rag.md) 的 pre-retrieval 階段 [02-gao2023-survey.pdf, §II-B, p.4]。

## 相關頁面

- [Advanced RAG](../methods/advanced-rag.md)
- [Modular RAG](../methods/modular-rag.md)
- [Retriever](retriever.md)
- [術語表](../glossary.md)
