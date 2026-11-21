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
