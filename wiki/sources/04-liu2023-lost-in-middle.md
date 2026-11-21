---
type: source
title: "Lost in the Middle: How Language Models Use Long Contexts"
raw: 04-liu2023-lost-in-middle.pdf
authors: [Nelson F. Liu, Kevin Lin, John Hewitt, Ashwin Paranjape, Michele Bevilacqua, Fabio Petroni, Percy Liang]
year: 2023
tags: [long-context, lost-in-the-middle, positional-bias, context-window, evaluation]
sources: [04-liu2023-lost-in-middle.pdf, 01-lewis2020-rag.pdf, 02-gao2023-survey.pdf, 03-anthropic-contextual-retrieval.pdf, 06-edge2024-graphrag.pdf]
updated: 2026-11-22
---

# Lost in the Middle: How Language Models Use Long Contexts（Liu et al., 2023）

作者來自 Stanford、UC Berkeley、Samaya AI [04-liu2023-lost-in-middle.pdf, p.1]。raw 檔是 arXiv 2307.03172 的 v3 版（2023 年 11 月 20 日），並經過 TACL 的審稿流程 [04-liu2023-lost-in-middle.pdf, p.1, p.11]。

## 一句話摘要

把「含有答案的文件」放在 prompt 的不同位置，發現 LLM 對開頭和結尾的資訊用得最好，放在中間時表現明顯變差，畫出來是一條 U 形曲線；連專門支援長 context 的模型也一樣 [04-liu2023-lost-in-middle.pdf, Abstract, p.1]。詳見 [Lost in the middle](../concepts/lost-in-the-middle.md)。

## 這篇想解決什麼問題

- 新的 language model 能接受很長的輸入，但我們不太清楚它們實際上把長 context 用得多好 [04-liu2023-lost-in-middle.pdf, Abstract, p.1]。
- 如果模型真的能好好使用長 context，那麼相關資訊放在哪個位置，應該不太影響表現 [04-liu2023-lost-in-middle.pdf, §1, p.2]。

## 核心方法

### 實驗一：多文件問答（multi-document QA）

- 給模型一個問題和 k 份文件，其中只有 1 份含有答案，其餘 k − 1 份是「干擾文件」（distractor）[04-liu2023-lost-in-middle.pdf, §2.1, p.3]。
- 這個設定是在模擬 RAG：增減文件數量，就像 RAG 多取或少取幾份文件 [04-liu2023-lost-in-middle.pdf, §1, p.2]。
- 資料來自 NaturalQuestions-Open 中長答案是段落的 2655 個問題；文件是最多 100 tokens 的 Wikipedia 段落 [04-liu2023-lost-in-middle.pdf, §2.1, p.3]。
- 干擾文件由 retriever（Contriever）找出：和問題最相關、但不含答案的段落 [04-liu2023-lost-in-middle.pdf, §2.1, p.3]。
- **控制兩個變數**：一是「含答案文件的位置」（調整文件順序），二是「context 的長度」（增減干擾文件，共試 10、20、30 份）[04-liu2023-lost-in-middle.pdf, §2.1, p.3; §2.3, p.5]。

### 實驗二：key-value 檢索

- 給模型一個 JSON 物件，裡面有很多組隨機產生的 key-value（UUID），要求回傳指定 key 對應的 value [04-liu2023-lost-in-middle.pdf, §3.1, p.6]。
- 這是測試「從 context 裡找出相符字串」這個最基本能力的極簡任務 [04-liu2023-lost-in-middle.pdf, §3, p.6]。

### 測試的模型

- 開源模型：MPT-30B-Instruct、LongChat-13B（16K）[04-liu2023-lost-in-middle.pdf, §2.2, p.4]。
- 商用模型：GPT-3.5-Turbo（4K 與 16K）、Claude-1.3（8K 與 100K）[04-liu2023-lost-in-middle.pdf, §2.2, p.4–5]。
- 附錄另外測了 GPT-4 和 Llama-2 [04-liu2023-lost-in-middle.pdf, App. D–E, p.15–16]。

## 關鍵結果（數字務必附出處）

### 1. U 形曲線：中間的資訊最容易被忽略

以 GPT-3.5-Turbo、20 份文件為例，答案文件放在不同位置時的準確率 [04-liu2023-lost-in-middle.pdf, Table 6, p.18]：

| 答案文件的位置 | 準確率 | 出處 |
|---|---|---|
| 第 1 份（開頭） | 75.8% | [04-liu2023-lost-in-middle.pdf, Table 6, p.18] |
| 第 5 份 | 57.2% | [04-liu2023-lost-in-middle.pdf, Table 6, p.18] |
| 第 10 份（中間） | 53.8% | [04-liu2023-lost-in-middle.pdf, Table 6, p.18] |
| 第 15 份 | 55.4% | [04-liu2023-lost-in-middle.pdf, Table 6, p.18] |
| 第 20 份（結尾） | 63.2% | [04-liu2023-lost-in-middle.pdf, Table 6, p.18] |

