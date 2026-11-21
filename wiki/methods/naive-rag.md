---
type: method
title: "Naive RAG"
tags: [method, rag, naive-rag, paradigm]
sources: [02-gao2023-survey.pdf, 01-lewis2020-rag.pdf]
updated: 2026-11-22
---

# Naive RAG

## 一句話說明

最基本的 RAG 流程：先把文件建成 index，收到問題時找出最相關的 top-k 個 chunk，再把問題和 chunk 一起交給 LLM 產生答案。也被稱為「Retrieve-Read」框架 [02-gao2023-survey.pdf, §II-A, p.3]。

## 跟 naive RAG 的差別

本頁就是 Naive RAG [02-gao2023-survey.pdf, §II-A, p.2–3]。它和[原始 RAG](original-rag.md) 有什麼不同，見下方的「和原始 RAG 的關係」。

## 運作步驟

1. **Indexing**：把 PDF、HTML、Word、Markdown 等格式的原始資料清理後轉成純文字 [02-gao2023-survey.pdf, §II-A, p.3]。
2. **Indexing（續）**：因為 language model 的 context 有限制，所以把文字切成較小的 [chunk](../concepts/chunking.md)，用 embedding model 轉成向量，存進 vector database [02-gao2023-survey.pdf, §II-A, p.3]。
3. **Retrieval**：用同一個 encoding model 把問題轉成向量，計算它和所有 chunk 向量的相似度，取出最相似的 top K 個 chunk [02-gao2023-survey.pdf, §II-A, p.3]。
4. **Generation**：把問題和選出的文件組成一個 prompt，交給 LLM 產生回答 [02-gao2023-survey.pdf, §II-A, p.3]。
5. **多輪對話**：如果是多輪對話，也可以把之前的對話紀錄放進 prompt [02-gao2023-survey.pdf, §II-A, p.3]。

LLM 回答時，可以使用自己的 parametric knowledge，也可以被要求只根據提供的文件作答，看任務需求而定 [02-gao2023-survey.pdf, §II-A, p.3]。

## 優點

- 成本效益高，而且表現勝過沒有 RAG 的 LLM [02-gao2023-survey.pdf, §II, p.2]。
- 對模型的修改需求很低 [02-gao2023-survey.pdf, Fig.4, p.7]。

## 代價與限制

- **檢索的問題**：precision 和 recall 都不夠好，會選到不對或不相關的 chunk，也可能漏掉關鍵資訊 [02-gao2023-survey.pdf, §II-A, p.3]。
- **生成的問題**：模型可能 [hallucinate](../concepts/hallucination.md)，產生檢索內容沒有支持的說法；輸出也可能離題、有害或帶有偏見 [02-gao2023-survey.pdf, §II-A, p.3]。
- **整合的問題**：把檢索到的資訊和任務結合時，輸出可能不連貫；多個來源找到相似資訊時，回答會重複 [02-gao2023-survey.pdf, §II-A, p.3]。
- **整合的問題（續）**：要判斷各段落的重要性與相關性、維持風格和語氣一致，也都會增加複雜度 [02-gao2023-survey.pdf, §II-A, p.3]。
- **一次檢索不夠**：遇到複雜問題時，只用原始問題檢索一次，可能找不到足夠的資訊 [02-gao2023-survey.pdf, §II-A, p.3]。
- **過度依賴檢索內容**：模型可能只是照抄檢索內容，沒有加入自己的整合或見解 [02-gao2023-survey.pdf, §II-A, p.3]。
- **直接用原始問題檢索**：使用者的問題不一定清楚精確，這會讓檢索效果變差 [02-gao2023-survey.pdf, §III-C, p.8]。

這些缺點正是發展 [Advanced RAG](advanced-rag.md) 和 [Modular RAG](modular-rag.md) 的原因 [02-gao2023-survey.pdf, §II, p.2]。

## 和原始 RAG 的關係

> ⚠️ **爭議／更新**：[02-gao2023-survey.pdf, §II-A, p.2–3] 說 Naive RAG 是「最早的方法」，在 ChatGPT 普及後不久受到重視。但「retrieval-augmented generation」這個名稱，以及「先檢索、再生成」的架構，早在 2020 年就由 [01-lewis2020-rag.pdf, §1, p.2] 提出。而綜述把這類早期研究歸在「Transformer 興起時、透過預訓練模型加強」的階段 [02-gao2023-survey.pdf, §I, p.1]。

兩者的實際差異：

| | 原始 RAG（2020） | Naive RAG |
|---|---|---|
| 生成模型 | BART-large（400M 參數）[01-lewis2020-rag.pdf, §2.3, p.3] | LLM [02-gao2023-survey.pdf, §II-A, p.3] |
| 要不要訓練 | retriever 和 generator 一起微調 [01-lewis2020-rag.pdf, §2.4, p.3] | 對模型的修改需求很低 [02-gao2023-survey.pdf, Fig.4, p.7] |
| 怎麼結合文件 | 直接串接，並對多份文件做 marginalize [01-lewis2020-rag.pdf, §2.1, §2.3, p.3] | 把問題和文件組成 prompt [02-gao2023-survey.pdf, §II-A, p.3] |

**給初學者的理解方式**：兩者都是「先查再寫」。今天大家常說的「RAG」比較接近 Naive RAG，也就是把檢索結果塞進 LLM 的 prompt [02-gao2023-survey.pdf, §II-A, p.3]；原始 RAG 則是把整個系統一起訓練 [01-lewis2020-rag.pdf, §2.4, p.3]。

## 出處

- [02-gao2023-survey.pdf](../sources/02-gao2023-survey.md)
- [01-lewis2020-rag.pdf](../sources/01-lewis2020-rag.md)

## 相關頁面

- [三種 RAG 典範比較](../comparisons/rag-paradigms.md)
- [Advanced RAG](advanced-rag.md)
- [Modular RAG](modular-rag.md)
- [原始 RAG](original-rag.md)
