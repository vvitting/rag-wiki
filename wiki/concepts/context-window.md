---
type: concept
title: "Context window 與「放多少文件」"
tags: [concept, context-window, long-context, lost-in-the-middle]
sources: [04-liu2023-lost-in-middle.pdf, 02-gao2023-survey.pdf, 01-lewis2020-rag.pdf, 03-anthropic-contextual-retrieval.pdf]
updated: 2026-11-22
---

# Context window 與「放多少文件」

## 白話說明

- LLM 主要是透過 prompting 來完成任務：把任務說明和要處理的資料全部整理成一段文字輸入（input context），模型再接著產生文字 [04-liu2023-lost-in-middle.pdf, §1, p.1]。
- Context window 就是模型一次能接受的最大輸入長度，以 token 計算。例如 GPT-3.5-Turbo 是 4K tokens，GPT-3.5-Turbo（16K）是 16K tokens [04-liu2023-lost-in-middle.pdf, §2.2, p.5]。
- 為了配合這個限制，RAG 會把文件切成較小的 [chunk](chunking.md) [02-gao2023-survey.pdf, §II-A, p.3]。

### Context window 為什麼有上限？

- Transformer 需要的記憶體和運算量，會隨著序列長度呈平方成長 [04-liu2023-lost-in-middle.pdf, §1, p.1]。
- 所以早期模型的 context window 通常只有 512 到 2048 tokens [04-liu2023-lost-in-middle.pdf, §1, p.1]。
- 後來硬體和演算法進步，出現了 4096、32K，甚至 100K tokens 的模型 [04-liu2023-lost-in-middle.pdf, §1, p.1–2]。
- 到 02 撰寫時，LLM 已經能處理超過 200,000 tokens [02-gao2023-survey.pdf, §VII-A, p.14]。

## 為什麼重要

- **放得進去，不代表用得好**：放在 context 中間的資訊最容易被忽略，這就是 [lost in the middle](lost-in-the-middle.md) [04-liu2023-lost-in-middle.pdf, Abstract, p.1]。
- 多餘的資訊也會干擾 LLM 生成答案 [02-gao2023-survey.pdf, §IV-A, p.10]。
- 給模型更長的 context 是一種取捨：資訊更多可能有幫助，但模型要處理的內容也變多，準確率可能下降 [04-liu2023-lost-in-middle.pdf, §5, p.9]。

## 運作方式：怎麼控制 context

- **Reranking**：把最相關的內容排到前面，或排到 prompt 的頭尾 [02-gao2023-survey.pdf, §II-B, p.4; 04-liu2023-lost-in-middle.pdf, §5, p.10]。詳見 [Reranking](reranking.md)。
- **少放幾份文件**（ranked list truncation）：在適當時候少取幾份 [04-liu2023-lost-in-middle.pdf, §5, p.10]。
- **Context 壓縮**：例如 LLMLingua 用 GPT-2 Small、LLaMA-7B 這類小模型刪掉不重要的 token [02-gao2023-survey.pdf, §IV-A, p.10]。
- **先篩選文件**：讓 LLM 先評估檢索到的內容，濾掉相關性低的文件 [02-gao2023-survey.pdf, §IV-A, p.10]。
- **把問題放在文件前後**（query-aware contextualization）：對多文件問答幾乎沒有幫助 [04-liu2023-lost-in-middle.pdf, §4.2, p.8]。

## 「放越多文件越好」嗎？

> ⚠️ **爭議／更新**：[01-lewis2020-rag.pdf, §4.5, p.8]、[02-gao2023-survey.pdf, §IV-A, p.10; §VII-B, p.14]、[03-anthropic-contextual-retrieval.pdf, p.8]、[04-liu2023-lost-in-middle.pdf, §5, p.10] 的五個說法並不一致：
> - [01-lewis2020-rag.pdf, §4.5, p.8; Fig.3, p.8]：RAG-Sequence 在測試時取越多份文件，NQ 表現就越好；RAG-Token 則在 10 份時最好。
> - [02-gao2023-survey.pdf, §IV-A, p.10]：「盡量多檢索、全部串成長 prompt」是 RAG 的常見誤解，過多的 context 會帶來雜訊。
> - [02-gao2023-survey.pdf, §VII-B, p.14]：綜述引用 Cuconasu et al. 的研究，加入不相關的文件反而讓準確率提高超過 30%。
> - [03-anthropic-contextual-retrieval.pdf, p.8]：放越多 chunk，越有機會包含相關資訊，但資訊太多會讓模型分心，所以有上限；實測 5、10、20 個 chunk 中，20 個最好。
> - [04-liu2023-lost-in-middle.pdf, §5, p.10]：retriever 的 recall 還在上升，模型的表現卻早早停止進步；取 50 份和取 20 份相比，GPT-3.5-Turbo 只多約 1.5%，Claude-1.3 約 1%，但延遲和成本都增加了。

### 目前最合理的整合

> 下面是 wiki 根據上面五個說法整理出的結論，每一點都附上依據：