- GPT-3.5-Turbo 在多文件問答上的表現，可能因為答案文件的位置不同而下降超過 20% [04-liu2023-lost-in-middle.pdf, §2.3, p.5]。
- **比不給文件還差**：同一個模型完全不給文件（closed-book）時的準確率是 56.1% [04-liu2023-lost-in-middle.pdf, Table 1, p.5]。在 20 和 30 份文件的設定中，最差情況反而低於這個數字 [04-liu2023-lost-in-middle.pdf, §2.3, p.5]。
- **只給正確文件**（oracle）時，GPT-3.5-Turbo 的準確率是 88.3% [04-liu2023-lost-in-middle.pdf, Table 1, p.5]。
- 開頭表現好叫 primacy bias，結尾表現好叫 recency bias [04-liu2023-lost-in-middle.pdf, Fig.1, p.1]。

### 2. 支援長 context 的模型不一定比較會用 context

- 當輸入同時放得進一般版和長 context 版時，兩者的表現幾乎一樣 [04-liu2023-lost-in-middle.pdf, §2.3, p.5]。
- 例如 GPT-3.5-Turbo 和 GPT-3.5-Turbo（16K）在 20 份文件、答案位於第 10 份時，分別是 53.8% 和 54.1% [04-liu2023-lost-in-middle.pdf, Table 6, p.18]。

### 3. 連「找相同字串」都會受位置影響

- Claude-1.3 在所有長度下的 key-value 檢索幾乎都做到完美，其他模型則有困難，尤其是 140 或 300 組 key-value 的時候 [04-liu2023-lost-in-middle.pdf, §3.2, p.6]。
- GPT-3.5-Turbo、GPT-3.5-Turbo（16K）、MPT-30B-Instruct 在 key-value 位於中間時表現最差 [04-liu2023-lost-in-middle.pdf, §3.2, p.6]。

### 4. 放越多文件，進步有限

- 在 open-domain QA 上，retriever 的 recall 還在上升，模型的表現卻早早就停止進步了 [04-liu2023-lost-in-middle.pdf, §5, p.10; Fig.11, p.10]。
- 取 50 份文件和取 20 份相比，GPT-3.5-Turbo 只多進步約 1.5%，Claude-1.3 約 1% [04-liu2023-lost-in-middle.pdf, §5, p.10]。
- 但 context 卻變長很多，延遲和成本也跟著增加 [04-liu2023-lost-in-middle.pdf, §5, p.10]。

### 5. 為什麼會這樣？（初步探討）

- **模型架構**：encoder-decoder 模型（Flan-UL2、Flan-T5-XXL）在訓練時見過的長度內，對位置比較不敏感；Flan-UL2 最好和最差只差 1.9% [04-liu2023-lost-in-middle.pdf, §4.1, p.7]。但輸入一超過訓練時的長度，就會出現 U 形曲線 [04-liu2023-lost-in-middle.pdf, §4.1, p.7]。
- **把問題放在前後（query-aware contextualization）**：key-value 任務幾乎都變成完美，例如 GPT-3.5-Turbo（16K）在 300 組時從最差 45.6% 變成 100% [04-liu2023-lost-in-middle.pdf, §4.2, p.8]。但對多文件問答的趨勢影響很小 [04-liu2023-lost-in-middle.pdf, §4.2, p.8]。
- **Instruction fine-tuning 不是主因**：MPT-30B 的 base 模型和 instruct 模型都有 U 形曲線 [04-liu2023-lost-in-middle.pdf, §4.3, p.9]。Fine-tuning 只把最好和最差的差距，從將近 10% 縮小到約 4% [04-liu2023-lost-in-middle.pdf, §4.3, p.9]。
- **模型大小**：Llama-2 的 7B 模型只有 recency bias；13B 和 70B 才出現 U 形曲線 [04-liu2023-lost-in-middle.pdf, §4.3, p.9; App. E, p.16]。
- **GPT-4** 的整體表現比其他模型都高，但仍然是 U 形曲線 [04-liu2023-lost-in-middle.pdf, App. D, p.15]。

## 限制與後續爭議

