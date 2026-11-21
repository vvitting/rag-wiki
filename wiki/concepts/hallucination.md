---
type: concept
title: "Hallucination（幻覺）"
tags: [concept, hallucination, factuality]
sources: [01-lewis2020-rag.pdf, 02-gao2023-survey.pdf, 04-liu2023-lost-in-middle.pdf, 05-asai2023-self-rag.pdf, 07-es2023-ragas.pdf, 06-edge2024-graphrag.pdf]
updated: 2026-11-22
---

# Hallucination

## 白話說明

Hallucination 指模型講出聽起來很像真的、但其實是錯的內容。原始 RAG 論文把它列為純參數模型的缺點之一 [01-lewis2020-rag.pdf, §1, p.1]。

## 為什麼重要

- 這正是 RAG 想解決的問題之一：作者認為，RAG 的生成更紮根在真實的知識上（這裡指 Wikipedia），所以比較少「hallucinate」[01-lewis2020-rag.pdf, Broader Impact, p.10]。
- LLM 在處理超出訓練資料範圍、或需要最新資訊的問題時，特別容易產生 hallucination [02-gao2023-survey.pdf, §I, p.1]。
- 透過參考外部知識，RAG 能有效減少產生錯誤內容的問題 [02-gao2023-survey.pdf, §I, p.1]。

> ⚠️ **爭議／更新**：[02-gao2023-survey.pdf, §I, p.1] 認為 RAG 能有效減少錯誤內容；但檢索不一定有幫助：[04-liu2023-lost-in-middle.pdf, Table 6, p.18; Table 1, p.5] 發現 GPT-3.5-Turbo 在 20 份文件、答案位於中間時，準確率是 53.8%，低於完全不給文件的 56.1%；[05-asai2023-self-rag.pdf, App. C.1, p.20] 也指出，文件不相關時，一般 instruction-tuned 模型仍會產生看似合理的答案。注意 04 量的是答題準確率，不等於 hallucination 的比例。詳見 [Closed-book vs open-book](../comparisons/closed-book-vs-open-book.md)。

## 兩種 hallucination

- **模型「背錯」的知識**：純參數模型講出錯誤的事實，例如下面 BART 的中耳例子 [01-lewis2020-rag.pdf, Table 3, p.7]。
- **沒有依據檢索內容**：即使用了 RAG，模型仍可能產生「檢索內容沒有支持」的說法 [02-gao2023-survey.pdf, §II-A, p.3]。評估時對應的是 answer faithfulness，詳見 [RAG 評估](rag-evaluation.md) [02-gao2023-survey.pdf, §VI-C, p.12]。

## 讓模型自己檢查「有沒有根據」

- Self-RAG 訓練模型在每段回答後產生 ISSUP token，自我評估這段話有沒有被文件支持：完全支持、部分支持，或沒有支持／矛盾 [05-asai2023-self-rag.pdf, Table 1, p.4; App. A.1, p.17]。
- 推論時可以設硬性規則：只要產生「沒有支持」就丟掉那段回答 [05-asai2023-self-rag.pdf, §3.3, p.6]。
- **例子**：模型寫「此人從 2010 年起擔任 CEO」，但文件說他 2015 年就卸任了，於是模型標出 Contradictory [05-asai2023-self-rag.pdf, App. C.3, p.21]。
- 但作者也承認，Self-RAG 仍可能產生沒有被引用完全支持的內容 [05-asai2023-self-rag.pdf, Ethical Concerns, p.11]。
- **「看似合理」的陷阱**：文件不相關時，一般 instruction-tuned 模型仍會繼續產生看似合理的答案 [05-asai2023-self-rag.pdf, App. C.1, p.20]。

## 怎麼偵測 hallucination？

- **RAGAS 的 faithfulness**：把答案拆成小陳述，逐一檢查能不能從檢索到的 context 推論出來；這正是為了避免 hallucination [07-es2023-ragas.pdf, §3, p.3]。在 WikiEval 上，它和人類判斷的一致度是 0.95 [07-es2023-ragas.pdf, Table 1, p.5]。
- **偵測並不容易**：既有研究顯示，用一般的 prompt 讓模型偵測 hallucination，效果不好 [07-es2023-ragas.pdf, §2, p.2]。
- **SelfCheckGPT**：對同一個問題取樣多個答案；如果答案是事實，多次取樣的內容應該相近，hallucination 則不太會這樣 [07-es2023-ragas.pdf, §2, p.2]。06 也建議用這類方法比較捏造率 [06-edge2024-graphrag.pdf, §6.1, p.11]。

## 實際例子

- 問 BART「define middle ear」，它回答「中耳是介於中耳和鼻子之間的部分」，這是錯的答案 [01-lewis2020-rag.pdf, Table 3, p.7]。
- 同一個問題，RAG-Sequence 回答「中耳包含鼓室和三塊聽小骨」[01-lewis2020-rag.pdf, Table 3, p.7]。

## RAG 有比較少 hallucination 嗎？

- 從質性觀察來看，RAG 比 BART 更少 hallucinate，也更常寫出正確的內容 [01-lewis2020-rag.pdf, §4.2, p.6]。
- Jeopardy 出題的人工評估中，認為 RAG 比較符合事實的有 42.7%，認為 BART 比較符合事實的只有 7.1% [01-lewis2020-rag.pdf, Table 4, p.8]。
- 論文對 factuality 的定義是：一句話能不能被可信的外部來源證實 [01-lewis2020-rag.pdf, §3.3, p.5]。

## 常見誤解

- **「用了 RAG 就不會 hallucinate」**：論文只說「更少」，沒說「不會」[01-lewis2020-rag.pdf, §4.2, p.6]。
- 而且外部知識來源本身也可能有錯或有偏見 [01-lewis2020-rag.pdf, Broader Impact, p.10]。

## 各論文怎麼說

- **[01-lewis2020-rag.pdf](../sources/01-lewis2020-rag.md)**：用人工評估和範例展示 RAG 比 BART 更符合事實 [01-lewis2020-rag.pdf, §4.2–4.3, p.6]。
- **[05-asai2023-self-rag.pdf](../sources/05-asai2023-self-rag.md)**：傳統 RAG 的模型沒有被明確訓練去遵循文件中的事實，所以輸出不一定和文件一致 [05-asai2023-self-rag.pdf, §1, p.1]。
- **[02-gao2023-survey.pdf](../sources/02-gao2023-survey.md)**：把 hallucination 列為 LLM 的主要挑戰之一，也是 Naive RAG 在生成階段的缺點 [02-gao2023-survey.pdf, Abstract, p.1; §II-A, p.3]。還提到 Chain-of-Verification 這類驗證查詢的方法可以減少 hallucination [02-gao2023-survey.pdf, §III-C, p.8]。

## 相關頁面

- [Closed-book vs open-book](../comparisons/closed-book-vs-open-book.md)
- [Generator](generator.md)
- [Parametric 與 non-parametric memory](parametric-vs-non-parametric-memory.md)
- [RAG 評估](rag-evaluation.md)
- [RAGAS](ragas.md)
- [Self-RAG](../methods/self-rag.md)
- [術語表](../glossary.md)
