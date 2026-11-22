 ▐▛███▛█   Claude Code v2.1.330
▝▜██████▀  Opus 5.5 · Claude Pro
 ▝▝   ▝▝   ~/rag-wiki

▎ [✻] [✻] [✻] · Share Claude Code and earn $10 in usage credits · /passes

❯ /topic-slides RAG 是什麼？                                                    

  Ran 1 shell command (ctrl+o to expand)

⏺ ⓪ Wiki lint 關卡

  Ran 2 shell commands (ctrl+o to expand)

⏺ Lint 0 error。接著呼叫 reviewer（模式 A）做語意檢查。

⏺ reviewer(Wiki semantic lint (mode A))
  ⎿  Backgrounded agent (↓ to manage · ctrl+o to expand)

⏺ Reviewer 執行中。在等的同時，先讀 workflow 腳本以了解各節點的檢查規則（不進入
  ①）。

  Read 1 file, ran 2 shell commands (ctrl+o to expand)

⏺ 機械性檢查已寫入 lint.md，等 reviewer 的語意檢查結果回來再判定 ⓪。

  <br>

  Ran 1 shell command (ctrl+o to expand)

⏺ 我已經開始為「RAG 是什麼？」做簡報，目前停在第一關 ⓪（wiki
  健康檢查），還沒有往下走。

  - 機械性檢查：tools/lint.py 跑完是 0 error、0 warning，結果已寫進
    output/what-is-rag/lint.md。
  - 語意檢查：reviewer 還在跑，它只會讀 wiki/ 下的 36 個頁面。

  reviewer 回報後，我會核對它有沒有讀清單外的檔案，再決定這一關過不過：
  - 沒有嚴重問題：記為通過並 commit，接著做 ① 檢索。
  - 有嚴重問題：記為退回並 commit，然後停下來，列出要先修哪些 wiki 頁給你。

❯ 繼續                                                                          

⏺ 我還不能往下走：⓪ 的語意檢查 reviewer 還在跑（剛啟動約 1 分鐘），還沒有結果。

  workflow 規定 ⓪ 要先判定通過，才能進入 ① 檢索，所以現在不能跳過。reviewer
  要逐頁讀 wiki/ 下的 36
  個頁面，需要一點時間。它跑完我會自動收到通知，然後馬上接著做：

  1. 核對它實際讀了哪些檔案，確認沒有讀清單外的檔案。
  2. 把結果寫進 output/what-is-rag/lint.md 的「語意檢查」段。
  3. 判定這一關：
     - 沒有嚴重問題：記為通過、commit，接著做 ① 到 ④，然後在 ⑤
       停下來給你看大綱。
     - 有嚴重問題：記為退回、commit，然後列出要先修哪些 wiki 頁給你。

  你不用再回覆，結果出來我會直接繼續。