- **測試的模型較舊**：測的是 2023 年的模型，例如 GPT-3.5-Turbo、Claude-1.3 [04-liu2023-lost-in-middle.pdf, §2.2, p.4–5]。
- **探討原因的實驗是初步的**：作者自己稱這些是「preliminary investigations」[04-liu2023-lost-in-middle.pdf, §4, p.7]。
- **只用 greedy decoding**：其他 decoding 方法留給未來研究 [04-liu2023-lost-in-middle.pdf, §2.2, p.4]。
- **排除其他解釋**：
  - 用沒有歧義的問題子集重做，結果和結論相似 [04-liu2023-lost-in-middle.pdf, App. A, p.14]。
  - 把干擾文件換成隨機文件，準確率整體變高，但仍然無法好好使用整個 context [04-liu2023-lost-in-middle.pdf, App. B, p.14]。
  - 打亂干擾文件的順序，並在 prompt 中說明「結果是隨機排序的」，仍然是 U 形曲線 [04-liu2023-lost-in-middle.pdf, App. C, p.14–15]。

> ⚠️ **爭議／更新**：[03-anthropic-contextual-retrieval.pdf, p.2] 建議知識庫小於 200,000 tokens 時，直接全部放進 prompt；但本篇發現，即使是支援長 context 的模型，也很難用好放在中間的資訊 [04-liu2023-lost-in-middle.pdf, §2.3, p.5]。兩篇測試的模型世代不同（本篇是 2023 年的 GPT-3.5、Claude-1.3），03 也沒有附上「整份放進 prompt」的準確率數據。詳見 [Context window](../concepts/context-window.md)。

## 和既有頁面的關係

- **印證 02**：02 說「LLM 和人一樣，傾向只注意長文的開頭和結尾」[02-gao2023-survey.pdf, §IV-A, p.10]，引用的正是這篇的研究 [02-gao2023-survey.pdf, Ref.[98], p.19]。
- **心理學的對應**：本篇把 U 形曲線連結到心理學的「序列位置效應」（serial-position effect）：人在回想一串項目時，最記得第一個和最後一個 [04-liu2023-lost-in-middle.pdf, §6.3, p.10]。不過作者也指出，Transformer 的 self-attention 理論上能同等地取用任何位置的 token，所以這個現象其實有點令人意外 [04-liu2023-lost-in-middle.pdf, §6.3, p.11]。
- **被 06 引用**：GraphRAG 因為擔心 lost in the middle，才為一般 RAG 測試不同大小的 context window，結果 8k 最好 [06-edge2024-graphrag.pdf, App. C, p.19]。但 06 在另一處把本篇的結論描述成「chunk **前段**的資訊容易被漏掉」[06-edge2024-graphrag.pdf, §3.1.1, p.4]，和本篇「中間最差」的發現不一致，詳見 [Lost in the middle](../concepts/lost-in-the-middle.md)。
- **支持 reranking**：作者建議把相關文件 rerank 到 context 的開頭，或在適當時少取幾份文件（ranked list truncation）[04-liu2023-lost-in-middle.pdf, §5, p.10]。這支持了 02、03 的看法，詳見 [Reranking](../concepts/reranking.md)。

## 關鍵圖表說明

- **Fig.1**：U 形曲線，橫軸是答案文件的位置，縱軸是準確率，並畫出 closed-book 的基準線 [04-liu2023-lost-in-middle.pdf, Fig.1, p.1]。**這是整篇最適合放進簡報的圖。**
- **Fig.2**：多文件問答的 prompt 範例（「誰得到第一座諾貝爾物理獎」）[04-liu2023-lost-in-middle.pdf, Fig.2, p.4]。
- **Fig.5**：10、20、30 份文件下，各模型的位置效應 [04-liu2023-lost-in-middle.pdf, Fig.5, p.5]。
- **Table 1**：各模型的 closed-book 與 oracle 準確率 [04-liu2023-lost-in-middle.pdf, Table 1, p.5]。
- **Fig.11**：retriever recall 和模型表現隨文件數量的變化；模型表現很早就停止進步 [04-liu2023-lost-in-middle.pdf, Fig.11, p.10]。
- **Table 5–7**：每個位置的完整數字 [04-liu2023-lost-in-middle.pdf, App. G, p.18]。

## 對初學者的重點

1. 把資料塞進 prompt，不代表模型會好好讀；放在中間的資料最容易被忽略 [04-liu2023-lost-in-middle.pdf, Abstract, p.1]。
2. 最糟的時候，給模型文件反而比不給還差 [04-liu2023-lost-in-middle.pdf, §2.3, p.5]。
3. 放更多文件，進步很有限，成本卻一直增加 [04-liu2023-lost-in-middle.pdf, §5, p.10]。
4. 所以，把最相關的資料排在前面（reranking），比一直加文件更有用 [04-liu2023-lost-in-middle.pdf, §5, p.10]。

## 相關頁面

- [Lost in the middle](../concepts/lost-in-the-middle.md)
- [Context window](../concepts/context-window.md)
- [Reranking](../concepts/reranking.md)
- [Closed-book vs open-book](../comparisons/closed-book-vs-open-book.md)
- [02 RAG 綜述](02-gao2023-survey.md)
- [03 Contextual Retrieval](03-anthropic-contextual-retrieval.md)
