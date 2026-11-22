---
page: wiki/comparisons/rag-paradigms.md
---
# 證據卡：三種 RAG 典範比較

## 重點摘錄
> 綜述把 RAG 研究分成三個階段：Naive RAG、Advanced RAG、Modular RAG [02-gao2023-survey.pdf, §II, p.2; Fig.3, p.4]。後兩者都是為了改善 Naive RAG 的特定缺點而發展出來的 [02-gao2023-survey.pdf, §II, p.2]。
> - 三者是逐步改進的關係，不是互相取代：Modular RAG 仍然建立在 Advanced 和 Naive RAG 的基本原理上 [02-gao2023-survey.pdf, §II-C, p.4]。

## ⚠️ 爭議
> > ⚠️ **爭議／更新**：綜述說 Naive RAG 是「最早的方法」[02-gao2023-survey.pdf, §II-A, p.2]，但 retrieval-augmented generation 這個名稱和「先檢索、再生成」的架構，2020 年就由 [01-lewis2020-rag.pdf, §1, p.2] 提出 [02-gao2023-survey.pdf, Ref. 4, p.17]。所以這三個「階段」是綜述的分類方式，不完全等於時間先後。詳見 [Naive RAG](../methods/naive-rag.md)、[原始 RAG](../methods/original-rag.md)。

## 可以用在
- 進階變體（10）：Naive → Advanced → Modular，及「階段」不等於時間先後的 ⚠️
