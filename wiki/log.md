# 工作紀錄

> 只能往後追加，最新的放最下面。查最近 5 筆：`grep "^## \[" wiki/log.md | tail -5`

## [2026-11-22] setup | 建立 AGENTS.md 與資料夾結構
- 新增：AGENTS.md、CLAUDE.md、wiki/（index、log、overview、glossary、analogies 與 5 個子目錄）、slides/、tools/lint.py
- 需求：讀者是不熟 AI 的大學生；繁體中文、專有名詞保留英文；嚴格只用 raw/；每個主張都標 [raw 檔名, 位置]
- raw/ 共 7 篇，尚未 ingest

## [2026-11-22] ingest | 01-lewis2020-rag.pdf
- 新增：sources/01-lewis2020-rag.md、concepts/（parametric-vs-non-parametric-memory、retriever、generator、embedding、chunking、hallucination）、methods/original-rag.md、comparisons/closed-book-vs-open-book.md
- 修改：overview.md（填入 1–3、5、6 節）、glossary.md（新增 28 個詞條）、analogies.md（新增 3 個比喻）、index.md
- ⚠️ 新標註：原文內部不一致，§4.3 p.6 寫「both factual 17%」，但 Table 4 p.8 為「Both good 11.7%／Both poor 17.7%」（標在 sources/01-lewis2020-rag.md）
- 與既有頁面衝突：無（第一篇來源）
- 待補來源：embedding 直覺、chunk 切法的影響、naive RAG 定義、LLM／Token 白話定義、EM 正式定義
- 備註：App. G 記載 index 向量為「728 dimensional」，照原文記錄、未更正
- tools：lint.py 修正兩處誤判（連結文字被當成缺頁碼的引用、被當成主張）
- lint：0 error, 0 warning；語意檢查抽查 17 處引用，全部吻合

## [2026-11-22] ingest | 02-gao2023-survey.pdf
- 新增（11）：sources/02-gao2023-survey.md；methods/（naive-rag、advanced-rag、modular-rag）；concepts/（reranking、query-optimization、context-window、rag-evaluation）；comparisons/（rag-paradigms、rag-vs-fine-tuning、rag-timeline）
- 修改（12）：concepts/（chunking、embedding、retriever、generator、hallucination、parametric-vs-non-parametric-memory）、methods/original-rag.md、sources/01-lewis2020-rag.md、glossary.md（28 → 59 條）、analogies.md（+2）、overview.md（第 1–6 節都已有內容）、index.md
- ⚠️ 新標註（3 組，與 01 對照）：
  1. Reranking：01 §4.1 認為不需要 re-ranker；02 §II-B 把它列為 Advanced RAG 的關鍵策略（標在 reranking、retriever、advanced-rag、01、02 頁）
  2. 文件數量：01 §4.5 發現 RAG-Seq 取越多份文件越好；02 §IV-A 說這是常見誤解；02 §VII-B 又引用「加入不相關文件可提升 30% 以上」（標在 context-window、retriever、01、02 頁）
  3. Naive RAG 的定位：02 §II-A 稱它是「最早的方法」卻放在 ChatGPT 之後，但 RAG 一詞在 2020 年由 01 提出（標在 naive-rag、original-rag、rag-timeline、02 頁）
- 已補上的待補來源：chunk 切法的影響（02 §III-B）、naive RAG 的定義（02 §II-A）
- 新增的待補來源：context window 的正式定義、Prompt／In-context learning 的白話定義
- 備註：02 原文有重複的句子（§III-A p.7）和錯字（bge-raranker-large），wiki 採用正確拼法 bge-reranker-large
- lint：0 error, 0 warning；語意檢查抽查 19 處引用，全部吻合

## [2026-11-22] ingest | 03-anthropic-contextual-retrieval.pdf
- 新增（3）：sources/03-anthropic-contextual-retrieval.md、methods/contextual-retrieval.md、comparisons/rag-techniques.md
- 修改（17）：concepts/（retriever、reranking、context-window、chunking、embedding、rag-evaluation、query-optimization）、methods/（advanced-rag、naive-rag）、sources/02-gao2023-survey.md、comparisons/rag-timeline.md、glossary.md（59 → 67 條）、analogies.md（+2，共 7 個）、overview.md、index.md、log.md
- ⚠️ 新標註：
  1. 小型知識庫需要 RAG 嗎：03 p.2 說小於 200k tokens 可以直接全放進 prompt；02 §VII-A 說 RAG 仍無可取代（標在 context-window、02、03 頁）
  2. 摘要類方法：02 §III-B 把段落摘要、階層式摘要 index 列為優化方法；03 p.5 實測通用文件摘要提升非常有限、以摘要為基礎的 indexing 表現很差（標在 chunking、02 頁）
