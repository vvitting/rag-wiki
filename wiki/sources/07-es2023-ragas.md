---
type: source
title: "Ragas: Automated Evaluation of Retrieval Augmented Generation"
raw: 07-es2023-ragas.pdf
authors: [Shahul Es, Jithin James, Luis Espinosa-Anke, Steven Schockaert]
year: 2023
tags: [evaluation, ragas, faithfulness, answer-relevance, context-relevance, reference-free]
sources: [07-es2023-ragas.pdf, 02-gao2023-survey.pdf, 04-liu2023-lost-in-middle.pdf, 06-edge2024-graphrag.pdf]
updated: 2026-11-22
---

# Ragas: Automated Evaluation of Retrieval Augmented Generation（Es et al., 2023）

作者來自 Exploding Gradients、Cardiff University、AMPLYFI [07-es2023-ragas.pdf, p.1]。raw 檔是 arXiv 2309.15217 的 v2 版（2025 年 4 月 28 日）[07-es2023-ragas.pdf, p.1]。

## 一句話摘要

提出 RAGAS，一套**不需要標準答案**的 RAG 自動評估方法：讓 LLM 分別評估三件事，答案有沒有根據（faithfulness）、答案有沒有回答問題（answer relevance）、檢索到的內容是否切題（context relevance）[07-es2023-ragas.pdf, Abstract, p.1; §3, p.3]。詳見 [RAGAS 概念頁](../concepts/ragas.md)。

## 這篇想解決什麼問題

- RAG 的表現會受到 retriever、資料庫、LLM、prompt 等許多因素影響，需要大量調整，所以自動評估非常重要 [07-es2023-ragas.pdf, §1, p.1]。
- 常見的評估方式有問題：用 perplexity 衡量，不一定能預測實際任務的表現，而且 ChatGPT、GPT-4 這類封閉模型也拿不到機率值 [07-es2023-ragas.pdf, §1, p.1]。
- 問答資料集通常只有簡短、可直接擷取的答案，不一定能代表系統實際被使用的方式 [07-es2023-ragas.pdf, §1, p.1]。
- 建置 RAG 系統時，通常也沒有人工標註的資料或標準答案 [07-es2023-ragas.pdf, §3, p.2–3]。

### 背景：為什麼需要 RAG

- LLM 有兩個根本限制：一是無法回答訓練之後才發生的事；二是即使是最大的模型，也很難記住訓練資料中很少出現的知識 [07-es2023-ragas.pdf, §1, p.1]。
- 標準的解法就是 RAG：先從資料庫取回相關段落，再和原始問題一起交給 LM [07-es2023-ragas.pdf, §1, p.1]。
- 近期的研究顯示，只要把檢索到的文件直接加進一般 LM 的輸入就很有效，所以 RAG 也能搭配只能透過 API 使用的 LLM [07-es2023-ragas.pdf, §1, p.1]。

## 核心方法：三個指標

所有指標都由 LLM（gpt-3.5-turbo-16k）透過 prompt 計算 [07-es2023-ragas.pdf, §3, p.3]。

| 指標 | 衡量什麼 | 怎麼算 | 出處 |
|---|---|---|---|
| Faithfulness | 答案中的說法，能不能從檢索到的 context 推論出來 | LLM 先把答案拆成多個簡短陳述，再逐一判斷是否被 context 支持；分數 = 被支持的陳述數 ÷ 陳述總數 | [07-es2023-ragas.pdf, §3, p.3] |
| Answer relevance | 答案是否直接、適當地回答了問題（不考慮事實是否正確） | LLM 根據答案反推 n 個可能的問題，計算它們和原始問題的 embedding cosine 相似度，取平均 | [07-es2023-ragas.pdf, §3, p.3] |
| Context relevance | 檢索到的 context 是否只包含回答問題需要的資訊 | LLM 從 context 中挑出回答問題必要的句子；分數 = 挑出的句子數 ÷ context 的總句數 | [07-es2023-ragas.pdf, §3, p.3–4] |

### 為什麼是這三個？

- **Faithfulness**：可以避免 hallucination，並讓檢索到的 context 成為答案的依據；在法律這類資訊不斷變動、又很重視事實一致的領域尤其重要 [07-es2023-ragas.pdf, §3, p.3]。
- **Answer relevance**：答案應該回應實際被問的問題；答案不完整或包含多餘資訊都會被扣分 [07-es2023-ragas.pdf, §3, p.3]。
- **Context relevance**：把長段落交給 LLM 有成本；而且段落太長時，LLM 比較難利用其中的資訊，尤其是放在中間的資訊（引用 04）[07-es2023-ragas.pdf, §3, p.3]。

## 關鍵結果（數字務必附出處）

### 驗證資料集：WikiEval

- 選了 50 個 Wikipedia 頁面，內容是 2022 年之後發生的事件，也就是超過所用模型的訓練截止時間 [07-es2023-ragas.pdf, §4, p.4]。
- 讓 ChatGPT 針對每頁的開頭段落出題並作答 [07-es2023-ragas.pdf, §4, p.4]。
- 兩位標註者比較兩個答案（或兩段 context）哪個比較好。faithfulness 和 context relevance 的標註者一致度約 95%，answer relevance 約 90% [07-es2023-ragas.pdf, §4, p.4]。

### 和人類判斷的一致度（Table 1）

| 方法 | Faithfulness | Answer relevance | Context relevance | 出處 |
|---|---|---|---|---|
| RAGAS | 0.95 | 0.78 | 0.70 | [07-es2023-ragas.pdf, Table 1, p.5] |
| GPT Score（讓 ChatGPT 打 0–10 分） | 0.72 | 0.52 | 0.63 | [07-es2023-ragas.pdf, Table 1, p.5] |
| GPT Ranking（讓 ChatGPT 直接挑比較好的） | 0.54 | 0.40 | 0.52 | [07-es2023-ragas.pdf, Table 1, p.5] |

