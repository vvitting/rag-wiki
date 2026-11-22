---
slide: 9
section: 怎麼運作
title: 找資料：用意思找，也用字找
---
## 投影片
- **Retriever** 負責查資料：從一大堆文件中找出最相關的幾份〔wiki/concepts/retriever.md〕
- Embedding 擅長找「意思相近」的內容〔wiki/concepts/embedding.md〕
- 但可能漏掉精確字串，例如錯誤碼「TS-999」〔wiki/concepts/embedding.md〕
- **BM25** 靠字面比對，專門找精確的詞〔wiki/concepts/retriever.md〕
- 兩種一起用，比只用 embedding 好〔wiki/concepts/retriever.md〕

## 講稿
負責找資料的元件叫 retriever，它找到的文件好不好，直接影響答案好不好〔wiki/concepts/retriever.md〕。就像問圖書館員有沒有講心臟病的書，館員會依意思推薦，這就像 embedding；但要找書號「TS-999」，就該直接比對字串，這就像 BM25〔wiki/analogies.md〕。實驗也發現，embedding 加上 BM25，比只用 embedding 好〔wiki/concepts/retriever.md〕。
