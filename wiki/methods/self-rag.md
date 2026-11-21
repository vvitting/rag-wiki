---
type: method
title: "Self-RAG（自我反思的 RAG）"
tags: [method, self-rag, adaptive-retrieval, reflection-tokens, modular-rag]
sources: [05-asai2023-self-rag.pdf, 02-gao2023-survey.pdf, 06-edge2024-graphrag.pdf]
updated: 2026-11-22
---

# Self-RAG

## 一句話說明

訓練一個 LLM，讓它在寫答案的過程中，用特殊的「reflection tokens」自己決定要不要檢索，並為檢索到的文件和自己寫的內容打分數 [05-asai2023-self-rag.pdf, Abstract, p.1]。

## 跟 naive RAG 的差別

| | [Naive RAG](naive-rag.md)／傳統 RAG | Self-RAG |
|---|---|---|
| 什麼時候檢索 | 不管需不需要，都取固定數量的文件 [05-asai2023-self-rag.pdf, §1, p.2] | 模型自己判斷，需要時才檢索 [05-asai2023-self-rag.pdf, §1, p.1] |
| 怎麼用文件 | 把所有文件一起放進 prompt [02-gao2023-survey.pdf, §II-A, p.3] | 每份文件分別、平行產生一段回答 [05-asai2023-self-rag.pdf, §3.1, p.4] |
| 生成後 | 不回頭檢查品質 [05-asai2023-self-rag.pdf, §1, p.2] | 為每段回答的相關性、有無根據、有用程度打分數 [05-asai2023-self-rag.pdf, §3.1, p.4] |
| 要不要訓練 | 可以直接用現成的 LLM [02-gao2023-survey.pdf, Fig.4, p.7] | 要訓練 critic 和 generator 兩個模型 [05-asai2023-self-rag.pdf, §3.2, p.4] |

依 02 的分類，Self-RAG 屬於 [Modular RAG](modular-rag.md) 中的 adaptive retrieval [02-gao2023-survey.pdf, §V-C, p.11–12]。

## 運作步驟

### 推論（使用時）

1. **要不要查？**模型產生 Retrieve token 判斷 [05-asai2023-self-rag.pdf, Algorithm 1, p.4]。
2. **不用查**：像一般 LLM 一樣寫下一段，再用 ISUSE 評估有不有用 [05-asai2023-self-rag.pdf, Algorithm 1, p.4]。
3. **要查**：retriever 取回多份文件，模型針對每份文件分別判斷 ISREL（相不相關），並寫出一段回答 [05-asai2023-self-rag.pdf, Algorithm 1, p.4]。
4. **自我評分**：對每段回答產生 ISSUP（有沒有被文件支持）和 ISUSE（有不有用）[05-asai2023-self-rag.pdf, Algorithm 1, p.4]。
5. **選最好的**：用三種分數的加權總和，做 segment-level beam search，選出最好的那段 [05-asai2023-self-rag.pdf, §3.3, p.6]。
6. 重複以上步驟，直到寫完 [05-asai2023-self-rag.pdf, §3.3, p.6]。

### 訓練（事前準備）

1. 用 GPT-4 為部分資料標出 reflection tokens [05-asai2023-self-rag.pdf, §3.2.1, p.5]。
2. 訓練一個小的 critic 模型，學會模仿 GPT-4 的標註 [05-asai2023-self-rag.pdf, §3.2.1, p.5]。
3. 用 critic 把 reflection tokens 插入 150k 筆訓練資料 [05-asai2023-self-rag.pdf, §3.2.2, p.5; §4.3, p.7]。
4. 訓練 generator 自己產生 reflection tokens，推論時就不需要 critic 了 [05-asai2023-self-rag.pdf, §3, p.4]。

### 範例（Fig.1）

- **問「美國各州的名字怎麼來的？」**：模型判斷需要檢索；取回 3 份文件，第 2 份被判為 Irrelevant，第 3 份只有 Partially supported，最後選用第 1 份 [05-asai2023-self-rag.pdf, §3.1, p.4; Fig.1, p.2]。
- **「寫一篇最棒的暑假作文」**：模型判斷不需要檢索，直接寫 [05-asai2023-self-rag.pdf, Fig.1, p.2]。

## 優點

- 在六個任務上，勝過參數更多的 LLM，以及傳統的 RAG 方法 [05-asai2023-self-rag.pdf, §6, p.10]。
- 每段回答都附上引用和「有沒有根據」的自我評估，事實查核更容易 [05-asai2023-self-rag.pdf, §1, p.2]。
- 推論時可以調整檢索頻率和評分權重，不需要重新訓練 [05-asai2023-self-rag.pdf, §3.3, p.6]。
- 答對的題目中，只有 2% 的答案不在提供的文件裡 [05-asai2023-self-rag.pdf, App. C.1, p.20]。

## 代價與限制

- 要先用 GPT-4 標資料，再訓練兩個模型 [05-asai2023-self-rag.pdf, §3.2, p.4–5]。
- 每份文件都要平行產生一段回答，再用 beam search 挑選 [05-asai2023-self-rag.pdf, §3.3, p.6]。
- 仍可能產生沒有被引用完全支持的內容 [05-asai2023-self-rag.pdf, Ethical Concerns, p.11]。
- **權重的取捨**：重視「有根據」，引用 precision 會上升，但流暢度會下降 [05-asai2023-self-rag.pdf, §5.2, p.9–10]。
- **檢索頻率的取捨**：少檢索可以省時間，但在 PopQA 這類冷門知識題上表現下降較多 [05-asai2023-self-rag.pdf, §5.2, p.10]。

## 容易混淆：GraphRAG 的「self-reflection」

GraphRAG 也用了名為 self-reflection 的技巧，但兩者不同 [06-edge2024-graphrag.pdf, App. A.2, p.18]：

- **Self-RAG**：**訓練**模型產生 reflection tokens，在回答時自我評分 [05-asai2023-self-rag.pdf, §3.2, p.4]。
- **GraphRAG**：只是一種 **prompt 技巧**，抽完實體後再問 LLM「還有沒有漏掉的？」，不需要訓練 [06-edge2024-graphrag.pdf, App. A.2, p.18]。

## 出處

- [05-asai2023-self-rag.pdf](../sources/05-asai2023-self-rag.md)

## 相關頁面

- [Modular RAG](modular-rag.md)
- [Naive RAG](naive-rag.md)
- [Hallucination](../concepts/hallucination.md)
- [RAG 評估](../concepts/rag-evaluation.md)
- [RAG 進階技巧比較](../comparisons/rag-techniques.md)
- [術語表](../glossary.md)