› Message from reviewer
  ## 問題清單

  整體來說：36 頁都讀完了。index 裡的 sources
  計數、詞條數（98）、比喻數（11）都和各頁一致，`[待補來源]`
  清單和頁面內容也一致（index 和各頁都是 0 處）。主要問題有四類：1
  處數字說錯是由哪幾項技巧組合得出的、幾處把限定條件拿掉的概括、幾組舊的 ⚠️
  標註沒有跟著更新、初學者讀不懂的術語偏多。

  ### wiki/comparisons/rag-techniques.md
  1. [嚴重｜說法不一致] 第 20 行，Reranking 列：「和上一列合用時，失敗率總共降低
  67%」
     - 來源：「上一列」是 Hybrid retrieval（embedding + BM25）。但
  methods/contextual-retrieval.md 第 40 行、sources/03 第 55 行都寫明，67%
  是「Contextual Embeddings + Contextual BM25 + reranking」的結果。
     - 說明：照字面讀，會以為「一般 hybrid + reranking」就能降低 67%，漏掉了
  Contextual Retrieval 這個前提。這和其他頁對同一個數字的說法不一致。
     - 建議：改成「在 Contextual Embeddings + Contextual BM25 之上再加
  reranking，失敗率總共降低 67%（5.7% → 1.9%）」。

  ### methods/self-rag.md
  2. [輕微｜限定條件被拿掉，可能和別頁矛盾] 第 51
  行：「在六個任務上，勝過參數更多的 LLM，以及傳統的 RAG 方法 [05, §6, p.10]」
     - 來源：sources/05 第 74–75 行寫的是「非商用模型中表現最好；在
  PubHealth、PopQA、傳記、ASQA 上甚至勝過 ChatGPT」。同一頁的 Table 2
  中，ChatGPT 在 TriviaQA（74.3 vs 69.3）和 ARC-C（75.3 vs 73.1）都高於 Self-RAG
  13B，而「ChatGPT 加上檢索」本身就是一種傳統 RAG 基準。
     - 說明：這句可能是忠實轉述原文 §6 的結論，但和 wiki
  自己整理的表格衝突。列為輕微是因為 wiki 沒寫 ChatGPT
  的參數量，無法確定「參數更多的 LLM」是否包含 ChatGPT。
     - 建議：加上限定，例如「多數任務；在 TriviaQA、ARC-C 上仍低於
  ChatGPT」。或者把它標成原文結論和表格之間的不一致。

  ### concepts/hallucination.md（也涉及 overview.md 第 22 行）
  3. [輕微｜可能是未標註的矛盾] 第 19 行：「透過參考外部知識，RAG
  能有效減少產生錯誤內容的問題 [02, §I, p.1]」
     - 來源：methods/naive-rag.md 第 36–39 行已經把 02 的類似概括（「勝過沒有
  RAG 的 LLM」）加上 ⚠️，反例是 04 Table 6 和 05 Table 2。sources/05 第 101
  行也提到，文件不相關時，一般模型仍會產生「看似合理」的答案。
     - 說明：這句和 naive-rag 已加 ⚠️
  的說法是同一類概括，但這一頁沒有任何反面說明。列為輕微是因為 04、05
  衡量的是準確率，不一定等於 hallucination，是否算同一組矛盾需要判斷。
     - 建議：加一行 ⚠️ 或「但檢索不一定有幫助」，連到
  closed-book-vs-open-book.md。

  ### concepts/retriever.md、methods/advanced-rag.md、sources/01-lewis2020-rag.m
  d、sources/02-gao2023-survey.md
  4. [輕微｜⚠️ 沒有跟著更新] reranking 的爭議在 concepts/reranking.md 第 54–55
  行已更新為「01 vs 02＋03＋04」，並補了情境說明（01 是每份文件分別交給
  generator，沒有位置問題）。但其他頁的同一組 ⚠️ 沒有更新：
     - retriever.md 第 95 行、advanced-rag.md 第 45 行、02 來源頁第 78 行只寫到
  02、03；
     - 01 來源頁第 99 行只寫到 02。
     - 說明：這些頁都有連到 reranking 頁，所以不算矛盾。但它們把爭議講成「01 vs
  02」，而且少了「情境不同」這個關鍵限定，可能讓讀者以為 01 和其他來源直接衝突。
     - 建議：在這些 ⚠️ 中補上 04，以及一句「情境不同，詳見 Reranking」。
  5. [輕微｜⚠️ 沒有跟著更新] sources/01 第 101 行，「文件數量」的 ⚠️ 只對照
  02。但 context-window.md 已整合成六種說法，並加了「01 是不同的情境」這一點。
     - 建議：補上「情境不同（01 的文件是分別處理）」和連結。

  ### comparisons/closed-book-vs-open-book.md
  6. [輕微｜限定條件被拿掉] 第 51 行：「答案放在中間時，open-book 的表現反而低於
  closed-book [04, §2.3, p.5]」
     - 來源：sources/04 第 61 行寫的是「在 20 和 30
  份文件的設定中，最差情況反而低於這個數字」。lost-in-the-middle.md
  的表格也顯示，第 5 份（57.2%）仍高於 closed-book（56.1%）。
     - 建議：加上「GPT-3.5-Turbo、20／30 份文件時的最差位置」這類限定。

  ### concepts/lost-in-the-middle.md
  7. [輕微｜因果可能被放大] 第 54 行把「用較小的 context window（06：8k 勝過
  16k–64k）」列為減輕 lost in the middle 的方法。
     - 來源：06 只說「因為擔心 lost in the middle 才測試不同大小」（同頁第 64
  行）。它衡量的是全面性勝率，沒有直接測位置效應。
     - 建議：改寫成「06 出於這個顧慮測試 context 大小，結果 8k
  的全面性最好」，不要直接說它是減輕方法。

  ### overview.md
  8. [輕微｜和其他頁的說法不一致] 第 37 行：「原始的 RAG（2020）流程相同，但
  retriever 和 generator 是一起訓練的」
     - 來源：naive-rag.md 第 65 行、lost-in-the-middle.md 第 60 行、reranking.md
  第 55 行都強調，原始 RAG 是把每份文件分別串接後交給 generator，再做
  marginalize，「不是串成一個長 prompt」。這也是 wiki 化解
  reranking、文件數量兩組爭議時的關鍵論點。
     -
  建議：改成「整體都是先查再寫，但文件是分別處理再加權合併，而且一起訓練」。
  9. [輕微｜引用不完整] 第 65 行：「拆成小步驟、重複多次、交叉驗證會比較可靠
  [06, §3.3, p.8]」
     - 說明：「拆成小步驟」的出處是 07 §5（見 rag-evaluation.md 第 118
  行），這一句只引用了 06。
  10. [輕微｜第一次出現的術語沒有連結] 第 15 行「hallucination」（第 17
  行才連結），第 23 行「context window」（概念頁已經存在）。第 15
  行的「LLM」也沒有連到術語表。

  ### concepts/rag-evaluation.md、comparisons/rag-vs-fine-tuning.md、concepts/em
  bedding.md、concepts/context-window.md、methods/graphrag.md、glossary.md
  11. [輕微｜初學者讀不懂] 以下術語第一次出現時沒有解釋，術語表裡也沒有：
     - rag-evaluation.md 第 40、125 行：Hit Rate、MRR、NDCG、F1、BLEU、ROUGE
     - rag-vs-fine-tuning.md 第 32 行：RLHF、PPO
     - embedding.md 第 33 行：HNSW
     - context-window.md 第 21
  行：Transformer；lost-in-the-middle.md、analogies.md：self-attention
     - self-rag.md 和 sources/05：MAUVE
     - 多頁出現的 NQ、TriviaQA、FEVER、MS-MARCO
     - 建議：在術語表補上這些詞條，或在第一次出現時加一句白話說明。
  12. [輕微｜術語表有、但頁面上沒有連結] 例如 retriever.md 第 24 行
  MIPS、graphrag.md 第 34 行 Leiden／map-reduce、ragas.md 第 34 行
  cosine、self-rag.md 第 34 行 segment-level beam
  search。各頁只在「相關頁面」放了術語表的總連結，第一次出現時沒有連結。

  ### concepts/ragas.md
  13. [輕微｜引用錯頁] 第 60 行：「Self-RAG 是模型在生成時自己評估，RAGAS
  則是事後由另一個 LLM 評估 [07, §3, p.3]」
     - 說明：Self-RAG 那一半應該引用 05（例如 rag-evaluation.md 第 97 行用的
  [05, §3.1, p.4]）。

  ### concepts/retriever.md
  14. [輕微｜結構] 第 81 行「LLM 自己產生的內容：GenRead」被放在「Retriever
  的天生限制：只找得到局部」這一節裡，但內容屬於上一節「從哪裡檢索？」。

  ### 跨頁：被提到多次卻沒有獨立頁面的概念
  15. [輕微｜建議新增頁面]
     - **BM25／hybrid retrieval**：在 retriever、embedding、contextual-retrieval
  、rag-techniques、analogies、overview、glossary 都有出現，目前是 retriever.md
  裡的子節。
     - **LLM-as-a-judge**：在 rag-evaluation、graphrag、06、07、overview
  都有出現，且帶有 ⚠️ 爭議。
     - **Robustness**：仍列在待建頁面。
     - log
  已記錄「暫不拆頁」的決定，這裡只提醒：簡報的「怎麼評估」段落很可能會用到
  LLM-as-a-judge，獨立成頁會比較好引用。
  16. [輕微｜內容重疊] context-window.md 和 lost-in-the-middle.md
  有三組重複內容：減輕方法（reranking、truncation、query-aware）、「長 context
  模型不一定比較會用」、06 的 8k
  實驗。兩頁列出的減輕方法已經不同步（壓縮、篩選只出現在前者，GraphRAG 打亂只出
  現在後者）。不一定要合併，但建議讓同一份清單只放在一頁，另一頁改成連結。

  ### 需要更多資料（要核對 raw/，不在允許讀取的清單內）
  17. [輕微｜需要更多資料] 以下引用需要讀 raw PDF 才能核對：
     - (a) analogies.md 第 40 行說「年份不對應時只剩 4%」，但
  parametric-vs-non-parametric-memory.md 寫「12% 和
  4%」，沒有說哪個數字對應哪種組合。需要核對 01 §4.5 p.8，確認 4% 是不是「2018
  年的領袖配 2016 年的 index」。
     - (b) 「chunk 通常不超過幾百 tokens」在 chunking.md 引用 03 p.2，在
  retriever.md 引用 03 p.3，在 naive-rag.md 引用 p.2–3，頁碼不一致。
     - (c) rag-techniques.md 第 26 行的
  Llama2-7B（38.2、30.0）在其他頁都沒有，需要核對 05 Table 2 p.8。
     - (d) self-rag.md 第 51 行所引用 05 §6 p.10
  的原句，是否真的是「六個任務」「傳統 RAG 方法」。
     - (e) sources/03 第 88 行說「p.8 的長條圖：失敗率降低
  49%」，但同一個數字在表格中引用 p.7，需要確認圖的實際頁碼。

  ## 統計
  - 嚴重：1；輕微：16
  - 需要修正的 wiki 頁：wiki/comparisons/rag-techniques.md,
  wiki/methods/self-rag.md, wiki/concepts/hallucination.md, wiki/overview.md,
  wiki/concepts/retriever.md, wiki/methods/advanced-rag.md,
  wiki/sources/01-lewis2020-rag.md, wiki/sources/02-gao2023-survey.md,
  wiki/comparisons/closed-book-vs-open-book.md,
  wiki/concepts/lost-in-the-middle.md, wiki/concepts/ragas.md,
  wiki/concepts/rag-evaluation.md, wiki/glossary.md（以及第 11、12
  項提到的術語連結相關頁面）

  ## 實際讀取的檔案
  - /Users/ting/rag-wiki/wiki/index.md
  - /Users/ting/rag-wiki/wiki/overview.md
  - /Users/ting/rag-wiki/wiki/glossary.md
  - /Users/ting/rag-wiki/wiki/analogies.md
  - /Users/ting/rag-wiki/wiki/log.md
  - /Users/ting/rag-wiki/wiki/comparisons/closed-book-vs-open-book.md
  - /Users/ting/rag-wiki/wiki/comparisons/rag-paradigms.md
  - /Users/ting/rag-wiki/wiki/comparisons/rag-techniques.md
  - /Users/ting/rag-wiki/wiki/comparisons/rag-timeline.md
  - /Users/ting/rag-wiki/wiki/comparisons/rag-vs-fine-tuning.md
  - /Users/ting/rag-wiki/wiki/concepts/chunking.md
  - /Users/ting/rag-wiki/wiki/concepts/context-window.md
  - /Users/ting/rag-wiki/wiki/concepts/embedding.md
  - /Users/ting/rag-wiki/wiki/concepts/generator.md
  - /Users/ting/rag-wiki/wiki/concepts/hallucination.md
  - /Users/ting/rag-wiki/wiki/concepts/lost-in-the-middle.md
  - /Users/ting/rag-wiki/wiki/concepts/parametric-vs-non-parametric-memory.md
  - /Users/ting/rag-wiki/wiki/concepts/query-optimization.md
  - /Users/ting/rag-wiki/wiki/concepts/rag-evaluation.md
  - /Users/ting/rag-wiki/wiki/concepts/ragas.md
  - /Users/ting/rag-wiki/wiki/concepts/reranking.md
  - /Users/ting/rag-wiki/wiki/concepts/retriever.md
  - /Users/ting/rag-wiki/wiki/methods/advanced-rag.md
  - /Users/ting/rag-wiki/wiki/methods/contextual-retrieval.md
  - /Users/ting/rag-wiki/wiki/methods/graphrag.md
  - /Users/ting/rag-wiki/wiki/methods/modular-rag.md
  - /Users/ting/rag-wiki/wiki/methods/naive-rag.md
  - /Users/ting/rag-wiki/wiki/methods/original-rag.md
  - /Users/ting/rag-wiki/wiki/methods/self-rag.md
  - /Users/ting/rag-wiki/wiki/sources/01-lewis2020-rag.md
  - /Users/ting/rag-wiki/wiki/sources/02-gao2023-survey.md
  - /Users/ting/rag-wiki/wiki/sources/03-anthropic-contextual-retrieval.md
  - /Users/ting/rag-wiki/wiki/sources/04-liu2023-lost-in-middle.md
  - /Users/ting/rag-wiki/wiki/sources/05-asai2023-self-rag.md
  - /Users/ting/rag-wiki/wiki/sources/06-edge2024-graphrag.md
  - /Users/ting/rag-wiki/wiki/sources/07-es2023-ragas.md

