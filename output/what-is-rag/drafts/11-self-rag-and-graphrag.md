---
slide: 11
section: 進階變體
title: 兩個例子：Self-RAG 與 GraphRAG
---
## 投影片
- 問「美國各州的名字怎麼來的」：一般 RAG 寫出和文件不一致的答案〔wiki/sources/05-asai2023-self-rag.md〕
- **Self-RAG**：先判斷要不要查，再為每段打分數，選出最好的那段〔wiki/methods/self-rag.md〕
- 寫暑假作文這種題目，就不用查〔wiki/methods/self-rag.md〕
- **GraphRAG**：先把整批資料整理成關係圖和摘要，回答「整體主題」這類大問題〔wiki/methods/graphrag.md〕
- 代價：事先建 index 很花時間〔wiki/methods/graphrag.md〕

## 講稿
同樣問美國各州的名字怎麼來的，一般 RAG 寫說 California 是以 Christopher Columbus 命名，和它自己找到的文件對不上〔wiki/sources/05-asai2023-self-rag.md〕。Self-RAG 則是每寫一段前先判斷要不要查，再為每段打分數，最後選中「11 個州以人名命名」那段，因為它完全被文件支持〔wiki/sources/05-asai2023-self-rag.md〕。GraphRAG 適合「這批資料的主要主題是什麼」這種大問題，在 Podcast 資料上，GraphRAG 等全局方法的全面性勝率是 72%–83%〔wiki/methods/graphrag.md〕。
