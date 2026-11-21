---
type: source
title: "Retrieval-Augmented Generation for Large Language Models: A Survey"
raw: 02-gao2023-survey.pdf
authors: [Yunfan Gao, Yun Xiong, Xinyu Gao, Kangxiang Jia, Jinliu Pan, Yuxi Bi, Yi Dai, Jiawei Sun, Meng Wang, Haofen Wang]
year: 2023
tags: [rag, survey, naive-rag, advanced-rag, modular-rag, evaluation]
sources: [02-gao2023-survey.pdf, 01-lewis2020-rag.pdf, 03-anthropic-contextual-retrieval.pdf, 04-liu2023-lost-in-middle.pdf, 05-asai2023-self-rag.pdf, 06-edge2024-graphrag.pdf, 07-es2023-ragas.pdf]
updated: 2026-11-22
---

# Retrieval-Augmented Generation for Large Language Models: A Survey（Gao et al., 2023，RAG 綜述）

這是一篇整理 RAG 研究全貌的綜述，作者來自同濟大學與復旦大學 [02-gao2023-survey.pdf, p.1]。raw 檔是 arXiv 2312.10997 的 v5 版（2024 年 3 月 27 日）[02-gao2023-survey.pdf, p.1]。

## 一句話摘要

把 100 多篇 RAG 研究整理成三種典範：[Naive RAG](../methods/naive-rag.md)、[Advanced RAG](../methods/advanced-rag.md)、[Modular RAG](../methods/modular-rag.md)；並從「Retrieval、Generation、Augmentation」三個面向分析關鍵技術，最後整理評估方法和未來挑戰 [02-gao2023-survey.pdf, §I, p.1]。

## 這篇想解決什麼問題

- LLM 雖然很強，但有 hallucination、知識過時、推理過程不透明又無法追溯等問題 [02-gao2023-survey.pdf, Abstract, p.1]。
- RAG 發展很快，卻缺少一份系統性的整理，讓人看清它的整體走向 [02-gao2023-survey.pdf, §I, p.1]。
- 既有研究多半聚焦在方法，比較少討論該怎麼評估 RAG [02-gao2023-survey.pdf, §I, p.1]。

## 核心內容

### RAG 的發展階段

- RAG 剛出現時，正好是 Transformer 興起的時候，研究重點是透過預訓練模型（PTM）把額外知識加進 language model [02-gao2023-survey.pdf, §I, p.1]。
- ChatGPT 出現後，LLM 展現出強大的 in-context learning 能力，RAG 研究轉向在推論（inference）階段提供更好的資訊給 LLM [02-gao2023-survey.pdf, §I, p.1]。
- 後來的研究不再只限於推論階段，開始更多地結合 LLM 的 fine-tuning [02-gao2023-survey.pdf, §I, p.1]。
- 詳見 [RAG 演進時間軸](../comparisons/rag-timeline.md)。

### 三種典範

- **Naive RAG**：indexing → retrieval → generation 三步驟，也被稱為「Retrieve-Read」框架 [02-gao2023-survey.pdf, §II-A, p.3]。
- **Advanced RAG**：在 Naive RAG 的基礎上加入 pre-retrieval 和 post-retrieval 的優化策略 [02-gao2023-survey.pdf, §II-B, p.3]。
- **Modular RAG**：可以新增、替換、重新安排模組，流程不再固定 [02-gao2023-survey.pdf, §II-C, p.4–5]。
- 詳見 [三種 RAG 典範比較](../comparisons/rag-paradigms.md)。

### RAG vs fine-tuning vs prompt engineering

- 作者用「需要多少外部知識」和「需要改動模型多少」兩個維度，比較這三種方法 [02-gao2023-survey.pdf, §II-D, p.5; Fig.4, p.7]。
- 詳見 [RAG vs fine-tuning](../comparisons/rag-vs-fine-tuning.md)。

### 三大技術面向

- **Retrieval**：檢索來源、檢索單位（granularity）、indexing 優化（[chunking](../concepts/chunking.md)、metadata、結構化 index）、[query 優化](../concepts/query-optimization.md)、[embedding](../concepts/embedding.md)、adapter [02-gao2023-survey.pdf, §III, p.5–10]。
- **Generation**：檢索後的內容整理（[reranking](../concepts/reranking.md)、context 壓縮）與 LLM fine-tuning [02-gao2023-survey.pdf, §IV, p.10]。
- **Augmentation**：除了檢索一次之外，還有 iterative、recursive、adaptive 三種檢索流程 [02-gao2023-survey.pdf, §V, p.10–12; Fig.5, p.11]。

