---
page: wiki/concepts/chunking.md
---
# 證據卡：Chunking

## 重點摘錄
> Chunking 就是把長文件切成一小段一小段（chunk），讓 [retriever](retriever.md) 以這些小段為單位去搜尋。原始 RAG 把每篇 Wikipedia 文章切成互不重疊的 100-word chunk [01-lewis2020-rag.pdf, §3, p.4]。
> - 要切塊，是為了配合 language model 的 context 限制 [02-gao2023-survey.pdf, §II-A, p.3]。
> - 傳統 RAG 切塊時會把 context 去掉，系統因此常常找不到相關資訊 [03-anthropic-contextual-retrieval.pdf, p.1]。

## 數字
> - 切出來的 chunk 就是 retriever 能找到、generator 能讀到的單位；原始 RAG 的知識庫一共是 21M 個 chunk [01-lewis2020-rag.pdf, §3, p.4]。
> - 最常見的方法是依固定的 token 數切分，例如 100、256、512 [02-gao2023-survey.pdf, §III-B, p.8]；03 也說 chunk 通常不超過幾百 tokens [03-anthropic-contextual-retrieval.pdf, p.2]。
> - **例子**：「公司營收比上一季成長 3%」這個 chunk，沒說是哪家公司、哪個時期，所以問「ACME Corp 2023 年 Q2 的營收成長」時很難被找到 [03-anthropic-contextual-retrieval.pdf, p.4]。

## 可以用在
- 怎麼運作（08）：為什麼切塊、切多大、原始 RAG 的 100-word chunk 與 21M 個 chunk
