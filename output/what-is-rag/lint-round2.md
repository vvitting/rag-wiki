# Wiki lint：RAG 是什麼？（第 2 輪）

第 1 輪結果見 lint-round1.md。

## 機械性檢查

```

== INFO (2) ==
  - wiki 頁面數：36；[待補來源] 標記：0 處
  - slides/rag-intro.html 尚未產生，略過簡報檢查

結果：0 error, 0 warning
```

## 語意檢查

reviewer（模式 A，第 2 輪）。實際讀取的檔案：wiki/ 下 36 頁，全部在允許清單內（有效）。

**判定：未通過**（嚴重 1、輕微 19）。主持者已確認嚴重問題屬實。此問題在第 1 輪修改前就存在，第 1 輪 reviewer 沒有抓到。

### 嚴重
1. **wiki/sources/07-es2023-ragas.md 第 99 行**：「直接讓 ChatGPT 挑比較好的答案，和人類判斷一致的比例常常不到一半 [07, Table 1, p.5]」。同頁第 63 行（及 concepts/ragas.md 第 51 行）GPT Ranking 是 0.54／0.40／0.52，只有 0.40 低於一半；overview.md、rag-evaluation.md 寫的是「只有 0.40–0.54」。
   - 建議：改成「只有 0.40–0.54」。

### 輕微
2. 06 的 8k context 結果被概括成「8k 最好」，漏了「在全面性上」：lost-in-the-middle.md 第 54 行、context-window.md 第 55 行、sources/04 第 106 行、sources/06 第 110 行。
3. closed-book-vs-open-book.md 第 51 行：缺「20、30 份文件」限定（第 1 輪 #6）。
4. self-rag.md 第 51 行「六個任務勝過參數更多的 LLM」可能過度概括（第 1 輪 #2）。
5. generator.md 第 24 行「把問題和檢索到的文件串接」容易被讀成串成一個長 prompt，和 overview 等頁不一致；sources/01 第 36 行同。
6. overview.md 第 68 行「拆成小步驟」應另引 07 §5（第 1 輪 #9）。
7. overview.md 第 72 行、sources/01 第 120 行「小模型勝過大模型」缺「open-domain QA（NQ）」限定。
8. overview.md 第 76 行的 ⚠️ 沒用 §8 標準格式。
9. Reranking ⚠️ 未同步：retriever.md 95、advanced-rag.md 45、sources/02 78、sources/03 82、sources/01 99；sources/01 101 文件數量 ⚠️（第 1 輪 #4、#5）。
10. retriever.md 第 81 行 GenRead 放錯小節（第 1 輪 #14）。
11. rag-timeline.md 第 24–25 行 GraphRAG／Contextual Retrieval 時間順序不清。
12. context-window.md 第 57 行句意不清。
13. 多頁第一次出現的術語沒連結（hallucination、context-window、lost-in-the-middle、ragas、graphrag、self-rag）。
14. 術語表缺詞條：Hit Rate、MRR、NDCG、F1、BLEU、ROUGE、RLHF、PPO、unsupervised fine-tuning、cross-encoder、HNSW、marginalize、forward pass、Thorough／Fast Decoding、reinforcement learning。
15–19. 需要核對 raw：overview 第 50 行與 sources/03 第 20 行 49%／67% 的頁碼（p.2、p.4–6 vs p.7、p.10）；「chunk 不超過幾百 tokens」頁碼；advanced-rag.md 02 §II-B 的 p.3／p.4；rag-techniques.md Llama2-7B 數字；reranking.md 04 §5 p.9 vs p.10、lost-in-the-middle.md 用 05 §3.3 證明「沒有提到」。
20. 無法讀取 output/what-is-rag/lint.md，無法比對前輪清單（屬設計上的限制，不需處理）。
