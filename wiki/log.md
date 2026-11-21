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
