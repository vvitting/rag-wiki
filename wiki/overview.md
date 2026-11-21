---
type: overview
title: "RAG 總覽"
tags: [rag, overview]
sources: [01-lewis2020-rag.pdf, 02-gao2023-survey.pdf, 03-anthropic-contextual-retrieval.pdf, 04-liu2023-lost-in-middle.pdf, 05-asai2023-self-rag.pdf, 06-edge2024-graphrag.pdf, 07-es2023-ragas.pdf]
updated: 2026-11-22
---

# RAG 總覽

> 本頁會在每次 ingest 時更新，結構對齊簡報。目前已 ingest：01–07（全部）。

## 1. 為什麼需要 RAG

- [LLM](glossary.md) 很強，但有三個主要問題：[hallucination](concepts/hallucination.md)、知識過時、推理過程不透明又無法追溯 [02-gao2023-survey.pdf, Abstract, p.1]。
- Language model 把知識存在參數裡，很難更新或擴充，也無法說明答案的出處 [01-lewis2020-rag.pdf, §1, p.1]。
- 遇到超出訓練資料範圍、或需要最新資訊的問題時，LLM 特別容易產生 hallucination [02-gao2023-survey.pdf, §I, p.1]。
- 兩個根本限制：LLM 不知道訓練之後才發生的事，也很難記住訓練資料中很少出現的知識 [07-es2023-ragas.pdf, §1, p.1]。

## 2. RAG 是什麼

- RAG 讓 LLM 先從外部知識庫找出相關資料，再根據資料回答，藉此減少錯誤內容 [02-gao2023-survey.pdf, §I, p.1]。

> ⚠️ **爭議／更新**：「減少錯誤內容」是 02 的整體概括 [02-gao2023-survey.pdf, §I, p.1]；但檢索不一定有幫助，答案文件放在中間，或加上檢索後，表現都可能比完全不給文件還差 [04-liu2023-lost-in-middle.pdf, §2.3, p.5] [05-asai2023-self-rag.pdf, Table 2, p.8]。詳見 [Hallucination](concepts/hallucination.md)、[Closed-book vs open-book](comparisons/closed-book-vs-open-book.md)。

- 最適合用 RAG 的情況：資料量太大，超過 LLM 一次能處理的 [context window](concepts/context-window.md) [06-edge2024-graphrag.pdf, §2.1, p.2]。
- 它結合了兩種記憶：模型參數裡的知識，以及外部的資料 [01-lewis2020-rag.pdf, Abstract, p.1] [02-gao2023-survey.pdf, §VIII, p.16]。詳見 [兩種記憶](concepts/parametric-vs-non-parametric-memory.md)。
- **比喻一**：閉書考 vs 開書考，RAG 屬於開書考 [01-lewis2020-rag.pdf, §4.1, p.5]。
- **比喻二**：RAG 像給模型一本量身訂做的教科書；fine-tuning 則像把知識內化 [02-gao2023-survey.pdf, §II-D, p.5]。詳見 [比喻集](analogies.md)、[RAG vs fine-tuning](comparisons/rag-vs-fine-tuning.md)。
- 這個名稱來自 Lewis et al. 2020 的論文 [01-lewis2020-rag.pdf, §1, p.2] [02-gao2023-survey.pdf, Ref. 4, p.17]，詳見 [來源頁](sources/01-lewis2020-rag.md) 和 [演進時間軸](comparisons/rag-timeline.md)。

## 3. RAG 怎麼運作

最基本的流程（[Naive RAG](methods/naive-rag.md)）有三步 [02-gao2023-survey.pdf, Fig.2, p.3]：

1. **Indexing**：把文件切成 [chunk](concepts/chunking.md)，用 [embedding](concepts/embedding.md) model 轉成向量，存進 vector database [02-gao2023-survey.pdf, §II-A, p.3]。
2. **Retrieval**：[Retriever](concepts/retriever.md) 把問題轉成向量，找出最相似的 top-k 個 chunk [02-gao2023-survey.pdf, §II-A, p.3]。
3. **Generation**：把問題和 chunk 組成 prompt，交給 LLM（[generator](concepts/generator.md)）寫出答案 [02-gao2023-survey.pdf, §II-A, p.3]。

原始的 RAG（2020）[02-gao2023-survey.pdf, Ref. 4, p.17] 也是「先查再寫」，但有兩點不同：每份文件分別交給 generator，再按檢索機率加權合併（marginalize），不是把所有文件串成一個長 prompt [01-lewis2020-rag.pdf, §2.1, p.3]；而且 retriever 和 generator 是一起訓練的 [01-lewis2020-rag.pdf, §2.4, p.3]。詳見 [原始 RAG](methods/original-rag.md)。

**放進 prompt 之後的陷阱**：LLM 最會利用開頭和結尾的資訊，放在中間的容易被忽略（[lost in the middle](concepts/lost-in-the-middle.md)）。GPT-3.5-Turbo 在 20 份文件中，答案在第 1 份時是 75.8%，在第 10 份時只有 53.8%，比完全不給文件的 56.1% 還低 [04-liu2023-lost-in-middle.pdf, Table 6, p.18; Table 1, p.5]。

## 4. 進階變體

- Naive RAG 有檢索不準、生成出錯、整合困難等問題，因此發展出 Advanced 和 Modular RAG [02-gao2023-survey.pdf, §II, p.2; §II-A, p.3]。詳見 [三種 RAG 典範比較](comparisons/rag-paradigms.md)。
- [Advanced RAG](methods/advanced-rag.md)：檢索前改善 index 和 [query](concepts/query-optimization.md)，檢索後做 [reranking](concepts/reranking.md) 和壓縮 [02-gao2023-survey.pdf, §II-B, p.4]。
- [Modular RAG](methods/modular-rag.md)：把流程拆成模組，支援 iterative、recursive、adaptive 檢索 [02-gao2023-survey.pdf, §II-C, p.4–5; Fig.5, p.11]。

