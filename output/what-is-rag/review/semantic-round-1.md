# ②b 相關頁語意檢查 — 第 1 輪（reviewer 模式 A 完整輸出）

- 允許讀取：sources.md 的 14 頁、raw-text/01–07、issues.md
- 核對「實際讀取的檔案」：全部在清單內（有效）
- 判定：嚴重 0、輕微 17 → 通過

---

## 舊問題狀態
issues.md 沒有「待修」的條目。我抽查了和這 14 頁有關的已登記問題，全部仍維持已修或已核對的狀態，沒有復發：
- E03：已解決。wiki/methods/self-rag.md 第 53 行的 ⚠️ 還在。數字和 raw-text/05 page 8 的 Table 2 一致（ChatGPT TQA 74.3、ARC 75.3；Self-RAG 13B 69.3、73.1）。§6 p.10 和 §1 p.2 的原文也對得上。
- Q01：已解決。overview.md 第 24 行、hallucination.md 第 21 行都有 ⚠️。
- Q03：已解決。closed-book-vs-open-book.md 第 51 行保留了「20 和 30 份文件、最差位置」的限定。和 raw-text/04 page 5 一致。
- Q04：已解決。overview.md 第 72 行有「open-domain QA（例如 NQ）」的限定。
- Q05：已解決。naive-rag.md 第 65 行寫的是「分別串接，再 marginalize」。
- Q06：已解決。overview.md 第 58 行、graphrag.md 第 56–58 行都寫「GraphRAG 等全局方法」，並且分開寫資料集。和 raw-text/06 page 9 一致（72–83%／72–80%／75–82%／62–71%）。
- Q07：已解決。analogies.md 第 60 行已補上限制。
- W01、W02：已解決。retriever.md 第 41–42 行、第 96–97 行的 ⚠️ 是新版（01／02／03／04（＋06），加上「情境不同」）。
- W05：已解決。rag-paradigms.md 第 13 行有 ⚠️。
- W06：已解決。overview.md 第 78 行是標準 ⚠️ 區塊。
- W07：已解決。self-rag.md 第 53 行的 ⚠️ 後面有空行。
- C01、C02、C07、C10、C11、C12：已解決。overview.md 第 68 行、ragas.md 第 60 行、closed-book 第 62 行、rag-evaluation.md 第 114 行、analogies.md 第 40 行、parametric 第 35 行、self-rag.md 第 41 行都和 raw-text 一致。
- T01：已解決。
- S01：已解決。
- S04：已解決。

## 問題清單（只列新問題）

這一輪沒有發現嚴重問題。抽查過的數字（每頁至少 3 處，共 80 處以上）都和 raw-text 對得上。下面全部是輕微問題。

### wiki/overview.md
1. [輕微｜限定條件] 第 67–68 行：「faithfulness 和人類判斷的一致度達 0.95」「一致的比例只有 0.40–0.54」
   - 來源：raw-text/07 page 5 的 Table 1 標題寫「using the WikEval dataset (accuracy)」。
   - 說明：拿掉了資料集的限定。hallucination.md 第 38 行有寫「在 WikiEval 上」，overview 沒寫。
   - 建議：補上「在 WikiEval 資料集上」。
2. [輕微｜⚠️ 同步] 第 63 行：「三個品質分數是 context relevance、answer faithfulness、answer relevance」
   - 來源：rag-evaluation.md 第 109 行和 ragas.md 第 62 行都有 ⚠️：06 §2.4 p.4 認為這三個分數只適用於 vector RAG。
   - 說明：overview 是簡報骨架，這裡只有一般敘述，沒有提醒適用範圍。
   - 建議：加一句短的限定，或連到 rag-evaluation 的 ⚠️。

### wiki/concepts/hallucination.md
3. [輕微｜⚠️ 同步] 第 21 行的 ⚠️ 用的證據是 04 加上 05 App. C.1 p.20。
   - 說明：overview.md 第 24 行和 naive-rag.md 第 36–38 行是對同一句 02 的說法加 ⚠️，用的卻是 04 加上 05 Table 2 p.8（ChatGPT 的 PubHealth 從 70.1 降到 54.7）。這幾處對同一個主題列的反證不一樣。
   - 建議：三處統一成同一組證據。
