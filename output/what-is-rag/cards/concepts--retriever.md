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

## ⚠️ 爭議
> > ⚠️ **爭議／更新**：「要放多少份文件」各來源的說法不一致：[01-lewis2020-rag.pdf, §4.5, p.8] 發現 RAG-Sequence 取越多份文件，NQ 表現越好；[02-gao2023-survey.pdf, §IV-A, p.10] 認為「盡量多檢索」是常見的誤解，過多的 context 會帶來雜訊；[03-anthropic-contextual-retrieval.pdf, p.8] 實測 5、10、20 個 chunk，20 個最好；[04-liu2023-lost-in-middle.pdf, §5, p.10] 發現取 50 份和取 20 份相比只多約 1%–1.5%；[06-edge2024-graphrag.pdf, App. C, p.19] 為一般 RAG 選 context 大小時，8k 在全面性上勝過更大的 context。
> > 情境不同：01 是每份文件分別交給 generator 再加權合併 [01-lewis2020-rag.pdf, §2.1, p.3]，不是串成一個長 prompt。完整的六種說法與整合見 [Context window](context-window.md)。

## 可以用在
- 怎麼運作（09）：retriever 的角色、embedding vs BM25
- 進階變體（11）：一般 RAG 只找得到局部
- 總結（13）：「要放多少份文件」各來源看法不一致；04 的 50 份 vs 20 份只是其中一種說法（⑦ 第 1 輪退回後補）