- **[Contextual Retrieval](methods/contextual-retrieval.md)**：切塊會讓 chunk 失去上下文，所以先用 LLM 為每個 chunk 補上說明；檢索失敗率降低 49%，再加上 reranking 降低 67% [03-anthropic-contextual-retrieval.pdf, p.2, p.4–5]。
- **Hybrid retrieval**：embedding（找意思）加上 BM25（找精確字串），比只用 embedding 好 [03-anthropic-contextual-retrieval.pdf, p.3, p.11]。
- **Reranking**：把最相關的文件排到前面，同時應對 lost in the middle [04-liu2023-lost-in-middle.pdf, §5, p.10]；03 的實驗中，再加上 reranking 讓檢索失敗率降到 1.9% [03-anthropic-contextual-retrieval.pdf, p.10]。

> 各種技巧的整理：[RAG 進階技巧比較](comparisons/rag-techniques.md)

- **[Self-RAG](methods/self-rag.md)**：不是每個問題都需要查資料。Self-RAG 訓練模型自己決定何時檢索，並為文件和自己的回答打分數 [05-asai2023-self-rag.pdf, Abstract, p.1]；7B 和 13B 的 Self-RAG 在多個任務上勝過 ChatGPT [05-asai2023-self-rag.pdf, §5.1, p.8]。

- **[GraphRAG](methods/graphrag.md)**：一般 RAG 擅長找特定事實，卻回答不了「這批資料的主要主題是什麼？」。GraphRAG 先用 LLM 建 knowledge graph 和社群摘要，在這類全局問題上，答案的全面性勝率達 72%–83% [06-edge2024-graphrag.pdf, Abstract, p.1; §5.1, p.9]。

## 5. 怎麼評估

- 要分開評估「找得好不好」（retrieval quality）和「寫得好不好」（generation quality）[02-gao2023-survey.pdf, §VI-B, p.12]。
- 三個品質分數是 context relevance、answer faithfulness、answer relevance [02-gao2023-survey.pdf, §VI-C, p.12]。詳見 [RAG 評估](concepts/rag-evaluation.md)。
- 沒有標準答案的問題（例如全局問題），可以讓 LLM 當評審，兩兩比較答案（LLM-as-a-judge）[06-edge2024-graphrag.pdf, §2.4, p.4]。
- 原始 RAG 用 Exact Match 評估問答，並用人工評估比較事實性 [01-lewis2020-rag.pdf, §3.1, p.4; §3.3, p.5]。

- **[RAGAS](concepts/ragas.md)**：不需要標準答案，讓 LLM 分步驟計算三個分數；faithfulness 和人類判斷的一致度達 0.95 [07-es2023-ragas.pdf, Abstract, p.1; Table 1, p.5]。
- **小心 LLM 評審**：直接讓 ChatGPT 挑比較好的答案，和人類判斷一致的比例只有 0.40–0.54 [07-es2023-ragas.pdf, Table 1, p.5]。拆成小步驟、重複多次、交叉驗證會比較可靠，詳見 [RAG 評估](concepts/rag-evaluation.md) [06-edge2024-graphrag.pdf, §3.3, p.8]。

## 6. 總結

- 在 open-domain QA（例如 NQ）上，RAG 讓小模型也能勝過大很多的純參數模型 [01-lewis2020-rag.pdf, App. G, p.19]。
- 更新知識只要換掉 index，不用重新訓練 [01-lewis2020-rag.pdf, §4.5, p.8]。
- RAG 和 fine-tuning 可以互補，不是二選一 [02-gao2023-survey.pdf, §II-D, p.5]。
- 即使 LLM 能讀很長的 context，RAG 在效率和可驗證性上仍有優勢 [02-gao2023-survey.pdf, §VII-A, p.14]。
- 反過來說，知識庫小於 200,000 tokens（約 500 頁）時，不一定需要 RAG，直接全部放進 prompt 可能就夠了 [03-anthropic-contextual-retrieval.pdf, p.2]。這點和上一條有 ⚠️ 爭議，詳見 [Context window](concepts/context-window.md)。
- **檢索不一定有幫助**：ChatGPT 加上檢索後，PubHealth 從 70.1 降到 54.7 [05-asai2023-self-rag.pdf, Table 2, p.8]；所以「什麼時候該查」也是一個問題 [05-asai2023-self-rag.pdf, §1, p.1]。
- **放得進去，不代表用得好**：支援長 context 的模型，不一定比較會用 context [04-liu2023-lost-in-middle.pdf, §2.3, p.5]。文件也不是越多越好：取 50 份和取 20 份相比，只多進步約 1%–1.5% [04-liu2023-lost-in-middle.pdf, §5, p.10]。
- 但 RAG 不是萬靈丹：外部資料本身可能有錯 [01-lewis2020-rag.pdf, Broader Impact, p.10]，雜訊或互相矛盾的資訊也會影響輸出品質 [02-gao2023-survey.pdf, §VII-B, p.14]。

## 相關頁面
- [目錄](index.md)
- [術語表](glossary.md)
- [比喻集](analogies.md)
- [Closed-book vs open-book](comparisons/closed-book-vs-open-book.md)
- [RAG 演進時間軸](comparisons/rag-timeline.md)
