---
type: concept
title: "Retriever（檢索器）"
tags: [concept, retrieval, dpr, bm25, mips]
sources: [01-lewis2020-rag.pdf, 02-gao2023-survey.pdf, 03-anthropic-contextual-retrieval.pdf, 04-liu2023-lost-in-middle.pdf]
updated: 2026-11-22
---

# Retriever

## 白話說明

Retriever 是 RAG 裡負責「查資料」的部分：拿到問題後，它會從一大堆文件中找出最相關的幾份，交給 [generator](generator.md) 去寫答案 [01-lewis2020-rag.pdf, §2, p.2]。

## 為什麼重要

- 找到的文件好不好，直接影響答案好不好。原始 RAG 論文的消融實驗顯示，「學會怎麼檢索」能提升所有任務的表現 [01-lewis2020-rag.pdf, §4.5, p.7]。
- 在 open-domain QA 上，用什麼 retriever 尤其關鍵 [01-lewis2020-rag.pdf, §4.5, p.7]。

## 運作方式（以原始 RAG 為例）

1. **事先準備**：把每份文件用 document encoder 轉成一個 [embedding](embedding.md)，存成 index [01-lewis2020-rag.pdf, §3, p.4]。
2. **收到問題時**：用 query encoder 把問題也轉成一個 embedding [01-lewis2020-rag.pdf, §2.2, p.3]。
3. **比對**：找出跟問題 embedding 內積（inner product）最大的 k 份文件，也就是 top-k；這是一個 MIPS（Maximum Inner Product Search）問題，可以近似地快速求解 [01-lewis2020-rag.pdf, §2.2, p.3]。
4. **交出結果**：把這 k 份文件交給 generator [01-lewis2020-rag.pdf, Fig.1, p.2]。

### DPR 與 bi-encoder

- 原始 RAG 的 retriever 用的是 DPR（Dense Passage Retriever）[01-lewis2020-rag.pdf, §1, p.2]。
- DPR 是 bi-encoder 架構：文件和問題各用一個 BERT-base encoder 轉成向量 [01-lewis2020-rag.pdf, §2.2, p.3]。
- 這個 retriever 原本是訓練來找出「含有 TriviaQA、Natural Questions 答案」的文件 [01-lewis2020-rag.pdf, §2.2, p.3]。

### Top-k：要取幾份文件？

- 原始 RAG 訓練時取 5 或 10 份，兩者的表現沒有明顯差異 [01-lewis2020-rag.pdf, §3, p.4; §4.5, p.8]。
- 測試時取越多份，RAG-Sequence 在 NQ 上的表現就越好；RAG-Token 則在 10 份時最好 [01-lewis2020-rag.pdf, §4.5, p.8; Fig.3, p.8]。
- 文件取得越多，執行時間也會受影響 [01-lewis2020-rag.pdf, §4.5, p.8]。

- **Retriever 找到了，不代表 LLM 用得到**：04 發現 retriever 的 recall 隨文件數量持續上升，LLM 的表現卻在大約 20 份時就停止進步了 [04-liu2023-lost-in-middle.pdf, §5, p.10; Fig.11, p.10]。

> ⚠️ **爭議／更新**：[02-gao2023-survey.pdf, §IV-A, p.10] 認為「盡量多檢索文件」是常見的誤解，過多的 context 會帶來雜訊；[04-liu2023-lost-in-middle.pdf, §5, p.10] 也發現取 50 份和取 20 份相比，進步只有約 1%–1.5%。詳見 [Context window](context-window.md)。

### Dense retriever vs BM25

- BM25 是一種靠「字詞重疊」來檢索的方法 [01-lewis2020-rag.pdf, §4.5, p.7]。
- 在 FEVER 上 BM25 表現最好，作者推測是因為 FEVER 的句子以實體（人名、地名等）為中心，很適合用字詞比對 [01-lewis2020-rag.pdf, §4.5, p.7]。
- 在其他任務上，可微分的 dense retriever 都比較好 [01-lewis2020-rag.pdf, §4.5, p.7]。
- 例如在 NQ dev set 上，RAG-Token 用 BM25 是 29.7 EM，用 dense retriever 則是 43.5 [01-lewis2020-rag.pdf, Table 6, p.8]。
- 綜述把 BM25 歸為 sparse encoder，把 BERT 類的模型歸為 dense retriever [02-gao2023-survey.pdf, §III-D, p.9]。
- **Hybrid retrieval**：sparse 和 dense 可以互補。例如 sparse retrieval 能幫助 dense retriever 處理含有罕見實體的問題，讓檢索更穩定 [02-gao2023-survey.pdf, §III-D, p.9]。

#### BM25 怎麼運作？

