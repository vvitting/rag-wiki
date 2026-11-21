# Wiki lint：RAG 是什麼？

## 機械性檢查

```

== INFO (2) ==
  - wiki 頁面數：36；[待補來源] 標記：0 處
  - slides/rag-intro.html 尚未產生，略過簡報檢查

結果：0 error, 0 warning
```

## 語意檢查

reviewer（模式 A，第 1 輪）。實際讀取的檔案：wiki/ 下 36 頁，全部在允許清單內（有效）。

**判定：未通過**（嚴重 1、輕微 16）。主持者已用 grep 確認嚴重問題屬實。

### 嚴重
1. **wiki/comparisons/rag-techniques.md 第 20 行**（Reranking 列）：「和上一列合用時，失敗率總共降低 67%」。「上一列」是 Hybrid retrieval（embedding + BM25），但 methods/contextual-retrieval.md 第 40 行、sources/03 第 55 行都寫明 67% 是「Contextual Embeddings + Contextual BM25 + reranking」的結果。照字面讀會以為一般 hybrid + reranking 就能降低 67%。
   - 建議：改成「在 Contextual Embeddings + Contextual BM25 之上再加 reranking，失敗率總共降低 67%（5.7% → 1.9%）」。

### 輕微
2. methods/self-rag.md 第 51 行「在六個任務上，勝過參數更多的 LLM，以及傳統的 RAG 方法」：和 sources/05 Table 2 不一致（ChatGPT 在 TriviaQA、ARC-C 高於 Self-RAG 13B）。建議加限定。
3. concepts/hallucination.md 第 19 行（及 overview.md 第 22 行）「RAG 能有效減少產生錯誤內容」：naive-rag.md 已對同類概括加 ⚠️，這頁沒有。建議加 ⚠️ 或連到 closed-book-vs-open-book.md。
4. reranking 爭議的 ⚠️ 沒同步：retriever.md 第 95 行、advanced-rag.md 第 45 行、sources/02 第 78 行只寫到 02、03；sources/01 第 99 行只寫到 02。建議補上 04 與「情境不同，詳見 Reranking」。
5. sources/01 第 101 行「文件數量」的 ⚠️ 只對照 02，未跟上 context-window.md 的整合。
6. comparisons/closed-book-vs-open-book.md 第 51 行「答案放在中間時，open-book 低於 closed-book」：拿掉了「20／30 份文件、最差位置」的限定。
7. concepts/lost-in-the-middle.md 第 54 行把 06 的 8k context 實驗列為減輕方法，因果可能被放大。
8. overview.md 第 37 行沒提原始 RAG 是「文件分別處理再加權合併」，和 naive-rag、reranking 等頁的關鍵論點不一致。
9. overview.md 第 65 行「拆成小步驟」應另引 07 §5。
10. overview.md 第 15、23 行：hallucination、context window、LLM 第一次出現沒有連結。
11. 多個術語第一次出現時沒有解釋、術語表也沒有：Hit Rate、MRR、NDCG、F1、BLEU、ROUGE、RLHF、PPO、HNSW、Transformer、self-attention、MAUVE、NQ、TriviaQA、FEVER、MS-MARCO。
12. 術語表有、但頁面上沒有連結：MIPS、Leiden／map-reduce、cosine、segment-level beam search。
13. concepts/ragas.md 第 60 行：Self-RAG 那一半應引用 05，不是 07。
14. concepts/retriever.md 第 81 行 GenRead 放錯小節。
15. 建議新增頁面：BM25／hybrid retrieval、LLM-as-a-judge、Robustness。
16. context-window.md 與 lost-in-the-middle.md 有三組重複內容，減輕方法清單已不同步。
17. 需要核對 raw（不在 reviewer 允許範圍）：(a) analogies.md「年份不對應只剩 4%」的對應組合；(b)「chunk 通常不超過幾百 tokens」在三頁引用的頁碼不一致（03 p.2／p.3／p.2–3）；(c) rag-techniques.md 第 26 行 Llama2-7B 數字；(d) self-rag.md 第 51 行原句；(e) sources/03 第 88 行 49% 長條圖頁碼 p.8 vs 表格 p.7。
