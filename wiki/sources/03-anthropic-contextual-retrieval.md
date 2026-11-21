---
type: source
title: "Introducing Contextual Retrieval"
raw: 03-anthropic-contextual-retrieval.pdf
authors: [Anthropic]
year: 2024
tags: [rag, contextual-retrieval, bm25, hybrid-search, reranking, industry-blog]
sources: [03-anthropic-contextual-retrieval.pdf, 01-lewis2020-rag.pdf, 02-gao2023-survey.pdf]
updated: 2026-11-22
---

# Introducing Contextual Retrieval（Anthropic, 2024）

Anthropic 在 2024 年 9 月 19 日發表的技術文章 [03-anthropic-contextual-retrieval.pdf, p.1]。raw 檔是網頁的 PDF 列印版，總共 14 頁 [03-anthropic-contextual-retrieval.pdf, p.1]。

**來源性質**：這是業界的技術文章，不是同儕審查的論文。文中也介紹了發表者自家的產品，例如 Claude、prompt caching、cookbook [03-anthropic-contextual-retrieval.pdf, p.2, p.6]。引用它的數字時要留意這一點。

## 一句話摘要

在把每個 chunk 轉成 embedding、建 BM25 index 之前，先用 LLM 為它寫一段 50–100 tokens 的「背景說明」貼在前面，讓 chunk 不再「斷章取義」；這樣能讓檢索失敗率下降 49%，再加上 reranking 則下降 67% [03-anthropic-contextual-retrieval.pdf, p.2, p.5–6]。

## 這篇想解決什麼問題

- 傳統 RAG 把文件切成 chunk 時，會把 context 去掉，導致系統常常找不到相關資訊 [03-anthropic-contextual-retrieval.pdf, p.1]。
- **例子**：問題是「ACME Corp 在 2023 年 Q2 的營收成長多少？」，相關的 chunk 寫著「公司營收比上一季成長 3%」[03-anthropic-contextual-retrieval.pdf, p.4]。
- 但這個 chunk 本身沒有說是哪家公司、哪個時期，所以很難被找到，找到了也很難用 [03-anthropic-contextual-retrieval.pdf, p.4]。

## 核心方法

詳見 [Contextual Retrieval 方法頁](../methods/contextual-retrieval.md)。

- **Contextual Embeddings**：把 chunk 專屬的說明文字貼在 chunk 前面，再轉成 embedding [03-anthropic-contextual-retrieval.pdf, p.5]。
- **Contextual BM25**：同樣貼上說明文字後，再建 BM25 index [03-anthropic-contextual-retrieval.pdf, p.5]。
- **誰來寫說明**：用 Claude 3 Haiku 和一個 prompt，讓模型讀完整份文件後，為每個 chunk 寫一段簡短的定位說明 [03-anthropic-contextual-retrieval.pdf, p.5]。
- **說明多長**：產生的說明文字通常是 50–100 tokens [03-anthropic-contextual-retrieval.pdf, p.6]。
- **成本**：搭配 prompt caching，每份文件只要載入快取一次 [03-anthropic-contextual-retrieval.pdf, p.6]。
- **成本試算**：假設 chunk 800 tokens、文件 8k tokens、指令 50 tokens、每個說明 100 tokens，一次性的成本是每百萬文件 tokens 1.02 美元 [03-anthropic-contextual-retrieval.pdf, p.6–7]。

### 背景：embedding + BM25 的混合檢索

- Embedding model 擅長捕捉語意關係，但可能漏掉關鍵的精確比對 [03-anthropic-contextual-retrieval.pdf, p.3]。
- BM25 用字面比對（lexical matching）找出精確的詞或片語，特別適合含有獨特代碼或專業術語的查詢 [03-anthropic-contextual-retrieval.pdf, p.3]。
- **例子**：查詢「Error code TS-999」時，embedding 可能找到一般性的錯誤碼說明，卻漏掉精確的「TS-999」；BM25 則會直接找這個字串 [03-anthropic-contextual-retrieval.pdf, p.3]。
- 兩種方法的結果用 rank fusion 合併、去除重複後，取 top-K 加進 prompt [03-anthropic-contextual-retrieval.pdf, p.3]。

## 關鍵結果（數字務必附出處）

評估指標是 1 − recall@20，也就是「相關文件沒出現在前 20 個 chunk 裡」的比例，越低越好 [03-anthropic-contextual-retrieval.pdf, p.7]。下表是所有領域的平均值，使用表現最好的 embedding（Gemini Text 004），取前 20 個 chunk [03-anthropic-contextual-retrieval.pdf, p.7]。

| 設定 | 檢索失敗率 | 相對降低 | 出處 |
|---|---|---|---|
| 一般 embedding（基準） | 5.7% | – | [03-anthropic-contextual-retrieval.pdf, p.7] |
| Contextual Embeddings | 3.7% | 35% | [03-anthropic-contextual-retrieval.pdf, p.7] |
| Contextual Embeddings + Contextual BM25 | 2.9% | 49% | [03-anthropic-contextual-retrieval.pdf, p.7] |
| 上一列 + reranking | 1.9% | 67% | [03-anthropic-contextual-retrieval.pdf, p.10] |

