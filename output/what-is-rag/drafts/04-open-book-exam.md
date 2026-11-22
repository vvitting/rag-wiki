---
slide: 4
section: 是什麼
title: 比喻：從閉書考變成開書考
---
## 投影片
- **閉書考**：只能靠腦袋裡背的東西作答〔wiki/analogies.md〕
- **開書考**：先翻課本找到相關段落，再用自己的話寫答案〔wiki/analogies.md〕
- RAG 就是讓模型參加開書考〔wiki/analogies.md〕
- 在 open-domain QA 上，參數少很多的開書考模型，能勝過參數多很多的閉書考模型〔wiki/comparisons/closed-book-vs-open-book.md〕
- 比喻的極限：模型可能翻到不相關的頁面〔wiki/analogies.md〕

## 講稿
原始 RAG 論文自己就把只靠參數的方法叫 closed-book，把會去檢索資料的方法叫 open-book〔wiki/comparisons/closed-book-vs-open-book.md〕。在 open-domain QA 的 NQ 資料集上，RAG-Sequence 只有 626M 個可訓練參數，拿到 44.5 分〔wiki/comparisons/closed-book-vs-open-book.md〕。參數多很多的 T5-11B 有 11B 個參數，卻只有 34.5 分〔wiki/comparisons/closed-book-vs-open-book.md〕。不過要注意，開書考的學生通常知道該翻哪一章，RAG 卻可能翻到不相關的頁面〔wiki/analogies.md〕。