4. [輕微｜可讀性] 第 25、30、34 行：BART、ISSUP token、instruction-tuned 第一次出現時沒有連結。

### wiki/concepts/parametric-vs-non-parametric-memory.md
5. [輕微｜限定條件] 第 65 行：「推論時完全不檢索，Self-RAG 在 PopQA 上從 45.5 掉到 24.7，在 PubHealth 上則幾乎不變（73.5 → 73.0）」
   - 來源：raw-text/05 page 9。這組數字是消融實驗，Fig.3 標題寫「based on our 7B model」；§5.2 寫「we use a training instance size of 50k」。
   - 說明：拿掉了「7B、用 50k 筆訓練資料的消融版本」這個限定。完整版 Self-RAG 7B 在 Table 2 p.8 的 PopQA 是 54.9，讀者可能會混淆。
   - 建議：補上「在 50k 訓練資料的 7B 消融實驗中」。

### wiki/comparisons/closed-book-vs-open-book.md
6. [輕微｜引用] 第 56 行：「Self-RAG 論文也觀察到，加上檢索後，部分任務的表現反而下降 [05, §5.1, p.8]」
   - 來源：raw-text/05 page 8 的 §5.1 寫的是「baselines with retrieval do not improve performance notably from their no-retrieval counterparts」。
   - 說明：§5.1 說的是「沒有明顯進步」。「下降」要從 Table 2 的數字才看得到。這句的意思沒有講反，但引用的位置沒有直接說「下降」。
   - 建議：改引 Table 2, p.8，或把措辭改成和 §5.1 一致。
7. [輕微｜限定條件] 第 42 行：「04 在 LLM 上比較了三種設定：不給文件、給 20 份文件……、只給答案文件」
   - 來源：raw-text/04 page 5（§2.3）寫的是「input contexts containing 10, 20, and 30 total documents」。
   - 說明：只寫 20 份，容易讓人以為實驗只有一種文件數。
   - 建議：寫成「給 10／20／30 份文件（下表以 20 份為例）」。
8. [輕微｜可讀性] NQ、Exact Match、T5、REALM、DPR、oracle 第一次出現時沒有連結。issues.md T02 顯示術語表有 NQ 詞條。

### wiki/analogies.md
9. [輕微｜限定條件] 第 68 行：「補上 50–100 tokens 的說明後，檢索失敗率降低 35%–49%」
   - 來源：raw-text/03 page 7。35% 只用了 Contextual Embeddings（5.7% → 3.7%）；49% 要再加上 Contextual BM25（5.7% → 2.9%）。
   - 說明：這個範圍把兩種設定合在一起，沒有說 49% 需要搭配 BM25。
   - 建議：分開寫兩種設定。

### wiki/methods/naive-rag.md
10. [輕微｜可讀性] 第 13 行的 LLM、top-k，第 22 行的 embedding model、vector database，第一次出現時沒有連結（chunk 有連結）。

### wiki/concepts/chunking.md
11. [輕微｜可讀性] 第 25 行的 token 第一次出現時沒有連結。

### wiki/concepts/embedding.md
12. [輕微｜可讀性] 第 17、23、33 行：vector database、cosine similarity、FAISS、MIPS、HNSW 沒有連結。issues.md T02 顯示術語表有 HNSW；retriever.md 的 MIPS 已連到術語表。

### wiki/concepts/retriever.md
13. [輕微｜措辭] 第 39 行：「LLM 的表現卻在大約 20 份時就停止進步了」
   - 來源：raw-text/04 page 10 寫「saturates long before retriever」「Using more than 20 retrieved documents only marginally improves reader performance (∼1.5% … ∼1%)」。
   - 說明：「停止進步」比原文說得滿。同一頁第 41 行的 ⚠️ 又寫「只多約 1%–1.5%」，兩處說法略有落差。這和 Q07 是同一類問題，但出現在不同頁。
   - 建議：改成「超過 20 份後幾乎不再進步（只多約 1%–1.5%）」。
