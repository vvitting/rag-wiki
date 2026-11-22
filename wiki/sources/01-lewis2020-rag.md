---
type: source
title: "Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks"
raw: 01-lewis2020-rag.pdf
authors: [Patrick Lewis, Ethan Perez, Aleksandra Piktus, Fabio Petroni, Vladimir Karpukhin, Naman Goyal, Heinrich Küttler, Mike Lewis, Wen-tau Yih, Tim Rocktäschel, Sebastian Riedel, Douwe Kiela]
year: 2020
tags: [rag, foundational, retriever, generator, dpr, bart, open-domain-qa]
sources: [01-lewis2020-rag.pdf, 02-gao2023-survey.pdf, 05-asai2023-self-rag.pdf, 03-anthropic-contextual-retrieval.pdf, 04-liu2023-lost-in-middle.pdf, 06-edge2024-graphrag.pdf]
updated: 2026-11-22
---

# Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks（Lewis et al., 2020，原始 RAG 論文）

這篇論文提出並命名了「retrieval-augmented generation（RAG）」[01-lewis2020-rag.pdf, §1, p.2]。作者來自 Facebook AI Research、University College London 與 New York University [01-lewis2020-rag.pdf, p.1]。raw 檔是 arXiv 2005.11401 的 v4 版（2021 年 4 月 12 日）[01-lewis2020-rag.pdf, p.1]。

## 一句話摘要

把一個會「寫」答案的 [generator](../concepts/generator.md)，接上一個會「查」資料的 [retriever](../concepts/retriever.md)：回答前先到 Wikipedia 找相關段落，再根據找到的內容寫出答案 [01-lewis2020-rag.pdf, Abstract, p.1]。

## 這篇想解決什麼問題

- 預訓練的 language model 會從資料裡學到大量知識，並把知識存在自己的參數裡 [01-lewis2020-rag.pdf, §1, p.1]。
- 但這種模型有三個缺點：很難擴充或修改記憶、無法說明答案從哪裡來、可能產生 [hallucination](../concepts/hallucination.md) [01-lewis2020-rag.pdf, §1, p.1]。
- 在需要大量知識的任務上，這類模型的表現落後專門設計的系統 [01-lewis2020-rag.pdf, Abstract, p.1]。
- 作者所說的 knowledge-intensive task，是指「人類沒有外部知識來源就不太可能完成」的任務 [01-lewis2020-rag.pdf, §1, p.2]。
- 之前結合檢索的模型（REALM、ORQA）只做 extractive QA，也就是從文件裡「挑出」一段當答案 [01-lewis2020-rag.pdf, §1, p.1–2]。
- 本篇想把檢索帶進可以「生成」任意文字的 seq2seq 模型 [01-lewis2020-rag.pdf, §1, p.2]。

## 核心方法

詳見 [原始 RAG 方法頁](../methods/original-rag.md)。

- **兩個元件**：retriever 根據輸入 x 找出文件 z；generator 根據 x 和 z 逐字產生答案 y [01-lewis2020-rag.pdf, §2, p.2–3]。
- **Retriever 用 DPR**：document encoder 和 query encoder 都是 BERT-base（bi-encoder 架構）；找出最相關的文件被視為 Maximum Inner Product Search（MIPS）問題 [01-lewis2020-rag.pdf, §2.2, p.3]。
- **Generator 用 BART-large**：一個有 400M 參數的預訓練 seq2seq transformer [01-lewis2020-rag.pdf, §2.3, p.3]。
- **怎麼把資料交給 generator**：把輸入 x 和每一份檢索到的文件 z 分別串接（concatenate）起來 [01-lewis2020-rag.pdf, §2.3, p.3]，再對各份文件的結果加權合併（marginalize），不是把所有文件串成一段 [01-lewis2020-rag.pdf, §2.1, p.3]。
- **兩種版本**：RAG-Sequence 整個答案都根據同一份文件；RAG-Token 每產生一個 token 都可以根據不同的文件 [01-lewis2020-rag.pdf, §2.1, p.3]。
- **訓練方式**：retriever 和 generator 一起訓練，但不告訴模型「應該找哪份文件」[01-lewis2020-rag.pdf, §2.4, p.3]。
- **訓練時固定的部分**：document encoder 和 index 都不更新，只微調 query encoder 和 BART，作者認為這樣已足以得到強表現 [01-lewis2020-rag.pdf, §2.4, p.4]。
- **知識庫**：使用 2018 年 12 月的 Wikipedia，每篇文章切成互不重疊的 100-word [chunk](../concepts/chunking.md)，共 21M 份文件 [01-lewis2020-rag.pdf, §3, p.4]。
- **Index**：用 document encoder 為每份文件算出 [embedding](../concepts/embedding.md)，再用 FAISS 建立 MIPS index [01-lewis2020-rag.pdf, §3, p.4]。
- **取幾份文件**：訓練時取 top-k，k 為 5 或 10；測試時的 k 由 dev data 決定 [01-lewis2020-rag.pdf, §3, p.4]。
- **兩種記憶**：BART 的參數稱為 parametric memory，document index 稱為 non-parametric memory；詳見 [兩種記憶](../concepts/parametric-vs-non-parametric-memory.md) [01-lewis2020-rag.pdf, §2.2–2.3, p.3]。