- ⚠️ 既有標註的更新：
  - Reranking：03 p.10–11 支持 02，變成「01 vs 02＋03」；補註 03 衡量的是檢索失敗率，不是答案的 EM
  - 文件數量：03 p.8 加入第四種說法（越多越有機會，但會分心；實測 5／10／20 中 20 最好）
- 和既有內容一致之處：03 p.3 說 BM25 適合含有代碼或術語的查詢，和 01 §4.5（FEVER 以實體為中心，BM25 最佳）一致，已寫進 retriever 頁
- 已補上的待補來源：embedding 的直覺說明（03 p.2「vector embeddings that encode meaning」）
- 來源限制：03 是網頁列印的 PDF，沒有章節編號，只能用 p.N 引用；附錄 I、II 的分資料集結果是圖片，抽不到文字，無法引用
- 自我修正：刪掉「prompt caching 是 Claude 才有的功能」（原文只說 Claude 的 prompt caching 讓它能低成本實現）；「推廣自家產品」改成客觀描述
- lint：0 error, 0 warning；語意檢查抽查 26 處引用，全部吻合（其中 2 處是 PDF 換行造成的比對誤差，已人工確認）

## [2026-11-22] ingest | 04-liu2023-lost-in-middle.pdf
- 新增（2）：sources/04-liu2023-lost-in-middle.md、concepts/lost-in-the-middle.md
- 修改（14）：concepts/（context-window 整頁改寫、reranking、retriever、rag-evaluation）、comparisons/（closed-book-vs-open-book、rag-techniques、rag-timeline）、sources/（02、03）、glossary.md（67 → 76 條，並重新依字母排序）、analogies.md（改寫「讀長文只記頭尾」的依據，新增「書包塞太滿」，共 8 個）、overview.md、index.md、log.md
- ⚠️ 既有標註的更新：
  1. 文件數量：加入第五種說法（04 §5：20 份以上幾乎不再進步），並在 context-window 頁新增「目前最合理的整合」五點
  2. Reranking：04 §5 也建議 reranking，變成「01 vs 02＋03＋04」；補註 01 是每份文件分別交給 generator，沒有位置問題
  3. 小型知識庫需要 RAG 嗎：04 §2.3 發現支援長 context 的模型不一定比較會用 context，挑戰 03 p.2；補註兩者的模型世代不同
- 新增的 ⚠️：無（04 沒有和既有內容正面衝突，主要是補證據）
- 和既有內容一致之處：02 §IV-A 對 lost in the middle 的描述，引用的正是 04（02 Ref.[98], p.19）；04 App. B（隨機干擾文件的準確率較高）和 02 §VII-B 引用的 Cuconasu et al. 方向一致，但實驗設計不同
- 新發現（適合放進簡報）：答案在中間時，GPT-3.5-Turbo 給 20 份文件的準確率（53.8%）低於完全不給文件（56.1%），已寫進 closed-book-vs-open-book 頁
- 已補上的待補來源：context window 的定義（04 §2.2）、Prompt 的白話定義（04 §1）
- lint：0 error, 0 warning；語意檢查抽查 24 處引用，修正 1 處頁碼（App. C 應為 p.14–15）

## [2026-11-22] ingest | 05-asai2023-self-rag.pdf
- 新增（2）：sources/05-asai2023-self-rag.md、methods/self-rag.md
- 修改（17）：concepts/（parametric-vs-non-parametric-memory、hallucination、rag-evaluation、reranking、generator、lost-in-the-middle）、methods/modular-rag.md、comparisons/（closed-book-vs-open-book、rag-vs-fine-tuning、rag-techniques、rag-timeline）、sources/（01、02）、glossary.md（76 → 84 條）、analogies.md（+1，共 9 個）、overview.md、index.md
- ⚠️ 新標註：
  1. 該不該用模型自己的知識：01 §4.1 把「文件沒答案也答對 11.8%」視為優點；05 App. C.1 把「只有 2% 答案不在文件中」視為優點（標在 parametric-vs-non-parametric-memory、01、05 頁）
  2. 原文內部不一致：§3.2.1 說 critic 和 GPT-4 的一致度「在大多數類別上超過 90%」，但 App. A.2 的表只有 4 類中的 2 類超過 90%（標在 05 頁）
  3. 原文內部不一致：App. C.1 出現「Alpaca 30B」，但只評估了 7B 和 13B（標在 05 頁）
