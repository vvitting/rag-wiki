---
page: wiki/concepts/hallucination.md
---
# 證據卡：Hallucination

## 重點摘錄
> Hallucination 指模型講出聽起來很像真的、但其實是錯的內容。原始 RAG 論文把它列為純參數模型的缺點之一 [01-lewis2020-rag.pdf, §1, p.1]。
> - 這正是 RAG 想解決的問題之一：作者認為，RAG 的生成更紮根在真實的知識上（這裡指 Wikipedia），所以比較少「hallucinate」[01-lewis2020-rag.pdf, Broader Impact, p.10]。
> - [LLM](../glossary.md) 在處理超出訓練資料範圍、或需要最新資訊的問題時，特別容易產生 hallucination [02-gao2023-survey.pdf, §I, p.1]。
> - **「用了 RAG 就不會 hallucinate」**：論文只說「更少」，沒說「不會」[01-lewis2020-rag.pdf, §4.2, p.6]。
> - 而且外部知識來源本身也可能有錯或有偏見 [01-lewis2020-rag.pdf, Broader Impact, p.10]。

## 數字
> - 問 BART「define middle ear」，它回答「中耳是介於中耳和鼻子之間的部分」，這是錯的答案 [01-lewis2020-rag.pdf, Table 3, p.7]。
> - 同一個問題，RAG-Sequence 回答「中耳包含鼓室和三塊聽小骨」[01-lewis2020-rag.pdf, Table 3, p.7]。
> - Jeopardy 出題的人工評估中，認為 RAG 比較符合事實的有 42.7%，認為 BART 比較符合事實的只有 7.1% [01-lewis2020-rag.pdf, Table 4, p.8]。
> - **RAGAS 的 faithfulness**：把答案拆成小陳述，逐一檢查能不能從檢索到的 context 推論出來；這正是為了避免 hallucination [07-es2023-ragas.pdf, §3, p.3]。在 WikiEval 上，它和人類判斷的一致度是 0.95 [07-es2023-ragas.pdf, Table 1, p.5]。

## ⚠️ 爭議
> > ⚠️ **爭議／更新**：[02-gao2023-survey.pdf, §I, p.1] 認為 RAG 能有效減少錯誤內容；但檢索不一定有幫助：[04-liu2023-lost-in-middle.pdf, Table 6, p.18; Table 1, p.5] 發現 GPT-3.5-Turbo 在 20 份文件、答案位於中間時，準確率是 53.8%，低於完全不給文件的 56.1%；[05-asai2023-self-rag.pdf, App. C.1, p.20] 也指出，文件不相關時，一般 instruction-tuned 模型仍會產生看似合理的答案。注意 04 量的是答題準確率，不等於 hallucination 的比例。詳見 [Closed-book vs open-book](../comparisons/closed-book-vs-open-book.md)。

## 可以用在
- 為什麼需要（01）：hallucination 的白話定義、BART 中耳例子
- 怎麼評估（11）：faithfulness 在 WikiEval 上 0.95（帶資料集限定，對應 V2-01）
- 總結（12）：用了 RAG 也不保證不會講錯
