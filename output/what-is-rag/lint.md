# Wiki lint：RAG 是什麼？（第 3 輪）

前兩輪結果見 lint-round1.md、lint-round2.md。

## 機械性檢查

```

== INFO (2) ==
  - wiki 頁面數：36；[待補來源] 標記：0 處
  - slides/rag-intro.html 尚未產生，略過簡報檢查

結果：0 error, 0 warning
```

## 語意檢查

reviewer（模式 A，第 3 輪）。實際讀取的檔案：wiki/ 下 36 頁，全部在允許清單內（有效）。

**判定：未通過**（嚴重 1、輕微 21）。主持者已確認嚴重問題屬實。
注意：此問題在第 1、2 輪都被列為「輕微」（第 1 輪 #2、第 2 輪 #4），第 3 輪被提升為「嚴重｜矛盾未標註」。

### 嚴重
1. **wiki/methods/self-rag.md 第 51 行**：「在六個任務上，勝過參數更多的 LLM，以及傳統的 RAG 方法 [05, §6, p.10]」。sources/05 Table 2：ChatGPT（不檢索）TriviaQA 74.3、ARC-C 75.3，都高於 Self-RAG 13B 的 69.3、73.1；sources/05 第 74–75 行只說「所有任務上是非商用模型中最好」「在 PubHealth、PopQA、傳記、ASQA 上勝過 ChatGPT」；overview.md 第 56 行也是「在多個任務上」。
   - 建議：補上限定；若 05 §6 原文確實這樣寫，加 ⚠️ 標成「原文結論與 Table 2 不一致」。

### 輕微
2. self-rag.md 第 41 行「150k 筆訓練資料」：附錄為 145,619 筆，應註明約數。
3. overview 第 58 行、graphrag.md 第 56 行、rag-techniques 第 25 行：72%–83%／62%–82% 是「GraphRAG 等全局方法」且分資料集（Podcast／新聞），被全算在 GraphRAG 上。
4. naive-rag.md 第 65 行原始 RAG 欄「直接串接」未跟上上一輪 generator／sources/01 的修正。
5. ragas.md 第 60 行 Self-RAG 部分應引 05（第 1 輪 #13）。
6. ragas.md 與 rag-evaluation.md 第 58–66 行內容重複。
7. retriever.md 第 81 行 GenRead 放錯小節。
8. Reranking／文件數量 ⚠️ 未同步：retriever.md 41、95；advanced-rag.md 45；sources/01 99、101；sources/02 78。
9. sources/04 第 106 行「06 說前段容易被漏掉」未用 ⚠️ 格式，和 log 第 76 行不一致。
10. contextual-retrieval.md 第 56 行「摘要 indexing 表現很差」未標 ⚠️（chunking、03、06 有）。
11. context-window.md 第 57 行句意不清。
12. analogies.md 第 58 行「20 本比 50 本有用」說太滿，比喻的極限應補「50 本仍略好」。
13. rag-paradigms.md 第 11 行未提 Naive RAG 是否「最早」的 ⚠️。
14. rag-timeline.md 第 24–25 行排序。
15. 方法頁「## 出處」區塊和 frontmatter sources 不一致（advanced、contextual、self-rag、graphrag、modular）。
16. overview.md 術語第一次出現沒連結：vector database、top-k、prompt、BM25、knowledge graph、Exact Match、tokens。
17. 術語表缺詞條：cross-encoder、F1、BLEU、ROUGE、Hit Rate、MRR、NDCG、Leiden。
18–22. 需要核對 raw：「chunk 不超過幾百 tokens」頁碼；overview 第 50 行 49%／67% 頁碼；Llama2-7B 38.2／30.0、Llama2-13B ARC-C 29.4；06 評審用 GPT-4 或 gpt-4-turbo；self-rag.md 第 51 行 05 §6 原文用詞。
