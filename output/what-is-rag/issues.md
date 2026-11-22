# Wiki 問題總表：RAG 是什麼？（workflow v2）

> **v2 基準**：本表從 `v1/issues.md` 複製而來（v1 的 ⓪ 三輪合併、去重，整批修正見 commit 5ba5505），編號、狀態不變。
> v2 的 ②b 新發現的問題接續在各類別後面編號（例如 Q09、W08），或放進新的「V2」類別；不要重新編號。
>
> **嚴重度（已登記，不得改變）**：E 類（E01–E03）＝嚴重；Q、W、C、T、S、N 類＝輕微。
> 這是依 v2 的嚴重度規則定的：E 類是「數字或結論和 raw 原文不符」；其餘是限定條件、⚠️ 同步、引用、術語、結構問題，目前都已修或已核對，沒有「待修」的條目。
>
> 欄位說明：新登記的問題要寫：編號、類別、問題、頁面、嚴重度、出現輪次（例如 v2-②b-1）、狀態。

- 來源：`lint-round1.md`（R1，17 項）、`lint-round2.md`（R2，20 項）、`lint.md`（R3，22 項），共 59 筆，去除重複後剩 40 條；另加 1 條修正時自己發現的格式問題（W07），共 41 條。
- 「出現輪次」用 `R輪-編號` 表示，例如 `R1-4` 是第 1 輪第 4 項。
- 狀態有三種：**已修**、**已核對（不需修改）**、**不修**（附理由）。
- 核對 raw 的方式：用 pypdf 4.3.1 把 `raw/*.pdf` 抽成純文字，放在 session 的 scratchpad 裡（`raw/text/` 不存在；`raw/` 唯讀，所以不在裡面新增檔案）。頁碼 `p.N` 指 PDF 的第 N 頁。

## E｜事實或數字錯誤（曾被判為「嚴重」）

| 編號 | 問題 | 頁面 | 出現輪次 | 狀態 |
|---|---|---|---|---|
| E01 | 67% 被說成「Hybrid retrieval + reranking」的結果，其實是 Contextual Embeddings + Contextual BM25 + reranking | comparisons/rag-techniques.md | R1-1 | 已修（第 1 輪後，commit 94202cb） |
| E02 | GPT Ranking 和人類判斷的一致度寫成「常常不到一半」，和同頁的 0.54／0.40／0.52 矛盾 | sources/07 | R2-1 | 已修（第 2 輪後，commit fba23ea） |
| E03 | 「Self-RAG 在六個任務上勝過參數更多的 LLM 和傳統 RAG」，和 Table 2 衝突（ChatGPT 在 TriviaQA、ARC-C 較高） | methods/self-rag.md | R1-2、R2-4、R3-1、R3-22 | 已修：核對 05 §6 p.10 原文，確實寫「significantly outperforms LLMs with more parameters or with conventional retrieval-augmented generation approaches」。依規則保留原句、加 ⚠️ 標成「原文結論與 Table 2 不一致」，並補上 §1 p.2 與 §5.1 p.8 的限定說法 |

## Q｜限定條件被拿掉

| 編號 | 問題 | 頁面 | 出現輪次 | 狀態 |
|---|---|---|---|---|
| Q01 | 「RAG 能有效減少錯誤內容」沒有 ⚠️ | concepts/hallucination.md、overview.md | R1-3 | 已修（第 1 輪後） |
| Q02 | 06 的 8k 只在「全面性」上勝出，被說成整體最好 | lost-in-the-middle、context-window、sources/04、sources/06 | R1-7、R2-2 | 已修（第 2 輪後） |
| Q03 | 「open-book 低於 closed-book」少了「20、30 份文件、最差位置」的限定 | comparisons/closed-book-vs-open-book.md | R1-6、R2-3 | 已修（第 2 輪後） |
| Q04 | 「小模型勝過大模型」少了「open-domain QA（NQ）」的限定 | overview.md、sources/01 | R2-7 | 已修（第 2 輪後） |
| Q05 | 原始 RAG「直接串接」容易被讀成把所有文件串成一個長 prompt | generator.md、sources/01（第 2 輪後已修）；**naive-rag.md 第 65 行** | R2-5、R3-4 | 已修：naive-rag 比較表改成「問題和每份文件分別串接，再 marginalize」 |
| Q06 | GraphRAG 的 72%–83%／62%–82%，原文是「global approaches」（含直接摘要原文的 TS），而且分資料集 | overview.md、methods/graphrag.md、comparisons/rag-techniques.md | R3-3 | 已修：核對 06 §5.1 p.9，三頁都改成「GraphRAG 等全局方法」，並分開寫 Podcast 和新聞的範圍 |
| Q07 | 比喻「20 本比 50 本有用」說得太滿（50 份其實仍略好 1%–1.5%） | analogies.md | R3-12 | 已修：在「比喻的極限」補上這一點 |
| Q08 | 用 06 的 8k 實驗當成減輕 lost in the middle 的方法，因果被放大 | concepts/lost-in-the-middle.md | R1-7 | 已修（第 2 輪後）：補上「06 沒有直接測位置效應」 |

