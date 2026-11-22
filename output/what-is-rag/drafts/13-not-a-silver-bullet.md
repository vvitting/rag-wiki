---
slide: 13
section: 總結
title: 重點回顧：RAG 有用，但不是萬靈丹
---
## 投影片
- RAG = 先查再寫；換掉 index 就能更新知識〔wiki/overview.md〕
- 資料不是越多越好：取 50 份比 20 份，只多進步約 1%–1.5%〔wiki/overview.md〕
- 位置也有影響：放在中間的資訊最容易被忽略（**Lost in the Middle**）〔wiki/concepts/lost-in-the-middle.md〕
- GPT-3.5-Turbo、20 份文件、答案在中間：53.8%，低於不給文件的 56.1%〔wiki/concepts/lost-in-the-middle.md〕
- 外部資料也可能有錯；用了 RAG 仍可能講錯〔wiki/concepts/hallucination.md〕

## 講稿
最後幫大家整理：RAG 就是先查再寫，而且只要換掉外部資料，就能更新模型的知識〔wiki/overview.md〕。但資料不是越多越好，位置也有影響：在 GPT-3.5-Turbo 的實驗裡，20 份文件中答案放在第 1 份時答對 75.8%，放在中間只有 53.8%，比完全不給文件的 56.1% 還低〔wiki/concepts/lost-in-the-middle.md〕。這種反而更差的情況，只出現在 20 和 30 份文件設定的最差位置，所以重點是把相關的資料排到前面〔wiki/comparisons/closed-book-vs-open-book.md〕。另外，外部資料本身也可能有錯，用了 RAG 也不保證不會講錯〔wiki/concepts/hallucination.md〕。
