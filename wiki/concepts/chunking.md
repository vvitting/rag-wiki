---
type: concept
title: "Chunking（切塊）"
tags: [concept, chunking, preprocessing, indexing]
sources: [01-lewis2020-rag.pdf, 02-gao2023-survey.pdf, 03-anthropic-contextual-retrieval.pdf]
updated: 2026-11-22
---

# Chunking

## 白話說明

Chunking 就是把長文件切成一小段一小段（chunk），讓 [retriever](retriever.md) 以這些小段為單位去搜尋。原始 RAG 把每篇 Wikipedia 文章切成互不重疊的 100-word chunk [01-lewis2020-rag.pdf, §3, p.4]。

## 為什麼重要

- 要切塊，是為了配合 language model 的 context 限制 [02-gao2023-survey.pdf, §II-A, p.3]。
- Index 建得好不好，決定了檢索階段能不能拿到正確的 context [02-gao2023-survey.pdf, §III-B, p.8]。
- 切出來的 chunk 就是 retriever 能找到、generator 能讀到的單位；原始 RAG 的知識庫一共是 21M 個 chunk [01-lewis2020-rag.pdf, §3, p.4]。

## 運作方式

### 切多大？

- 最常見的方法是依固定的 token 數切分，例如 100、256、512 [02-gao2023-survey.pdf, §III-B, p.8]；03 也說 chunk 通常不超過幾百 tokens [03-anthropic-contextual-retrieval.pdf, p.2]。
- **大 chunk**：能涵蓋更多上下文，但雜訊也多，處理時間和成本都更高 [02-gao2023-survey.pdf, §III-B, p.8]。
- **小 chunk**：雜訊少，但可能無法完整傳達需要的上下文 [02-gao2023-survey.pdf, §III-B, p.8]。
- 檢索單位粗，理論上能提供更多相關資訊，但多餘的內容會干擾 retriever 和 LLM；檢索單位細，則會增加檢索負擔，也不保證語意完整 [02-gao2023-survey.pdf, §III-A, p.7]。

### 切法的改良

- **問題**：固定長度切分會把句子從中間切斷 [02-gao2023-survey.pdf, §III-B, p.8]。
- **遞迴切分與 sliding window**：用來改善句子被切斷的問題 [02-gao2023-survey.pdf, §III-B, p.8]。
- **Small2Big**：用句子（small）當檢索單位，再把前後的句子（big）一起交給 LLM 當 context [02-gao2023-survey.pdf, §III-B, p.8]。
- **Proposition**：DenseX 提出以「proposition」當檢索單位，也就是一段只包含一個事實、意思自足的簡潔敘述 [02-gao2023-survey.pdf, §III-A, p.8]。
- 檢索單位由細到粗依序是：Token、Phrase、Sentence、Proposition、Chunk、Document [02-gao2023-survey.pdf, §III-A, p.8]。

### 加上 metadata

- Chunk 可以附上頁碼、檔名、作者、類別、時間戳等 metadata，檢索時再用它來過濾、縮小範圍 [02-gao2023-survey.pdf, §III-B, p.8]。
- 依時間戳給不同的權重，可以做到 time-aware RAG，避免使用過時的資訊 [02-gao2023-survey.pdf, §III-B, p.8]。
- **Reverse HyDE**：用 LLM 為每段文件產生「它能回答的假設問題」，檢索時比對原始問題和假設問題的相似度 [02-gao2023-survey.pdf, §III-B, p.8]。

### 切塊的副作用：chunk 失去上下文

- 傳統 RAG 切塊時會把 context 去掉，系統因此常常找不到相關資訊 [03-anthropic-contextual-retrieval.pdf, p.1]。
- **例子**：「公司營收比上一季成長 3%」這個 chunk，沒說是哪家公司、哪個時期，所以問「ACME Corp 2023 年 Q2 的營收成長」時很難被找到 [03-anthropic-contextual-retrieval.pdf, p.4]。
- **解法**：[Contextual Retrieval](../methods/contextual-retrieval.md) 先用 LLM 為每個 chunk 寫一段 50–100 tokens 的說明，再建 index [03-anthropic-contextual-retrieval.pdf, p.5–6]。
- 03 也提醒，chunk 大小、切分邊界、chunk 之間重疊（overlap）多少，都會影響檢索表現 [03-anthropic-contextual-retrieval.pdf, p.8]。

> ⚠️ **爭議／更新**：[02-gao2023-survey.pdf, §III-B, p.8] 把「為段落加上摘要」和階層式 index（每個節點存摘要）列為優化方法；但 [03-anthropic-contextual-retrieval.pdf, p.5] 實驗發現，把**通用的文件摘要**加到 chunk 上提升非常有限，**以摘要為基礎的 indexing** 表現也很差。兩者指的摘要範圍不完全相同（段落摘要 vs 通用的文件摘要），而 02 沒有提供實測數字。

### 特殊資料：表格與 PDF

- 處理 PDF 這類半結構化資料時，切分可能把表格切開，造成資料損壞 [02-gao2023-survey.pdf, §III-A, p.7]。

## 各論文怎麼說

- **[01-lewis2020-rag.pdf](../sources/01-lewis2020-rag.md)**：使用 2018 年 12 月的 Wikipedia，切成互不重疊的 100-word chunk，沿用 Lee et al. 和 DPR 的設定 [01-lewis2020-rag.pdf, §3, p.4]。
- **[02-gao2023-survey.pdf](../sources/02-gao2023-survey.md)**：作者認為這些方法仍然無法在「語意完整」和「context 長度」之間取得平衡 [02-gao2023-survey.pdf, §III-B, p.8]。

## 相關頁面

- [Embedding](embedding.md)
- [Retriever](retriever.md)
- [Context window](context-window.md)
- [Contextual Retrieval](../methods/contextual-retrieval.md)
- [Advanced RAG](../methods/advanced-rag.md)
- [術語表](../glossary.md)
