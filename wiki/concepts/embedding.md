---
type: concept
title: "Embedding 與 vector index"
tags: [concept, embedding, vector, index, faiss, vector-database]
sources: [01-lewis2020-rag.pdf, 02-gao2023-survey.pdf, 03-anthropic-contextual-retrieval.pdf]
updated: 2026-11-22
---

# Embedding 與 vector index

## 白話說明

Embedding 就是把一段文字轉成一串數字（vector），讓電腦可以計算「兩段文字有多相關」。原始 RAG 用 document encoder 把每份文件轉成一個 dense representation，也就是 embedding [01-lewis2020-rag.pdf, §2.2, p.3; §3, p.4]。

RAG 是透過計算「語意相似度」來找出相關的 chunk [02-gao2023-survey.pdf, §I, p.1]；而 embedding model 表示語意的能力，在這當中扮演關鍵角色 [02-gao2023-survey.pdf, §III-D, p.9]。

03 的說法更白話：embedding model 會把 chunk 轉成「把意思編碼進去」的向量，存進 vector database 後，就可以依語意相似度來搜尋 [03-anthropic-contextual-retrieval.pdf, p.2]。也就是說，意思相近的文字會被找成「相似」的結果。

不過，embedding 擅長捕捉語意關係，卻可能漏掉關鍵的精確比對，例如錯誤碼「TS-999」[03-anthropic-contextual-retrieval.pdf, p.3]。這時要搭配 BM25，詳見 [Retriever](retriever.md)。

## 為什麼重要

- [Retriever](retriever.md) 是靠比對問題和文件的 embedding 來找資料的。原始 RAG 用內積（inner product）[01-lewis2020-rag.pdf, §2.2, p.3]，綜述則舉 cosine similarity 為例 [02-gao2023-survey.pdf, §III-D, p.9]。
- 所有文件的 embedding 合起來組成 index，也就是 RAG 的 [non-parametric memory](parametric-vs-non-parametric-memory.md) [01-lewis2020-rag.pdf, §2.2, p.3]。
- Naive RAG 把這些向量存在 vector database 裡 [02-gao2023-survey.pdf, §II-A, p.3]。

## 運作方式

### 建立 index（以原始 RAG 為例）

1. 把 Wikipedia 切成 100-word 的 [chunk](chunking.md)，共 21M 份文件 [01-lewis2020-rag.pdf, §3, p.4]。
2. 用 document encoder（BERT-base）為每份文件算出 embedding [01-lewis2020-rag.pdf, §2.2, p.3; §3, p.4]。
3. 用 FAISS 把所有 embedding 建成一個 MIPS index，搭配 HNSW 近似法加快檢索 [01-lewis2020-rag.pdf, §3, p.4]。

查詢時必須用**同一個** encoding model 把問題轉成向量 [02-gao2023-survey.pdf, §II-A, p.3]。

### Sparse vs dense

- Embedding 方法大致分成 sparse encoder（例如 BM25）和 dense retriever（例如以 BERT 為架構的預訓練模型）[02-gao2023-survey.pdf, §III-D, p.9]。
- 兩者捕捉到的相關性特徵不同，可以互補，這就是 hybrid retrieval [02-gao2023-survey.pdf, §III-D, p.9]。

### 要選哪個 embedding model？

- 較新的 embedding model 有 AngIE、Voyage、BGE 等 [02-gao2023-survey.pdf, §III-D, p.9]。
- Hugging Face 的 MTEB leaderboard 用 8 種任務、58 個資料集評估 embedding model；C-MTEB 專門評估中文，涵蓋 6 種任務、35 個資料集 [02-gao2023-survey.pdf, §III-D, p.9]。
- 「該用哪個 embedding model」沒有標準答案，要看使用情境 [02-gao2023-survey.pdf, §III-D, p.9]。
- 03 測試過的 embedding 中，Voyage 和 Gemini 最好；實驗中表現最好的設定是 Gemini Text 004 [03-anthropic-contextual-retrieval.pdf, p.7, p.11]。
- 在醫療、法律這類專業術語很多的領域，用自己領域的資料 fine-tune embedding model 是必要的 [02-gao2023-survey.pdf, §III-D, p.9]。

### 規模與成本（原始 RAG）

- 整個 index 是 21M 個向量，論文記載每個向量是 728 維，總共 15.3B 個數值 [01-lewis2020-rag.pdf, App. G, p.19]。
- 這些向量放在 CPU 記憶體中需要約 100 GB，用 FAISS 壓縮後降到 36 GB [01-lewis2020-rag.pdf, App. C, p.17]。

## 各論文怎麼說

- **[01-lewis2020-rag.pdf](../sources/01-lewis2020-rag.md)**：訓練時 document encoder 不更新。因為一旦更新，整個 index 都要重算，成本很高，而且不更新也能有強表現 [01-lewis2020-rag.pdf, §2.4, p.4]。
- **[02-gao2023-survey.pdf](../sources/02-gao2023-survey.md)**：fine-tune embedding model 的另一個目的，是讓 retriever 和 generator 對齊，例如用 LLM 的結果當作監督訊號 [02-gao2023-survey.pdf, §III-D, p.9]。
- **[03-anthropic-contextual-retrieval.pdf](../sources/03-anthropic-contextual-retrieval.md)**：在 embedding 之前先為 chunk 加上說明（Contextual Embeddings），檢索失敗率從 5.7% 降到 3.7% [03-anthropic-contextual-retrieval.pdf, p.7]。

## 相關頁面

- [Retriever](retriever.md)
- [Chunking](chunking.md)
- [術語表](../glossary.md)
