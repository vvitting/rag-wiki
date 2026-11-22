---
slide: 1
section: 為什麼需要
title: LLM 很強，但會一本正經地講錯
---
## 投影片
- **LLM** 有三個主要問題：會講錯、知識過時、無法追溯出處〔wiki/overview.md〕
- **Hallucination**：講出聽起來很像真的、但其實是錯的內容〔wiki/concepts/hallucination.md〕
- 例子：只靠記憶、不查資料的模型 BART，說中耳「介於中耳和鼻子之間」〔wiki/concepts/hallucination.md〕
- 遇到需要最新資訊、或超出訓練資料的問題，特別容易出錯〔wiki/overview.md〕

## 講稿
今天的大型語言模型，也就是 LLM，很會寫也很會聊，但它有三個主要問題：會講錯、知識會過時，而且說不出答案是從哪裡來的〔wiki/overview.md〕。其中最麻煩的是 hallucination，就是模型講出聽起來很像真的、其實是錯的內容〔wiki/concepts/hallucination.md〕。例如 BART 是一個只靠參數記憶、不查資料的模型，問它中耳是什麼，它竟然回答中耳是介於中耳和鼻子之間的部分〔wiki/concepts/hallucination.md〕。
