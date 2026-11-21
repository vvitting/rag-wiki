# RAG Wiki 目錄

> 每次查詢先讀這裡。格式：`- [標題](路徑) — 一行摘要（sources: N, updated: YYYY-MM-DD）`
> 規範見 [AGENTS.md](../AGENTS.md)；工作紀錄見 [log.md](log.md)。

## 總覽
- [RAG 總覽](overview.md) — RAG 全貌，結構對齊簡報；第 1–6 節都已有內容（sources: 2, updated: 2026-11-22）

## 來源
- [01 Lewis et al. 2020 — Retrieval-Augmented Generation](sources/01-lewis2020-rag.md) — 提出並命名 RAG 的原始論文：DPR + BART、RAG-Sequence 與 RAG-Token（sources: 2, updated: 2026-11-22）
- [02 Gao et al. 2023 — RAG for LLMs: A Survey](sources/02-gao2023-survey.md) — 綜述：Naive／Advanced／Modular 三典範、檢索與生成技術、評估、未來挑戰（sources: 2, updated: 2026-11-22）

## 概念
- [Parametric 與 non-parametric memory](concepts/parametric-vs-non-parametric-memory.md) — 模型「背的」知識 vs 可以「翻」的外部知識；index hot-swapping（sources: 2, updated: 2026-11-22）
- [Retriever](concepts/retriever.md) — 負責找資料：DPR、MIPS、top-k、sparse／dense／hybrid、檢索來源（sources: 2, updated: 2026-11-22）
- [Generator](concepts/generator.md) — 負責寫答案：BART → LLM、extractive vs generative、LLM fine-tuning（sources: 2, updated: 2026-11-22）
- [Embedding 與 vector index](concepts/embedding.md) — 把文字轉成向量並建成 index；相似度、選 embedding model、成本（sources: 2, updated: 2026-11-22）
- [Chunking](concepts/chunking.md) — 把文件切成小段；chunk 大小的取捨、Small2Big、proposition、metadata（sources: 2, updated: 2026-11-22）
- [Hallucination](concepts/hallucination.md) — 模型講錯卻像真的；兩種類型；RAG 能減少，但不能消除（sources: 2, updated: 2026-11-22）
- [Reranking](concepts/reranking.md) — 檢索後重新排序；⚠️ 01 和 02 對它是否必要看法不同（sources: 2, updated: 2026-11-22）
- [Query 優化](concepts/query-optimization.md) — 檢索前修整問題：expansion、rewrite、HyDE、step-back、routing（sources: 1, updated: 2026-11-22）
- [Context window 與「放多少文件」](concepts/context-window.md) — ⚠️ 文件越多越好嗎？lost in the middle、RAG vs long context（sources: 2, updated: 2026-11-22）
- [RAG 評估](concepts/rag-evaluation.md) — retrieval／generation quality、三個品質分數、四種能力、benchmark 與工具（sources: 2, updated: 2026-11-22）

## 方法
- [原始 RAG（RAG-Sequence 與 RAG-Token）](methods/original-rag.md) — Lewis 2020 的架構、步驟、兩種版本與限制（sources: 2, updated: 2026-11-22）
- [Naive RAG](methods/naive-rag.md) — indexing → retrieval → generation；缺點；⚠️ 和原始 RAG 的關係（sources: 2, updated: 2026-11-22）
- [Advanced RAG](methods/advanced-rag.md) — pre-retrieval 與 post-retrieval 優化（sources: 1, updated: 2026-11-22）
- [Modular RAG](methods/modular-rag.md) — 可組合的模組與模式；iterative／recursive／adaptive 檢索（sources: 1, updated: 2026-11-22）

## 比較與綜合
- [Closed-book vs open-book](comparisons/closed-book-vs-open-book.md) — 只靠記憶 vs 可以查資料，附 NQ 成績與參數量（sources: 1, updated: 2026-11-22）
- [三種 RAG 典範比較](comparisons/rag-paradigms.md) — Naive vs Advanced vs Modular 對照表（sources: 1, updated: 2026-11-22）
- [RAG vs fine-tuning vs prompt engineering](comparisons/rag-vs-fine-tuning.md) — 什麼時候用哪一個；兩者可以互補（sources: 1, updated: 2026-11-22）
- [RAG 演進時間軸](comparisons/rag-timeline.md) — 從 2020 年的原始 RAG 到 LLM 時代（sources: 2, updated: 2026-11-22）

## 問答

## 工具頁
- [術語表](glossary.md) — 59 個專有名詞的一句話白話解釋（sources: 2, updated: 2026-11-22）
- [比喻集](analogies.md) — 閉書考 vs 開書考、圖書館員＋作家、換新版課本、帶教科書 vs 內化、讀長文只記頭尾（sources: 2, updated: 2026-11-22）

## 待建頁面
- Contextual Retrieval（methods）— 預計 ingest 03
- Self-RAG（methods）— 02 已簡介 [02-gao2023-survey.pdf, §V-C, p.12]，預計 ingest 05 建立完整頁面
- GraphRAG（methods）— 02 提到 knowledge graph index [02-gao2023-survey.pdf, §III-B, p.8]，預計 ingest 06
- Robustness（concepts）— 02 §VII-B 提到雜訊和反事實資訊的影響；目前散落在 context-window、rag-evaluation 兩頁，之後資料更多時再考慮獨立成頁

## 待補來源
- [concepts/embedding.md](concepts/embedding.md) — 為什麼「意思相近的文字，向量也相近」的直覺說明
- [concepts/context-window.md](concepts/context-window.md) — context window 的正式定義
- [glossary.md](glossary.md) — LLM、Token、Prompt、In-context learning 的白話定義；Exact Match 的正式定義

## Ingest 進度
- [x] 01-lewis2020-rag.pdf
- [x] 02-gao2023-survey.pdf
- [ ] 03-anthropic-contextual-retrieval.pdf
- [ ] 04-liu2023-lost-in-middle.pdf
- [ ] 05-asai2023-self-rag.pdf
- [ ] 06-edge2024-graphrag.pdf
- [ ] 07-es2023-ragas.pdf