- 和既有內容一致之處：02 §V-C 對 Self-RAG 的描述和原始論文相符；05 Table 2「加上檢索反而退步」（ChatGPT 的 PubHealth 70.1 → 54.7）和 04 的「放錯位置時比 closed-book 差」，是 open-book 不一定比較好的兩份證據（已寫進 closed-book-vs-open-book 頁）
- 其他小瑕疵（已註明，不加 ⚠️）：訓練資料總數 150k vs 145,619；「1,2594」數字格式有誤
- 自我修正：closed-book 頁原本寫「需要推理的任務檢索幫助有限」，改回作者原話「不能直接從文件複製或擷取片段的任務」，並註明 TriviaQA 的退步作者沒有解釋
- lint：0 error, 0 warning；語意檢查抽查 33 處引用，全部吻合

## [2026-11-22] ingest | 06-edge2024-graphrag.pdf
- 新增（2）：sources/06-edge2024-graphrag.md、methods/graphrag.md
- 修改（18）：concepts/（rag-evaluation、context-window、chunking、lost-in-the-middle、reranking、retriever）、methods/（naive-rag、self-rag）、comparisons/（rag-techniques、rag-timeline）、sources/（02、03、04）、glossary.md（84 → 94 條）、analogies.md（+1，共 10 個）、overview.md、index.md、log.md
- ⚠️ 新標註：
  1. 06 對 04 的引用有誤：06 §3.1.1 引用 04（已在 References p.14 確認是 Lost in the Middle），說 chunk「前段」的資訊容易被漏掉；但 04 的發現是開頭最好、中間最差（標在 lost-in-the-middle、04、06 頁）
  2. 品質分數適用範圍：06 §2.4 認為 RAGAS 的 context relevance、faithfulness、answer relevance 和全局理解無關；02 §VI-C 把它們列為主要品質分數（標在 rag-evaluation、02、06 頁）
  3. 摘要類 index：06 用社群摘要當 index 並勝過一般 RAG，和 03 p.5「以摘要為基礎的 indexing 表現很差」對照；在 chunking 頁整合成「摘要類 index 對找特定事實幫助有限，對理解整批資料有幫助」（標在 chunking、03、06 頁）
- ⚠️ 既有標註的更新：文件數量加入第六種說法（06 App. C：一般 RAG 的 context 用 8k 勝過 16k–64k）
- 已補上的待補來源：Token 的定義（06 §1「tokens (units of text)」）
- 自我修正：App. C 的 context 大小實驗是在一般 RAG（SS）上做的，不是在 GraphRAG 上；已在 context-window、06 頁補上這個前提
- 釐清容易混淆的名詞：GraphRAG 的「self-reflection」是 prompt 技巧，Self-RAG 的 reflection tokens 需要訓練（寫在 self-rag 頁）
- lint：0 error, 0 warning；語意檢查抽查 36 處引用，全部吻合

## [2026-11-22] ingest | 07-es2023-ragas.pdf
- 新增（2）：sources/07-es2023-ragas.md、concepts/ragas.md
- 修改（14）：concepts/（rag-evaluation：新增「評估方式總覽」表和「LLM 當評審，可靠嗎？」一節；hallucination、parametric-vs-non-parametric-memory、lost-in-the-middle）、comparisons/rag-timeline.md、sources/（02、04、06）、glossary.md（94 → 98 條）、analogies.md（+1，共 11 個）、overview.md、index.md、log.md
- ⚠️ 新標註：
  1. LLM 評審的可靠度：07 Table 1 的 GPT Ranking（ChatGPT 直接挑選）和人類一致度只有 0.40–0.54，§2 也提醒答案順序會影響判斷；06 的主要結果靠 LLM 兩兩比較得出，raw 檔中沒有找到處理順序的說明。補註 06 用 GPT-4，並用 claim 指標交叉驗證（69%–78%）（標在 rag-evaluation、06、07 頁）