1. **到某個數量之前，多放會有幫助**：03 的 5 → 10 → 20 都在進步 [03-anthropic-contextual-retrieval.pdf, p.8]；04 的 retriever recall 也隨文件數量上升 [04-liu2023-lost-in-middle.pdf, Fig.11, p.10]。
2. **超過某個數量後，效益很小，成本卻持續增加**：04 發現 20 份以上幾乎不再進步 [04-liu2023-lost-in-middle.pdf, §5, p.10]。
3. **位置比數量更重要**：同樣 20 份文件，答案在第 1 份時是 75.8%，在第 10 份時是 53.8% [04-liu2023-lost-in-middle.pdf, Table 6, p.18]。
4. **01 是不同的情境**：原始 RAG 把每份文件分別交給 generator，再加權合併 [01-lewis2020-rag.pdf, §2.1, p.3]，不是串成一個長 prompt，所以不受位置影響的方式也不同。04 也發現 encoder-decoder 模型（01 的 BART 就屬於這類 [01-lewis2020-rag.pdf, §2.3, p.3]）在訓練長度內，對位置比較不敏感 [04-liu2023-lost-in-middle.pdf, §4.1, p.7]。
5. **「不相關的文件也可能有幫助」要看是哪種不相關**：04 發現用隨機文件當干擾時，準確率比用「相關但沒有答案」的文件當干擾還高 [04-liu2023-lost-in-middle.pdf, App. B, p.14]。這和 02 引用的 Cuconasu et al. 結果方向一致 [02-gao2023-survey.pdf, §VII-B, p.14]，但兩者的實驗設計不同，不能直接比較。

## RAG 和 long context 的關係

- 有了很長的 context window，於是有人問：還需要 RAG 嗎？[02-gao2023-survey.pdf, §VII-A, p.14]
- 綜述認為 RAG 仍然無可取代 [02-gao2023-survey.pdf, §VII-A, p.14]。
- 理由一：一次給大量 context 會明顯拖慢推論速度，分塊檢索、按需輸入比較有效率 [02-gao2023-survey.pdf, §VII-A, p.14]。
- 理由二：RAG 能快速找到原始出處讓使用者驗證，檢索過程看得見；只靠 long context 則像黑盒子 [02-gao2023-survey.pdf, §VII-A, p.14]。
- 04 的實驗也顯示：支援長 context 的模型，不一定比一般版本更會用 context [04-liu2023-lost-in-middle.pdf, §2.3, p.5–6]。

### 知識庫不大時，不一定需要 RAG

- 03 說，有時最簡單的方法就是最好的：如果知識庫小於 200,000 tokens（約 500 頁），可以直接把整個知識庫放進 prompt，不需要 RAG [03-anthropic-contextual-retrieval.pdf, p.2]。
- 搭配 prompt caching，這種做法更快也更便宜：延遲降低超過 2 倍，成本最多降低 90% [03-anthropic-contextual-retrieval.pdf, p.2]。
- 知識庫變大、放不進 context window 時，RAG 才是典型的解法 [03-anthropic-contextual-retrieval.pdf, p.2]。

> ⚠️ **爭議／更新**：[03-anthropic-contextual-retrieval.pdf, p.2] 認為小型知識庫不需要 RAG，直接全部放進 prompt；[02-gao2023-survey.pdf, §VII-A, p.14] 則強調 RAG 在推論效率和可驗證性上仍無可取代；[04-liu2023-lost-in-middle.pdf, §2.3, p.5] 更發現，即使是支援長 context 的模型，也很難用好放在中間的資訊。
> 但要注意：04 測的是 2023 年的模型（GPT-3.5-Turbo、Claude-1.3）[04-liu2023-lost-in-middle.pdf, §2.2, p.4–5]，03 是 2024 年的文章 [03-anthropic-contextual-retrieval.pdf, p.1]，模型世代不同；而 03 沒有附上「整份放進 prompt」的準確率數據 [03-anthropic-contextual-retrieval.pdf, p.2]。

## 各論文怎麼說

- **[01-lewis2020-rag.pdf](../sources/01-lewis2020-rag.md)**：測試時可以調整要取幾份文件，這會影響表現和執行時間 [01-lewis2020-rag.pdf, §4.5, p.8]。
- **[02-gao2023-survey.pdf](../sources/02-gao2023-survey.md)**：見上方說明 [02-gao2023-survey.pdf, §IV-A, p.10; §VII-A, p.14]。
- **[03-anthropic-contextual-retrieval.pdf](../sources/03-anthropic-contextual-retrieval.md)**：建議依自己的使用情境實驗 chunk 的數量 [03-anthropic-contextual-retrieval.pdf, p.8]。
- **[04-liu2023-lost-in-middle.pdf](../sources/04-liu2023-lost-in-middle.md)**：「要給模型多長的 context」最終要看任務而定，取決於多加的 context 有多少價值，以及模型能不能有效使用長 context [04-liu2023-lost-in-middle.pdf, §5, p.9]。

## 相關頁面

- [Lost in the middle](lost-in-the-middle.md)
- [Reranking](reranking.md)
- [Chunking](chunking.md)
- [Retriever](retriever.md)
- [術語表](../glossary.md)