## W｜⚠️ 不同步或格式不一致

| 編號 | 問題 | 頁面 | 出現輪次 | 狀態 |
|---|---|---|---|---|
| W01 | Reranking 的 ⚠️ 停在舊版（只寫到 01 vs 02 或 02＋03，沒有 04，也沒有「情境不同」） | retriever.md、advanced-rag.md、sources/01、sources/02、sources/03 | R1-4、R2-9、R3-8 | 已修：以 concepts/reranking.md 為準，5 頁換成同一版本（01 vs 02＋03＋04＋情境不同），各頁的 frontmatter `sources` 也補齊 |
| W02 | 「文件數量」的 ⚠️ 只對照 02 或 02＋04 | retriever.md、sources/01、sources/02 | R1-5、R2-9、R3-8 | 已修：以 concepts/context-window.md 為準，3 頁換成同一份摘要（01／02／03／04／06＋01 情境不同），完整的六種說法連到 context-window |
| W03 | 06 把 04 說成「前段容易被漏掉」：lost-in-the-middle、sources/06 有 ⚠️，sources/04 只用一般內文 | sources/04 | R3-9 | 已修：改成標準的 ⚠️ 區塊 |
| W04 | 「以摘要為基礎的 indexing 表現很差」：chunking 有 ⚠️，方法頁沒有 | methods/contextual-retrieval.md | R3-10 | 已修：加 ⚠️，連到 chunking |
| W05 | Naive RAG 是不是「最早」的 ⚠️ 沒有出現在比較頁 | comparisons/rag-paradigms.md | R3-13 | 已修：加 ⚠️，連到 naive-rag |
| W06 | 「小型知識庫不需要 RAG」用一般文字寫「有 ⚠️ 爭議」，沒有用標準的 ⚠️ 區塊 | overview.md | R2-8 | 已修 |
| W07 | ⚠️ 區塊後面直接接列表、沒有空行，格式不統一（修正時自己發現，不在 reviewer 清單中） | methods/self-rag.md、sources/01 | — | 已修：補上空行 |

## C｜引用與頁碼（raw 核對結果）