### 評估

- 整理了 26 種任務、近 50 個資料集，以及評估目標、指標、benchmark 和工具 [02-gao2023-survey.pdf, §I, p.2]。
- 詳見 [RAG 評估](../concepts/rag-evaluation.md)。

## 關鍵結果（數字務必附出處）

這是綜述，沒有自己的實驗；下面的數字都是作者整理或引用其他研究得到的 [02-gao2023-survey.pdf, §I, p.1]。

- 從 100 多篇 RAG 研究中整理出三種典範 [02-gao2023-survey.pdf, §I, p.1]。
- 評估部分涵蓋 26 種任務、近 50 個資料集 [02-gao2023-survey.pdf, §I, p.2]。
- 最常見的 chunking 方式是依固定 token 數切分，例如 100、256、512 [02-gao2023-survey.pdf, §III-B, p.8]。
- Hugging Face 的 MTEB leaderboard 用 8 種任務、58 個資料集評估 embedding model；C-MTEB 則專門評估中文能力，涵蓋 6 種任務、35 個資料集 [02-gao2023-survey.pdf, §III-D, p.9]。
- 當時的 LLM 已經能處理超過 200,000 tokens 的 context [02-gao2023-survey.pdf, §VII-A, p.14]。
- 作者引用 Cuconasu et al. 的研究：放入不相關的文件，竟然能讓準確率提高超過 30% [02-gao2023-survey.pdf, §VII-B, p.14]。
- 作者引用的研究顯示，在多種 knowledge-intensive 任務上，RAG 一致勝過 unsupervised fine-tuning [02-gao2023-survey.pdf, §II-D, p.5]。

## 限制與後續爭議

- **評估還不成熟**：作者說，現有的指標都是從相關研究借來的傳統指標，還不是成熟或標準化的 RAG 評估方式 [02-gao2023-survey.pdf, §VI-C, p.14]。
- **仍待解決的挑戰**：RAG 與長 context 的關係、robustness、和 fine-tuning 混合使用、scaling law、能否上線使用（production-ready）、多模態 [02-gao2023-survey.pdf, §VII, p.14–16]。
- **原文的文字瑕疵**：有重複的句子，例如「it requires additional effort to build, validate, and maintain structured databases」連續出現兩次 [02-gao2023-survey.pdf, §III-A, p.7]。這不影響內容，但引用原句時要留意。

> ⚠️ **爭議／更新**：本篇說 Naive RAG 是「最早的方法」，在 ChatGPT 普及後不久受到重視 [02-gao2023-survey.pdf, §II-A, p.2–3]；但 RAG 這個名稱和「先檢索、再生成」的架構早在 2020 年就出現了 [01-lewis2020-rag.pdf, §1, p.2] [02-gao2023-survey.pdf, Ref. 4, p.17]，而本篇把這類早期研究歸在「透過預訓練模型加強」的階段 [02-gao2023-survey.pdf, §I, p.1]。詳見 [Naive RAG](../methods/naive-rag.md)。

> ⚠️ **爭議／更新**：本篇把 reranking 列為 Advanced RAG 的關鍵策略 [02-gao2023-survey.pdf, §II-B, p.4]，[03-anthropic-contextual-retrieval.pdf, p.11] 的實驗也支持；但 [01-lewis2020-rag.pdf, §4.1, p.5] 認為，要達到當時的最佳表現並不需要 re-ranker。詳見 [Reranking](../concepts/reranking.md)。

> ⚠️ **爭議／更新**：本篇認為即使 LLM 能處理長 context，RAG 仍無可取代 [02-gao2023-survey.pdf, §VII-A, p.14]；[03-anthropic-contextual-retrieval.pdf, p.2] 則說，知識庫小於 200,000 tokens 時可以直接全放進 prompt，不需要 RAG。詳見 [Context window](../concepts/context-window.md)。

> ⚠️ **爭議／更新**：本篇把段落摘要、階層式摘要 index 列為優化方法 [02-gao2023-survey.pdf, §III-B, p.8]；[03-anthropic-contextual-retrieval.pdf, p.5] 實測通用文件摘要提升非常有限，以摘要為基礎的 indexing 表現很差。詳見 [Chunking](../concepts/chunking.md)。

