---
page: wiki/methods/self-rag.md
---
# 證據卡：Self-RAG

## 重點摘錄
> 訓練一個 LLM，讓它在寫答案的過程中，用特殊的「reflection tokens」自己決定要不要檢索，並為檢索到的文件和自己寫的內容打分數 [05-asai2023-self-rag.pdf, Abstract, p.1]。
> - **「寫一篇最棒的暑假作文」**：模型判斷不需要檢索，直接寫 [05-asai2023-self-rag.pdf, Fig.1, p.2]。
> - 每段回答都附上引用和「有沒有根據」的自我評估，事實查核更容易 [05-asai2023-self-rag.pdf, §1, p.2]。
> - 要先用 GPT-4 標資料，再訓練兩個模型 [05-asai2023-self-rag.pdf, §3.2, p.4–5]。

## ⚠️ 爭議
> > ⚠️ **爭議／更新（原文結論與 Table 2 不一致）**：[05-asai2023-self-rag.pdf, §6, p.10] 的結論說 Self-RAG 明顯勝過參數更多的 LLM 和傳統 RAG；但同一篇的 Table 2 中，ChatGPT（不檢索）在 TriviaQA（74.3）和 ARC-C（75.3）上都高於 Self-RAG 13B（69.3、73.1），加上檢索的 ChatGPT 在 ARC-C 也是 75.3 [05-asai2023-self-rag.pdf, Table 2, p.8]。正文 §1 也只說勝過加上檢索的 ChatGPT「四個任務」[05-asai2023-self-rag.pdf, §1, p.2]。引用這個結論時，請註明比較的對象。

## 可以用在
- 進階變體（10）：自己決定要不要查、為自己打分數；不使用「勝過更大模型」的結論（見 ⚠️）
