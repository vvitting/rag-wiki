---
page: wiki/concepts/ragas.md
---
# 證據卡：RAGAS

## 重點摘錄
> RAGAS 是一套讓 [LLM](../glossary.md) 幫忙評分 RAG 系統的方法。它不需要人工準備的標準答案，只看三件事：答案有沒有根據、答案有沒有回答問題、找來的資料是否切題 [07-es2023-ragas.pdf, Abstract, p.1; §3, p.3]。
> - 重點：**拆成小步驟再判斷**（RAGAS），比直接要 LLM 打分數或挑選準確得多 [07-es2023-ragas.pdf, §5, p.5]。
> - **「faithfulness 高，答案就是對的」**：不一定。Faithfulness 只檢查答案是否和**檢索到的 context** 一致 [07-es2023-ragas.pdf, §3, p.3]；如果 context 本身有錯，答案也會跟著錯，而外部知識來源本來就可能有錯 [01-lewis2020-rag.pdf, Broader Impact, p.10]。

## 數字
> | RAGAS | 0.95 | 0.78 | 0.70 | [07-es2023-ragas.pdf, Table 1, p.5] |

## 可以用在
- 怎麼評估（11）：不需要標準答案的自動評估；拆成小步驟比較準；faithfulness 高不代表答案對
