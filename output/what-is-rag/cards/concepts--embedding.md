---
page: wiki/concepts/embedding.md
---
# 證據卡：Embedding 與 vector index

## 重點摘錄
> Embedding 就是把一段文字轉成一串數字（vector），讓電腦可以計算「兩段文字有多相關」。原始 RAG 用 document encoder 把每份文件轉成一個 dense representation，也就是 embedding [01-lewis2020-rag.pdf, §2.2, p.3; §3, p.4]。
> 03 的說法更白話：embedding model 會把 chunk 轉成「把意思編碼進去」的向量，存進 vector database 後，就可以依語意相似度來搜尋 [03-anthropic-contextual-retrieval.pdf, p.2]。也就是說，意思相近的文字會被找成「相似」的結果。
> 不過，embedding 擅長捕捉語意關係，卻可能漏掉關鍵的精確比對，例如錯誤碼「TS-999」[03-anthropic-contextual-retrieval.pdf, p.3]。這時要搭配 BM25，詳見 [Retriever](retriever.md)。
> 查詢時必須用**同一個** encoding model 把問題轉成向量 [02-gao2023-survey.pdf, §II-A, p.3]。

## 可以用在
- 怎麼運作（07）：embedding 把意思轉成向量
- 怎麼運作（08）：embedding 會漏掉精確字串
