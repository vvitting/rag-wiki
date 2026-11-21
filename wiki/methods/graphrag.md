---
type: method
title: "GraphRAG"
tags: [method, graphrag, knowledge-graph, global-questions, map-reduce]
sources: [06-edge2024-graphrag.pdf, 02-gao2023-survey.pdf]
updated: 2026-11-22
---

# GraphRAG

## 一句話說明

先用 LLM 把整批文件整理成 knowledge graph，再把關係緊密的實體分成社群、為每個社群寫好摘要；回答時，把所有社群摘要彙整成一個全局答案 [06-edge2024-graphrag.pdf, Abstract, p.1]。

## 跟 naive RAG 的差別

| | 一般 RAG（vector RAG，[Naive RAG](naive-rag.md)） | GraphRAG |
|---|---|---|
| 擅長的問題 | 答案集中在少數幾份文件裡的問題 [06-edge2024-graphrag.pdf, §1, p.2] | 需要理解整批資料的全局問題 [06-edge2024-graphrag.pdf, §1, p.2] |
| 例子 | 找特定的事實 [06-edge2024-graphrag.pdf, §2.3, p.3] | 「資料集的主要主題是什麼？」[06-edge2024-graphrag.pdf, Abstract, p.1] |
| Index | 文字的 embedding，依語意相似度檢索 [06-edge2024-graphrag.pdf, §2.1, p.2] | LLM 抽出的 knowledge graph，加上各層社群摘要 [06-edge2024-graphrag.pdf, §1, p.2] |
| 回答方式 | 取回相似的 chunk，放進 context window [06-edge2024-graphrag.pdf, §4.1.2, p.8] | 用每份社群摘要平行產生部分答案，再彙整（map-reduce）[06-edge2024-graphrag.pdf, §1, p.2] |
| 答案特色 | 最直接 [06-edge2024-graphrag.pdf, §5.1, p.9] | 更全面、更多元 [06-edge2024-graphrag.pdf, §5.1, p.9] |

作者說 GraphRAG 是建立在既有的 advanced RAG 策略之上 [06-edge2024-graphrag.pdf, §2.1, p.3]。

## 運作步驟

### 建立 index

1. **切塊**：把文件切成 text chunk。chunk 越長，需要的 LLM 呼叫越少，成本越低，但資訊比較容易被漏掉 [06-edge2024-graphrag.pdf, §3.1.1, p.4]。
2. **抽取**：用 LLM 從每個 chunk 抽出實體、關係和 claim，並各寫一段描述 [06-edge2024-graphrag.pdf, §3.1.2, p.4–5]。
3. **建圖**：實體變成節點，關係變成邊；同一個關係出現幾次，就是那條邊的權重 [06-edge2024-graphrag.pdf, §3.1.3, p.5]。
4. **分群**：用 Leiden 演算法反覆切分，得到階層式的社群 [06-edge2024-graphrag.pdf, §3.1.4, p.5]。
5. **寫摘要**：為每個社群寫報告式的摘要；高層社群的摘要會整合低層的摘要 [06-edge2024-graphrag.pdf, §3.1.5, p.6]。

### 抽取的例子

原文：「NeoChip 的股票在 NewTech 交易所上市首週大漲……NeoChip 在 2016 年被 Quantum Systems 收購……」[06-edge2024-graphrag.pdf, §3.1.2, p.5]

| 抽出的東西 | 內容 | 出處 |
|---|---|---|
| 實體 | NeoChip：專門做穿戴裝置和 IoT 低功耗處理器的上市公司 | [06-edge2024-graphrag.pdf, §3.1.2, p.5] |
| 實體 | Quantum Systems：曾經擁有 NeoChip 的公司 | [06-edge2024-graphrag.pdf, §3.1.2, p.5] |
| 關係 | Quantum Systems 從 2016 年起擁有 NeoChip，直到 NeoChip 上市 | [06-edge2024-graphrag.pdf, §3.1.2, p.5] |

### 回答問題

1. 選定一個社群層級（C0 最高層、摘要最少；C3 最低層、摘要最多）[06-edge2024-graphrag.pdf, §4.1.2, p.8]。
2. 把該層的社群摘要打亂、切塊 [06-edge2024-graphrag.pdf, §3.1.6, p.6]。
3. **Map**：每一塊平行產生部分答案，並打 0–100 分的幫助程度；0 分的丟掉 [06-edge2024-graphrag.pdf, §3.1.6, p.6]。
4. **Reduce**：依分數由高到低放進 context window，產生最終答案 [06-edge2024-graphrag.pdf, §3.1.6, p.6]。

## 優點

- 在全局問題上，全面性和多樣性都明顯勝過一般 RAG：全面性勝率 72%–83%，多樣性勝率 62%–82% [06-edge2024-graphrag.pdf, §5.1, p.9]。
- 最高層摘要（C0）每次查詢需要的 tokens，比直接對原文做摘要少 97% 以上，同時仍勝過一般 RAG [06-edge2024-graphrag.pdf, §5.1, p.10]。
- 社群摘要本身就有用：使用者可以先瀏覽高層摘要找主題，再往下讀細節 [06-edge2024-graphrag.pdf, §3.1.5, p.6]。
- 有開源實作，也被整合進 LangChain、LlamaIndex、NebulaGraph、Neo4J [06-edge2024-graphrag.pdf, §1, p.2]。

## 代價與限制

- **建 index 很貴**：約 100 萬 tokens 的 Podcast 資料，用 gpt-4-turbo 花了 281 分鐘 [06-edge2024-graphrag.pdf, §4.1.3, p.9]。
- **答案不夠直接**：問題很具體時，一般 RAG 的答案更直接 [06-edge2024-graphrag.pdf, §5.1, p.9]。
- **細節可能流失**：在 empowerment 這個標準上結果好壞參半；具體例子、引言和引用是關鍵，作者建議調整抽取的 prompt，保留更多細節 [06-edge2024-graphrag.pdf, §5.1, p.9–10]。
- **評估範圍有限**：只測了兩個約 100 萬 tokens 的資料集，也沒有比較捏造率 [06-edge2024-graphrag.pdf, §6.1, p.11]。
- **knowledge graph 是 LLM 抽出來的**：作者把抽取實體、關係、claim 視為一種摘要，其中的關係和 claim 未必在原文中明說 [06-edge2024-graphrag.pdf, §3.1.3, p.5]；這和 02 所說「通常經過驗證」的 knowledge graph [02-gao2023-survey.pdf, §III-A, p.7] 不同。

## 出處

- [06-edge2024-graphrag.pdf](../sources/06-edge2024-graphrag.md)

## 相關頁面

- [Naive RAG](naive-rag.md)
- [Modular RAG](modular-rag.md)
- [RAG 評估](../concepts/rag-evaluation.md)
- [RAG 進階技巧比較](../comparisons/rag-techniques.md)