⏺ Reviewer 讀的 36 個檔案都在允許清單內，這一輪有效。它判了 1
  個嚴重問題，我先自己確認一下原文。

  Ran 1 shell command (ctrl+o to expand)

⏺ Agent "Wiki semantic lint (mode A)" finished · 2m 57s

⏺ 確認後發現，表格中 Reranking 的上一列是一般的 Hybrid retrieval，但 67%
  的結果其實是在 Contextual Embeddings 加 Contextual BM25 之上再做 reranking
  得來的，因此判定 ⓪ 未通過。 · summary

  Ran 1 shell command (ctrl+o to expand)

⏺ 第一關 ⓪（wiki 健康檢查）沒過，所以我停在這裡，還沒開始做 ① 檢索。這是 ⓪ 第 1
  次退回，上限 3 次；結果已記錄並 commit。

  - 機械性檢查：tools/lint.py 是 0 error、0 warning。
  - 語意檢查：reviewer 只讀了 wiki/ 下允許的 36 頁，找到 1 個嚴重問題、16
    個輕微問題。嚴重的那個我自己看過原文，確認是對的。

  一定要先修的（嚴重）

  rag-techniques.md:20 的 Reranking 那一列寫「和上一列合用時，失敗率總共降低
  67%」。「上一列」是一般的 Hybrid retrieval（embedding + BM25），但 67%
  其實是「Contextual Embeddings + Contextual BM25 +
  reranking」三者一起用的結果（contextual-retrieval.md:40、03 
  來源頁:55）。照現在的寫法，讀者會以為一般 hybrid 加 reranking 就能降低 67%。

  建議改成：「在 Contextual Embeddings + Contextual BM25 之上再加
  reranking，失敗率總共降低 67%（5.7% → 1.9%）」。

  建議順便修的（輕微，不會擋住流程）

  下面幾項跟「RAG 是什麼？」這份簡報直接有關，最好一起修：
  - #3 hallucination.md:19：寫「RAG 能有效減少產生錯誤內容」，但沒有
    ⚠️。naive-rag.md 對同一類說法已經加了
    ⚠️。這句很可能會用在簡報的「為什麼需要」。
  - #8 overview.md:37：沒寫出原始 RAG
    是「每份文件分別處理，再加權合併」。這一點和其他頁不一致。
  - #10 overview.md 第 15、23 行：hallucination、context window、LLM
    第一次出現時沒有連結。

  其餘 13 項（⚠️ 沒有跟著更新、少了限定條件、缺術語、建議新增頁面等）和 5
  處需要回去核對 raw PDF 的引用，都寫在 output/what-is-rag/lint.md。

  接下來

  照 workflow 規定，修 wiki 要另外依 AGENTS.md 處理，不能在這個 workflow
  裡做。你可以選：
  1. 叫我依 AGENTS.md 修上面的 wiki 頁，至少修那個嚴重問題，並記到 wiki/log.md。
  2. 你自己修。

  修好之後再執行一次 /topic-slides RAG 是什麼？，會從 ⓪ 重新檢查。

❯ 修嚴重問題和 #3、#8、#10                                                      

  Searched for 1 pattern, ran 2 shell commands (ctrl+o to expand)

⏺ 問題都確認過了。開始依 AGENTS.md 修 wiki。

  Ran 3 shell commands (ctrl+o to expand)

⏺ 我修好了嚴重問題和 #3、#8、#10，tools/lint.py 跑完是 0 error、0
  warning，也已記錄在 wiki/log.md 並 commit。

  嚴重：rag-techniques.md:20
  - 67% 原本寫成「和上一列（一般 Hybrid retrieval）合用」的結果。
  - 現在改成「在 Contextual Embeddings + Contextual BM25 之上再加
    reranking，失敗率從 5.7% 降到 1.9%，總共降低 67%」，和
    contextual-retrieval.md、03 來源頁 一致。

  #3：「RAG 能減少錯誤內容」加上 ⚠️
  - hallucination.md 加了一個 ⚠️，列出兩個反例：
    - 04：GPT-3.5-Turbo 在答案放在中間時，準確率 53.8%，比完全不給文件的 56.1%
      還低。
    - 05：文件不相關時，一般模型仍會產生看似合理的答案。
  - 我也註明 04 量的是答題準確率，不等於 hallucination 的比例。
  - overview.md 第 2 節的同一句也加了簡短的 ⚠️，連到 hallucination 頁和
    closed-book-vs-open-book 頁。

  #8：overview.md 第 3 節的原始 RAG
  - 改成寫出兩點不同：每份文件分別交給 generator，再加權合併（不是串成一個長
    prompt）；retriever 和 generator 是一起訓練的。

  #10：overview.md 的術語連結
  - LLM、hallucination、context window 改在第一次出現時就加連結。

  另外，wiki/index.md 裡 Hallucination 頁的來源數從 5 改成 6。

  reviewer 其餘 13 項輕微問題，和 5 處要回去核對 raw PDF
  的引用，這次都沒有處理；清單在 output/what-is-rag/lint.md。

  可以再執行一次 /topic-slides RAG 是什麼？。它會接續目前的進度，從 ⓪
  重新檢查；這次是 ⓪ 的第 2 輪，上限是 3 次退回。

❯ /topic-slides RAG 是什麼？                                                    

  Ran 1 shell command (ctrl+o to expand)

⏺ 接續：status running、node 0，⓪ 已退回 1 輪。開始 ⓪ 第 2 輪。

  Ran 1 shell command (ctrl+o to expand)

⏺ reviewer(Wiki semantic lint round 2)
  ⎿  Backgrounded agent (↓ to manage · ctrl+o to expand)

⏺ ⓪ 第 2 輪開始了。

  - 機械性檢查：tools/lint.py 跑完是 0 error、0 warning。
  - 語意檢查：reviewer 正在重新檢查 wiki/ 下的全部 36 頁，還沒有結果。

  第 1 輪的紀錄另存成 output/what-is-rag/lint-round1.md。reviewer
  回報後我會核對它讀了哪些檔案，再判定這一輪：
  - 沒有嚴重問題：記為通過，接著做 ① 到 ④，然後停在 ⑤ 給你確認大綱。
  - 有嚴重問題：記為退回並 commit，然後告訴你要修哪些頁。

❯ 繼續                                                                          
⏺ 還不能往下走：⓪ 第 2 輪的 reviewer 才剛開始跑（約 30 秒），還沒有結果。

  上一輪它讀完 36 頁大約花了 3 分鐘。workflow 規定 ⓪ 要先通過才能進入 ①
  檢索，所以要等它回報。

  它跑完我會自動收到通知，然後直接判定這一關。如果通過，我會一路做完 ① 檢索到 ④
  大綱，再停下來請你確認大綱。你不用再回覆。

