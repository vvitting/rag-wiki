---
type: comparison
title: "Closed-book vs open-book：只靠記憶 vs 可以查資料"
tags: [comparison, closed-book, open-book, open-domain-qa]
sources: [01-lewis2020-rag.pdf, 04-liu2023-lost-in-middle.pdf, 05-asai2023-self-rag.pdf]
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

## 但 open-book 不一定比較好：文件的位置很重要

04 在 LLM 上比較了三種設定：不給文件（closed-book）、給 20 份文件（含 1 份答案）、只給那 1 份答案文件（oracle）[04-liu2023-lost-in-middle.pdf, §2.3, p.5]。

| GPT-3.5-Turbo 的設定 | 準確率 | 出處 |
|---|---|---|
| Closed-book（不給文件） | 56.1% | [04-liu2023-lost-in-middle.pdf, Table 1, p.5] |
| Oracle（只給答案文件） | 88.3% | [04-liu2023-lost-in-middle.pdf, Table 1, p.5] |
| 20 份文件，答案在第 1 份 | 75.8% | [04-liu2023-lost-in-middle.pdf, Table 6, p.18] |
| 20 份文件，答案在第 10 份 | 53.8% | [04-liu2023-lost-in-middle.pdf, Table 6, p.18] |

- 在 20 和 30 份文件的設定中，答案放在最差的位置時（例如 20 份中的第 10 份，見上表），open-book 的表現反而**低於** closed-book [04-liu2023-lost-in-middle.pdf, §2.3, p.5]。
- 所以開書考要考得好，不只要「帶對書」，還要「把重點翻到前面」。詳見 [Lost in the middle](../concepts/lost-in-the-middle.md) [04-liu2023-lost-in-middle.pdf, §5, p.10]。

### 第二份證據：05 的 Table 2

Self-RAG 論文也觀察到，加上檢索後，部分任務的表現反而下降 [05-asai2023-self-rag.pdf, §5.1, p.8]：

| 模型 | 任務 | 不檢索 | 加上檢索 | 出處 |
|---|---|---|---|---|
| ChatGPT | TriviaQA | 74.3 | 65.7 | [05-asai2023-self-rag.pdf, Table 2, p.8] |
| ChatGPT | PubHealth | 70.1 | 54.7 | [05-asai2023-self-rag.pdf, Table 2, p.8] |
| Llama2-13B | ARC-Challenge | 29.4 | 26.0 | [05-asai2023-self-rag.pdf, Table 2, p.8] |
| ChatGPT | PopQA（冷門知識） | 29.3 | 50.8 | [05-asai2023-self-rag.pdf, Table 2, p.8] |

- PopQA 是冷門實體的問題（維基百科月瀏覽量少於 100）[05-asai2023-self-rag.pdf, §4.1, p.7]，加上檢索後大幅進步 [05-asai2023-self-rag.pdf, Table 2, p.8]。
- 作者的解釋是：對於不能直接從文件「複製或擷取片段」來回答的任務（例如 PubHealth、ARC-Challenge），這些加上檢索的基準模型幫助有限 [05-asai2023-self-rag.pdf, §5.1, p.8]。
- ChatGPT 在 TriviaQA 上的退步，作者沒有特別解釋 [05-asai2023-self-rag.pdf, §5.1, p.8]。
- Self-RAG 的解法是讓模型自己判斷要不要查，詳見 [Self-RAG](../methods/self-rag.md) [05-asai2023-self-rag.pdf, §1, p.1]。

## 相關頁面

- [Parametric 與 non-parametric memory](../concepts/parametric-vs-non-parametric-memory.md)
- [原始 RAG（方法）](../methods/original-rag.md)
- [Lost in the middle](../concepts/lost-in-the-middle.md)
- [比喻集：開書考 vs 閉書考](../analogies.md)
- [術語表](../glossary.md)