- RAGAS 的指標比兩種基準方法更接近人類判斷 [07-es2023-ragas.pdf, §5, p.5]。
- Faithfulness 的準確度最高；answer relevance 較低，主要是因為兩個候選答案的差異常常很細微 [07-es2023-ragas.pdf, §5, p.5]。
- Context relevance 最難評估：ChatGPT 常常挑不出 context 中真正關鍵的句子，context 越長越明顯 [07-es2023-ragas.pdf, §5, p.5]。

## 限制與後續爭議

- **驗證規模小**：WikiEval 只有 50 個頁面 [07-es2023-ragas.pdf, §4, p.4]。
- **依賴特定模型**：所有 prompt 都用 gpt-3.5-turbo-16k 計算 [07-es2023-ragas.pdf, §3, p.3]。
- **只評估三個面向**：不評估事實本身是否正確，answer relevance 也明確不考慮事實性 [07-es2023-ragas.pdf, §3, p.3]。
- **LLM 評審的已知問題**：讓 LLM 打分數對 prompt 的設計很敏感；讓 LLM 從多個答案中挑選時，答案的**順序**會影響結果 [07-es2023-ragas.pdf, §2, p.2]。

> ⚠️ **爭議／更新**：[06-edge2024-graphrag.pdf, §2.4, p.4] 認為 RAGAS 的三個指標只適用於一般的 vector RAG，和全局理解類的問題無關。這和本篇的設定一致：本篇考慮的是「給定一個問題，檢索 context，再生成答案」的標準 RAG [07-es2023-ragas.pdf, §3, p.2]，沒有討論全局問題。詳見 [RAG 評估](../concepts/rag-evaluation.md)。

> ⚠️ **爭議／更新**：本篇的基準方法「GPT Ranking」（讓 ChatGPT 直接從兩個答案中挑比較好的），和人類的一致度只有 0.40–0.54 [07-es2023-ragas.pdf, Table 1, p.5]，本篇也提醒答案的順序會影響 LLM 的判斷 [07-es2023-ragas.pdf, §2, p.2]。而 [06-edge2024-graphrag.pdf, §3.3, p.7–8] 的主要結果正是用 LLM 兩兩比較答案得出的，06 的 raw 檔中也沒有找到處理答案順序的說明。
> 但兩者條件不同：06 使用 GPT-4 [06-edge2024-graphrag.pdf, §1, p.2]（實驗用的是 gpt-4-turbo [06-edge2024-graphrag.pdf, §4.1.3, p.9]），評估的標準也不同；而且 06 另外用 claim 指標驗證過，兩種方法判斷一致的比例是 69%–78% [06-edge2024-graphrag.pdf, §5.2, p.11]。

## 和既有頁面的關係

- **02 的描述一致**：02 把 RAGAS 列為用 LLM 評判 context relevance、faithfulness、answer relevance 的自動化工具，answer relevance 用 cosine similarity 計算 [02-gao2023-survey.pdf, §VI-D, p.14; Table IV, p.15]，和本篇相符 [07-es2023-ragas.pdf, §3, p.3]。
- **正確引用 04**：本篇說 context 太長時，LLM 比較難利用中間的資訊 [07-es2023-ragas.pdf, §3, p.3]，和 04 的發現一致 [04-liu2023-lost-in-middle.pdf, Abstract, p.1]。
- **把答案拆成小陳述再檢查**：這個做法和 06 驗證時從答案中抽出 claim [06-edge2024-graphrag.pdf, §4.2, p.9] 類似。

## 關鍵圖表說明

- **§3 的三個 prompt**：拆解陳述、驗證陳述、挑出相關句子 [07-es2023-ragas.pdf, §3, p.3–4]。
- **Table 1**：RAGAS 和兩種基準方法與人類判斷的一致度 [07-es2023-ragas.pdf, Table 1, p.5]。**簡報「怎麼評估」段落最適合用的數字。**
- **Table 2**：faithfulness 高低的例子。問「電影《奧本海默》的導演和主演是誰？」，高 faithfulness 的答案是 Christopher Nolan 和 Cillian Murphy，低 faithfulness 的答案是 James Cameron 和 Tom Cruise [07-es2023-ragas.pdf, App. A, Table 2, p.8]。**很適合當作入門例子。**
- **Table 3、4**：answer relevance 和 context relevance 高低的例子 [07-es2023-ragas.pdf, App. A, p.8]。

## 對初學者的重點

1. 評估 RAG 不能只看「答案對不對」，要分開看三件事：有沒有根據、有沒有切題、找到的資料是否精準 [07-es2023-ragas.pdf, §6, p.5]。
2. RAGAS 不需要標準答案，用 LLM 就能自動評分 [07-es2023-ragas.pdf, Abstract, p.1]。
3. Faithfulness 的算法很直覺：把答案拆成一句句小陳述，算有幾成能在資料中找到根據 [07-es2023-ragas.pdf, §3, p.3]。
4. 用 LLM 評分也有極限：直接讓 ChatGPT 挑比較好的答案，和人類判斷一致的比例只有 0.40–0.54，遠低於 RAGAS [07-es2023-ragas.pdf, Table 1, p.5]。

## 相關頁面

- [RAGAS（概念）](../concepts/ragas.md)
- [RAG 評估](../concepts/rag-evaluation.md)
- [Hallucination](../concepts/hallucination.md)
- [02 RAG 綜述](02-gao2023-survey.md)
- [06 GraphRAG](06-edge2024-graphrag.md)
- [術語表](../glossary.md)
