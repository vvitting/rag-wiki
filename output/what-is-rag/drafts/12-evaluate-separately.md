---
slide: 12
section: 怎麼評估
title: 評估要分開看：找得好不好、寫得好不好
---
## 投影片
- 「找資料」和「寫答案」要分開評估〔wiki/concepts/rag-evaluation.md〕
- **Context relevance**：找來的資料切不切題〔wiki/concepts/rag-evaluation.md〕
- **Faithfulness**：答案是不是忠於找來的資料〔wiki/concepts/rag-evaluation.md〕
- **Answer relevance**：答案有沒有直接回答問題〔wiki/concepts/rag-evaluation.md〕
- ⚠️ 這三個分數適用於一般 RAG，不適合「整批資料的主題」這類問題〔wiki/concepts/rag-evaluation.md〕

## 講稿
評估 RAG 時，要分開看「找得好不好」和「寫得好不好」〔wiki/concepts/rag-evaluation.md〕。就像老師改開書考，會分開看翻對頁了沒、有沒有亂掰、有沒有離題，才知道學生是哪裡出問題〔wiki/analogies.md〕。RAGAS 這類工具不需要標準答案，而是把判斷拆成小步驟讓 LLM 評分〔wiki/concepts/ragas.md〕。不過 faithfulness 高，不代表答案就是對的，因為找來的資料本身也可能有錯〔wiki/concepts/ragas.md〕。
