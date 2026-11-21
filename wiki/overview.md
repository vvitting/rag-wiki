---
type: overview
title: "RAG 總覽"
tags: [rag, overview]
sources: [01-lewis2020-rag.pdf, 02-gao2023-survey.pdf]
updated: 2026-11-22
---

# RAG 總覽

> 本頁會在每次 ingest 時更新，結構對齊簡報。目前已 ingest：01、02。

## 1. 為什麼需要 RAG

- LLM 很強，但有三個主要問題：hallucination、知識過時、推理過程不透明又無法追溯 [02-gao2023-survey.pdf, Abstract, p.1]。
- Language model 把知識存在參數裡，很難更新或擴充，也無法說明答案的出處 [01-lewis2020-rag.pdf, §1, p.1]。
- 遇到超出訓練資料範圍、或需要最新資訊的問題時，LLM 特別容易產生 [hallucination](concepts/hallucination.md) [02-gao2023-survey.pdf, §I, p.1]。

## 2. RAG 是什麼

- RAG 讓 LLM 先從外部知識庫找出相關資料，再根據資料回答，藉此減少錯誤內容 [02-gao2023-survey.pdf, §I, p.1]。
- 它結合了兩種記憶：模型參數裡的知識，以及外部的資料 [01-lewis2020-rag.pdf, Abstract, p.1; 02-gao2023-survey.pdf, §VIII, p.16]。詳見 [兩種記憶](concepts/parametric-vs-non-parametric-memory.md)。
- **比喻一**：閉書考 vs 開書考，RAG 屬於開書考 [01-lewis2020-rag.pdf, §4.1, p.5]。
- **比喻二**：RAG 像給模型一本量身訂做的教科書；fine-tuning 則像把知識內化 [02-gao2023-survey.pdf, §II-D, p.5]。詳見 [比喻集](analogies.md)、[RAG vs fine-tuning](comparisons/rag-vs-fine-tuning.md)。
- 這個名稱來自 Lewis et al. 2020 的論文 [01-lewis2020-rag.pdf, §1, p.2]，詳見 [來源頁](sources/01-lewis2020-rag.md) 和 [演進時間軸](comparisons/rag-timeline.md)。

## 3. RAG 怎麼運作

最基本的流程（[Naive RAG](methods/naive-rag.md)）有三步 [02-gao2023-survey.pdf, Fig.2, p.3]：

1. **Indexing**：把文件切成 [chunk](concepts/chunking.md)，用 [embedding](concepts/embedding.md) model 轉成向量，存進 vector database [02-gao2023-survey.pdf, §II-A, p.3]。
2. **Retrieval**：[Retriever](concepts/retriever.md) 把問題轉成向量，找出最相似的 top-k 個 chunk [02-gao2023-survey.pdf, §II-A, p.3]。
3. **Generation**：把問題和 chunk 組成 prompt，交給 LLM（[generator](concepts/generator.md)）寫出答案 [02-gao2023-survey.pdf, §II-A, p.3]。

原始的 RAG（2020）流程相同，但 retriever 和 generator 是一起訓練的，詳見 [原始 RAG](methods/original-rag.md) [01-lewis2020-rag.pdf, §2.4, p.3]。

## 4. 進階變體

- Naive RAG 有檢索不準、生成出錯、整合困難等問題，因此發展出 Advanced 和 Modular RAG [02-gao2023-survey.pdf, §II, p.2; §II-A, p.3]。詳見 [三種 RAG 典範比較](comparisons/rag-paradigms.md)。
- [Advanced RAG](methods/advanced-rag.md)：檢索前改善 index 和 [query](concepts/query-optimization.md)，檢索後做 [reranking](concepts/reranking.md) 和壓縮 [02-gao2023-survey.pdf, §II-B, p.4]。
- [Modular RAG](methods/modular-rag.md)：把流程拆成模組，支援 iterative、recursive、adaptive 檢索 [02-gao2023-survey.pdf, §II-C, p.4–5; Fig.5, p.11]。

> 特定方法（Contextual Retrieval、Self-RAG、GraphRAG）將在 ingest 03、05、06 後補充。

## 5. 怎麼評估

- 要分開評估「找得好不好」（retrieval quality）和「寫得好不好」（generation quality）[02-gao2023-survey.pdf, §VI-B, p.12]。
- 三個品質分數是 context relevance、answer faithfulness、answer relevance [02-gao2023-survey.pdf, §VI-C, p.12]。詳見 [RAG 評估](concepts/rag-evaluation.md)。
- 原始 RAG 用 Exact Match 評估問答，並用人工評估比較事實性 [01-lewis2020-rag.pdf, §3.1, p.4; §3.3, p.5]。

> RAGAS 的原始論文將在 ingest 07 後補充。

## 6. 總結

- RAG 讓小模型也能勝過大很多的純參數模型 [01-lewis2020-rag.pdf, App. G, p.19]。
- 更新知識只要換掉 index，不用重新訓練 [01-lewis2020-rag.pdf, §4.5, p.8]。
- RAG 和 fine-tuning 可以互補，不是二選一 [02-gao2023-survey.pdf, §II-D, p.5]。
- 即使 LLM 能讀很長的 context，RAG 在效率和可驗證性上仍有優勢 [02-gao2023-survey.pdf, §VII-A, p.14]。
- 但 RAG 不是萬靈丹：外部資料本身可能有錯 [01-lewis2020-rag.pdf, Broader Impact, p.10]，雜訊或互相矛盾的資訊也會影響輸出品質 [02-gao2023-survey.pdf, §VII-B, p.14]。

## 相關頁面
- [目錄](index.md)
- [術語表](glossary.md)
- [比喻集](analogies.md)
- [Closed-book vs open-book](comparisons/closed-book-vs-open-book.md)
- [RAG 演進時間軸](comparisons/rag-timeline.md)