- 測試的領域包括程式碼庫、小說、ArXiv 論文、科學論文 [03-anthropic-contextual-retrieval.pdf, p.7]。
- 在測試過的每一種 embedding 和資料來源組合中，加上 context 都提升了表現 [03-anthropic-contextual-retrieval.pdf, p.7]。
- 給模型 5、10、20 個 chunk 的比較中，20 個的效果最好 [03-anthropic-contextual-retrieval.pdf, p.8]。
- 測試過的 embedding 中，Voyage 和 Gemini 最好 [03-anthropic-contextual-retrieval.pdf, p.11]。

### 結論（原文六點）

1. Embeddings 加 BM25，比只用 embeddings 好 [03-anthropic-contextual-retrieval.pdf, p.11]。
2. 測試過的 embedding 中，Voyage 和 Gemini 最好 [03-anthropic-contextual-retrieval.pdf, p.11]。
3. 給模型前 20 個 chunk，比只給前 10 或前 5 個有效 [03-anthropic-contextual-retrieval.pdf, p.11]。
4. 為 chunk 加上 context，大幅提升檢索準確度 [03-anthropic-contextual-retrieval.pdf, p.11]。
5. 有 reranking 比沒有好 [03-anthropic-contextual-retrieval.pdf, p.11]。
6. 這些好處可以疊加 [03-anthropic-contextual-retrieval.pdf, p.11]。

## 限制與後續爭議

- **評估範圍**：主要的數字衡量的是「檢索」的失敗率，不是最終答案的品質 [03-anthropic-contextual-retrieval.pdf, p.7]。文中只說檢索準確度的提升會「直接轉化」為下游任務更好的表現 [03-anthropic-contextual-retrieval.pdf, p.2]。
- **附錄抽不到文字**：附錄 I 的分資料集結果在 raw 檔中是圖片，文字抽取不到，所以本 wiki 無法引用那些細部數字 [03-anthropic-contextual-retrieval.pdf, p.11–12]。
- **Reranking 的代價**：多了一個執行步驟，一定會增加一點延遲；要在「rerank 更多 chunk 換更好表現」和「rerank 更少換更低延遲與成本」之間取捨 [03-anthropic-contextual-retrieval.pdf, p.10]。
- **其他方法的效果有限**：作者試過把通用的文件摘要加到 chunk 上，提升非常有限；也評估過以摘要為基礎的 indexing，表現很差 [03-anthropic-contextual-retrieval.pdf, p.5]。

> ⚠️ **爭議／更新**：本篇說知識庫小於 200,000 tokens（約 500 頁）時，可以直接把整個知識庫放進 prompt，不需要 RAG [03-anthropic-contextual-retrieval.pdf, p.2]；但 [02-gao2023-survey.pdf, §VII-A, p.14] 認為即使 LLM 能處理長 context，RAG 在效率和可驗證性上仍無可取代。詳見 [Context window](../concepts/context-window.md)。

> ⚠️ **爭議／更新**：本篇的結論是「有 reranking 比沒有好」[03-anthropic-contextual-retrieval.pdf, p.11]，支持 [02-gao2023-survey.pdf, §II-B, p.4] 的看法；而 [01-lewis2020-rag.pdf, §4.1, p.5] 認為 re-ranker 不是必要的。詳見 [Reranking](../concepts/reranking.md)。

## 關鍵圖表說明

- **p.4 的流程圖**：同時使用 embedding 和 BM25 的標準 RAG 系統 [03-anthropic-contextual-retrieval.pdf, p.4]。
- **p.5 的 chunk 轉換範例**：原始 chunk「公司營收比上一季成長 3%」，被改寫成開頭帶有「這段來自 ACME Corp 的 SEC 申報文件…」的版本 [03-anthropic-contextual-retrieval.pdf, p.5]。**最適合放進簡報說明 Contextual Retrieval。**
- **p.8 的長條圖**：Contextual Embedding 加 Contextual BM25，讓失敗率降低 49% [03-anthropic-contextual-retrieval.pdf, p.8]。
- **p.10 的長條圖**：再加上 reranking，失敗率降低 67% [03-anthropic-contextual-retrieval.pdf, p.10]。

## 對初學者的重點

1. 切塊會讓 chunk「斷章取義」，例如不知道「公司」指的是哪一家 [03-anthropic-contextual-retrieval.pdf, p.4]。
2. 解法很直覺：先幫每個 chunk 寫一段「這段是從哪裡來的」說明，再拿去建 index [03-anthropic-contextual-retrieval.pdf, p.5]。
3. 語意搜尋（embedding）和關鍵字搜尋（BM25）各有所長，合併使用效果更好 [03-anthropic-contextual-retrieval.pdf, p.3, p.11]。
4. 知識庫不大時，不一定需要 RAG [03-anthropic-contextual-retrieval.pdf, p.2]。

## 相關頁面

- [Contextual Retrieval（方法）](../methods/contextual-retrieval.md)
- [Retriever](../concepts/retriever.md)
- [Reranking](../concepts/reranking.md)
- [Chunking](../concepts/chunking.md)
- [Context window](../concepts/context-window.md)
- [RAG 進階技巧比較](../comparisons/rag-techniques.md)
