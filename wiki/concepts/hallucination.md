---
type: concept
title: "Hallucination（幻覺）"
tags: [concept, hallucination, factuality]
sources: [01-lewis2020-rag.pdf, 02-gao2023-survey.pdf]
updated: 2026-11-22
---

# Hallucination

## 白話說明

Hallucination 指模型講出聽起來很像真的、但其實是錯的內容。原始 RAG 論文把它列為純參數模型的缺點之一 [01-lewis2020-rag.pdf, §1, p.1]。

## 為什麼重要

- 這正是 RAG 想解決的問題之一：作者認為，RAG 的生成更紮根在真實的知識上（這裡指 Wikipedia），所以比較少「hallucinate」[01-lewis2020-rag.pdf, Broader Impact, p.10]。
- LLM 在處理超出訓練資料範圍、或需要最新資訊的問題時，特別容易產生 hallucination [02-gao2023-survey.pdf, §I, p.1]。
- 透過參考外部知識，RAG 能有效減少產生錯誤內容的問題 [02-gao2023-survey.pdf, §I, p.1]。

## 兩種 hallucination

- **模型「背錯」的知識**：純參數模型講出錯誤的事實，例如下面 BART 的中耳例子 [01-lewis2020-rag.pdf, Table 3, p.7]。
- **沒有依據檢索內容**：即使用了 RAG，模型仍可能產生「檢索內容沒有支持」的說法 [02-gao2023-survey.pdf, §II-A, p.3]。評估時對應的是 answer faithfulness，詳見 [RAG 評估](rag-evaluation.md) [02-gao2023-survey.pdf, §VI-C, p.12]。

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
- **[02-gao2023-survey.pdf](../sources/02-gao2023-survey.md)**：把 hallucination 列為 LLM 的主要挑戰之一，也是 Naive RAG 在生成階段的缺點 [02-gao2023-survey.pdf, Abstract, p.1; §II-A, p.3]。還提到 Chain-of-Verification 這類驗證查詢的方法可以減少 hallucination [02-gao2023-survey.pdf, §III-C, p.8]。

## 相關頁面

- [Generator](generator.md)
- [Parametric 與 non-parametric memory](parametric-vs-non-parametric-memory.md)
- [RAG 評估](rag-evaluation.md)
- [術語表](../glossary.md)
