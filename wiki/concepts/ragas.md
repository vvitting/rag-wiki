---
type: concept
title: "RAGAS：不用標準答案的 RAG 評估"
tags: [concept, evaluation, ragas, faithfulness, answer-relevance, context-relevance]
sources: [07-es2023-ragas.pdf, 02-gao2023-survey.pdf, 05-asai2023-self-rag.pdf, 01-lewis2020-rag.pdf, 06-edge2024-graphrag.pdf]
updated: 2026-11-22
---

# RAGAS

## 白話說明

RAGAS 是一套讓 LLM 幫忙評分 RAG 系統的方法。它不需要人工準備的標準答案，只看三件事：答案有沒有根據、答案有沒有回答問題、找來的資料是否切題 [07-es2023-ragas.pdf, Abstract, p.1; §3, p.3]。

## 為什麼重要

- 建置 RAG 系統時，通常沒有人工標註的資料或標準答案 [07-es2023-ragas.pdf, §3, p.2–3]。
- RAG 的表現受 retriever、資料庫、LLM、prompt 等許多因素影響，需要反覆調整，所以快速的自動評估很重要 [07-es2023-ragas.pdf, §1, p.1; Abstract, p.1]。
- 它對應到綜述列出的 RAG 三個主要品質分數 [02-gao2023-survey.pdf, §VI-C, p.12; Table IV, p.15]。

## 運作方式

### 1. Faithfulness：答案有沒有根據？

1. 讓 LLM 把答案拆成多個簡短的陳述 [07-es2023-ragas.pdf, §3, p.3]。
2. 讓 LLM 逐一判斷每個陳述能不能從 context 推論出來，回答 Yes 或 No [07-es2023-ragas.pdf, §3, p.3]。
3. 分數 = 被支持的陳述數 ÷ 陳述總數 [07-es2023-ragas.pdf, §3, p.3]。

**例子**：問「電影《奧本海默》的導演和主演是誰？」，context 寫的是 Christopher Nolan 和 Cillian Murphy。回答「James Cameron 導演、Tom Cruise 主演」就是低 faithfulness [07-es2023-ragas.pdf, Table 2, p.8]。

### 2. Answer relevance：有沒有回答問題？

1. 讓 LLM 根據答案，反推 n 個「這個答案可能在回答什麼問題」[07-es2023-ragas.pdf, §3, p.3]。
2. 用 embedding 計算這些反推問題和原始問題的 cosine 相似度，取平均 [07-es2023-ragas.pdf, §3, p.3]。
3. 這個指標**不考慮事實是否正確**；答案不完整或有多餘資訊會被扣分 [07-es2023-ragas.pdf, §3, p.3]。

**例子**：問發射日期和地點，回答「日期和時間尚未公布……這是一個研究天氣的重要任務」，就是低 answer relevance [07-es2023-ragas.pdf, Table 3, p.8]。

### 3. Context relevance：找來的資料切不切題？

1. 讓 LLM 從 context 中挑出回答問題**必要**的句子 [07-es2023-ragas.pdf, §3, p.4]。
2. 分數 = 挑出的句子數 ÷ context 的總句數 [07-es2023-ragas.pdf, §3, p.4]。
3. 目的是懲罰多餘的資訊：長 context 不僅成本高，LLM 也比較難利用其中間的資訊 [07-es2023-ragas.pdf, §3, p.3]。

### 準不準？（和人類判斷的一致度）

| 方法 | Faithfulness | Answer relevance | Context relevance | 出處 |
|---|---|---|---|---|
| RAGAS | 0.95 | 0.78 | 0.70 | [07-es2023-ragas.pdf, Table 1, p.5] |
| GPT Score（ChatGPT 打 0–10 分） | 0.72 | 0.52 | 0.63 | [07-es2023-ragas.pdf, Table 1, p.5] |
| GPT Ranking（ChatGPT 直接挑） | 0.54 | 0.40 | 0.52 | [07-es2023-ragas.pdf, Table 1, p.5] |

- 重點：**拆成小步驟再判斷**（RAGAS），比直接要 LLM 打分數或挑選準確得多 [07-es2023-ragas.pdf, §5, p.5]。
- Context relevance 最難，ChatGPT 常挑不出關鍵句，context 越長越明顯 [07-es2023-ragas.pdf, §5, p.5]。

## 各論文怎麼說

- **[07-es2023-ragas.pdf](../sources/07-es2023-ragas.md)**：原始論文，見上方說明 [07-es2023-ragas.pdf, §3, p.2–4]。
- **[02-gao2023-survey.pdf](../sources/02-gao2023-survey.md)**：把 RAGAS 列為評估 retrieval quality 和 generation quality 的工具，answer relevance 用 cosine similarity 計算 [02-gao2023-survey.pdf, Table IV, p.15]。
- **[05-asai2023-self-rag.pdf](../sources/05-asai2023-self-rag.md)**：Self-RAG 的 ISSUP token（答案是否被文件支持）[05-asai2023-self-rag.pdf, Table 1, p.4]，和 RAGAS 的 faithfulness 衡量的是相近的東西；差別在於 Self-RAG 是模型在生成時**自己**評估，RAGAS 則是事後由另一個 LLM 評估 [07-es2023-ragas.pdf, §3, p.3]。

> ⚠️ **爭議／更新**：[06-edge2024-graphrag.pdf, §2.4, p.4] 認為這三個指標只適用於一般 vector RAG，不適合「理解整批資料」的全局問題。詳見 [RAG 評估](rag-evaluation.md)。

## 常見誤解

- **「faithfulness 高，答案就是對的」**：不一定。Faithfulness 只檢查答案是否和**檢索到的 context** 一致 [07-es2023-ragas.pdf, §3, p.3]；如果 context 本身有錯，答案也會跟著錯，而外部知識來源本來就可能有錯 [01-lewis2020-rag.pdf, Broader Impact, p.10]。
- **「answer relevance 高，答案就是對的」**：也不一定，這個指標明確不考慮事實性 [07-es2023-ragas.pdf, §3, p.3]。

## 相關頁面

- [RAG 評估](rag-evaluation.md)
- [Hallucination](hallucination.md)
- [Self-RAG](../methods/self-rag.md)
- [術語表](../glossary.md)
