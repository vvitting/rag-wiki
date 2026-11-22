---
slide: 3
section: 是什麼
title: RAG：先查資料，再回答
---
## 投影片
- **RAG**：讓 LLM 先從外部知識庫找出相關資料，再根據資料回答〔wiki/overview.md〕
- 結合兩種記憶：參數裡「背的」知識＋外部「翻的」資料〔wiki/concepts/parametric-vs-non-parametric-memory.md〕
- 外部資料可以直接修改和擴充，用了哪些資料也能被檢查〔wiki/concepts/parametric-vs-non-parametric-memory.md〕
- 這個名稱來自 2020 年 Lewis et al. 的論文〔wiki/overview.md〕

## 講稿
RAG 的想法很簡單：先從外部的知識庫找出相關資料，再根據這些資料回答〔wiki/overview.md〕。它把兩種記憶結合起來，一種是模型自己背在參數裡的知識，另一種是需要時才去翻的外部資料〔wiki/concepts/parametric-vs-non-parametric-memory.md〕。外部資料可以直接修改和擴充，而且模型用了哪些資料，也能被檢查〔wiki/concepts/parametric-vs-non-parametric-memory.md〕。
