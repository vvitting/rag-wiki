---
type: concept
title: "Parametric memory 與 non-parametric memory"
tags: [concept, memory, foundational, knowledge-update]
sources: [01-lewis2020-rag.pdf, 02-gao2023-survey.pdf, 05-asai2023-self-rag.pdf, 07-es2023-ragas.pdf]
updated: 2026-11-22
---

# Parametric memory 與 non-parametric memory

## 白話說明

模型的知識可以存在兩個地方：一是模型自己「背起來」的部分（parametric memory），二是需要時才去「翻」的外部資料（non-parametric memory）。RAG 就是把這兩種記憶結合起來 [01-lewis2020-rag.pdf, Abstract, p.1]。

## 為什麼重要

- **只靠 parametric memory 的兩個根本限制**：一是無法回答訓練之後才發生的事；二是即使是最大的模型，也很難記住訓練資料中很少出現的知識 [07-es2023-ragas.pdf, §1, p.1]。

- 只靠 parametric memory 的模型，很難擴充或修改記憶、無法說明答案的出處，還可能產生 [hallucination](hallucination.md) [01-lewis2020-rag.pdf, §1, p.1]。
- 加上 non-parametric memory 之後，知識可以直接修改和擴充，取用了哪些知識也能被檢查和解讀 [01-lewis2020-rag.pdf, §1, p.1]。

## 運作方式

| | Parametric memory | Non-parametric memory |
|---|---|---|
| 在原始 RAG 裡是什麼 | [Generator](generator.md)（BART）的參數 [01-lewis2020-rag.pdf, §2.3, p.3] | Wikipedia 的 dense vector index [01-lewis2020-rag.pdf, §2.2, p.3] |
| 存的形式 | 模型參數；RAG 的可訓練參數共 626M [01-lewis2020-rag.pdf, App. G, p.18–19] | 原始文字，人類讀得懂、也能編輯 [01-lewis2020-rag.pdf, §5, p.9] |
| 怎麼更新 | T5、BART 這類模型要再訓練才能改變行為 [01-lewis2020-rag.pdf, §4.5, p.7] | 直接換掉 index 就好 [01-lewis2020-rag.pdf, §4.5, p.8] |
| 對應的考試方式 | Closed-book [01-lewis2020-rag.pdf, §4.1, p.5] | Open-book [01-lewis2020-rag.pdf, §4.1, p.5] |

### 實驗：換 index 就能更新知識（index hot-swapping）

- 作者準備了 82 位在 2016 到 2018 年間換人的世界領袖，用「Who is {position}?」的格式提問 [01-lewis2020-rag.pdf, §4.5, p.7–8]。
- 用 2016 年的 index 回答 2016 年的領袖，答對 70%；用 2018 年的 index 回答 2018 年的領袖，答對 68% [01-lewis2020-rag.pdf, §4.5, p.8]。
- index 和年份不對應時，答對率很低：用 2018 年的 index 問 2016 年的領袖是 12%，用 2016 年的 index 問 2018 年的領袖是 4% [01-lewis2020-rag.pdf, §4.5, p.8]。
- 作者的結論是：只要替換 non-parametric memory，就能更新 RAG 的知識 [01-lewis2020-rag.pdf, §4.5, p.8]。

### 兩種記憶會合作

- RAG-Token 產生書名「The Sun Also Rises」時，第一個字之後就不太依賴文件了，表示書名其實已經存在 BART 的參數裡 [01-lewis2020-rag.pdf, §4.3, p.6]。
- 作者的解讀是：non-parametric memory 負責「引導」生成，把存在 parametric memory 裡的特定知識「喚出來」[01-lewis2020-rag.pdf, §4.3, p.6]。

## 各論文怎麼說

- **[01-lewis2020-rag.pdf](../sources/01-lewis2020-rag.md)**：提出結合兩種記憶的 RAG，並且讓兩種記憶都是預訓練好、預先載入大量知識的；這和之前那些「針對特定任務從零訓練」的記憶架構不同 [01-lewis2020-rag.pdf, §1, p.2]。
- **[02-gao2023-survey.pdf](../sources/02-gao2023-survey.md)**：在 LLM 時代用同樣的框架總結 RAG：把 language model 的「參數化知識」和外部知識庫的「非參數化資料」結合起來 [02-gao2023-survey.pdf, §VIII, p.16]。也強調 RAG 能持續更新知識，並整合特定領域的資訊 [02-gao2023-survey.pdf, Abstract, p.1]。
- **和 fine-tuning 的對比**：fine-tuning 是把知識「內化」到參數裡，比較靜態，要更新就得再訓練 [02-gao2023-survey.pdf, §II-D, p.5]。詳見 [RAG vs fine-tuning](../comparisons/rag-vs-fine-tuning.md)。

## 常見誤解

- **「有了 RAG，模型就不需要自己的知識」**：錯。檢索到的文件裡沒有答案時，RAG 在 NQ 上仍有 11.8% 答對，這靠的是 parametric memory [01-lewis2020-rag.pdf, §4.1, p.6]。

## 該不該讓模型用自己的知識？

> ⚠️ **爭議／更新**：[01-lewis2020-rag.pdf, §4.1, p.5–6] 和 [05-asai2023-self-rag.pdf, App. C.1, p.20] 對同一件事的評價相反：
> - [01-lewis2020-rag.pdf, §4.1, p.5–6] 把「文件沒有答案也能答對（11.8%）」視為生成式 RAG 的**優點**，extractive 模型在這種情況下是 0%。
> - [05-asai2023-self-rag.pdf, App. C.1, p.20] 則把「答案幾乎都來自文件」視為**優點**：Self-RAG 答對的題目中，只有 2% 的答案不在文件裡；Llama2-chat 13B 是 18%，Alpaca 是 15%。

兩者重視的東西不同：01 重視「答對」，05 重視「有根據、可以驗證」[05-asai2023-self-rag.pdf, §1, p.2]。05 也指出，文件不相關時，一般模型仍會繼續產生「看似合理」的答案，Self-RAG 則會標出 Irrelevant [05-asai2023-self-rag.pdf, App. C.1, p.20]。

### 讓模型自己決定要不要查

- 不是每個問題都需要外部知識，例如寫一篇暑假作文 [05-asai2023-self-rag.pdf, Fig.1, p.2]。
- Self-RAG 讓模型自己判斷：需要事實根據時才檢索，不需要時就用自己的知識 [05-asai2023-self-rag.pdf, App. A.1, p.17]。
- 推論時完全不檢索，Self-RAG 在 PopQA（冷門知識）上從 45.5 掉到 24.7，在 PubHealth 上則幾乎不變（73.5 → 73.0）[05-asai2023-self-rag.pdf, Fig.3a, p.9]。

## 相關頁面

- [原始 RAG（方法）](../methods/original-rag.md)
- [Self-RAG（方法）](../methods/self-rag.md)
- [Closed-book vs open-book](../comparisons/closed-book-vs-open-book.md)
- [比喻集：開書考 vs 閉書考](../analogies.md)
- [術語表](../glossary.md)