- ⚠️ 既有標註的更新：品質分數適用範圍（02 vs 06）補上 07 的原始設定是「標準 RAG」，支持 06 的範圍界定
- 和既有內容一致之處：02 對 RAGAS 的描述（§VI-D、Table IV）和原始論文相符；07 §3 引用 04 時描述正確（中間的資訊最難利用），和 06 的誤引形成對照
- 已補上的待補來源（共 3 項，至此全部清空）：LLM 的白話定義（04 §1＋07 §1）、In-context learning（06 §3.1.2）、Exact Match（05 §4.1 的反面說明）
- 自我修正：rag-evaluation 的表格導言原本寫「每一格都附上出處」，改成「每一列」（「評估什麼」欄有些格子沒有單獨附出處）；index 原本寫「13 處待補來源」，核對 log 後改成正確的 9 項
- lint：0 error, 0 warning；語意檢查抽查 27 處引用，全部吻合

## [2026-11-22] lint | 全部 ingest 完成後的總檢查
- 機械性檢查：36 頁，0 error，0 warning，[待補來源] 0 處
- ⚠️ 標註共 37 個，分布在 19 頁
- 語意檢查清單：
  - [x] 沒有殘留「預計 ingest」「之後補充」等過時說明（grep 確認）
  - [x] 矛盾都已加 ⚠️；跨頁的同一組爭議已互相連結
  - [x] 待補來源清單已清空，index 已同步
  - [ ] 待建頁面「Robustness」：相關內容分散在 context-window（04 App. B、02 §VII-B）和 rag-evaluation（四種能力），目前決定不獨立成頁，產生簡報時再評估

## [2026-11-22] lint | 全 wiki 檢查（AGENTS.md §9.3）
### 機械性檢查
- 修改前 tools/lint.py：0 error, 0 warning；但另寫結構檢查腳本，找到 lint 沒涵蓋的 7 個問題，並發現 lint.py 本身的漏洞
- **lint.py 漏洞**：一個括號放多份來源（`[A, x; B, y]`）時，第二份檔案不會被驗證，頁碼也會被算到第一份檔案上；這也不符合 §7 的格式（一個括號一份來源）
  - 修正：把 16 處合併引用拆成多個括號（glossary 10、rag-evaluation 2、reranking 2、overview 1、context-window 1），之後又多找到 1 處（rag-timeline，原本被 `Ref.[164]` 的方括號擋住）
  - 未修改 AGENTS.md（修改規則需要使用者同意），改為讓內容符合既有規則
- **lint.py 新增 3 項檢查**：一個括號放多份來源（error）、frontmatter sources 和內文實際引用不一致（error）、index 的 sources 計數和 frontmatter 不符（warning）；開發時 regex 誤判了一次（檔名比對太寬），已修正並用測試頁驗證
- **frontmatter 不一致**：04 頁列了 01 但內文沒引用（已移除）；naive-rag 新增 ⚠️ 後缺 04、05（已補上）
- **index 計數過時**：01（2→3）、02（4→7）、03（4→5）、04（4→5）、naive-rag（4→6）
- **引用格式**：`Ref.[n]` 內含方括號會讓引用被提早截斷，4 處改為 `Ref. n`
### 引用正確性（全面檢查，不只抽查）
- 寫了腳本，逐行核對「說法中的數字」是否出現在所引用頁面上：標出 30 行，人工判讀後 17 行是真問題或格式問題，13 行是誤判（100 萬 vs 1 million、12 月 vs December、列表編號、第 15 份 vs Index 14）
- **年份的出處錯誤**：「RAG 在 2020 年提出」有 6 行只引用 01，但 01 的 raw 檔沒有這個年份（PDF 上只有 2021 年的 v4 日期）；補上 [02, Ref. 4, p.17]（rag-timeline、naive-rag、original-rag、02、overview ×2）
- **時間軸的 02 年份「2023」沒有出處**：補上 [06, References, p.13]
- **推論當成事實**：「04 測的是 2023 年的模型」原文沒有這樣寫，4 處改成「04 發表於 2023 年 [04, p.1]，測的是當時的模型」（04 ×2、03、context-window）
- **缺出處**：01 頁 ⚠️ 中的 11.8% 只引用 05，補上 [01, §4.1, p.6]；「約 100 萬 tokens 花了 281 分鐘」3 處只引用 p.9，補上 [06, §4.1.1, p.8]（analogies、graphrag、06）
- 另抽查 6 處不含數字的引用，全部吻合
### 語意檢查清單
- [x] 未標註的矛盾：找到 1 處。naive-rag「表現勝過沒有 RAG 的 LLM」（02 §II）和 04 Table 6、05 Table 2 的反例衝突，已加 ⚠️（⚠️ 共 38 個）
- [x] 被取代的舊說法：無新發現（既有的 ⚠️ 都已涵蓋）
- [x] 多次被提到卻沒有頁面的概念：BM25／hybrid retrieval、knowledge graph、LLM-as-a-judge 都已是既有頁面中的獨立小節，暫不拆頁；Robustness 維持「待建」
- [x] 應合併的頁面：context-window 和 lost-in-the-middle 有部分重疊，但前者談數量、後者談位置，已互相連結，不合併
- [x] 引用位置是否正確：見上方全面檢查
- [x] 初學者可讀性：19 頁完全沒有連到術語表，已在「相關頁面」補上連結（逐一檢查每個術語的第一次出現仍是人工項目）
- [x] 待補來源清單：0 處，index 已同步
- 修改後：lint 0 error, 0 warning；結構檢查 0 issues；數字核對只剩 13 處已確認的誤判

