---
type: concept
title: "RAG 評估"
tags: [concept, evaluation, metrics, benchmark]
sources: [02-gao2023-survey.pdf, 01-lewis2020-rag.pdf]
updated: 2026-11-22
---

# RAG 評估

## 白話說明

評估 RAG 要分開看兩件事：「找得好不好」（retrieval quality）和「寫得好不好」（generation quality）[02-gao2023-survey.pdf, §VI-B, p.12]。

## 為什麼重要

- 過去評估 RAG，多半只看它在特定任務上的表現，專門評估 RAG 特性的研究很少 [02-gao2023-survey.pdf, §VI-B, p.12]。
- 評估檢索品質，是判斷 retriever 找來的 context 是否有效的關鍵 [02-gao2023-survey.pdf, §VI-B, p.12]。

## 運作方式

### 兩個評估目標

| 目標 | 看什麼 | 常用指標 | 出處 |
|---|---|---|---|
| Retrieval quality | retriever 找來的 context 有沒有用 | Hit Rate、MRR、NDCG | [02-gao2023-survey.pdf, §VI-B, p.12] |
| Generation quality | generator 能不能根據 context 寫出連貫、相關的答案 | 沒有標準答案時看 faithfulness、relevance、是否有害；有標準答案時看準確度 | [02-gao2023-survey.pdf, §VI-B, p.12] |

### 三個品質分數（quality scores）

- **Context relevance**：檢索到的 context 是否精確、切題 [02-gao2023-survey.pdf, §VI-C, p.12]。
- **Answer faithfulness**：答案是否忠於檢索到的 context，沒有互相矛盾 [02-gao2023-survey.pdf, §VI-C, p.12]。
- **Answer relevance**：答案是否直接回答了問題 [02-gao2023-survey.pdf, §VI-C, p.12]。

### 四種能力（required abilities）

- **Noise robustness**：遇到和問題有關、但沒有實質資訊的文件時，能不能不被干擾 [02-gao2023-survey.pdf, §VI-C, p.12]。
- **Negative rejection**：檢索到的文件沒有答案時，能不能拒絕回答 [02-gao2023-survey.pdf, §VI-C, p.12]。
- **Information integration**：能不能整合多份文件的資訊，回答複雜的問題 [02-gao2023-survey.pdf, §VI-C, p.12]。
- **Counterfactual robustness**：能不能辨認並忽略文件中已知的錯誤 [02-gao2023-survey.pdf, §VI-C, p.12]。

Context relevance 和 noise robustness 用來評估檢索；其餘五項用來評估生成 [02-gao2023-survey.pdf, §VI-C, p.12]。

### 傳統的任務指標

- 問答常用 EM 和 F1，事實查核常用 Accuracy，答案品質也常用 BLEU 和 ROUGE [02-gao2023-survey.pdf, §VI-B, p.12]。
- 原始 RAG 就是用 Exact Match、BLEU、ROUGE-L、Label Accuracy，再加上人工評估 [01-lewis2020-rag.pdf, §3, p.4–5]。

### Benchmark 與工具

| 名稱 | 類型 | 評估面向 | 出處 |
|---|---|---|---|
| RGB | benchmark | noise robustness、negative rejection、information integration、counterfactual robustness | [02-gao2023-survey.pdf, Table IV, p.15] |
| RECALL | benchmark | counterfactual robustness | [02-gao2023-survey.pdf, Table IV, p.15] |
| CRUD | benchmark | 創意生成、知識問答、錯誤修正、摘要 | [02-gao2023-survey.pdf, Table IV, p.15] |
| RAGAS | 工具 | context relevance、faithfulness、answer relevance | [02-gao2023-survey.pdf, Table IV, p.15] |
| ARES | 工具 | context relevance、faithfulness、answer relevance | [02-gao2023-survey.pdf, Table IV, p.15] |
| TruLens | 工具 | context relevance、faithfulness、answer relevance | [02-gao2023-survey.pdf, Table IV, p.15] |

- RAGAS、ARES、TruLens 這類自動化工具，是用 LLM 來評判品質分數 [02-gao2023-survey.pdf, §VI-D, p.14]。RAGAS 的原始論文會在 ingest 07 時補充。

## 各論文怎麼說

- **[02-gao2023-survey.pdf](../sources/02-gao2023-survey.md)**：作者坦承，這些指標都是從相關研究借來的傳統指標，還不是成熟或標準化的 RAG 評估方式 [02-gao2023-survey.pdf, §VI-C, p.14]。
- **[01-lewis2020-rag.pdf](../sources/01-lewis2020-rag.md)**：用人工評估比較事實性（factuality）和具體性（specificity）[01-lewis2020-rag.pdf, §3.3, p.5]。

## 相關頁面

- [Hallucination](hallucination.md)
- [Retriever](retriever.md)
- [Generator](generator.md)
- [術語表](../glossary.md)