| 編號 | 問題 | 頁面 | 出現輪次 | 核對結果 | 狀態 |
|---|---|---|---|---|---|
| C01 | 「拆成小步驟」只引用 06，應該補 07 | overview.md | R1-9、R2-6 | 07 §5 p.5：RAGAS 的指標比兩個直接打分或挑選的基準更接近人類判斷 | 已修：三個原則分別附上出處 |
| C02 | Self-RAG「生成時自己評估」只引用 07 | concepts/ragas.md | R1-13、R3-5 | rag-evaluation 引用的 05 §3.1 p.4 才是出處 | 已修 |
| C03 | 「chunk 通常不超過幾百 tokens」在三頁分別引用 03 p.2、p.3、p.2–3 | chunking、retriever、naive-rag | R1-17b、R2-16、R3-18 | 03 p.2（embedding 流程）和 p.3（加上 BM25 的流程）都有這句話 | 已核對（不需修改） |
| C04 | 49%／67% 引用 03 p.2, p.4–5 或 p.2, p.5–6，和表格的 p.7、p.10 不同 | overview.md、sources/03 | R2-15、R3-19 | p.2 就有 49% 和 67%；p.4–5 是「chunk 失去上下文、補上說明」，p.6 是「50–100 tokens」 | 已核對（不需修改） |
| C05 | 49% 的長條圖寫 p.8，表格寫 p.7 | sources/03 | R1-17e | 數字在 p.7 的內文，長條圖的說明在 p.8，兩處都對 | 已核對（不需修改） |
| C06 | 02 §II-B 有時標 p.3，有時標 p.4 | methods/advanced-rag.md | R2-17 | §II-B 從 p.3 開始，pre-／post-retrieval 的細節在 p.4；每一處都對得上原文 | 已核對（不需修改） |
| C07 | Llama2-7B 加上檢索（38.2、30.0）、Llama2-13B 不檢索的 ARC 29.4，在 sources/05 的摘錄中沒有 | rag-techniques、closed-book-vs-open-book | R1-17c、R2-18、R3-20 | 05 Table 2 p.8：Llama2 7B（檢索）PopQA 38.2、PubHealth 30.0；Llama2 13B（不檢索）ARC 29.4，都正確 | 已核對：在 sources/05 的 Table 2 摘錄補上這兩列，讓 wiki 內部可以互相核對 |
| C08 | 04 §5 標 p.9，其他頁標 p.10 | concepts/reranking.md | R2-19 | §5 從 p.9 開始；「we simply include them in the prompt」在 p.9 | 已核對（不需修改） |
| C09 | 用 05 §3.3 證明「05 沒有討論位置效應」 | concepts/lost-in-the-middle.md | R2-19 | 「沒有提到」無法用單一章節證明 | 已修：改成「05 的 raw 檔中沒有找到討論位置效應的段落」，拿掉這個引用 |
| C10 | 06 用的是 GPT-4 還是 gpt-4-turbo | rag-evaluation、sources/06、sources/07 | R3-21 | 06 §1 p.2 寫 GPT-4；§4.1.3 p.9 寫實驗使用 gpt-4-turbo 的 endpoint | 已修：三頁都補上「實驗用 gpt-4-turbo」 |
| C11 | 「年份不對應只剩 4%」沒有說是哪一種組合 | analogies.md、parametric-vs-non-parametric-memory.md | R1-17a | 01 §4.5 p.8：2018 年的 index 問 2016 年的領袖是 12%，2016 年的 index 問 2018 年的領袖是 4% | 已修：兩頁都寫明組合 |
| C12 | 「150k 筆訓練資料」和附錄的 145,619 筆不同 | methods/self-rag.md | R3-2 | sources/05 已經說明這是四捨五入的差異 | 已修：改成「約 150k 筆（附錄是 145,619 筆）」 |

## T｜術語

| 編號 | 問題 | 頁面 | 出現輪次 | 狀態 |
|---|---|---|---|---|
| T01 | overview 的 LLM、hallucination、context window 第一次出現時沒有連結 | overview.md | R1-10 | 已修（第 1 輪後） |
| T02 | 術語表缺詞條：BLEU、Cross-encoder、F1、FEVER、Forward pass、Hit Rate、HNSW、Leiden、Marginalize、MAUVE、MRR、MS-MARCO、NDCG、Natural Questions（NQ）、PPO、Reinforcement learning、RLHF、ROUGE、Self-attention、Thorough／Fast Decoding、Transformer、TriviaQA、Unsupervised fine-tuning | glossary.md | R1-11、R2-14、R3-17 | 已修：新增 23 條，每條都引用 raw 中實際出現的位置。raw 只「提到」、沒有定義的指標（例如 BLEU、MRR），解釋只寫 raw 說了什麼（用途、分類），不用背景知識補定義 |
| T03 | 術語表有詞條，但頁面第一次出現時沒有連結 | hallucination、context-window、lost-in-the-middle、ragas、graphrag、self-rag、retriever、overview（vector database、top-k、prompt、BM25、knowledge graph、Exact Match、token） | R1-12、R2-13、R3-16 | 已修：在這些位置加上連到 glossary.md 或概念頁的連結 |

