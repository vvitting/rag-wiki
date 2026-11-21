---
type: method
title: "Modular RAG"
tags: [method, rag, modular-rag, paradigm, adaptive-retrieval, iterative-retrieval]
sources: [02-gao2023-survey.pdf, 05-asai2023-self-rag.pdf]
updated: 2026-11-22
---

# Modular RAG

## 一句話說明

把 RAG 拆成一個個可以新增、替換、重新排列的模組，流程不再固定是「檢索一次、生成一次」[02-gao2023-survey.pdf, §II-C, p.4–5]。

## 跟 naive RAG 的差別

- Naive RAG 和 Advanced RAG 是固定的「Retrieve」加「Read」結構；Modular RAG 可以替換或重新設定模組 [02-gao2023-survey.pdf, §II-C, p.5]。
- Modular RAG 仍然建立在 Advanced 和 Naive RAG 的基本原理上 [02-gao2023-survey.pdf, §II-C, p.4]。
- 它同時支援依序處理，以及讓各元件端到端一起訓練 [02-gao2023-survey.pdf, §II-C, p.4]。

## 運作步驟

Modular RAG 沒有單一固定的步驟，而是從下面這些「模組」和「模式」裡組合 [02-gao2023-survey.pdf, §II-C, p.4–5]。

### 新模組（New Modules）

- **Search**：用 LLM 產生的程式碼和查詢語言，直接搜尋搜尋引擎、資料庫、knowledge graph 等來源 [02-gao2023-survey.pdf, §II-C, p.4]。
- **RAG-Fusion**：把使用者的問題擴展成多個角度的查詢，平行做向量搜尋，再重新排序 [02-gao2023-survey.pdf, §II-C, p.4]。
- **Memory**：利用 LLM 自己的記憶來引導檢索 [02-gao2023-survey.pdf, §II-C, p.4–5]。
- **Routing**：依照問題選擇最適合的路徑，例如做摘要、查特定資料庫，或合併多個資訊來源 [02-gao2023-survey.pdf, §II-C, p.5]。
- **Predict**：直接讓 LLM 產生 context，以減少重複和雜訊 [02-gao2023-survey.pdf, §II-C, p.5]。
- **Task Adapter**：讓 RAG 適應不同的下游任務 [02-gao2023-survey.pdf, §II-C, p.5]。

### 新模式（New Patterns）

- **Rewrite-Retrieve-Read**：先用 LLM 改寫查詢，再檢索、再閱讀 [02-gao2023-survey.pdf, §II-C, p.5]。
- **Generate-Read**：用 LLM 產生的內容取代傳統檢索 [02-gao2023-survey.pdf, §II-C, p.5]。
- **Hybrid retrieval**：結合關鍵字、語意、向量搜尋 [02-gao2023-survey.pdf, §II-C, p.5]。
- **Iterative 流程**：例如 ITER-RETGEN 的「Retrieve-Read-Retrieve-Read」[02-gao2023-survey.pdf, §II-C, p.5]。

### 三種進階檢索流程

最常見的是只檢索一次就生成，但對需要多步推理的複雜問題常常不夠 [02-gao2023-survey.pdf, §V, p.10]。

| 流程 | 做法 | 例子 | 出處 |
|---|---|---|---|
| Iterative（反覆） | 依照原始問題和目前已生成的內容，反覆搜尋知識庫 | ITER-RETGEN | [02-gao2023-survey.pdf, §V-A, p.10–11] |
| Recursive（遞迴） | 依照前一次的搜尋結果逐步修正查詢，把問題拆成子問題 | IRCoT、ToC | [02-gao2023-survey.pdf, §V-B, p.11; Fig.5, p.11] |
| Adaptive（自適應） | 讓 LLM 自己決定何時需要檢索、何時停止 | FLARE、Self-RAG | [02-gao2023-survey.pdf, §V-C, p.11; Fig.5, p.11] |

- Iterative 檢索的缺點：可能出現語意不連貫，也可能累積不相關的資訊 [02-gao2023-survey.pdf, §V-A, p.11]。
- FLARE 會監看生成時的信心（詞的機率），低於門檻時才觸發檢索 [02-gao2023-survey.pdf, §V-C, p.11–12]。
- Self-RAG 用「reflection tokens」讓模型檢視自己的輸出，自行決定何時檢索 [02-gao2023-survey.pdf, §V-C, p.12]。原始論文的完整說明見 [Self-RAG](self-rag.md)。
- **Adaptive retrieval 的實測**：在 Self-RAG 中，推論時完全不檢索，PopQA 會從 45.5 掉到 24.7；但 PubHealth 幾乎不受影響（73.5 vs 73.0）[05-asai2023-self-rag.pdf, Fig.3a, p.9]。可見不同任務對檢索的需求差很多。

## 優點

- 適應性和彈性更高 [02-gao2023-survey.pdf, §II-C, p.4]。
- 更容易和 fine-tuning、reinforcement learning 等其他技術結合 [02-gao2023-survey.pdf, §II-C, p.5]。

## 代價與限制

- 綜述沒有直接整理 Modular RAG 的代價；不過 iterative 檢索可能累積不相關的資訊 [02-gao2023-survey.pdf, §V-A, p.11]。

## 出處

- [02-gao2023-survey.pdf](../sources/02-gao2023-survey.md)

## 相關頁面

- [Naive RAG](naive-rag.md)
- [Advanced RAG](advanced-rag.md)
- [三種 RAG 典範比較](../comparisons/rag-paradigms.md)
- [Self-RAG](self-rag.md)
- [Query 優化](../concepts/query-optimization.md)
