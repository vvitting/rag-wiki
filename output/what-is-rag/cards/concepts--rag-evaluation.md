---
page: wiki/concepts/rag-evaluation.md
---
# 證據卡：RAG 評估

## 重點摘錄
> 評估 RAG 要分開看兩件事：「找得好不好」（retrieval quality）和「寫得好不好」（generation quality）[02-gao2023-survey.pdf, §VI-B, p.12]。
> - **Context relevance**：檢索到的 context 是否精確、切題 [02-gao2023-survey.pdf, §VI-C, p.12]。
> - **Answer faithfulness**：答案是否忠於檢索到的 context，沒有互相矛盾 [02-gao2023-survey.pdf, §VI-C, p.12]。
> - **Answer relevance**：答案是否直接回答了問題 [02-gao2023-survey.pdf, §VI-C, p.12]。

## ⚠️ 爭議
> > ⚠️ **爭議／更新**：[02-gao2023-survey.pdf, §VI-C, p.12] 把 context relevance、answer faithfulness、answer relevance 列為 RAG 的三個主要品質分數；[06-edge2024-graphrag.pdf, §2.4, p.4] 則認為這三個（以 RAGAS 為例）只適用於一般的 vector RAG，和全局理解類的問題無關。RAGAS 原始論文的設定也確實是「一個問題 → 檢索 context → 生成答案」的標準 RAG [07-es2023-ragas.pdf, §3, p.2]。兩者適用的問題類型不同：找特定事實時用前者，理解整批資料時則需要全面性、多樣性這類標準。

## 可以用在
- 怎麼評估（12）：兩個目標、三個品質分數，以及「只適用於一般 RAG」的 ⚠️（對應 V2-02）