## 關鍵結果（數字務必附出處）

### Open-domain QA（Exact Match，越高越好）

| 模型 | 類型 | NQ | WQ | CT | 出處 |
|---|---|---|---|---|---|
| T5-11B | closed-book | 34.5 | 37.4 | – | [01-lewis2020-rag.pdf, Table 1, p.6] |
| T5-11B+SSM | closed-book | 36.6 | 44.7 | – | [01-lewis2020-rag.pdf, Table 1, p.6] |
| REALM | open-book | 40.4 | 40.7 | 46.8 | [01-lewis2020-rag.pdf, Table 1, p.6] |
| DPR | open-book | 41.5 | 41.1 | 50.6 | [01-lewis2020-rag.pdf, Table 1, p.6] |
| RAG-Token | open-book | 44.1 | 45.5 | 50.0 | [01-lewis2020-rag.pdf, Table 1, p.6] |
| RAG-Sequence | open-book | 44.5 | 45.2 | 52.2 | [01-lewis2020-rag.pdf, Table 1, p.6] |

- RAG 在四個 open-domain QA 資料集上都創下當時的最佳成績；TriviaQA 只有在和 T5 可比較的那個 split 上是最佳 [01-lewis2020-rag.pdf, §4.1, p.5]。
- 檢索到的文件裡都沒有正確答案時，RAG 在 NQ 上仍有 11.8% 答對，extractive 模型則是 0% [01-lewis2020-rag.pdf, §4.1, p.6]。

> ⚠️ **爭議／更新**：本篇把這 11.8% 視為優點 [01-lewis2020-rag.pdf, §4.1, p.6]；[05-asai2023-self-rag.pdf, App. C.1, p.20] 則把「答案幾乎都來自文件」（Self-RAG 只有 2% 不在文件中）視為優點。詳見 [Parametric 與 non-parametric memory](../concepts/parametric-vs-non-parametric-memory.md)。

- 模型大小：RAG 共有 626M 個可訓練參數；最好的 closed-book 模型 T5-11B 有 11B 個 [01-lewis2020-rag.pdf, App. G, p.18–19]。
- 參數量最接近的 T5-large（770M）在 NQ 只有 28.9 EM，遠低於 RAG-Sequence 的 44.5 [01-lewis2020-rag.pdf, App. G, p.19]。

### 生成任務

- MS-MARCO：RAG-Sequence 比 BART 高 2.6 BLEU-1 與 2.6 ROUGE-L [01-lewis2020-rag.pdf, §4.2, p.6]。
- Jeopardy 出題的人工評估（452 組）：認為 BART 比較符合事實的只有 7.1%，認為 RAG 比較符合事實的有 42.7% [01-lewis2020-rag.pdf, §4.3, p.6; Table 4, p.8]。
- 同一份人工評估中，認為 RAG 比較具體（specific）的有 37.4%，認為 BART 比較具體的有 16.8% [01-lewis2020-rag.pdf, Table 4, p.8]。
- 用「不重複的 tri-gram 比例」衡量多樣性，Jeopardy 出題的結果是：BART 32.4%、RAG-Token 46.8%、RAG-Sequence 53.8% [01-lewis2020-rag.pdf, Table 5, p.8]。

> ⚠️ **爭議／更新（原文內部不一致）**：內文說「both RAG and BART were factual in a further 17% of cases」[01-lewis2020-rag.pdf, §4.3, p.6]；但 Table 4 的 Factuality 欄是「Both good 11.7%」「Both poor 17.7%」[01-lewis2020-rag.pdf, Table 4, p.8]。兩邊數字對不上，引用時建議以 Table 4 為準並註明。

### 事實查核（FEVER）