› Message from reviewer
  ## 問題清單

  ### wiki/sources/07-es2023-ragas.md
  1. [嚴重｜講反（和同頁數字矛盾）] 第 99 行：「直接讓 ChatGPT
  挑比較好的答案，和人類判斷一致的比例常常不到一半 [07-es2023-ragas.pdf, Table
  1, p.5]」
     - 來源：同頁第 63 行（以及 concepts/ragas.md 第 51 行）的 GPT Ranking 是
  0.54／0.40／0.52
     - 說明：三個數字裡只有 0.40 低於一半，0.54 和 0.52
  都超過一半。「常常不到一半」和引用的表格相反。overview.md、rag-evaluation.md
  的寫法是「只有 0.40–0.54」，和這裡也不一致。
     - 建議：改成「只有 0.40–0.54」，或「最低只有 0.40」。

  ### wiki/concepts/lost-in-the-middle.md、wiki/concepts/context-window.md、wiki
  /sources/04-liu2023-lost-in-middle.md、wiki/sources/06-edge2024-graphrag.md
  2. [輕微｜拿掉限定條件] lost-in-the-middle.md 第 54 行：「06 為一般 RAG 挑選
  context 大小時，8k 勝過 16k、32k、64k」；context-window.md 第 55 行：「06
  也發現，一般 RAG 的 context 用 8k 比用 64k 好」；04 來源頁第 106 行和 06
  來源頁第 110 行都寫「結果 8k 最好」
     - 來源：06 來源頁第 89 行和 context-window.md 第 48 行都寫明「8k
  在全面性上全面勝出（平均勝率 58.1%），在多樣性和幫助判斷上則差不多」
     - 說明：這四處把「只在全面性上勝出」講成整體最好。這不算正面矛盾，所以列為
  輕微；但如果引用到簡報，就會變成過度概括。
     - 建議：四處都補上「在全面性上」，或加上「其他標準差不多」。

  ### wiki/comparisons/closed-book-vs-open-book.md
  3. [輕微｜拿掉限定條件] 第 51 行：「答案放在中間時，open-book
  的表現反而**低於** closed-book」
     - 來源：sources/04 第 61 行寫「在 20 和 30
  份文件的設定中，最差情況反而低於這個數字」
     - 說明：這句沒有說明是 20／30
  份文件的設定，讀起來像在任何文件數量下都成立。
     - 建議：補上「在 20、30 份文件的設定中」。

  ### wiki/methods/self-rag.md
  4. [輕微｜可能過度概括] 第 51 行：「在六個任務上，勝過參數更多的
  LLM，以及傳統的 RAG 方法 [05, §6, p.10]」
     - 來源：sources/05 的 Table 2（第 68–72 行）中，ChatGPT 在 TriviaQA（74.3
  vs 69.3）和 ARC-C（75.3 vs 73.1）上高於 Self-RAG 13B。第 75 行也只說在
  PubHealth、PopQA、傳記、ASQA 上勝過 ChatGPT。
     - 說明：如果「參數更多的 LLM」包含 ChatGPT，這句就和表格衝突；如果只指
  Llama2-13B 和 Alpaca，就沒有問題。不能確定是哪一種，所以列為輕微。
     - 建議：講清楚比較的對象，或改寫成「在多數任務上……；ChatGPT 在
  TriviaQA、ARC-C 上仍較高」。

  ### wiki/concepts/generator.md
  5. [輕微｜可能被讀成和其他頁矛盾] 第 24
  行：「直接把問題和檢索到的文件串接（concatenate）在一起」
     - 來源：overview.md 第 40 行、lost-in-the-middle.md 第 60 行、naive-rag.md
  第 65 行都強調，原始 RAG 是把每份文件分別和問題串接，再
  marginalize，「不是把所有文件串成一個長 prompt」。
     - 說明：「檢索到的文件」是複數，初學者容易讀成「把所有文件串成一段」，和其
  他頁的說法相反。
     -
  建議：改成「把問題和**每一份**檢索到的文件分別串接，再把結果加權合併」，並連到
  original-rag.md。sources/01 第 36 行也可以一起釐清。

  ### wiki/overview.md
  6. [輕微｜引用不完整] 第 68
  行：「拆成小步驟、重複多次、交叉驗證會比較可靠，詳見 RAG 評估
  [06-edge2024-graphrag.pdf, §3.3, p.8]」
     - 來源：rag-evaluation.md 第 118–121 行把「拆成小步驟」歸給 [07, §5,
  p.5]，「交叉驗證」歸給 [07, §4] 和 [06, §4.2]。06 §3.3
  只支持「重複多次」和「對照標準」。
     - 建議：補上 07 §5 的引用，並依 rag-evaluation.md 分別附出處。
  7. [輕微｜拿掉限定條件] 第 72 行：「RAG 讓小模型也能勝過大很多的純參數模型
  [01, App. G, p.19]」
     - 來源：closed-book-vs-open-book.md 和 sources/01 第 63
  行都顯示，這個比較是 NQ 上的 open-domain QA（T5 vs RAG）。
     - 建議：補上「在 open-domain QA（例如 NQ）上」。sources/01 第 120
  行也要同樣處理。
  8. [輕微｜格式] 第 76 行用一般文字寫「這點和上一條有 ⚠️ 爭議」，沒有用 §8
  規定的 `> ⚠️ **爭議／更新**：` 區塊格式。
     - 建議：改成標準區塊格式，或明確指向 context-window.md 的 ⚠️ 區塊。

  ### wiki/concepts/retriever.md、wiki/methods/advanced-rag.md、wiki/sources/01-
  lewis2020-rag.md、wiki/sources/02-gao2023-survey.md、wiki/sources/03-anthropic
  -contextual-retrieval.md
  9. [輕微｜⚠️ 沒有跟著更新] Reranking 爭議在 reranking.md 第 54 行和 index.md
  中已經是「01 vs 02＋03＋04」，log 第 52 行也記錄了這次更新。但以下各頁的同一個
  ⚠️ 仍是舊版：
     - retriever.md 第 95 行、advanced-rag.md 第 45 行、sources/02 第 78
  行、sources/03 第 82 行：只列 01 vs 02＋03，沒有 04。
     - sources/01 第 99 行：只列 02，沒有 03、04。
     - 建議：補上 04 §5 的證據，讓所有頁面的這個 ⚠️ 版本一致。另外，sources/01
  第 101 行「文件數量」的 ⚠️ 只對照 02，也可以補上 04、03、06。

  ### wiki/concepts/retriever.md
  10. [輕微｜段落放錯位置] 第 81 行「LLM 自己產生的內容：例如
  GenRead……」放在「Retriever
  的天生限制：只找得到局部」小節裡，但內容是在講檢索來源。
      - 建議：移到第 70–75 行的「從哪裡檢索？」小節。

  ### wiki/comparisons/rag-timeline.md
  11. [輕微｜時間順序] 第 24–25 行：GraphRAG（2024–2025）排在 Contextual
  Retrieval（2024 年 9 月 19 日）之前。sources/06 第 14 行的 arXiv 編號是
  2404，表示首次發表在 2024 年 4 月，但目前時間欄寫的是 2024–2025，看不出先後。
      - 建議：依實際時間排序，或在時間欄註明首次發表與 raw 版本的差別。

  ### wiki/concepts/context-window.md
  12. [輕微｜可讀性] 第 57
  行：「所以不受位置影響的方式也不同」，句意不清，初學者讀不懂。
      - 建議：改成「所以 04 談的『文件在長 prompt 中的位置』問題，不能直接套用到
  01」。

  ### 多頁：專有名詞第一次出現時沒有連結或解釋（初學者可讀性）
  13. [輕微｜缺連結]
  下列頁面在內文第一次出現專有名詞時沒有連結，只有在頁尾「相關頁面」連到術語表：
      - hallucination.md 第 18 行的 LLM
      - context-window.md 第 13 行的 LLM、prompting、token
      - lost-in-the-middle.md 第 13 行的 prompt、LLM
      - ragas.md 第 13、34 行的 LLM、embedding、cosine
      - graphrag.md 第 13、34、22 行的 knowledge
  graph、Leiden、map-reduce（術語表都有詞條）
      - self-rag.md 第 34 行的 segment-level beam search（術語表有詞條）
      - 建議：在第一次出現時連到 glossary.md 或對應的概念頁。
  14. [輕微｜術語表缺詞條] 以下術語在內文出現，但沒有白話解釋，術語表也沒有：
      - Hit Rate、MRR、NDCG、F1、BLEU、ROUGE（rag-evaluation.md 第 26、40 行）
      - RLHF、PPO（rag-vs-fine-tuning.md 第 32 行）
      - unsupervised fine-tuning（rag-vs-fine-tuning.md 第 27 行）
      - cross-encoder（reranking.md 第 44 行）
      - HNSW（embedding.md 第 33 行）
      - marginalize、forward pass、Thorough／Fast Decoding（original-rag.md）
      - reinforcement learning（modular-rag.md 第 59 行）
      - 建議：補進術語表，或在原句加一句白話說明。

  ### 需要更多資料（核對引用位置需要讀 raw/，不在本次允許的清單內）
  15. [輕微｜需要更多資料] overview.md 第 50 行把「降低 49%、加 reranking 降低
  67%」引用到 [03, p.2, p.4–5]，sources/03 第 20 行引用到 [03, p.2, p.5–6]；但
  sources/03 的表格、contextual-retrieval.md、rag-techniques.md 都引用 p.7 和
  p.10。需要讀 raw 確認 p.2／p.4–6 是否真的有這兩個數字。
  16. [輕微｜需要更多資料] 「chunk 通常不超過幾百 tokens」這句，在 chunking.md
  第 25 行引用 [03, p.2]，在 retriever.md 第 61 行引用 [03, p.3]，在
  naive-rag.md 第 29 行引用 [03, p.2–3]。頁碼不一致，需要核對 raw。
  17. [輕微｜需要更多資料] advanced-rag.md 對 02 §II-B 的引用，同一段內容有時標
  p.3（第 13、17、25、39 行），有時標 p.4（第 24、27、31 行），需要確認。
  18. [輕微｜需要更多資料] rag-techniques.md 第 26 行的「加上檢索的
  Llama2-7B（38.2、30.0）」在 sources/05 的 Table 2 摘錄中沒有出現（摘錄只列了
  Llama2-13B），無法用 wiki 核對，需要讀 raw Table 2。
  19. [輕微｜需要更多資料] reranking.md 第 55 行用 [04, §5, p.9] 支持「04
  談的是把多份文件串成一個 prompt 的情境」，但其他頁的 04 §5 都標
  p.10；lost-in-the-middle.md 第 61 行用 [05, §3.3, p.6] 支持「05 沒有討論位置效
  應」，等於拿一個章節來證明「沒有提到」，引用方式不恰當。兩處都需要核對 raw。
  20. [輕微｜需要更多資料] log.md 第 139 行說「reviewer 其餘 13 項輕微問題與 5
  處待核對 raw 的引用，見 output/what-is-rag/lint.md」。那個檔案不在允許清單內，
  無法確認這些問題是否已經處理，或是否和本清單重複。

  ### 其他清單項目的檢查結果（沒有發現問題）
  - 待補來源：index.md 第 58 行寫 0 處，log.md 也記為 0；本次讀到的頁面中都沒有
  `[待補來源]` 標記，兩邊一致。
  - index.md：每一頁的 sources 計數都和 frontmatter 一致；術語表 98 條、比喻 11
  個，也和實際數量一致。
  - 應合併的頁面：沒有找到需要合併的頁面。context-window 和 lost-in-the-middle
  分別談數量和位置，已經互相連結；rag-evaluation 和 ragas
  有部分重疊，但已經互相連結，可以接受。
  - 多次出現卻沒有獨立頁面的概念：BM25／hybrid retrieval、knowledge
  graph、LLM-as-a-judge、Robustness 的處理方式和 log
  的決定一致，這次沒有新的建議。

  ## 統計
  - 嚴重：1；輕微：19
  - 需要修正的 wiki 頁：wiki/sources/07-es2023-ragas.md（嚴重）；以下為輕微：wik
  i/concepts/lost-in-the-middle.md, wiki/concepts/context-window.md,
  wiki/sources/04-liu2023-lost-in-middle.md,
  wiki/sources/06-edge2024-graphrag.md,
  wiki/comparisons/closed-book-vs-open-book.md, wiki/methods/self-rag.md,
  wiki/concepts/generator.md, wiki/overview.md,
  wiki/sources/01-lewis2020-rag.md, wiki/concepts/retriever.md,
  wiki/methods/advanced-rag.md, wiki/sources/02-gao2023-survey.md,
  wiki/sources/03-anthropic-contextual-retrieval.md,
  wiki/comparisons/rag-timeline.md, wiki/concepts/hallucination.md,
  wiki/concepts/ragas.md, wiki/methods/graphrag.md,
  wiki/concepts/rag-evaluation.md, wiki/comparisons/rag-vs-fine-tuning.md,
  wiki/concepts/reranking.md, wiki/concepts/embedding.md,
  wiki/methods/original-rag.md, wiki/methods/modular-rag.md, wiki/glossary.md

  ## 實際讀取的檔案
  - /Users/ting/rag-wiki/wiki/index.md
  - /Users/ting/rag-wiki/wiki/log.md
  - /Users/ting/rag-wiki/wiki/overview.md
  - /Users/ting/rag-wiki/wiki/glossary.md
  - /Users/ting/rag-wiki/wiki/analogies.md
  - /Users/ting/rag-wiki/wiki/comparisons/closed-book-vs-open-book.md
  - /Users/ting/rag-wiki/wiki/comparisons/rag-paradigms.md
  - /Users/ting/rag-wiki/wiki/comparisons/rag-techniques.md
  - /Users/ting/rag-wiki/wiki/comparisons/rag-timeline.md
  - /Users/ting/rag-wiki/wiki/comparisons/rag-vs-fine-tuning.md
  - /Users/ting/rag-wiki/wiki/concepts/chunking.md
  - /Users/ting/rag-wiki/wiki/concepts/context-window.md
  - /Users/ting/rag-wiki/wiki/concepts/embedding.md
  - /Users/ting/rag-wiki/wiki/concepts/generator.md
  - /Users/ting/rag-wiki/wiki/concepts/hallucination.md
  - /Users/ting/rag-wiki/wiki/concepts/lost-in-the-middle.md
  - /Users/ting/rag-wiki/wiki/concepts/parametric-vs-non-parametric-memory.md
  - /Users/ting/rag-wiki/wiki/concepts/query-optimization.md
  - /Users/ting/rag-wiki/wiki/concepts/rag-evaluation.md
  - /Users/ting/rag-wiki/wiki/concepts/ragas.md
  - /Users/ting/rag-wiki/wiki/concepts/reranking.md
  - /Users/ting/rag-wiki/wiki/concepts/retriever.md
  - /Users/ting/rag-wiki/wiki/methods/advanced-rag.md
  - /Users/ting/rag-wiki/wiki/methods/contextual-retrieval.md
  - /Users/ting/rag-wiki/wiki/methods/graphrag.md
  - /Users/ting/rag-wiki/wiki/methods/modular-rag.md
  - /Users/ting/rag-wiki/wiki/methods/naive-rag.md
  - /Users/ting/rag-wiki/wiki/methods/original-rag.md
  - /Users/ting/rag-wiki/wiki/methods/self-rag.md
  - /Users/ting/rag-wiki/wiki/sources/01-lewis2020-rag.md
  - /Users/ting/rag-wiki/wiki/sources/02-gao2023-survey.md
  - /Users/ting/rag-wiki/wiki/sources/03-anthropic-contextual-retrieval.md
  - /Users/ting/rag-wiki/wiki/sources/04-liu2023-lost-in-middle.md
  - /Users/ting/rag-wiki/wiki/sources/05-asai2023-self-rag.md
  - /Users/ting/rag-wiki/wiki/sources/06-edge2024-graphrag.md
  - /Users/ting/rag-wiki/wiki/sources/07-es2023-ragas.md

