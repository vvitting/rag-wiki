---
type: method
title: "原始 RAG（RAG-Sequence 與 RAG-Token）"
tags: [method, rag, foundational, rag-sequence, rag-token]
sources: [01-lewis2020-rag.pdf, 02-gao2023-survey.pdf]
updated: 2026-11-22
---

# 原始 RAG（Lewis et al., 2020）

## 一句話說明

把預訓練的 [retriever](../concepts/retriever.md)（DPR）和預訓練的 [generator](../concepts/generator.md)（BART）接起來，一起微調，讓模型「先查 Wikipedia，再寫答案」[01-lewis2020-rag.pdf, §1, p.2]。

## 跟 naive RAG 的差別

- [Naive RAG](naive-rag.md) 是把問題和檢索到的 chunk 組成 prompt 交給 LLM，對模型的修改需求很低 [02-gao2023-survey.pdf, §II-A, p.3; Fig.4, p.7]。
- 原始 RAG 則是把 retriever 的 query encoder 和 generator **一起訓練**，不是只把兩個現成的元件接起來 [01-lewis2020-rag.pdf, §2.4, p.3–4]。
- 原始 RAG 的 generator 是 400M 參數的 BART，不是 LLM [01-lewis2020-rag.pdf, §2.3, p.3]。

> ⚠️ **爭議／更新**：綜述說 Naive RAG 是「最早的方法」[02-gao2023-survey.pdf, §II-A, p.2]，但 RAG 這個名稱在 2020 年就由本篇提出了 [01-lewis2020-rag.pdf, §1, p.2] [02-gao2023-survey.pdf, Ref. 4, p.17]。兩者的完整對照見 [Naive RAG](naive-rag.md)。

## 運作步驟

1. **準備知識庫**：把 Wikipedia 切成 100-word 的 [chunk](../concepts/chunking.md)（共 21M 份），算出 [embedding](../concepts/embedding.md) 並建好 index [01-lewis2020-rag.pdf, §3, p.4]。
2. **檢索**：把問題 x 轉成向量，用 MIPS 找出 top-K 份文件 z [01-lewis2020-rag.pdf, Fig.1, p.2]。
3. **生成**：把 x 和每份 z 串接起來交給 BART，產生答案 y [01-lewis2020-rag.pdf, §2.3, p.3]。
4. **合併（marginalize）**：把「文件是哪一份」視為一個隱藏變數，將不同文件得到的結果按照檢索機率加權合併 [01-lewis2020-rag.pdf, §2, p.3]。

### 兩種版本

| | RAG-Sequence | RAG-Token |
|---|---|---|
| 怎麼使用文件 | 整個答案都根據同一份文件 [01-lewis2020-rag.pdf, §2.1, p.3] | 每個 token 都可以根據不同的文件 [01-lewis2020-rag.pdf, §2.1, p.3] |
| 適合的情境 | Open-domain QA 的 NQ、CT 分數較高 [01-lewis2020-rag.pdf, Table 1, p.6] | 需要組合多份文件的資訊時，例如 Jeopardy 出題 [01-lewis2020-rag.pdf, §4.3, p.6] |
| 解碼方式 | 不能只跑一次 beam search，要改用 Thorough 或 Fast Decoding [01-lewis2020-rag.pdf, §2.5, p.4] | 可以直接用標準的 beam decoder [01-lewis2020-rag.pdf, §2.5, p.4] |
| 生成多樣性（Jeopardy tri-gram） | 53.8% [01-lewis2020-rag.pdf, Table 5, p.8] | 46.8% [01-lewis2020-rag.pdf, Table 5, p.8] |

在分類任務上，兩種版本是等價的 [01-lewis2020-rag.pdf, §2.1, p.3]。

## 優點

- 在 open-domain QA 上創下當時的最佳成績，而且不需要昂貴的特殊預訓練 [01-lewis2020-rag.pdf, §4.1, p.5]。
- 生成的內容比 BART 更符合事實、更具體，也更多樣 [01-lewis2020-rag.pdf, Abstract, p.1]。
- 換掉 index 就能更新知識，不用重新訓練 [01-lewis2020-rag.pdf, §4.5, p.8]。
- 可訓練參數只有 626M，遠少於 T5-11B 的 11B [01-lewis2020-rag.pdf, App. G, p.18–19]。
- 記憶是原始文字，人類讀得懂、也改得動 [01-lewis2020-rag.pdf, §5, p.9]。

## 代價與限制

- 整個 Wikipedia 的 index 約需 100 GB CPU 記憶體，壓縮後是 36 GB [01-lewis2020-rag.pdf, App. C, p.17]。
- RAG-Sequence 用 Thorough Decoding 時，答案越長，需要額外跑的 forward pass 就越多 [01-lewis2020-rag.pdf, §2.5, p.4]。
- 在部分任務上可能發生 retrieval collapse [01-lewis2020-rag.pdf, App. H, p.19]。
- 外部知識來源本身可能有錯或有偏見 [01-lewis2020-rag.pdf, Broader Impact, p.10]。

## 出處

- [01-lewis2020-rag.pdf](../sources/01-lewis2020-rag.md)

## 相關頁面

- [Parametric 與 non-parametric memory](../concepts/parametric-vs-non-parametric-memory.md)
- [Closed-book vs open-book](../comparisons/closed-book-vs-open-book.md)
- [Naive RAG](naive-rag.md)
- [RAG 演進時間軸](../comparisons/rag-timeline.md)
- [RAG 總覽](../overview.md)
- [術語表](../glossary.md)