## S｜結構與可讀性

| 編號 | 問題 | 頁面 | 出現輪次 | 狀態 |
|---|---|---|---|---|
| S01 | GenRead 放在「只找得到局部」小節，內容其實屬於「從哪裡檢索？」 | concepts/retriever.md | R1-14、R2-10、R3-7 | 已修：移到「從哪裡檢索？」 |
| S02 | 「所以不受位置影響的方式也不同」句意不清 | concepts/context-window.md | R2-12、R3-11 | 已修 |
| S03 | 時間軸上 GraphRAG（2024–2025）排在 Contextual Retrieval（2024-09-19）前面 | comparisons/rag-timeline.md | R2-11、R3-14 | 已修：核對 06 p.1，raw 是 arXiv:2404.16130 的 v2（2025-02-19）。時間欄改寫成「arXiv 2404.16130；raw 為 v2，2025-02-19」，並把這一列移到 Contextual Retrieval 後面，依 raw 版本的日期排序 |
| S04 | 方法頁的「## 出處」只列主要來源，和 frontmatter 的 `sources` 不一致 | advanced-rag、contextual-retrieval、self-rag、graphrag、modular-rag | R3-15 | 已修：「出處」補上內文引用到的其他 raw |

## N｜不修（附理由）

| 編號 | 問題 | 出現輪次 | 不修的理由 |
|---|---|---|---|
| N01 | 建議新增 BM25／hybrid retrieval、LLM-as-a-judge、Robustness 的獨立頁面 | R1-15、R3（統計） | log.md 之前的 lint 已經決定暫不拆頁：BM25／hybrid 在 retriever.md、LLM-as-a-judge 在 rag-evaluation.md 都是獨立小節，也都有術語表詞條連過去。Robustness 維持在 index 的「待建頁面」。拆頁屬於結構調整，不是錯誤，等使用者決定 |
| N02 | context-window.md 和 lost-in-the-middle.md 有部分內容重疊 | R1-16 | log.md 之前已經決定不合併（前者講數量、後者講位置，兩頁互相連結）。這次修 Q02、S02 時，已經讓兩頁和 06 8k 有關的說法一致 |
| N03 | ragas.md 和 rag-evaluation.md 的 RAGAS 段落重複 | R3-6 | rag-evaluation 是「評估方法總覽」，需要一段能獨立閱讀的 RAGAS 摘要；ragas.md 是細節頁。兩邊的數字已經核對一致（0.95／0.78／0.70），也互相連結。在 log 記錄為刻意保留 |
| N04 | reviewer 無法讀取 output/what-is-rag/lint.md，無法比對前幾輪的清單 | R2-20 | 這是 workflow 的設計：⓪ 的 reviewer 只能讀 wiki/。本表就是為了這個問題建立的 |

## V2｜v2 ②b 第 1 輪新發現（全部輕微，不阻擋）