⏺ Reviewer 讀的檔案都在清單內，這一輪有效。先確認嚴重問題。

  Ran 1 shell command (ctrl+o to expand)

⏺ Agent "Wiki semantic lint round 2" finished · 3m 0s

⏺ 確認屬實：第 07 來源頁說「常常不到一半」，但同頁表格的數字多半不低於一半，第 2
  輪判定因此未通過。 · summary

  Ran 1 shell command (ctrl+o to expand)

⏺ ⓪ 第 2 輪還是沒過，我又停下來了，還沒開始做 ① 檢索。⓪ 已累計退回 2 次，再退回
  2 次（第 4 次）就會觸發停止程序。

  這一輪 tools/lint.py 是 0 error、0 warning；reviewer 找到 1 個嚴重問題、19
  個輕微問題，嚴重的那個我看過原文，確認是對的。它不是你上次修改造成的，而是一開
  始就存在、第 1 輪沒抓到。

  嚴重問題

  07 來源頁:99 寫「直接讓 ChatGPT
  挑比較好的答案，和人類判斷一致的比例常常不到一半」。但同一頁的表格是
  0.54／0.40／0.52，只有 0.40 低於一半。

  建議改成和 overview.md、rag-evaluation.md 一樣的寫法：「只有 0.40–0.54」。

  建議這次一起修的輕微問題

  reviewer 每一輪都會重新讀全部 36 頁，所以每次可能挑出不同的問題。下面 3
  項都是「拿掉了限定條件」或「容易讀成相反」，下一輪有可能被判成嚴重。而且它們都
  會用在「RAG 是什麼？」的簡報裡：

  - #2「8k context 最好」：06 的 8k 只在「全面性」上勝出，其他標準差不多。現在有
    4 處寫成整體最好：lost-in-the-middle.md:54、context-window.md:55、04 
    來源頁:106、06 來源頁:110。
  - #5 generator.md:24：寫「把問題和檢索到的文件串接」，容易讀成把所有文件串成一
    個長 prompt。這正好和上次在 overview 改的說法相反；01 來源頁:36
    也有同樣的寫法。
  - #3、#7：
    - closed-book-vs-open-book.md:51 缺「20、30 份文件」這個限定。
    - overview.md:72、01 來源頁:120 的「小模型勝過大模型」，缺「在 open-domain
      QA（NQ）上」這個限定。

  其他的輕微問題（⚠️ 沒有跟著更新、術語沒連結或沒解釋、需要回去核對 raw PDF
  的頁碼）都在 output/what-is-rag/lint.md。

  接下來

  要我依 AGENTS.md 修 wiki 嗎？我建議修「嚴重 +
  #2、#3、#5、#7」，你也可以只修嚴重的那一項。修好後再執行一次 /topic-slides RAG
  是什麼？，會跑 ⓪ 的第 3 輪。

