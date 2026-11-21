---
type: comparison
title: "Closed-book vs open-book：只靠記憶 vs 可以查資料"
tags: [comparison, closed-book, open-book, open-domain-qa]
sources: [01-lewis2020-rag.pdf]
updated: 2026-11-22
---

# Closed-book vs open-book

原始 RAG 論文用「closed-book」形容只靠參數記憶的方法，用「open-book」形容會去檢索資料的方法 [01-lewis2020-rag.pdf, §4.1, p.5]。

## 兩類方法的差別

| | Closed-book | Open-book |
|---|---|---|
| 知識從哪來 | 只靠 [parametric memory](../concepts/parametric-vs-non-parametric-memory.md) [01-lewis2020-rag.pdf, §3.1, p.4] | 另外從外部文件檢索 [01-lewis2020-rag.pdf, §3.1, p.4] |
| 代表模型 | T5、T5+SSM [01-lewis2020-rag.pdf, Table 1, p.6] | REALM、DPR、RAG [01-lewis2020-rag.pdf, Table 1, p.6] |
| 怎麼更新知識 | 要再訓練 [01-lewis2020-rag.pdf, §4.5, p.7] | 換掉 index 就好（RAG）[01-lewis2020-rag.pdf, §4.5, p.8] |

RAG 結合了兩邊的優點：closed-book 能自由生成文字，open-book 有檢索帶來的表現 [01-lewis2020-rag.pdf, §4.1, p.5]。

## Open-domain QA 成績（NQ，Exact Match）

| 模型 | 類型 | 可訓練參數 | NQ EM | 出處 |
|---|---|---|---|---|
| T5-large | closed-book | 770M | 28.9 | [01-lewis2020-rag.pdf, App. G, p.19] |
| T5-11B | closed-book | 11B | 34.5 | [01-lewis2020-rag.pdf, Table 1, p.6; App. G, p.19] |
| T5-11B+SSM | closed-book | – | 36.6 | [01-lewis2020-rag.pdf, Table 1, p.6] |
| REALM | open-book | – | 40.4 | [01-lewis2020-rag.pdf, Table 1, p.6] |
| DPR | open-book | – | 41.5 | [01-lewis2020-rag.pdf, Table 1, p.6] |
| RAG-Sequence | open-book | 626M | 44.5 | [01-lewis2020-rag.pdf, Table 1, p.6; App. G, p.18–19] |

表中的「–」代表原文沒有列出該模型的參數量 [01-lewis2020-rag.pdf, App. G, p.18–19]。

## 重點

- 參數少很多的 open-book 模型，可以勝過參數多很多的 closed-book 模型；作者據此認為，結合兩種記憶的模型只需要少得多的可訓練參數 [01-lewis2020-rag.pdf, App. G, p.19]。

## 相關頁面

- [Parametric 與 non-parametric memory](../concepts/parametric-vs-non-parametric-memory.md)
- [原始 RAG（方法）](../methods/original-rag.md)
- [比喻集：開書考 vs 閉書考](../analogies.md)