| 編號 | 類別 | 問題 | 頁面 | 嚴重度 | 出現輪次 | 狀態 |
|---|---|---|---|---|---|---|
| V2-01 | 限定條件 | RAGAS 0.95、GPT Ranking 0.40–0.54 沒有寫「在 WikiEval 資料集上」 | overview.md 第 67–68 行 | 輕微 | v2-②b-1 | 待修（簡報使用時改用 hallucination.md 或 ragas.md 中帶限定的句子） |
| V2-02 | ⚠️ 同步 | 三個品質分數沒有提醒「06 認為只適用於 vector RAG」 | overview.md 第 63 行 | 輕微 | v2-②b-1 | 待修 |
| V2-03 | ⚠️ 同步 | 「RAG 減少錯誤內容」的 ⚠️，三頁列的反證不同（05 App. C.1 vs 05 Table 2） | hallucination.md 第 21 行、overview.md 第 24 行、naive-rag.md 第 36–38 行 | 輕微 | v2-②b-1 | 待修 |
| V2-04 | 可讀性 | BART、ISSUP token、instruction-tuned 第一次出現時沒有連結 | hallucination.md | 輕微 | v2-②b-1 | 待修 |
| V2-05 | 限定條件 | PopQA 45.5 → 24.7 是「7B、50k 訓練資料的消融實驗」，沒有寫明 | parametric-vs-non-parametric-memory.md 第 65 行 | 輕微 | v2-②b-1 | 待修（簡報不使用這組數字） |
| V2-06 | 引用 | 「加上檢索後部分任務下降」引 05 §5.1，但 §5.1 寫的是「沒有明顯進步」，下降要看 Table 2 | closed-book-vs-open-book.md 第 56 行 | 輕微 | v2-②b-1 | 待修 |
| V2-07 | 限定條件 | 04 的實驗有 10／20／30 份文件，頁面只寫 20 份 | closed-book-vs-open-book.md 第 42 行 | 輕微 | v2-②b-1 | 待修 |
| V2-08 | 可讀性 | NQ、Exact Match、T5、REALM、DPR、oracle 沒有連結 | closed-book-vs-open-book.md | 輕微 | v2-②b-1 | 待修 |
| V2-09 | 限定條件 | 「35%–49%」把兩種設定合併，49% 需要再加 Contextual BM25 | analogies.md 第 68 行 | 輕微 | v2-②b-1 | 待修（簡報不使用這個範圍） |
| V2-10 | 可讀性 | LLM、top-k、embedding model、vector database 沒有連結 | naive-rag.md | 輕微 | v2-②b-1 | 待修 |
| V2-11 | 可讀性 | token 沒有連結 | chunking.md | 輕微 | v2-②b-1 | 待修 |
| V2-12 | 可讀性 | vector database、cosine similarity、FAISS、MIPS、HNSW 沒有連結 | embedding.md | 輕微 | v2-②b-1 | 待修 |
| V2-13 | 措辭 | 「大約 20 份時就停止進步」比原文說得滿，原文是「只多約 1%–1.5%」 | retriever.md 第 39 行 | 輕微 | v2-②b-1 | 待修（簡報使用時改用 overview 的「只多進步約 1%–1.5%」） |
| V2-14 | 可讀性 | DPR、bi-encoder、FEVER、NQ、EM 沒有連結 | retriever.md | 輕微 | v2-②b-1 | 待修 |
| V2-15 | 引用 | 「Self-RAG 屬於 Modular RAG 的 adaptive retrieval」只引 02 §V-C，應補 §II-C p.5 | self-rag.md 第 24 行 | 輕微 | v2-②b-1 | 待修 |
| V2-16 | 可讀性 | LLM、reflection tokens 沒有連結 | self-rag.md | 輕微 | v2-②b-1 | 待修 |
| V2-17 | 可讀性 | EM、F1、BLEU、ROUGE、Hit Rate、MRR、NDCG 沒有連結 | rag-evaluation.md | 輕微 | v2-②b-1 | 待修 |

