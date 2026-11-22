---
page: wiki/overview.md
---
# 證據卡：RAG 總覽

## 重點摘錄
> - [LLM](glossary.md) 很強，但有三個主要問題：[hallucination](concepts/hallucination.md)、知識過時、推理過程不透明又無法追溯 [02-gao2023-survey.pdf, Abstract, p.1]。
> - Language model 把知識存在參數裡，很難更新或擴充，也無法說明答案的出處 [01-lewis2020-rag.pdf, §1, p.1]。
> - 兩個根本限制：LLM 不知道訓練之後才發生的事，也很難記住訓練資料中很少出現的知識 [07-es2023-ragas.pdf, §1, p.1]。
> - RAG 讓 LLM 先從外部知識庫找出相關資料，再根據資料回答，藉此減少錯誤內容 [02-gao2023-survey.pdf, §I, p.1]。
> - 它結合了兩種記憶：模型參數裡的知識，以及外部的資料 [01-lewis2020-rag.pdf, Abstract, p.1] [02-gao2023-survey.pdf, §VIII, p.16]。詳見 [兩種記憶](concepts/parametric-vs-non-parametric-memory.md)。
> - **比喻一**：閉書考 vs 開書考，RAG 屬於開書考 [01-lewis2020-rag.pdf, §4.1, p.5]。
> - 這個名稱來自 Lewis et al. 2020 的論文 [01-lewis2020-rag.pdf, §1, p.2] [02-gao2023-survey.pdf, Ref. 4, p.17]，詳見 [來源頁](sources/01-lewis2020-rag.md) 和 [演進時間軸](comparisons/rag-timeline.md)。
> 最基本的流程（[Naive RAG](methods/naive-rag.md)）有三步 [02-gao2023-survey.pdf, Fig.2, p.3]：
> 1. **Indexing**：把文件切成 [chunk](concepts/chunking.md)，用 [embedding](concepts/embedding.md) model 轉成向量，存進 [vector database](glossary.md) [02-gao2023-survey.pdf, §II-A, p.3]。
> 2. **Retrieval**：[Retriever](concepts/retriever.md) 把問題轉成向量，找出最相似的 [top-k](glossary.md) 個 chunk [02-gao2023-survey.pdf, §II-A, p.3]。
> 3. **Generation**：把問題和 chunk 組成 [prompt](glossary.md)，交給 LLM（[generator](concepts/generator.md)）寫出答案 [02-gao2023-survey.pdf, §II-A, p.3]。
> - Naive RAG 有檢索不準、生成出錯、整合困難等問題，因此發展出 Advanced 和 Modular RAG [02-gao2023-survey.pdf, §II, p.2; §II-A, p.3]。詳見 [三種 RAG 典範比較](comparisons/rag-paradigms.md)。
> - 要分開評估「找得好不好」（retrieval quality）和「寫得好不好」（generation quality）[02-gao2023-survey.pdf, §VI-B, p.12]。
> - 三個品質分數是 context relevance、answer faithfulness、answer relevance [02-gao2023-survey.pdf, §VI-C, p.12]。詳見 [RAG 評估](concepts/rag-evaluation.md)。
> - 更新知識只要換掉 index，不用重新訓練 [01-lewis2020-rag.pdf, §4.5, p.8]。
> - 但 RAG 不是萬靈丹：外部資料本身可能有錯 [01-lewis2020-rag.pdf, Broader Impact, p.10]，雜訊或互相矛盾的資訊也會影響輸出品質 [02-gao2023-survey.pdf, §VII-B, p.14]。

## 數字
> **放進 prompt 之後的陷阱**：LLM 最會利用開頭和結尾的資訊，放在中間的容易被忽略（[lost in the middle](concepts/lost-in-the-middle.md)）。GPT-3.5-Turbo 在 20 份文件中，答案在第 1 份時是 75.8%，在第 10 份時只有 53.8%，比完全不給文件的 56.1% 還低 [04-liu2023-lost-in-middle.pdf, Table 6, p.18; Table 1, p.5]。
> - **檢索不一定有幫助**：ChatGPT 加上檢索後，PubHealth 從 70.1 降到 54.7 [05-asai2023-self-rag.pdf, Table 2, p.8]；所以「什麼時候該查」也是一個問題 [05-asai2023-self-rag.pdf, §1, p.1]。
> - **放得進去，不代表用得好**：支援長 context 的模型，不一定比較會用 context [04-liu2023-lost-in-middle.pdf, §2.3, p.5]。文件也不是越多越好：取 50 份和取 20 份相比，只多進步約 1%–1.5% [04-liu2023-lost-in-middle.pdf, §5, p.10]。

## ⚠️ 爭議
> > ⚠️ **爭議／更新**：「減少錯誤內容」是 02 的整體概括 [02-gao2023-survey.pdf, §I, p.1]；但檢索不一定有幫助，答案文件放在中間，或加上檢索後，表現都可能比完全不給文件還差 [04-liu2023-lost-in-middle.pdf, §2.3, p.5] [05-asai2023-self-rag.pdf, Table 2, p.8]。詳見 [Hallucination](concepts/hallucination.md)、[Closed-book vs open-book](comparisons/closed-book-vs-open-book.md)。

## 可以用在
- 為什麼需要（01、02）：LLM 的三個問題、知識存在參數裡
- 是什麼（03）：定義、兩種記憶、2020 年命名
- 怎麼運作（06）：三步驟與流程圖
- 進階變體（10）：為什麼會有進階版
- 怎麼評估（12）：兩個評估目標、三個品質分數
- 總結（13）：陷阱、檢索不一定有幫助、不是萬靈丹