❯ 修嚴重問題和 #2、#3、#5、#7                                                   

  Searched for 1 pattern, ran 3 shell commands (ctrl+o to expand)

⏺ 我修好了嚴重問題和 #2、#3、#5、#7。tools/lint.py 是 0 error、0
  warning，已記錄在 wiki/log.md 並 commit。

  嚴重：07 來源頁
  - 「常常不到一半」改成「只有 0.40–0.54，遠低於
    RAGAS」，和同頁的表格、overview、rag-evaluation 一致。

  #2：8k context 的結果
  - 4 處都補上「在全面性上」「其他標準差不多」：lost-in-the-middle.md、context-w
    indow.md、04 來源頁、06 來源頁。
  - lost-in-the-middle.md 另外註明：06 量的是答案品質，沒有直接測位置效應。

  #3：closed-book-vs-open-book.md:51
  - 補上限定條件：「在 20 和 30 份文件的設定中，答案放在最差的位置時（例如 20
    份中的第 10 份）」。

  #5：原始 RAG 怎麼把文件交給 generator
  - generator.md 和 01 來源頁
    改成：問題和每一份文件分別串接，再加權合併，不是把所有文件串成一個長
    prompt。
  - generator 頁也加了連到原始 RAG 頁的連結。

  #7：「小模型勝過大模型」
  - overview.md 和 01 來源頁 都補上「在 open-domain QA（例如 NQ）上」。

  修的時候我也搜尋了整個 wiki，沒有其他地方還留著同樣的舊寫法。

  可以再執行 /topic-slides RAG 是什麼？，會跑 ⓪ 的第 3 輪。⓪ 已退回 2
  次，這一輪再退回還不會觸發停止，再下一次（第 4 次）才會。

❯ /topic-slides RAG 是什麼？                                                    

  Ran 2 shell commands (ctrl+o to expand)

⏺ 接續：running、node 0、⓪ 已退回 2 輪。lint.py 0 error，啟動 ⓪ 第 3 輪
  reviewer。

⏺ reviewer(Wiki semantic lint round 3)
  ⎿  Backgrounded agent (↓ to manage · ctrl+o to expand)

⏺ ⓪ 第 3 輪開始了。

  - 機械性檢查：tools/lint.py 跑完是 0 error、0 warning。
  - 語意檢查：reviewer 正在重新讀全部 36 頁，上一輪大約花了 3 分鐘。

  前兩輪的結果另存成 output/what-is-rag/lint-round1.md、lint-round2.md。

  ⓪ 已經退回 2 次。這一輪如果又有嚴重問題，會記為第 3 次退回並停下來請你修；第 4
  次退回就會觸發停止程序。如果沒有嚴重問題，我會接著做 ① 檢索到 ④
  大綱，然後停在 ⑤ 給你確認大綱。

  結果出來我會直接接手，你不用再回覆。