> 這 17 條都是輕微問題，依 workflow v2 不阻擋 ②b。之後依 AGENTS.md §9.3 的 Wiki 維護流程整批處理。製作這份簡報時，不使用 V2-05、V2-09 的數字；V2-01、V2-13 涉及的數字，只引用帶有限定條件的句子。
| V2-18 | 引用 | Fig.1 例子的步驟 3、4：「Wikipedia」「加權」只引 Fig.1, p.2，應補 §1, p.2 與 §2.1, p.3 | sources/01-lewis2020-rag.md | 輕微 | wiki 維護（⑤ 退回後） | 已修 |
| V2-19 | 限定條件 | Fig.1 例子的步驟 6：Table 3 的 middle ear 屬於 MS-MARCO 任務，沒有註明 | sources/01-lewis2020-rag.md | 輕微 | wiki 維護（⑤ 退回後） | 已修 |
| V2-20 | 簡化 | Fig.1 例子：「先判斷這個問題需要檢索」，實際上每一段之前都會判斷 | sources/05-asai2023-self-rag.md | 輕微 | wiki 維護（⑤ 退回後） | 已修（引 §3.1, p.4） |
| V2-21 | 需要更多資料 | Fig.1 左邊另有「Contradictory」「No information in passages」標籤，文字抽取看不出標在哪一句 | sources/05-asai2023-self-rag.md | 輕微 | wiki 維護（⑤ 退回後） | 不修：要看原圖才能確認標籤位置；目前寫的「和取回的文件不一致」已可由圖中兩段文字直接對照，沒有講錯 |
| V2-22 | 可讀性 | Relevant／Supported 等標籤沒有對應到 ISREL／ISSUP，也沒說最後選中哪一段 | sources/05-asai2023-self-rag.md | 輕微 | wiki 維護（⑤ 退回後） | 已修（引 §3.1, p.4） |
| V2-23 | 限定條件 | 42.7% 的人工評估比的是 BART vs RAG-Token，頁面只寫 RAG | sources/01-lewis2020-rag.md 第 69–70 行 | 輕微 | v2-②b-2 | 待修 |
| V2-24 | 可讀性 | 多個術語沒有連結；Fig.1 例子第 3 步的 MIPS、top-K 沒有白話說明 | sources/01-lewis2020-rag.md | 輕微 | v2-②b-2 | 待修（簡報的「走一遍」頁不使用 MIPS 這個詞，改用「找出意思最接近的幾份文件」——該說法出自 overview／embedding 的卡片） |
| V2-25 | 引用 | 「只檢索一次」應引 §2, p.3 | sources/05-asai2023-self-rag.md 第 25 行 | 輕微 | v2-②b-2 | 待修 |
| V2-26 | 限定條件 | 2% 是 Self-RAG 7B、TriviaQA 和 PopQA 上的結果 | sources/05-asai2023-self-rag.md 第 103 行 | 輕微 | v2-②b-2 | 待修（簡報不使用 2%） |
| V2-27 | 限定條件 | 「04 發現比不給還差」缺 GPT-3.5-Turbo、20／30 份文件、最差位置的限定 | sources/05-asai2023-self-rag.md 第 128 行 | 輕微 | v2-②b-2 | 待修（簡報的這個數字只引用 closed-book-vs-open-book.md 帶限定的句子） |
| V2-28 | 原文不一致 | 「每類 4k–20k 筆」與附錄 utility 3,831 筆不一致，未註明 | sources/05-asai2023-self-rag.md 第 50 行 | 輕微 | v2-②b-2 | 待修 |
| V2-29 | 需要更多資料 | 「PopQA 和傳記各只抽 50 筆」可能是合計 50 筆 | sources/05-asai2023-self-rag.md 第 113 行 | 輕微 | v2-②b-2 | 待修 |
| V2-30 | ⚠️ 格式 | 「注意：結論 §6…」沒有用標準 ⚠️ 區塊 | sources/05-asai2023-self-rag.md 第 77 行 | 輕微 | v2-②b-2 | 待修 |
| V2-31 | 可讀性 | LLM、reflection tokens、critic、RLHF／PPO、beam search、MAUVE、引用 precision 沒有連結 | sources/05-asai2023-self-rag.md | 輕微 | v2-②b-2 | 待修 |
| V2-32 | 限定條件 | 「測試過的模型都有這個現象」和同頁的兩個例外對不上 | concepts/lost-in-the-middle.md 第 42 行 | 輕微 | v2-②b-2 | 待修（簡報不使用這句） |
| V2-33 | 引用 | 「正確的文件很可能剛好落在中間」是推論，原文沒這樣說 | concepts/lost-in-the-middle.md 第 17 行 | 輕微 | v2-②b-2 | 待修（簡報不使用這句） |
| V2-34 | 可讀性 | primacy／recency bias 等術語沒有連結或白話說明 | concepts/lost-in-the-middle.md | 輕微 | v2-②b-2 | 待修 |
| V2-35 | ⚠️ 同步 | 「放得進去，不代表用得好……取 50 份和取 20 份相比，只多進步約 1%–1.5%」沒有附「要放多少份文件」的 ⚠️（retriever.md、sources/01、context-window.md 都有），讀起來像定論 | overview.md 第 81 行 | 輕微 | v2-⑦-1（⑦ 第 1 輪 reviewer 在 13 的問題 2 中指出） | 待修（簡報第 13 頁已改為引用 retriever.md 的 ⚠️，不受影響） |