> ⚠️ **爭議／更新**：本篇說「盡量多檢索文件」是常見的誤解，太多 context 會帶來雜訊 [02-gao2023-survey.pdf, §IV-A, p.10]；但 [01-lewis2020-rag.pdf, §4.5, p.8] 發現 RAG-Sequence 取越多份文件，NQ 表現就越好。[04-liu2023-lost-in-middle.pdf, §5, p.10] 的結果支持本篇：在 LLM 上，取 20 份以上幾乎不再進步。詳見 [Context window](../concepts/context-window.md)。

- **RAGAS 的原始論文已經 ingest**：本篇對 RAGAS 的描述（用 LLM 評判三個品質分數、answer relevance 用 cosine similarity）[02-gao2023-survey.pdf, §VI-D, p.14; Table IV, p.15] 和原始論文一致 [07-es2023-ragas.pdf, §3, p.3]，詳見 [07 來源頁](07-es2023-ragas.md)。
- **本篇的三個品質分數不適用於全局問題**：GraphRAG 論文認為 context relevance、faithfulness、answer relevance 只適用於一般 vector RAG，和全局理解類的問題無關 [06-edge2024-graphrag.pdf, §2.4, p.4]。詳見 [RAG 評估](../concepts/rag-evaluation.md)。
- **本篇對 Self-RAG 的描述與原始論文一致**：本篇說 Self-RAG 用 retrieve 和 critic 兩類 reflection tokens [02-gao2023-survey.pdf, §V-C, p.12]，和原始論文的定義相符 [05-asai2023-self-rag.pdf, Table 1, p.4]，詳見 [05 來源頁](05-asai2023-self-rag.md)。
- **本篇引用的原始研究已經 ingest**：本篇對 lost in the middle 的描述 [02-gao2023-survey.pdf, §IV-A, p.10]，引用的是 04 這篇 [02-gao2023-survey.pdf, Ref. 98, p.19]，詳見 [04 來源頁](04-liu2023-lost-in-middle.md)。

## 關鍵圖表說明

- **Fig.1**：RAG 研究的技術樹，分成 pre-training、fine-tuning、inference 三個階段 [02-gao2023-survey.pdf, Fig.1, p.2]。
- **Fig.2**：RAG 用在問答時的典型流程：indexing、retrieval、generation 三步 [02-gao2023-survey.pdf, Fig.2, p.3]。**很適合當簡報的流程圖。**
- **Fig.3**：Naive、Advanced、Modular RAG 三種典範的比較圖 [02-gao2023-survey.pdf, Fig.3, p.4]。**適合放在簡報的「進階變體」段落。**
- **Fig.4**：RAG、fine-tuning、prompt engineering 的四象限比較 [02-gao2023-survey.pdf, Fig.4, p.7]。
- **Fig.5**：iterative、recursive、adaptive 三種檢索流程 [02-gao2023-survey.pdf, Fig.5, p.11]。
- **Table I**：各種 RAG 方法的檢索來源、檢索單位、在哪個階段加強、檢索流程 [02-gao2023-survey.pdf, Table I, p.6]。
- **Table II**：RAG 的下游任務與資料集 [02-gao2023-survey.pdf, Table II, p.13]。
- **Table III**：各評估面向適用的指標 [02-gao2023-survey.pdf, Table III, p.14]。
- **Table IV**：RGB、RAGAS、ARES 等評估框架的整理 [02-gao2023-survey.pdf, Table IV, p.15]。

## 對初學者的重點

1. RAG 最基本的流程就是三步：把文件切塊存起來、找出相關的塊、交給 LLM 寫答案 [02-gao2023-survey.pdf, Fig.2, p.3]。
2. 最基本的做法（Naive RAG）有不少問題，所以才發展出 Advanced 和 Modular RAG [02-gao2023-survey.pdf, §II, p.2]。
3. RAG 像是給模型一本量身訂做的教科書；fine-tuning 則像學生花時間把知識內化 [02-gao2023-survey.pdf, §II-D, p.5]。
4. 評估 RAG 要分開看「找得好不好」和「寫得好不好」[02-gao2023-survey.pdf, §VI-B, p.12]。

## 相關頁面

- [Naive RAG](../methods/naive-rag.md)
- [Advanced RAG](../methods/advanced-rag.md)
- [Modular RAG](../methods/modular-rag.md)
- [三種 RAG 典範比較](../comparisons/rag-paradigms.md)
- [RAG vs fine-tuning](../comparisons/rag-vs-fine-tuning.md)
- [RAG 演進時間軸](../comparisons/rag-timeline.md)
- [RAG 評估](../concepts/rag-evaluation.md)
- [01 原始 RAG 論文](01-lewis2020-rag.md)
- [術語表](../glossary.md)
