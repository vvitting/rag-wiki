---
slide: 8
section: 怎麼運作
title: 先切塊，再把意思轉成向量
---
## 投影片
- **Chunking**：把長文件切成一小段一小段（chunk）〔wiki/concepts/chunking.md〕
- 為什麼要切：配合模型一次能處理的長度限制〔wiki/concepts/chunking.md〕
- 原始 RAG：每篇 Wikipedia 文章切成 100 個英文字一段，共 21M 段〔wiki/concepts/chunking.md〕
- **Embedding**：把一段文字的意思轉成一串數字（向量）〔wiki/concepts/embedding.md〕
- 副作用：切開之後，chunk 可能失去上下文〔wiki/concepts/chunking.md〕

## 講稿
因為 language model 一次能處理的長度有限，所以要先把文件切成小段〔wiki/concepts/chunking.md〕。每一段再用 embedding 轉成一串數字，意思相近的文字，就會被找成相似的結果〔wiki/concepts/embedding.md〕。但切開也有副作用：像「公司營收比上一季成長 3%」這一段，沒說是哪家公司、哪個時期，就很難被找到〔wiki/concepts/chunking.md〕。