## [2026-11-22] lint | 修正 topic-slides ⓪ reviewer 指出的問題（嚴重 1 + 輕微 #3、#8、#10）
- 修改：comparisons/rag-techniques.md — Reranking 列的 67% 原本寫成「和上一列（Hybrid retrieval）合用」，改為「在 Contextual Embeddings + Contextual BM25 之上再加 reranking，5.7% → 1.9%」，和 contextual-retrieval.md、sources/03 一致（嚴重）
- 修改：concepts/hallucination.md — 「RAG 能有效減少錯誤內容」（02 §I）加 ⚠️，對照 04 Table 6／Table 1 與 05 App. C.1；frontmatter sources 補 04；相關頁面補 closed-book-vs-open-book
- 修改：overview.md — §2 同一句加 ⚠️；§3 原始 RAG 改寫為「文件分別交給 generator 再 marginalize、retriever 與 generator 一起訓練」，和 naive-rag、reranking 頁一致；LLM、hallucination、context window 改在第一次出現時連結
- 修改：index.md — Hallucination 的 sources 計數 5 → 6
- ⚠️ 新標註：hallucination.md、overview.md 各 1 個（RAG 是否減少錯誤內容）
- 待補來源：無
- 未處理：reviewer 其餘 13 項輕微問題與 5 處待核對 raw 的引用，見 output/what-is-rag/lint.md
- lint：0 error, 0 warning

## [2026-11-22] lint | 修正 topic-slides ⓪ 第 2 輪 reviewer 指出的問題（嚴重 1 + 輕微 #2、#3、#5、#7）
- 修改：sources/07-es2023-ragas.md — GPT Ranking 和人類判斷的一致度原寫「常常不到一半」，和同頁表格 0.54／0.40／0.52 矛盾，改為「只有 0.40–0.54」，和 overview、rag-evaluation 一致（嚴重）
- 修改：concepts/lost-in-the-middle.md、concepts/context-window.md、sources/04、sources/06 — 06 的 8k context 結果補上「在全面性上」「其他標準差不多」；lost-in-the-middle 另註明 06 沒有直接測位置效應
- 修改：comparisons/closed-book-vs-open-book.md — 「open-book 低於 closed-book」補上「20、30 份文件設定、最差位置」的限定
- 修改：concepts/generator.md、sources/01 — 原始 RAG 是把問題和每一份文件分別串接，再 marginalize，不是串成一個長 prompt；generator 頁連到原始 RAG
- 修改：overview.md、sources/01 — 「小模型勝過大模型」補上「在 open-domain QA（例如 NQ）上」
- ⚠️ 新標註：無
- 待補來源：無
- 未處理：第 2 輪其餘輕微問題，見 output/what-is-rag/lint.md
- lint：0 error, 0 warning

