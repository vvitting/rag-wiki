---
type: glossary
title: "術語表"
tags: [glossary]
sources: [01-lewis2020-rag.pdf, 02-gao2023-survey.pdf]
updated: 2026-11-22
---

# 術語表

> 依英文字母排序。格式：`- **Term**：一句白話解釋 [raw 檔名, 位置] → [詳見](concepts/xxx.md)`

- **Adaptive retrieval**：讓 LLM 自己決定什麼時候需要檢索、什麼時候停止 [02-gao2023-survey.pdf, §V-C, p.11] → [詳見](methods/modular-rag.md)
- **Advanced RAG**：在 Naive RAG 的前後加上 pre-retrieval 和 post-retrieval 優化 [02-gao2023-survey.pdf, §II-B, p.3] → [詳見](methods/advanced-rag.md)
- **Answer faithfulness**：答案是否忠於檢索到的 context，沒有互相矛盾 [02-gao2023-survey.pdf, §VI-C, p.12] → [詳見](concepts/rag-evaluation.md)
- **Answer relevance**：答案是否直接回答了問題 [02-gao2023-survey.pdf, §VI-C, p.12] → [詳見](concepts/rag-evaluation.md)
- **BART**：原始 RAG 用來寫答案的預訓練 seq2seq 模型，BART-large 有 400M 參數 [01-lewis2020-rag.pdf, §2.3, p.3] → [詳見](concepts/generator.md)
- **Bi-encoder**：用兩個 encoder 分別把「問題」和「文件」轉成向量，再比對兩者；DPR 就是這種架構 [01-lewis2020-rag.pdf, §2.2, p.3] → [詳見](concepts/retriever.md)
- **BM25**：靠字詞重疊來找文件的傳統檢索方法，屬於 sparse encoder [01-lewis2020-rag.pdf, §4.5, p.7; 02-gao2023-survey.pdf, §III-D, p.9] → [詳見](concepts/retriever.md)
- **Chunk**：把長文件切成的小段落；常見大小是 100、256、512 個 token [02-gao2023-survey.pdf, §III-B, p.8] → [詳見](concepts/chunking.md)
- **Closed-book**：不查資料、只靠模型自己記住的知識回答 [01-lewis2020-rag.pdf, §3.1, p.4; §4.1, p.5] → [詳見](comparisons/closed-book-vs-open-book.md)
- **Context relevance**：檢索到的 context 是否精確、切題 [02-gao2023-survey.pdf, §VI-C, p.12] → [詳見](concepts/rag-evaluation.md)
- **Context window**：LLM 一次能處理的文字量；當時的 LLM 已能處理超過 200,000 tokens [02-gao2023-survey.pdf, §VII-A, p.14]。正式定義 [待補來源] → [詳見](concepts/context-window.md)
- **Cosine similarity**：計算兩個 embedding 有多相似的一種方式 [02-gao2023-survey.pdf, §III-D, p.9] → [詳見](concepts/embedding.md)
- **Counterfactual robustness**：能否辨認並忽略文件中已知的錯誤 [02-gao2023-survey.pdf, §VI-C, p.12] → [詳見](concepts/rag-evaluation.md)
- **Dense retriever**：用預訓練模型（例如 BERT）把文字轉成 dense vector 來檢索 [02-gao2023-survey.pdf, §III-D, p.9] → [詳見](concepts/retriever.md)
- **DPR（Dense Passage Retriever）**：原始 RAG 使用的 retriever，以 BERT-base 為基礎 [01-lewis2020-rag.pdf, §1, p.2; §2.2, p.3] → [詳見](concepts/retriever.md)
- **Embedding**：把一段文字轉成的一串數字（dense representation）[01-lewis2020-rag.pdf, §2.2, p.3] → [詳見](concepts/embedding.md)
- **Exact Match（EM）**：模型答案和標準答案「完全一樣」才算對的評分方式；問答任務常用 [01-lewis2020-rag.pdf, §3.1, p.4; 02-gao2023-survey.pdf, §VI-B, p.12]。（「完全一樣」是依名稱的白話說明，原文沒有給出定義 [待補來源]）
- **Extractive QA**：從檢索到的文件中「挑出」一段文字當答案 [01-lewis2020-rag.pdf, §3.1, p.4] → [詳見](concepts/generator.md)
- **FAISS**：用來建立向量 index、快速找出相似向量的工具 [01-lewis2020-rag.pdf, §3, p.4] → [詳見](concepts/embedding.md)
- **Fine-tuning（FT）**：用額外的資料再訓練模型，像學生花時間把知識內化 [02-gao2023-survey.pdf, §II-D, p.5] → [詳見](comparisons/rag-vs-fine-tuning.md)
- **Generator**：讀完問題和檢索到的文件後寫出答案的模型 [01-lewis2020-rag.pdf, §2, p.2–3] → [詳見](concepts/generator.md)
- **Hallucination**：模型講出聽起來像真的、但其實是錯的內容，或檢索內容沒有支持的說法 [01-lewis2020-rag.pdf, §1, p.1; 02-gao2023-survey.pdf, §II-A, p.3] → [詳見](concepts/hallucination.md)
- **Hybrid retrieval**：結合 sparse（關鍵字）和 dense（語意）檢索，讓兩者互補 [02-gao2023-survey.pdf, §III-D, p.9] → [詳見](concepts/retriever.md)
- **HyDE**：先讓 LLM 寫一份假設的答案，再用它去找相似的真實文件 [02-gao2023-survey.pdf, §III-C, p.9] → [詳見](concepts/query-optimization.md)
- **In-context learning（ICL）**：ChatGPT 之後 LLM 展現的能力，讓 RAG 研究轉向在推論階段提供資訊 [02-gao2023-survey.pdf, §I, p.1]。白話定義 [待補來源] → [詳見](comparisons/rag-timeline.md)
- **Index（document index）**：所有文件 embedding 的集合，也就是 RAG 的 non-parametric memory [01-lewis2020-rag.pdf, §2.2, p.3] → [詳見](concepts/embedding.md)
- **Information integration**：能否整合多份文件的資訊，回答複雜的問題 [02-gao2023-survey.pdf, §VI-C, p.12] → [詳見](concepts/rag-evaluation.md)
- **Iterative retrieval**：依照原始問題和目前已生成的內容，反覆搜尋知識庫 [02-gao2023-survey.pdf, §V-A, p.10] → [詳見](methods/modular-rag.md)
- **Knowledge graph（KG）**：用節點和關係表示知識的結構化資料，通常經過驗證、資訊較精確 [02-gao2023-survey.pdf, §III-A, p.7] → [詳見](concepts/retriever.md)
- **Knowledge-intensive task**：人類沒有外部知識來源就不太可能完成的任務 [01-lewis2020-rag.pdf, §1, p.2] → [詳見](sources/01-lewis2020-rag.md)
- **Language model / LLM**：從資料中學到大量知識，並存在參數裡的預訓練模型；LLM 能力很強，但有 hallucination、知識過時等問題 [01-lewis2020-rag.pdf, §1, p.1; 02-gao2023-survey.pdf, Abstract, p.1]。給完全新手的白話定義 [待補來源] → [詳見](concepts/parametric-vs-non-parametric-memory.md)
- **Lost in the middle**：LLM 讀長文時傾向只注意開頭和結尾、忽略中間的現象 [02-gao2023-survey.pdf, §IV-A, p.10] → [詳見](concepts/context-window.md)
- **Metadata**：附在 chunk 上的額外資訊，例如頁碼、檔名、作者、時間戳，可以用來過濾檢索結果 [02-gao2023-survey.pdf, §III-B, p.8] → [詳見](concepts/chunking.md)
- **MIPS（Maximum Inner Product Search）**：在 index 中找出和問題向量內積最大的 k 份文件 [01-lewis2020-rag.pdf, §2.2, p.3] → [詳見](concepts/retriever.md)
- **Modular RAG**：把 RAG 拆成可以新增、替換、重排的模組，流程不再固定 [02-gao2023-survey.pdf, §II-C, p.4–5] → [詳見](methods/modular-rag.md)
- **Naive RAG**：最基本的「indexing → retrieval → generation」流程，也叫 Retrieve-Read [02-gao2023-survey.pdf, §II-A, p.3] → [詳見](methods/naive-rag.md)
- **Negative rejection**：檢索到的文件沒有答案時，能否拒絕回答 [02-gao2023-survey.pdf, §VI-C, p.12] → [詳見](concepts/rag-evaluation.md)
- **Noise robustness**：遇到相關但沒有實質資訊的文件時，能否不被干擾 [02-gao2023-survey.pdf, §VI-C, p.12] → [詳見](concepts/rag-evaluation.md)
- **Non-parametric memory**：存在模型外部、可以查閱和替換的知識，例如 Wikipedia index [01-lewis2020-rag.pdf, §2.2, p.3] → [詳見](concepts/parametric-vs-non-parametric-memory.md)
- **Open-book**：回答前先去檢索外部資料 [01-lewis2020-rag.pdf, §4.1, p.5] → [詳見](comparisons/closed-book-vs-open-book.md)
- **Open-domain QA**：可以問任何主題的問答任務，是測試 knowledge-intensive 任務的常用基準 [01-lewis2020-rag.pdf, §3.1, p.4] → [詳見](sources/01-lewis2020-rag.md)
- **Parametric memory**：存在模型參數裡、模型自己「背起來」的知識 [01-lewis2020-rag.pdf, §2.3, p.3] → [詳見](concepts/parametric-vs-non-parametric-memory.md)
- **Prompt**：交給 LLM 的輸入；Naive RAG 把問題和檢索到的文件組成 prompt [02-gao2023-survey.pdf, §II-A, p.3]。白話定義 [待補來源] → [詳見](methods/naive-rag.md)
- **Prompt engineering**：不改模型、只靠設計輸入來發揮模型本身能力的方法 [02-gao2023-survey.pdf, §II-D, p.5] → [詳見](comparisons/rag-vs-fine-tuning.md)
- **Proposition**：一段只包含一個事實、意思自足的簡潔敘述，可以當作檢索單位 [02-gao2023-survey.pdf, §III-A, p.8] → [詳見](concepts/chunking.md)
- **Query rewriting**：檢索前先讓 LLM 改寫使用者的問題 [02-gao2023-survey.pdf, §III-C, p.9] → [詳見](concepts/query-optimization.md)
- **RAG（Retrieval-Augmented Generation）**：結合 parametric 與 non-parametric memory 來生成文字的模型 [01-lewis2020-rag.pdf, Abstract, p.1] → [詳見](methods/original-rag.md)
- **RAG-Sequence**：整個答案都根據同一份檢索文件的 RAG 版本 [01-lewis2020-rag.pdf, §2.1, p.3] → [詳見](methods/original-rag.md)
- **RAG-Token**：每個 token 都可以根據不同檢索文件的 RAG 版本 [01-lewis2020-rag.pdf, §2.1, p.3] → [詳見](methods/original-rag.md)
- **RAGAS**：用 LLM 自動評估 context relevance、faithfulness、answer relevance 的工具 [02-gao2023-survey.pdf, §VI-D, p.14; Table IV, p.15] → [詳見](concepts/rag-evaluation.md)
- **Recursive retrieval**：依照前一次的搜尋結果逐步修正查詢，把問題拆成子問題 [02-gao2023-survey.pdf, §V-B, p.11] → [詳見](methods/modular-rag.md)
- **Reranking**：把檢索到的文件重新排序，讓最相關的排在前面 [02-gao2023-survey.pdf, §IV-A, p.10] → [詳見](concepts/reranking.md)
- **Retrieval collapse**：retriever 不管輸入是什麼都找同一批文件，generator 也就開始忽略文件 [01-lewis2020-rag.pdf, App. H, p.19] → [詳見](concepts/retriever.md)
- **Retriever**：根據問題找出相關文件的模型 [01-lewis2020-rag.pdf, §2, p.2] → [詳見](concepts/retriever.md)
- **Seq2seq**：讀入一段文字、輸出另一段文字的模型，原始 RAG 稱它為「NLP 的主力」[01-lewis2020-rag.pdf, §1, p.2] → [詳見](concepts/generator.md)
- **Sparse retrieval**：以關鍵字或字詞權重為基礎的檢索，例如 BM25 [02-gao2023-survey.pdf, §III-D, p.9] → [詳見](concepts/retriever.md)
- **Token**：模型逐一產生的文字單位；原始 RAG 以 token 為單位生成答案 [01-lewis2020-rag.pdf, §2, p.2–3]。對 token 的白話定義 [待補來源] → [詳見](concepts/generator.md)
- **Top-k**：檢索時取出最相關的前 k 份文件 [01-lewis2020-rag.pdf, §3, p.4; 02-gao2023-survey.pdf, §II-A, p.3] → [詳見](concepts/retriever.md)
- **Vector database**：存放 chunk 向量、支援相似度搜尋的資料庫 [02-gao2023-survey.pdf, §II-A, p.3] → [詳見](concepts/embedding.md)

## 相關頁面
- [目錄](index.md)
- [RAG 總覽](overview.md)