› Message from reviewer
  ## 問題清單

  ### wiki/methods/self-rag.md
  1. [嚴重｜矛盾未標註] 第 51 行：「在六個任務上，勝過參數更多的 LLM，以及傳統的
  RAG 方法 [05-asai2023-self-rag.pdf, §6, p.10]」
     - 來源：sources/05-asai2023-self-rag.md 的 Table 2（第 68–72 行）列出
  ChatGPT（不檢索）TriviaQA 74.3、ARC-C 75.3，都高於 Self-RAG 13B 的
  69.3、73.1。同頁第 74–75 行只寫「在所有任務上都是**非商用模型**中最好」「在
  PubHealth、PopQA、傳記生成、ASQA 上勝過 ChatGPT」。overview.md 第 56
  行也寫成有限定的「在多個任務上勝過 ChatGPT」。
     - 說明：本頁拿掉了限定，讀起來像「六個任務都勝過更大的 LLM」，和同一個 wiki
  裡的 Table 2 數字衝突。這句可能是照 05 §6 結論原文寫的，但沒有加
  ⚠️，也沒有加限定。
     - 建議：補上限定（「在所有任務上勝過非商用模型；在部分任務上勝過
  ChatGPT」）。如果 §6 原文真的是這樣寫，就加 ⚠️ 標成「原文結論和 Table 2
  不一致」。
  2. [輕微｜一致性] 第 41 行：「插入 150k 筆訓練資料」
     - 來源：sources/05 第 118 行說明正文寫 150k，附錄是 145,619 筆。
     - 建議：註明這是約數，或連到 05 來源頁的說明。

  ### wiki/overview.md, wiki/methods/graphrag.md,
  wiki/comparisons/rag-techniques.md
  3. [輕微｜限定被拿掉] overview 第 58 行「GraphRAG……全面性勝率達
  72%–83%」；graphrag.md 第 56 行、rag-techniques 第 25 行「全面性勝率
  72%–83%、多樣性勝率 62%–82%」
     - 來源：sources/06 第 65–66 行寫的是「GraphRAG **等全局方法**對一般 RAG
  的勝率」，而且分資料集：Podcast 72%–83%，新聞 72%–80%；多樣性 Podcast
  75%–82%，新聞 62%–71%。
     - 說明：「全局方法」可能也包含 TS（直接對原文做摘要），不只
  GraphRAG。三頁把數字全算在 GraphRAG 身上，也拿掉了資料集的區分。不確定 TS
  是否算在這個範圍內，所以標為輕微。
     - 建議：改成「GraphRAG 等全局方法」，或標明各資料集的範圍。

  ### wiki/methods/naive-rag.md
  4. [輕微｜和上一輪修正不同步] 第 65 行，原始 RAG
  欄：「直接串接，並對多份文件做 marginalize」
     - 來源：generator.md 第 24 行和 sources/01 第 36
  行，上一輪已經改成「把問題和**每一份**文件分別串接，不是串成一段」。
     - 說明：「直接串接」容易讓人誤以為是把所有文件串成一個 prompt。
     - 建議：改成「把問題和每份文件分別串接，再 marginalize」。

  ### wiki/concepts/ragas.md
  5. [輕微｜引錯出處] 第 60 行：「差別在於 Self-RAG
  是模型在生成時**自己**評估，RAGAS 則是事後由另一個 LLM 評估
  [07-es2023-ragas.pdf, §3, p.3]」
     - 說明：Self-RAG 的部分只引用了 07。rag-evaluation.md 第 97
  行同一個說法引用的是 [05-asai2023-self-rag.pdf, §3.1, p.4]。
     - 建議：Self-RAG 的部分補上 05 的引用。
  6. [輕微｜可合併／重疊] ragas.md 和 rag-evaluation.md
  的「三個品質分數怎麼自動算？RAGAS」一節（rag-evaluation 第 58–66
  行）重複了三個指標的算法和 Table 1 的數字。
     - 建議：rag-evaluation 只保留一兩句摘要加連結；或在 log
  裡記錄「刻意保留重複」的決定（之前只記錄了 context-window 和
  lost-in-the-middle 的合併決定）。

  ### wiki/concepts/retriever.md
  7. [輕微｜段落放錯位置] 第 81 行：「**LLM 自己產生的內容**：例如
  GenRead……」放在「Retriever
  的天生限制：只找得到局部」底下，但它講的是檢索來源。
     - 建議：移到「從哪裡檢索？」一節。
  8. [輕微｜⚠️ 沒有跟著後來的來源更新] 第 95 行的 reranking ⚠️ 只寫了「01 vs
  02＋03」，沒有 04；第 41 行的「文件數量」⚠️ 只有 02、04，沒有 03（20
  份最好）和 06（8k）。
     - 說明：reranking.md 和 context-window.md 已經整合成 01 vs
  02＋03＋04，以及六種說法。
     - 建議：補上缺的來源，或改寫成「完整的對照見 X 頁」。
     - 同類問題也出現在：methods/advanced-rag.md 第 45 行（reranking ⚠️ 沒有
  04）；sources/01 第 99 行（reranking ⚠️ 只寫 02）和第 101 行（文件數量 ⚠️ 只寫
  02，沒有 03、04、06）；sources/02 第 78 行（reranking ⚠️ 沒有 04）。

  ### wiki/sources/04-liu2023-lost-in-middle.md
  9. [輕微｜⚠️ 標註缺漏，和 log 不一致] 第 106 行用一般內文描述「06
  把本篇結論說成 chunk 前段的資訊容易被漏掉，和本篇不一致」，沒有用 `> ⚠️
  **爭議／更新**` 格式。
     - 來源：log.md 第 76 行寫「標在 lost-in-the-middle、04、06
  頁」。lost-in-the-middle.md 和 sources/06 都有 ⚠️ 區塊，04 頁沒有。
     - 建議：在 04 頁加上正式的 ⚠️ 區塊。

  ### wiki/methods/contextual-retrieval.md
  10. [輕微｜爭議沒有標到方法頁] 第 56 行：「以摘要為基礎的
  indexing：作者評估後發現表現很差」
      - 來源：chunking.md、sources/03、sources/06 都有 ⚠️，對照的是 GraphRAG
  用社群摘要當 index 並勝過一般 RAG。
      - 說明：AGENTS §8 要求概念頁、方法頁都要加；本頁直接陳述 03
  的說法，沒有提醒範圍限制。
      - 建議：加一個簡短的 ⚠️ 並連到 chunking.md。

  ### wiki/concepts/context-window.md
  11. [輕微｜可讀性] 第 57 行：「……不是串成一個長
  prompt，所以不受位置影響的方式也不同。」
      - 說明：句意不清楚，初學者很難理解。
      - 建議：改成「所以沒有『文件排在 prompt 哪個位置』的問題」（和
  reranking.md 第 55 行的說法一致）。

  ### wiki/analogies.md
  12. [輕微｜比喻說得太滿] 第 58 行：「帶 20 本挑過、排好的書，比帶 50
  本亂放的書更有用。」
      - 來源：同一條的技術事實（第 61 行）和 sources/04 第 78 行都說 50 份仍然比
  20 份多進步約 1%–1.5%，只是效益小、成本高。
      - 說明：比喻不需要引用，但這句沒有寫在「比喻的極限」裡，容易讓初學者以為
  50 份比較差。
      - 建議：在「比喻的極限」補一句「50
  本其實仍略好一點，只是多花的成本不划算」。

  ### wiki/comparisons/rag-paradigms.md
  13. [輕微｜爭議沒有提醒] 第 11 行說綜述把 RAG 研究分成 Naive → Advanced →
  Modular 三個「階段」，但沒有提到 naive-rag、original-rag、rag-timeline
  都標過的 ⚠️（Naive RAG 是不是「最早」，以及它和 2020 年原始 RAG 的關係）。
      - 建議：加一句連到 naive-rag.md 的 ⚠️。

  ### wiki/comparisons/rag-timeline.md
  14. [輕微｜排序] 第 24–25 行：「2024–2025」的 GraphRAG 排在「2024 年 9 月 19
  日」的 Contextual Retrieval 前面，時間軸讀起來不連貫。
      - 建議：調整順序，或註明依 arXiv 初版時間排序（初版時間需要從 raw 確認）。

  ### wiki/methods/advanced-rag.md、contextual-retrieval.md、self-rag.md、graphr
  ag.md、modular-rag.md
  15. [輕微｜「出處」區塊不完整] 各頁的「##
  出處」只列了主要來源，但內文也引用了其他 raw：advanced-rag 引用了
  03、01；contextual-retrieval 引用了 02；self-rag 引用了 02、06；graphrag
  引用了 02；modular-rag 引用了 05。frontmatter 已經列齊。
      - 建議：讓「出處」和 frontmatter 的 sources 一致。

  ### wiki/overview.md
  16. [輕微｜術語第一次出現時沒有連結] 第 36–38 行的 vector
  database、top-k、prompt；第 51 行的 BM25；第 58 行的 knowledge graph；第 65
  行的 Exact Match；第 76 行的 tokens。這些詞在 glossary.md 都有詞條，但在
  overview（簡報骨架）第一次出現時沒有連結。
      - 建議：第一次出現時連到 glossary.md 或對應的概念頁。
  17. [輕微｜多次出現卻沒有術語條目] cross-encoder（reranking.md 第 44
  行）、F1／BLEU／ROUGE（rag-evaluation.md、sources/01）、Hit
  Rate／MRR／NDCG（rag-evaluation.md）、Leiden（graphrag.md、glossary
  內文）在多頁出現，但 glossary 沒有獨立詞條。初學者讀不懂。
      - 建議：補上 glossary 詞條，或在第一次出現時加一句白話說明。

  ### 需要更多資料（要讀 raw PDF 才能判斷，本次沒有讀）
  18. [輕微｜需要更多資料] 「chunk 通常不超過幾百 tokens」在 chunking.md 第 25
  行引用 [03, p.2]，retriever.md 第 61 行引用 [03, p.3]，naive-rag.md 第 29
  行引用 [03, p.2–3]。同一句話引用了不同頁碼，需要回 raw 確認。
  19. [輕微｜需要更多資料] overview.md 第 50 行把 49%／67% 引用為 [03, p.2,
  p.4–5]；sources/03 的表格把 49% 引用為 p.7、67% 引用為 p.10，摘要則引用 p.2,
  p.5–6。需要確認 p.4–5 是否真的有這兩個數字。
  20. [輕微｜需要更多資料] rag-techniques.md 第 26 行的「加上檢索的
  Llama2-7B（38.2、30.0）」和 closed-book-vs-open-book.md 第 62 行的「Llama2-13B
  ARC-Challenge 不檢索 29.4」，在 sources/05 的 Table 2 摘錄裡都沒有。wiki
  內部無法核對，需要回 05 Table 2 確認。
  21. [輕微｜需要更多資料] sources/06、rag-evaluation、sources/07 都寫「06 使用
  GPT-4 [06, §1, p.2]」，但 sources/06 其他地方寫的是 gpt-4-turbo（§4.1.3、App.
  C）。需要確認評審用的模型。
  22. [輕微｜需要更多資料] self-rag.md 第 51 行引用 [05, §6,
  p.10]，需要確認原文用詞（見第 1 項）。

  ## 統計
  - 嚴重：1；輕微：21（其中 5 項需要更多資料）
  - 需要修正的 wiki
  頁：wiki/methods/self-rag.md（嚴重）；以下是輕微：wiki/overview.md,
  wiki/methods/graphrag.md, wiki/comparisons/rag-techniques.md,
  wiki/methods/naive-rag.md, wiki/concepts/ragas.md,
  wiki/concepts/rag-evaluation.md, wiki/concepts/retriever.md,
  wiki/methods/advanced-rag.md, wiki/sources/01-lewis2020-rag.md,
  wiki/sources/02-gao2023-survey.md, wiki/sources/04-liu2023-lost-in-middle.md,
  wiki/methods/contextual-retrieval.md, wiki/concepts/context-window.md,
  wiki/analogies.md, wiki/comparisons/rag-paradigms.md,
  wiki/comparisons/rag-timeline.md, wiki/methods/modular-rag.md,
  wiki/glossary.md, wiki/concepts/chunking.md,
  wiki/comparisons/closed-book-vs-open-book.md
  - 其他檢查項目：index 的 sources 計數、glossary 98 條、analogies 11
  個都和頁面一致；`[待補來源]` 為 0，和 index
  一致；跨頁數字抽查（11.8%、626M、70/68/12/4、5.7/3.7/2.9/1.9、75.8/53.8/56.1/8
  8.3、0.95/0.78/0.70、0.40–0.54、73.5、281 分鐘、69%–78%）都一致。

  ## 實際讀取的檔案
  - /Users/ting/rag-wiki/wiki/index.md
  - /Users/ting/rag-wiki/wiki/log.md
  - /Users/ting/rag-wiki/wiki/overview.md
  - /Users/ting/rag-wiki/wiki/glossary.md
  - /Users/ting/rag-wiki/wiki/analogies.md
  - /Users/ting/rag-wiki/wiki/sources/01-lewis2020-rag.md
  - /Users/ting/rag-wiki/wiki/sources/02-gao2023-survey.md
  - /Users/ting/rag-wiki/wiki/sources/03-anthropic-contextual-retrieval.md
  - /Users/ting/rag-wiki/wiki/sources/04-liu2023-lost-in-middle.md
  - /Users/ting/rag-wiki/wiki/sources/05-asai2023-self-rag.md
  - /Users/ting/rag-wiki/wiki/sources/06-edge2024-graphrag.md
  - /Users/ting/rag-wiki/wiki/sources/07-es2023-ragas.md
  - /Users/ting/rag-wiki/wiki/concepts/chunking.md
  - /Users/ting/rag-wiki/wiki/concepts/context-window.md
  - /Users/ting/rag-wiki/wiki/concepts/embedding.md
  - /Users/ting/rag-wiki/wiki/concepts/generator.md
  - /Users/ting/rag-wiki/wiki/concepts/hallucination.md
  - /Users/ting/rag-wiki/wiki/concepts/lost-in-the-middle.md
  - /Users/ting/rag-wiki/wiki/concepts/parametric-vs-non-parametric-memory.md
  - /Users/ting/rag-wiki/wiki/concepts/query-optimization.md
  - /Users/ting/rag-wiki/wiki/concepts/rag-evaluation.md
  - /Users/ting/rag-wiki/wiki/concepts/ragas.md
  - /Users/ting/rag-wiki/wiki/concepts/reranking.md
  - /Users/ting/rag-wiki/wiki/concepts/retriever.md
  - /Users/ting/rag-wiki/wiki/methods/advanced-rag.md
  - /Users/ting/rag-wiki/wiki/methods/contextual-retrieval.md
  - /Users/ting/rag-wiki/wiki/methods/graphrag.md
  - /Users/ting/rag-wiki/wiki/methods/modular-rag.md
  - /Users/ting/rag-wiki/wiki/methods/naive-rag.md
  - /Users/ting/rag-wiki/wiki/methods/original-rag.md
  - /Users/ting/rag-wiki/wiki/methods/self-rag.md
  - /Users/ting/rag-wiki/wiki/comparisons/closed-book-vs-open-book.md
  - /Users/ting/rag-wiki/wiki/comparisons/rag-paradigms.md
  - /Users/ting/rag-wiki/wiki/comparisons/rag-techniques.md
  - /Users/ting/rag-wiki/wiki/comparisons/rag-timeline.md
  - /Users/ting/rag-wiki/wiki/comparisons/rag-vs-fine-tuning.md