- 3-way 分類的準確率是 72.5，和當時最佳的 76.8 相差 4.3% [01-lewis2020-rag.pdf, Table 2, p.6; §4.4, p.6]。
- 2-way 分類的準確率是 89.5，和使用標準證據的模型（92.2）相差 2.7% [01-lewis2020-rag.pdf, Table 2, p.6; §4.4, p.7]。
- 檢索到的第 1 份文件，有 71% 的情況來自人工標註的正確文章；前 10 份文件中有正確文章的比例是 90% [01-lewis2020-rag.pdf, §4.4, p.7]。

### 消融實驗與其他發現

- 把 retriever 凍結（不訓練）後，所有任務的表現都下降，表示「學會檢索」是有幫助的 [01-lewis2020-rag.pdf, §4.5, p.7; Table 6, p.8]。
- 把 dense retriever 換成 BM25 時，FEVER 反而表現最好；其他任務則都是 dense retriever 比較好，open-domain QA 尤其明顯 [01-lewis2020-rag.pdf, §4.5, p.7]。
- 例如在 NQ dev set 上，RAG-Token 用 BM25 只有 29.7 EM，用原本的 retriever 則是 43.5 [01-lewis2020-rag.pdf, Table 6, p.8]。
- **換 index 就能更新知識**：作者用 82 位在 2016 到 2018 年間換人的世界領袖做測試 [01-lewis2020-rag.pdf, §4.5, p.7–8]。
- 用 2016 年的 index 回答 2016 年的領袖，答對 70%；用 2018 年的 index 回答 2018 年的領袖，答對 68% [01-lewis2020-rag.pdf, §4.5, p.8]。
- index 和年份不對應時只剩 12%（2018 年的 index、2016 年的領袖）與 4%（2016 年的 index、2018 年的領袖）答對 [01-lewis2020-rag.pdf, §4.5, p.8]。
- **取更多文件**：RAG-Sequence 在 NQ 上取越多份文件，表現就越好；RAG-Token 則在 10 份時最好 [01-lewis2020-rag.pdf, §4.5, p.8; Fig.3, p.8]。
- **成本**：把整個 Wikipedia 的 index 放在 CPU 記憶體需要約 100 GB，壓縮後降到 36 GB [01-lewis2020-rag.pdf, App. C, p.17]。

## 限制與後續爭議

- **Retrieval collapse**：在 story generation 等任務上，retriever 會「崩潰」，不管輸入是什麼都找同一批文件，generator 也就開始忽略文件 [01-lewis2020-rag.pdf, App. H, p.19]。
- **知識來源本身可能有錯**：Wikipedia 或任何外部知識來源都不可能完全正確、毫無偏見 [01-lewis2020-rag.pdf, Broader Impact, p.10]。
- **知識庫涵蓋不到的問題**：有些 MS-MARCO 的問題光靠 Wikipedia 答不出來，這時 RAG 只能依賴 parametric knowledge [01-lewis2020-rag.pdf, §3.2, p.5]。
- **Retriever 不是從零開始學**：RAG 的 retriever 用 DPR 初始化，而 DPR 本身在 NQ 和 TriviaQA 上有用到檢索監督 [01-lewis2020-rag.pdf, §4.1, p.5]。
- **「不需要 re-ranker」的主張**：作者認為要達到當時的最佳表現，re-ranker 和 extractive reader 都不是必要的 [01-lewis2020-rag.pdf, §4.1, p.5]。

> ⚠️ **爭議／更新**：[01-lewis2020-rag.pdf, §4.1, p.5] 認為，要達到當時的最佳表現，re-ranker 不是必要的；但 [02-gao2023-survey.pdf, §II-B, p.4] 把 reranking 視為 Advanced RAG 的關鍵策略，[03-anthropic-contextual-retrieval.pdf, p.10–11] 的實驗顯示 reranking 能進一步降低檢索失敗率，[04-liu2023-lost-in-middle.pdf, §5, p.10] 也建議用 reranking 來應對位置效應。
> 情境不同：01 是每份文件分別交給 generator 再加權合併 [01-lewis2020-rag.pdf, §2.1, p.3]，所以沒有「文件排在 prompt 哪個位置」的問題；02、03、04 談的則是把多份文件串成一個 prompt 交給 LLM 的情境 [02-gao2023-survey.pdf, §II-A, p.3] [04-liu2023-lost-in-middle.pdf, §5, p.9]。詳見 [Reranking](../concepts/reranking.md)。

