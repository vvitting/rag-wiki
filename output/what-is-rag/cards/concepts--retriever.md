---
page: wiki/concepts/retriever.md
---
# 證據卡：Retriever

## 重點摘錄
> Retriever 是 RAG 裡負責「查資料」的部分：拿到問題後，它會從一大堆文件中找出最相關的幾份，交給 [generator](generator.md) 去寫答案 [01-lewis2020-rag.pdf, §2, p.2]。
> - 找到的文件好不好，直接影響答案好不好。原始 RAG 論文的消融實驗顯示，「學會怎麼檢索」能提升所有任務的表現 [01-lewis2020-rag.pdf, §4.5, p.7]。
> - **什麼時候 BM25 比 embedding 好**：查詢含有獨特代碼或專業術語時。例如查「Error code TS-999」，embedding 可能只找到一般的錯誤碼說明，BM25 則會精確比對「TS-999」[03-anthropic-contextual-retrieval.pdf, p.3]。
> 03 的實驗結論是：embedding 加 BM25，比只用 embedding 好 [03-anthropic-contextual-retrieval.pdf, p.11]。
> - 一般 RAG 取回的是「各自和問題相關」的少數幾筆資料，所以適合答案集中在少數文件裡的問題 [06-edge2024-graphrag.pdf, §1, p.1–2]。

## 數字
> - 例如在 NQ dev set 上，RAG-Token 用 BM25 是 29.7 EM，用 dense retriever 則是 43.5 [01-lewis2020-rag.pdf, Table 6, p.8]。

## 可以用在
- 怎麼運作（08）：retriever 的角色、embedding vs BM25
- 進階變體（10）：一般 RAG 只找得到局部