## [2026-11-22] lint | 整批修正 topic-slides ⓪ 第 1–3 輪的問題
- 依據：output/what-is-rag/issues.md（三輪共 59 筆，去重後 40 條，另加 1 條修正時自己發現的格式問題，共 41 條；每條都有編號、類別、狀態）
- raw 核對方式：raw/text/ 不存在；為了不動 raw/，用 pypdf 4.3.1 把 PDF 抽成文字放在 session 暫存區核對。頁碼仍以 PDF 頁為準
- 事實／限定條件：
  - methods/self-rag.md：核對 05 §6 p.10，原文確實寫「significantly outperforms LLMs with more parameters or with conventional RAG」→ 保留原句並加 ⚠️「原文結論與 Table 2 不一致」，補上 §5.1 p.8、§1 p.2 的限定說法；sources/05 補一行說明，Table 2 摘錄補上 Llama2-13B（不檢索）、Llama2-7B（檢索）兩列
  - overview、methods/graphrag、comparisons/rag-techniques：72%–83% 改成「GraphRAG 等全局方法」，分開寫 Podcast 和新聞的範圍（06 §5.1 p.9）
  - methods/naive-rag：原始 RAG 改成「每份文件分別串接，再 marginalize」，和 generator、sources/01 同步
  - analogies「書包塞太滿」：比喻的極限補上「50 本不會比較差，只是不划算」
  - analogies、parametric-vs-non-parametric-memory、sources/01：12%／4% 寫明 index 和年份的組合（01 §4.5 p.8）
  - methods/self-rag：150k 註明附錄是 145,619 筆
- ⚠️ 同步：
  - Reranking ⚠️ 以 concepts/reranking.md 為準，同步到 retriever、advanced-rag、sources/01、sources/02、sources/03（01 vs 02＋03＋04，加上「情境不同」）
  - 文件數量 ⚠️ 以 concepts/context-window.md 為準，同步到 retriever、sources/01、sources/02
- ⚠️ 新標註：methods/self-rag.md（原文結論與 Table 2）、methods/contextual-retrieval.md（摘要 indexing vs GraphRAG）、comparisons/rag-paradigms.md（Naive RAG 是否「最早」）
- ⚠️ 格式：sources/04「06 說前段」、overview「小型知識庫」改成標準的 ⚠️ 區塊；self-rag、sources/01 的 ⚠️ 區塊後補上空行
- 引用：overview 的「拆成小步驟」補上 07 §5；ragas.md 的 Self-RAG 改引 05 §3.1；lost-in-the-middle 拿掉用 05 §3.3 證明「沒有提到」的引用；rag-evaluation、sources/06、sources/07 補上「實驗用 gpt-4-turbo」（06 §4.1.3 p.9）
- 已核對、不需修改：「chunk 不超過幾百 tokens」（03 p.2、p.3 都有）、49%／67% 的頁碼（03 p.2、p.4–7、p.10 都對）、advanced-rag 的 02 §II-B p.3／p.4、reranking 的 04 §5 p.9
- 術語：glossary 新增 23 條（98 → 121），包括 BLEU、Cross-encoder、F1、FEVER、Forward pass、Hit Rate、HNSW、Leiden、Marginalize、MAUVE、MRR、MS-MARCO、NQ、NDCG、PPO、Reinforcement learning、RLHF、ROUGE、Self-attention、Thorough／Fast Decoding、Transformer、TriviaQA、Unsupervised fine-tuning。raw 只列名、沒有定義的指標，詞條就只寫 raw 說了什麼。另外在 overview、hallucination、context-window、lost-in-the-middle、ragas、graphrag、self-rag、retriever 中，術語第一次出現時補上連結
- 結構：retriever 的 GenRead 移到「從哪裡檢索？」；context-window 第 57 行改寫；rag-timeline 的 GraphRAG 改成依 raw 版本的日期（2025-02-19）排序並註明原因；5 個方法頁的「出處」和 frontmatter `sources` 一致
- 不修（理由見 issues.md N01–N04）：新增 BM25／LLM-as-a-judge／Robustness 頁（維持之前「暫不拆頁」的決定）；context-window 和 lost-in-the-middle 不合併（維持之前的決定）；ragas 和 rag-evaluation 的 RAGAS 段落刻意保留重複（總覽頁需要能獨立閱讀的摘要，數字已核對一致）；reviewer 讀不到 output/ 屬於 workflow 的設計
- index.md：術語表 121 條；sources/01、advanced-rag、contextual-retrieval、rag-paradigms 的 sources 計數更新
- 待補來源：無
- lint：0 error, 0 warning