> ⚠️ **爭議／更新**：「要放多少份文件」各來源的說法不一致：[01-lewis2020-rag.pdf, §4.5, p.8] 發現 RAG-Sequence 取越多份文件，NQ 表現越好；[02-gao2023-survey.pdf, §IV-A, p.10] 認為「盡量多檢索」是常見的誤解，過多的 context 會帶來雜訊；[03-anthropic-contextual-retrieval.pdf, p.8] 實測 5、10、20 個 chunk，20 個最好；[04-liu2023-lost-in-middle.pdf, §5, p.10] 發現取 50 份和取 20 份相比只多約 1%–1.5%；[06-edge2024-graphrag.pdf, App. C, p.19] 為一般 RAG 選 context 大小時，8k 在全面性上勝過更大的 context。
> 情境不同：01 是每份文件分別交給 generator 再加權合併 [01-lewis2020-rag.pdf, §2.1, p.3]，不是串成一個長 prompt。完整的六種說法與整合見 [Context window](../concepts/context-window.md)。
- **Null document 沒有幫助**：作者試過加入「空文件」選項，讓模型在找不到有用資料時可以不用文件，但沒有提升表現 [01-lewis2020-rag.pdf, App. F, p.18]。
- **安全疑慮**：RAG 也可能被用來產生假新聞、冒充他人、自動化產生垃圾或釣魚內容 [01-lewis2020-rag.pdf, Broader Impact, p.10]。

## 關鍵圖表說明

- **Fig.1**：整體架構圖。Query Encoder 把問題轉成向量，用 MIPS 從 Document Index 找出 top-K 文件，再交給 Generator 產生答案；整個流程可以端到端訓練 [01-lewis2020-rag.pdf, Fig.1, p.2]。**做簡報時最適合拿來畫流程圖。**
- **Fig.2**：RAG-Token 產生「The Sun Also Rises」「A Farewell to Arms」這兩個書名時，分別依賴不同的文件，顯示它可以組合多份文件的資訊 [01-lewis2020-rag.pdf, Fig.2, p.7]。
- **Fig.2 的延伸觀察**：書名的第一個字產生後，模型就不太依賴文件了，表示其餘部分來自 BART 自己記住的知識 [01-lewis2020-rag.pdf, §4.3, p.6]。
- **Table 1**：closed-book 與 open-book 方法在 open-domain QA 上的比較 [01-lewis2020-rag.pdf, Table 1, p.6]。
- **Table 3**：BART 與 RAG 的生成範例；BART 把中耳說成「位於中耳與鼻子之間」，是錯誤的答案 [01-lewis2020-rag.pdf, Table 3, p.7]。**很適合當作 hallucination 的實例。**
- **Table 4**：人工評估的事實性與具體性 [01-lewis2020-rag.pdf, Table 4, p.8]。
- **Fig.3**：取更多文件時，NQ 表現、檢索 recall 與 MS-MARCO 分數各怎麼變化 [01-lewis2020-rag.pdf, Fig.3, p.8]。

## 對初學者的重點

1. RAG 的核心就是「先查，再寫」：retriever 負責查，generator 負責寫 [01-lewis2020-rag.pdf, Fig.1, p.2]。
2. 論文本身就用 closed-book（只靠記憶）和 open-book（可以查資料）來形容兩類方法，這正是「閉書考 vs 開書考」的比喻 [01-lewis2020-rag.pdf, §4.1, p.5]。
3. 知識存在可以替換的 index 裡，所以換一份資料就能更新知識，不用重新訓練模型 [01-lewis2020-rag.pdf, §4.5, p.8]。
4. 在 open-domain QA（例如 NQ）上，小模型加上檢索，可以打贏大很多、只靠記憶的模型 [01-lewis2020-rag.pdf, App. G, p.19]。
5. RAG 的記憶是人類讀得懂、也改得動的原始文字，這讓模型更容易解釋，也更容易更新 [01-lewis2020-rag.pdf, §5, p.9]。

## 相關頁面

- [原始 RAG（方法）](../methods/original-rag.md)
- [Parametric 與 non-parametric memory](../concepts/parametric-vs-non-parametric-memory.md)
- [Retriever](../concepts/retriever.md)
- [Generator](../concepts/generator.md)
- [Embedding](../concepts/embedding.md)
- [Chunking](../concepts/chunking.md)
- [Hallucination](../concepts/hallucination.md)
- [Closed-book vs open-book](../comparisons/closed-book-vs-open-book.md)
- [Naive RAG（和原始 RAG 的對照）](../methods/naive-rag.md)
- [02 RAG 綜述](02-gao2023-survey.md)
- [術語表](../glossary.md)
