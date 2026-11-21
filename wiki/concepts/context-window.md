---
type: concept
title: "Context window 與「放多少文件」"
tags: [concept, context-window, long-context, lost-in-the-middle]
sources: [02-gao2023-survey.pdf, 01-lewis2020-rag.pdf]
updated: 2026-11-22
---

# Context window 與「放多少文件」

## 白話說明

LLM 一次能讀進去的文字量是有上限的。為了配合這個 context 限制，RAG 會把文件切成較小的 [chunk](chunking.md) [02-gao2023-survey.pdf, §II-A, p.3]。

Context window 的正式定義，目前在 raw/ 裡還找不到出處 [待補來源]。

## 為什麼重要

- 不是放越多文件越好：多餘的資訊會干擾 LLM 生成答案，太長的 context 還可能讓 LLM 遇到「Lost in the middle」問題 [02-gao2023-survey.pdf, §IV-A, p.10]。
- 綜述的描述是：LLM 和人一樣，傾向只注意長文的開頭和結尾，忘了中間 [02-gao2023-survey.pdf, §IV-A, p.10]。Lost in the middle 的原始研究會在 ingest 04 時補充。

## 運作方式：怎麼控制 context

- **Reranking**：把最相關的內容排到前面或 prompt 的頭尾 [02-gao2023-survey.pdf, §II-B, p.4]。詳見 [Reranking](reranking.md)。
- **Context 壓縮**：例如 LLMLingua 用 GPT-2 Small、LLaMA-7B 這類小模型刪掉不重要的 token [02-gao2023-survey.pdf, §IV-A, p.10]。
- **減少文件數量**：讓 LLM 先評估檢索到的內容，濾掉相關性低的文件 [02-gao2023-survey.pdf, §IV-A, p.10]。

## 「放越多文件越好」嗎？

> ⚠️ **爭議／更新**：[01-lewis2020-rag.pdf, §4.5, p.8] 和 [02-gao2023-survey.pdf, §IV-A, p.10; §VII-B, p.14] 的三個說法並不一致：
> - [01-lewis2020-rag.pdf, §4.5, p.8; Fig.3, p.8]：RAG-Sequence 在測試時取越多份文件，NQ 表現就越好；RAG-Token 則在 10 份時最好。
> - [02-gao2023-survey.pdf, §IV-A, p.10]：「盡量多檢索、全部串成長 prompt」是 RAG 的常見誤解，過多的 context 會帶來雜訊。
> - [02-gao2023-survey.pdf, §VII-B, p.14]：綜述引用 Cuconasu et al. 的研究，加入不相關的文件反而讓準確率提高超過 30%。

可能的解讀是：01 的生成模型是 BART，而且文件會先經過 marginalize 加權，並不是全部串成一個長 prompt [01-lewis2020-rag.pdf, §2.1, p.3]；02 討論的則是把文件串接後交給 LLM 的情境 [02-gao2023-survey.pdf, §IV-A, p.10]。

## RAG 和 long context 的關係

- 當時的 LLM 已經能處理超過 200,000 tokens 的 context，於是有人問：還需要 RAG 嗎？[02-gao2023-survey.pdf, §VII-A, p.14]
- 綜述認為 RAG 仍然無可取代 [02-gao2023-survey.pdf, §VII-A, p.14]。
- 理由一：一次給大量 context 會明顯拖慢推論速度，分塊檢索、按需輸入比較有效率 [02-gao2023-survey.pdf, §VII-A, p.14]。
- 理由二：RAG 能快速找到原始出處讓使用者驗證，檢索過程看得見；只靠 long context 則像黑盒子 [02-gao2023-survey.pdf, §VII-A, p.14]。

## 各論文怎麼說

- **[01-lewis2020-rag.pdf](../sources/01-lewis2020-rag.md)**：測試時可以調整要取幾份文件，這會影響表現和執行時間 [01-lewis2020-rag.pdf, §4.5, p.8]。
- **[02-gao2023-survey.pdf](../sources/02-gao2023-survey.md)**：見上方說明。

## 相關頁面

- [Reranking](reranking.md)
- [Chunking](chunking.md)
- [Retriever](retriever.md)
- [術語表](../glossary.md)
