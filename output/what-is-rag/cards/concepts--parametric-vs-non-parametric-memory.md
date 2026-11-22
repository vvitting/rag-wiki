---
page: wiki/concepts/parametric-vs-non-parametric-memory.md
---
# 證據卡：Parametric 與 non-parametric memory

## 重點摘錄
> 模型的知識可以存在兩個地方：一是模型自己「背起來」的部分（parametric memory），二是需要時才去「翻」的外部資料（non-parametric memory）。RAG 就是把這兩種記憶結合起來 [01-lewis2020-rag.pdf, Abstract, p.1]。
> - **只靠 parametric memory 的兩個根本限制**：一是無法回答訓練之後才發生的事；二是即使是最大的模型，也很難記住訓練資料中很少出現的知識 [07-es2023-ragas.pdf, §1, p.1]。
> - 只靠 parametric memory 的模型，很難擴充或修改記憶、無法說明答案的出處，還可能產生 [hallucination](hallucination.md) [01-lewis2020-rag.pdf, §1, p.1]。
> - 加上 non-parametric memory 之後，知識可以直接修改和擴充，取用了哪些知識也能被檢查和解讀 [01-lewis2020-rag.pdf, §1, p.1]。
> - 作者的結論是：只要替換 non-parametric memory，就能更新 RAG 的知識 [01-lewis2020-rag.pdf, §4.5, p.8]。

## 數字
> - 作者準備了 82 位在 2016 到 2018 年間換人的世界領袖，用「Who is {position}?」的格式提問 [01-lewis2020-rag.pdf, §4.5, p.7–8]。
> - 用 2016 年的 index 回答 2016 年的領袖，答對 70%；用 2018 年的 index 回答 2018 年的領袖，答對 68% [01-lewis2020-rag.pdf, §4.5, p.8]。
> - index 和年份不對應時，答對率很低：用 2018 年的 index 問 2016 年的領袖是 12%，用 2016 年的 index 問 2018 年的領袖是 4% [01-lewis2020-rag.pdf, §4.5, p.8]。

## 可以用在
- 為什麼需要（02）：只靠參數的限制
- 是什麼（03）：兩種記憶
- 是什麼（05）：換 index 就能更新知識（70%／68% vs 12%／4%）