⏺ Reviewer 讀的檔案都在清單內，這一輪有效。確認嚴重問題：

  Ran 1 shell command (ctrl+o to expand)

⏺ Agent "Wiki semantic lint round 3" finished · 2m 46s

⏺ 確認したところ、wiki 自身の Table 2 では ChatGPT が TriviaQA と ARC-C で
  Self-RAG 13B を上回っているのに、self-rag.md
  の該当箇所にはその条件が書かれていないことが分かりました。そのため第 3
  輪の判定は未通過としています。 · summary

  Ran 1 shell command (ctrl+o to expand)

⏺ ⓪ 第 3 輪還是沒過，我又停下來了，還沒開始做 ① 檢索。⓪ 已累計退回 3
  次，到上限了：下一輪只要再有 1 個嚴重問題，就會觸發停止程序，整個 workflow
  會中止。

  這一輪 tools/lint.py 是 0 error、0 warning；reviewer 找到 1 個嚴重問題、21
  個輕微問題，嚴重的那個我看過原文，確認是對的。

  嚴重問題

  self-rag.md:51 寫「在六個任務上，勝過參數更多的 LLM，以及傳統的 RAG 方法」。但
  05 來源頁 的 Table 2 顯示：
  - ChatGPT 在 TriviaQA（74.3 vs 69.3）和 ARC-C（75.3 vs 73.1）上都高於 Self-RAG
    13B。
  - 同一頁只寫 Self-RAG「是非商用模型中最好的」，以及「在
    PubHealth、PopQA、傳記、ASQA 上勝過 ChatGPT」。

  要注意的地方

  1. 同一個問題，嚴重度變了。 這一條在第 1、2
     輪都被列為「輕微」，所以我沒有建議你修；這一輪卻變成「嚴重」。reviewer
     每輪都重讀 36 頁，輕微清單裡的「拿掉限定條件」「沒有跟著更新」這類問題，都
     可能在下一輪變成嚴重。
  2. 只修嚴重的那條，不夠保險。 這次最好把同類的輕微問題一起修掉：
     - #3：GraphRAG 的 72%–83% 原文是「GraphRAG
       等全局方法」的結果，而且分資料集。現在
       overview.md、graphrag.md、rag-techniques.md 三頁都把它全算在 GraphRAG
       身上。
     - #4：naive-rag.md:65 的「直接串接」，沒有跟著上次 generator
       頁的修正一起改。
     - #8：reranking 和「文件數量」的 ⚠️ 沒有同步到
       retriever.md、advanced-rag.md、01／02 來源頁。這一條三輪都被提到。
     - #9、#10：04 來源頁 的爭議沒有用 ⚠️ 格式；contextual-retrieval.md
       沒有標「摘要 indexing」的 ⚠️。
  3. self-rag 那條最好回去看 raw。 05 §6 p.10 的原文可能真的這樣寫。依
     AGENTS.md，修 wiki 時可以讀 raw 核對：如果原文就這樣寫，就照 §8 加
     ⚠️，標成「原文結論和 Table 2 不一致」；如果不是，就直接改成有限定的說法。

  完整清單在 output/what-is-rag/lint.md。

  請你決定

  - A（建議）：我修嚴重的那條，加上 #3、#4、#8、#9、#10；self-rag 那條會回去讀
    05 §6 核對。修好後你再執行 /topic-slides，跑最後一次 ⓪。
  - B：只修嚴重的那條，不過下一輪被判退回的風險比較高。
  - C：如果你覺得 ⓪ 太嚴，可以先調整 workflow 的規則，例如只看和主題有關的頁面，
    或者讓同一個問題的嚴重度不能每輪變來變去。這要改 workflow
    定義檔，需要你決定。