## [2026-11-22] schema | graph workflow v2、raw-text/
- 新增：`tools/pdf2text.py`（pymupdf 1.24.10，安裝在 `.venv/`，版本記在 `requirements.txt`）→ 產生 `raw-text/*.md`，每頁開頭有 `<!-- page N -->`，和 PDF 頁數一致（7 個檔案都已核對頁數）；把 PDF 中的控制字元換成空白（01 p.3 的公式括號）
- AGENTS.md：
  - §2 目錄樹加入 `raw-text/`、`tools/pdf2text.py`、`requirements.txt`；註明 `raw-text/` 是衍生檔、不可手動編輯；新增 PDF 後要跑 pdf2text.py
  - §7 可以讀 `raw-text/` 核對，但引用仍然寫原始 PDF 的檔名和頁碼
  - §9.1 ingest 可以讀 `raw-text/`；第 9 步改成 Wiki 維護流程
  - §9.3 改成「Wiki 維護流程（v2）」：lint.py → reviewer 只檢查有變動的頁面＋對應的 raw-text/ → index、log、commit；寫入 v2 的嚴重度規則；不再每次檢查全部頁面
  - §9.4 主題簡報改用 `/topic-slides`（v2）
  - §12 禁止手動編輯 `raw-text/`，也禁止在引用中寫 raw-text 路徑
- `.claude/commands/topic-slides.md`：⓪ 只跑 lint.py；新增 ②b 相關頁語意檢查（reviewer 只讀 sources.md 的頁面＋對應 raw-text/＋issues.md，最多 2 輪，可修正相關 wiki 頁）；嚴重度規則寫死；② 補完來源後回到 ⓪；⑥ 小 loop 上限改為 2 輪
- `.claude/agents/reviewer.md`：模式 A 可以讀 raw-text/、issues.md，並回報舊問題的狀態；寫入嚴重度規則；已登記的問題不得改變嚴重度
- `scripts/wf_state.py`：新增節點 `2b`；每個關卡有各自的退回上限（②b、⑥ 是 2，其他是 3）；report.md 保留 `<!-- preamble -->` 開頭區塊
- README.md：`raw/text` 改成 `raw-text/`；v1 紀錄的路徑改成 `output/what-is-rag/v1/`
- topic-slides（what-is-rag）：v1 的執行狀態封存到 `output/what-is-rag/v1/`（含 run-log-v1.md）；v2 重新開始，issues.md 以 v1 的總表為基準
- lint：0 error, 0 warning

## [2026-11-22] lint | 補 Fig.1 的完整例子（topic-slides what-is-rag ⑤ 退回，使用者批准）
- 修改：sources/01-lewis2020-rag.md — 「關鍵圖表說明」新增「Fig.1 的例子：走一遍『Define "middle ear"』」6 個步驟（輸入 → 問題轉成向量 → MIPS 找 top-K → 分別生成再加權合併 → 輸出 → 對照 BART 的錯誤答案），引用 Fig.1 p.2、§1 p.2、§2.1 p.3、Table 3 p.7
- 修改：sources/05-asai2023-self-rag.md — 新增「Fig.1 的例子：走一遍『How did US states get their names?』」：一般 RAG 3 步（答案和取回的文件不一致）、Self-RAG 3 步（每段前判斷要不要檢索 → 平行生成並標 ISREL／ISSUP → 選中完全被支持的段落）、不需要檢索的暑假作文例子，引用 Fig.1 p.2、§3.1 p.4
- 依據：raw-text/01 page 2、page 7；raw-text/05 page 2、page 4
- reviewer（Wiki 維護流程，只看這兩頁＋對應 raw-text）：嚴重 0、輕微 5；4 條當場修正，1 條不修（要看原圖才能確認標籤位置），登記為 output/what-is-rag/issues.md 的 V2-18–V2-22
- ⚠️ 新標註：無
- 待補來源：無
- lint：0 error, 0 warning
