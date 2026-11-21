---
type: concept
title: "Generator（生成器）"
tags: [concept, generation, bart, seq2seq]
sources: [01-lewis2020-rag.pdf, 02-gao2023-survey.pdf]
updated: 2026-11-22
---

# Generator

## 白話說明

Generator 是 RAG 裡負責「寫答案」的部分：它讀了問題和 [retriever](retriever.md) 找來的文件之後，一個 token 接一個 token 地產生答案 [01-lewis2020-rag.pdf, §2, p.2–3]。

## 為什麼重要

- Generator 可以「寫」出答案，不只是從文件裡「挑」一段出來；所以即使文件只含線索、沒有原句，它還是有機會寫出正確答案 [01-lewis2020-rag.pdf, §4.1, p.5]。
- 檢索到的文件都沒有正確答案時，RAG 在 NQ 上仍有 11.8% 答對；只能挑原句的 extractive 模型則是 0% [01-lewis2020-rag.pdf, §4.1, p.6]。

## 運作方式（以原始 RAG 為例）

- 原始 RAG 用 BART-large 當 generator，它是一個有 400M 參數的預訓練 seq2seq transformer [01-lewis2020-rag.pdf, §2.3, p.3]。
- 理論上任何 encoder-decoder 模型都可以當 generator [01-lewis2020-rag.pdf, §2.3, p.3]。
- 把資料交給 generator 的方式很簡單：直接把問題和檢索到的文件串接（concatenate）在一起 [01-lewis2020-rag.pdf, §2.3, p.3]。
- Generator 的參數就是 RAG 的 [parametric memory](parametric-vs-non-parametric-memory.md) [01-lewis2020-rag.pdf, §2.3, p.3]。

### Extractive vs generative（abstractive）

| | Extractive QA | Generative QA（RAG） |
|---|---|---|
| 答案怎麼來 | 從檢索到的文件中挑出一段 [01-lewis2020-rag.pdf, §3.1, p.4] | 自由生成文字 [01-lewis2020-rag.pdf, §3.2, p.4] |
| 文件只有線索、沒有原句時 | 答不出來 [01-lewis2020-rag.pdf, §4.1, p.5] | 仍有機會答對 [01-lewis2020-rag.pdf, §4.1, p.5–6] |

### 在 LLM 時代：generator 就是 LLM

- 在 [Naive RAG](../methods/naive-rag.md) 中，問題和選出的文件會組成一個 prompt，交給 LLM 產生回答 [02-gao2023-survey.pdf, §II-A, p.3]。
- LLM 可以使用自己的 parametric knowledge，也可以被要求只根據提供的文件回答 [02-gao2023-survey.pdf, §II-A, p.3]。
- 把檢索到的資訊全部直接丟給 LLM 並不是好做法；檢索後通常要先整理內容（[reranking](reranking.md)、壓縮），或調整 LLM 本身 [02-gao2023-survey.pdf, §IV, p.10]。
- **調整 LLM**：針對特定情境 fine-tune，可以補充領域知識，也能讓輸出符合特定格式或風格 [02-gao2023-survey.pdf, §IV-B, p.10]。

## 各論文怎麼說

- **[01-lewis2020-rag.pdf](../sources/01-lewis2020-rag.md)**：和只用 BART、不檢索的版本相比，RAG 寫出的內容更符合事實、更具體，也更多樣 [01-lewis2020-rag.pdf, Abstract, p.1]。
- **[02-gao2023-survey.pdf](../sources/02-gao2023-survey.md)**：生成時可能出現 hallucination、離題、有害或偏見的內容；也可能過度依賴檢索內容，只是照抄 [02-gao2023-survey.pdf, §II-A, p.3]。

## 相關頁面

- [Retriever](retriever.md)
- [Hallucination](hallucination.md)
- [原始 RAG（方法）](../methods/original-rag.md)
- [術語表](../glossary.md)
