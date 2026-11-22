---
slide: 7
section: 怎麼運作
title: 走一遍：一個問題的旅程
---
## 投影片
- 問題：「Define "middle ear"」（中耳是什麼）〔wiki/sources/01-lewis2020-rag.md〕
- 把問題轉成向量，從 Wikipedia 的 index 找出最相關的幾份文件〔wiki/sources/01-lewis2020-rag.md〕
- 依每份文件分別寫答案，再合併成最後的答案〔wiki/sources/01-lewis2020-rag.md〕
- 輸出：「中耳包含鼓室和三塊聽小骨」〔wiki/sources/01-lewis2020-rag.md〕
- 對照：不查資料的 BART 把中耳講錯了〔wiki/concepts/hallucination.md〕

## 圖
問題 → 轉成向量 → 找出相關文件 → 寫出答案〔wiki/sources/01-lewis2020-rag.md〕

## 講稿
我們跟著原始 RAG 論文的圖，看一個問題怎麼走完全程〔wiki/sources/01-lewis2020-rag.md〕。問題「中耳是什麼」先被轉成向量，系統再從 Wikipedia 的 index 裡找出最相關的幾份文件〔wiki/sources/01-lewis2020-rag.md〕。模型依照每一份文件分別寫答案、再合併，最後輸出「中耳包含鼓室和三塊聽小骨」〔wiki/sources/01-lewis2020-rag.md〕。同一個問題，不查資料的 BART 卻回答錯了〔wiki/concepts/hallucination.md〕。
