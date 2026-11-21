---
type: concept
title: "Lost in the middle（中間迷失）"
tags: [concept, lost-in-the-middle, positional-bias, long-context]
sources: [04-liu2023-lost-in-middle.pdf, 02-gao2023-survey.pdf, 01-lewis2020-rag.pdf]
updated: 2026-11-22
---

# Lost in the middle

## 白話說明

把一堆文件塞進 prompt 時，LLM 最會利用放在**開頭**和**結尾**的資訊，放在**中間**的資訊最容易被忽略。把「答案的位置」和「準確率」畫成圖，會是一條 U 形曲線 [04-liu2023-lost-in-middle.pdf, Fig.1, p.1]。

## 為什麼重要

- RAG 會把檢索到的多份文件放進 prompt，所以正確的文件很可能剛好落在中間 [04-liu2023-lost-in-middle.pdf, §1, p.2]。
- 最糟的時候，給模型文件反而比完全不給還差：GPT-3.5-Turbo 在 20 份文件、答案位於中間時，準確率是 53.8%，不給文件時則是 56.1% [04-liu2023-lost-in-middle.pdf, Table 6, p.18; Table 1, p.5]。

## 運作方式：實驗怎麼做

1. 給模型一個問題和 k 份文件，其中只有 1 份含有答案 [04-liu2023-lost-in-middle.pdf, §2.1, p.3]。
2. 其餘的文件是 retriever 找來的：和問題相關，但不含答案的「干擾文件」[04-liu2023-lost-in-middle.pdf, §2.1, p.3]。
3. 把含答案的文件輪流放在第 1、第 5、第 10……個位置，觀察準確率怎麼變 [04-liu2023-lost-in-middle.pdf, §2.1, p.3; Fig.3, p.4]。

### 結果：U 形曲線（GPT-3.5-Turbo，20 份文件）

| 答案位置 | 準確率 | 出處 |
|---|---|---|
| 第 1 份（開頭） | 75.8% | [04-liu2023-lost-in-middle.pdf, Table 6, p.18] |
| 第 5 份 | 57.2% | [04-liu2023-lost-in-middle.pdf, Table 6, p.18] |
| 第 10 份（中間） | 53.8% | [04-liu2023-lost-in-middle.pdf, Table 6, p.18] |
| 第 15 份 | 55.4% | [04-liu2023-lost-in-middle.pdf, Table 6, p.18] |
| 第 20 份（結尾） | 63.2% | [04-liu2023-lost-in-middle.pdf, Table 6, p.18] |
| 不給文件（closed-book） | 56.1% | [04-liu2023-lost-in-middle.pdf, Table 1, p.5] |

- **Primacy bias**：開頭的資訊用得比較好 [04-liu2023-lost-in-middle.pdf, Fig.1, p.1]。
- **Recency bias**：結尾的資訊用得比較好 [04-liu2023-lost-in-middle.pdf, Fig.1, p.1]。

### 誰會受影響？

- 測試過的模型都有這個現象，包括支援長 context 的版本 [04-liu2023-lost-in-middle.pdf, §2.3, p.5]。
- GPT-4 的整體表現較高，但仍然是 U 形 [04-liu2023-lost-in-middle.pdf, App. D, p.15]。
- 模型夠大才會出現完整的 U 形：Llama-2 的 7B 模型只有 recency bias，13B 和 70B 才是 U 形 [04-liu2023-lost-in-middle.pdf, §4.3, p.9]。
- Encoder-decoder 模型在訓練時見過的長度內比較不受影響；超過那個長度，也會出現 U 形 [04-liu2023-lost-in-middle.pdf, §4.1, p.7]。

## 怎麼減輕？

- **Reranking**：把最相關的文件排到 context 的開頭 [04-liu2023-lost-in-middle.pdf, §5, p.10]。綜述則建議移到 prompt 的「頭尾」[02-gao2023-survey.pdf, §II-B, p.4]。詳見 [Reranking](reranking.md)。
- **少放幾份文件**：在適當時候少取幾份（ranked list truncation）[04-liu2023-lost-in-middle.pdf, §5, p.10]。
- **把問題放在文件前後**（query-aware contextualization）：對 key-value 檢索效果很大，對多文件問答則幾乎沒有幫助 [04-liu2023-lost-in-middle.pdf, §4.2, p.8]。

## 各論文怎麼說

- **[04-liu2023-lost-in-middle.pdf](../sources/04-liu2023-lost-in-middle.md)**：提出這個現象的原始研究 [04-liu2023-lost-in-middle.pdf, Abstract, p.1]。
- **[02-gao2023-survey.pdf](../sources/02-gao2023-survey.md)**：引用這個現象，說明為什麼檢索後要先整理內容，不能把所有文件直接丟給 LLM [02-gao2023-survey.pdf, §IV-A, p.10]。
- **[01-lewis2020-rag.pdf](../sources/01-lewis2020-rag.md)**：原始 RAG 是把每份文件「分別」和問題串接後交給 generator，再把結果加權合併 [01-lewis2020-rag.pdf, §2.1, §2.3, p.3]，並不是把所有文件串成一個長 prompt；所以 lost in the middle 描述的情境，和它不完全相同。

## 常見誤解

- **「context window 夠大，就能把資料全塞進去」**：放得進去，不代表用得好。支援長 context 的模型，不一定比一般版更會用 context [04-liu2023-lost-in-middle.pdf, §2.3, p.5–6]。
- **「這只是因為模型把搜尋結果當成依相關性排序」**：作者打亂干擾文件的順序，並在 prompt 中說明「結果是隨機排序的」，仍然是 U 形 [04-liu2023-lost-in-middle.pdf, App. C, p.14–15]。
- **「這和人一樣，所以很自然」**：作者確實把它連結到人類的序列位置效應，但也指出 Transformer 的 self-attention 理論上能同等地取用任何位置，所以這個現象其實令人意外 [04-liu2023-lost-in-middle.pdf, §6.3, p.10–11]。

## 相關頁面

- [Context window](context-window.md)
- [Reranking](reranking.md)
- [Closed-book vs open-book](../comparisons/closed-book-vs-open-book.md)
- [比喻集：讀長文章只記得頭尾](../analogies.md)
- [術語表](../glossary.md)
