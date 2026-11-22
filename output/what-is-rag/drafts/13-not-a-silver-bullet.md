---
slide: 13
section: 總結
title: 重點回顧：RAG 有用，但不是萬靈丹
---
## 投影片
- RAG = 先查再寫；換掉 index 就能更新知識，不用重新訓練〔wiki/overview.md〕
- 位置有影響：放在中間的資訊最容易被忽略（**Lost in the Middle**）〔wiki/concepts/lost-in-the-middle.md〕
- GPT-3.5-Turbo、20 份文件、答案在中間：53.8%，低於不給文件的 56.1%〔wiki/concepts/lost-in-the-middle.md〕
- ⚠️ 文件放越多越好嗎？各研究看法不一；有實驗發現 50 份比 20 份只多約 1%–1.5%〔wiki/concepts/retriever.md〕
- 檢索不一定有幫助，外部資料本身也可能有錯〔wiki/overview.md〕

## 講稿
最後幫大家整理：RAG 就是先查再寫，只要換掉 index，就能更新 RAG 的知識，不用重新訓練模型〔wiki/overview.md〕。但它不是萬靈丹：在 GPT-3.5-Turbo 的實驗裡，20 份文件中答案放在第 1 份時答對 75.8%，放在中間只有 53.8%，比完全不給文件的 56.1% 還低，這是在 20 和 30 份文件設定的最差位置觀察到的〔wiki/concepts/lost-in-the-middle.md〕〔wiki/comparisons/closed-book-vs-open-book.md〕。另一份研究也發現，ChatGPT 加上檢索後，PubHealth 反而從 70.1 降到 54.7〔wiki/methods/naive-rag.md〕。至於要放幾份文件，各研究的看法並不一致，例如有一項實驗發現，取 50 份比 20 份只多進步約 1%–1.5%，而外部資料本身也可能有錯〔wiki/concepts/retriever.md〕〔wiki/overview.md〕。
