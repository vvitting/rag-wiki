---
slide: 6
section: 怎麼運作
title: 三個步驟：建索引、找資料、寫答案
---
## 投影片
- **Indexing**：把文件切成 chunk，轉成向量，存進資料庫〔wiki/overview.md〕
- **Retrieval**：把問題也轉成向量，找出最相似的幾個 chunk〔wiki/overview.md〕
- **Generation**：把問題和 chunk 組成 prompt，交給 LLM 寫答案〔wiki/overview.md〕
- 比喻：圖書館員（retriever）找書，作家（generator）讀完寫答案〔wiki/analogies.md〕

## 圖
文件 → 切塊與向量 → 找出相關段落 → LLM 寫答案〔wiki/overview.md〕

## 講稿
最基本的 RAG 流程只有三步〔wiki/overview.md〕。先把文件切成小段、轉成向量存起來；收到問題時，把問題也轉成向量，找出最相似的幾段〔wiki/overview.md〕。最後把問題和找到的段落一起交給 LLM 寫出答案，就像圖書館員先找書、作家再讀完書寫出回答〔wiki/overview.md〕〔wiki/analogies.md〕。