14. [輕微｜可讀性] DPR、bi-encoder、FEVER、NQ、EM 第一次出現時沒有連結。issues.md T02 顯示術語表有 FEVER、NQ。

### wiki/methods/self-rag.md
15. [輕微｜引用] 第 24 行：「依 02 的分類，Self-RAG 屬於 Modular RAG 中的 adaptive retrieval [02, §V-C, p.11–12]」
   - 來源：raw-text/02 page 11–12 的 §V-C 只說 Self-RAG 是 adaptive retrieval，沒有提到 Modular RAG。把 Self-RAG 和 Modular RAG 連在一起的是 §II-C p.5：「The flexible orchestration of Modular RAG Flow showcases the benefits of adaptive retrieval through techniques such as FLARE and Self-RAG」。
   - 建議：補上 §II-C, p.5。
16. [輕微｜可讀性] 第 13 行的 LLM、reflection tokens 第一次出現時沒有連結。術語表不在允許讀取的清單內，我無法確認有沒有對應詞條。

### wiki/concepts/rag-evaluation.md
17. [輕微｜可讀性] 第 26、40 行：EM、F1、BLEU、ROUGE、Hit Rate、MRR、NDCG 沒有連結。issues.md T02 顯示術語表有這些詞條。

（wiki/comparisons/rag-paradigms.md、wiki/methods/graphrag.md、wiki/concepts/ragas.md 沒有發現新問題。）

## 統計
- 嚴重：0；輕微：17
- 需要修正的 wiki 頁（都只有輕微問題）：wiki/overview.md、wiki/concepts/hallucination.md、wiki/concepts/parametric-vs-non-parametric-memory.md、wiki/comparisons/closed-book-vs-open-book.md、wiki/analogies.md、wiki/methods/naive-rag.md、wiki/concepts/chunking.md、wiki/concepts/embedding.md、wiki/concepts/retriever.md、wiki/methods/self-rag.md、wiki/concepts/rag-evaluation.md

## 實際讀取的檔案
- /Users/ting/rag-wiki/output/what-is-rag/issues.md
- /Users/ting/rag-wiki/wiki/overview.md
- /Users/ting/rag-wiki/wiki/concepts/hallucination.md
- /Users/ting/rag-wiki/wiki/concepts/parametric-vs-non-parametric-memory.md
- /Users/ting/rag-wiki/wiki/comparisons/closed-book-vs-open-book.md
- /Users/ting/rag-wiki/wiki/analogies.md
- /Users/ting/rag-wiki/wiki/methods/naive-rag.md
- /Users/ting/rag-wiki/wiki/concepts/chunking.md
- /Users/ting/rag-wiki/wiki/concepts/embedding.md
- /Users/ting/rag-wiki/wiki/concepts/retriever.md
- /Users/ting/rag-wiki/wiki/comparisons/rag-paradigms.md
- /Users/ting/rag-wiki/wiki/methods/self-rag.md
- /Users/ting/rag-wiki/wiki/methods/graphrag.md
- /Users/ting/rag-wiki/wiki/concepts/rag-evaluation.md
- /Users/ting/rag-wiki/wiki/concepts/ragas.md
- /Users/ting/rag-wiki/raw-text/01-lewis2020-rag.md（部分：page 1–10、17–19）
- /Users/ting/rag-wiki/raw-text/02-gao2023-survey.md（部分：page 1–9、11–17）
- /Users/ting/rag-wiki/raw-text/03-anthropic-contextual-retrieval.md（全文）
- /Users/ting/rag-wiki/raw-text/04-liu2023-lost-in-middle.md（部分：page 1–6、8–11、14–18）
- /Users/ting/rag-wiki/raw-text/05-asai2023-self-rag.md（部分：page 1–11、17–21）
- /Users/ting/rag-wiki/raw-text/06-edge2024-graphrag.md（部分：page 1–12、18–22）
- /Users/ting/rag-wiki/raw-text/07-es2023-ragas.md（部分：page 1–6）