- BM25（Best Matching 25）是一種排序函數，用字面比對找出精確的詞或片語 [03-anthropic-contextual-retrieval.pdf, p.3]。
- 它建立在 TF-IDF 的概念上：TF-IDF 衡量一個詞對某份文件有多重要；BM25 再考慮文件長度，並對詞頻做「飽和」處理，避免常見詞主導結果 [03-anthropic-contextual-retrieval.pdf, p.3]。
- **什麼時候 BM25 比 embedding 好**：查詢含有獨特代碼或專業術語時。例如查「Error code TS-999」，embedding 可能只找到一般的錯誤碼說明，BM25 則會精確比對「TS-999」[03-anthropic-contextual-retrieval.pdf, p.3]。
- **和 01 的結果一致**：01 也發現 BM25 在 FEVER 上表現最好，作者推測是因為 FEVER 的句子以實體為中心 [01-lewis2020-rag.pdf, §4.5, p.7]。

#### 混合檢索的步驟

1. 把知識庫切成 chunk，通常每個不超過幾百 tokens [03-anthropic-contextual-retrieval.pdf, p.3]。
2. 為每個 chunk 建立 TF-IDF 編碼和語意 embedding [03-anthropic-contextual-retrieval.pdf, p.3]。
3. 用 BM25 找出精確比對分數最高的 chunk [03-anthropic-contextual-retrieval.pdf, p.3]。
4. 用 embedding 找出語意最相似的 chunk [03-anthropic-contextual-retrieval.pdf, p.3]。
5. 用 rank fusion 合併兩邊的結果並去除重複 [03-anthropic-contextual-retrieval.pdf, p.3]。
6. 把 top-K 個 chunk 加進 prompt 產生回答 [03-anthropic-contextual-retrieval.pdf, p.3]。

03 的實驗結論是：embedding 加 BM25，比只用 embedding 好 [03-anthropic-contextual-retrieval.pdf, p.11]。

### 從哪裡檢索？

- **非結構化資料**：文字是最常用的來源；open-domain QA 主要用 Wikipedia dump [02-gao2023-survey.pdf, §III-A, p.7]。
- **半結構化資料**：例如含有表格的 PDF。切分可能把表格切斷，表格也會讓語意相似度搜尋變得更複雜 [02-gao2023-survey.pdf, §III-A, p.7]。
- **結構化資料**：例如 knowledge graph，通常經過驗證、資訊較精確，但建立和維護都要額外的功夫 [02-gao2023-survey.pdf, §III-A, p.7]。
- **LLM 自己產生的內容**：例如 GenRead 用 LLM 產生的內容取代 retriever [02-gao2023-survey.pdf, §III-A, p.7]。

### 讓 retriever 更貼合任務

- 可以用 LLM 的結果當作監督訊號來 fine-tune retriever，這叫 LM-supervised Retriever（LSR）[02-gao2023-survey.pdf, §III-D, p.9]。
- 如果不方便 fine-tune，也可以外接一個 adapter 來輔助對齊 [02-gao2023-survey.pdf, §III-E, p.9]。

## 各論文怎麼說

- **[01-lewis2020-rag.pdf](../sources/01-lewis2020-rag.md)**：retriever 和 generator 一起訓練，但不給「應該找哪份文件」的監督 [01-lewis2020-rag.pdf, §2.4, p.3]。訓練時只更新 query encoder，document encoder 和 index 保持不變 [01-lewis2020-rag.pdf, §2.4, p.4]。作者也認為，要達到當時的最佳成績，re-ranker 並非必要 [01-lewis2020-rag.pdf, §4.1, p.5]。
- **[02-gao2023-survey.pdf](../sources/02-gao2023-survey.md)**：Naive RAG 的檢索常常 precision 和 recall 不足，會選到不相關的 chunk，或漏掉關鍵資訊 [02-gao2023-survey.pdf, §II-A, p.3]。

- **[03-anthropic-contextual-retrieval.pdf](../sources/03-anthropic-contextual-retrieval.md)**：傳統 RAG 切塊時會把 context 去掉，導致系統常常找不到相關資訊；解法是 [Contextual Retrieval](../methods/contextual-retrieval.md) [03-anthropic-contextual-retrieval.pdf, p.1, p.5]。

> ⚠️ **爭議／更新**：[01-lewis2020-rag.pdf, §4.1, p.5] 認為 re-ranker 不是必要的；[02-gao2023-survey.pdf, §II-B, p.4] 則把 reranking 視為 Advanced RAG 的關鍵策略，[03-anthropic-contextual-retrieval.pdf, p.11] 的實驗也發現有 reranking 比沒有好。詳見 [Reranking](reranking.md)。

## 常見問題

- **Retrieval collapse**：在 story generation 這類任務上，retriever 可能不管輸入是什麼都找同一批文件，generator 也就開始忽略它們 [01-lewis2020-rag.pdf, App. H, p.19]。
- **找到的不一定是對的**：FEVER 上，第 1 份檢索結果來自人工標註正確文章的比例是 71% [01-lewis2020-rag.pdf, §4.4, p.7]。

## 相關頁面

- [Embedding](embedding.md)
- [Chunking](chunking.md)
- [Reranking](reranking.md)
- [Query 優化](query-optimization.md)
- [Contextual Retrieval](../methods/contextual-retrieval.md)
- [Generator](generator.md)
- [原始 RAG（方法）](../methods/original-rag.md)
- [術語表](../glossary.md)
