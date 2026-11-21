---
type: comparison
title: "RAG vs fine-tuning vs prompt engineering"
tags: [comparison, fine-tuning, prompt-engineering]
sources: [02-gao2023-survey.pdf, 05-asai2023-self-rag.pdf]
updated: 2026-11-22
---

# RAG vs fine-tuning vs prompt engineering

讓 LLM 變得更好用，常見的方法有三種：RAG、fine-tuning（FT）、prompt engineering [02-gao2023-survey.pdf, §II-D, p.5]。綜述用兩個維度來比較它們：需要多少外部知識，以及需要改動模型多少 [02-gao2023-survey.pdf, §II-D, p.5; Fig.4, p.7]。

| | Prompt engineering | RAG | Fine-tuning |
|---|---|---|---|
| 做什麼 | 發揮模型本身的能力 [02-gao2023-survey.pdf, §II-D, p.5] | 給模型一本量身訂做的教科書，讓它查資料 [02-gao2023-survey.pdf, §II-D, p.5] | 像學生花時間把知識內化 [02-gao2023-survey.pdf, §II-D, p.5] |
| 外部知識需求 | 低 [02-gao2023-survey.pdf, §II-D, p.5] | 會有效利用外部知識來源 [02-gao2023-survey.pdf, §II-D, p.5] | – |
| 改動模型 | 低 [02-gao2023-survey.pdf, §II-D, p.5] | Naive RAG 低，Modular RAG 較多 [02-gao2023-survey.pdf, Fig.4, p.7] | 要再訓練模型 [02-gao2023-survey.pdf, Fig.4, p.7] |
| 適合 | – | 需要精確資訊的檢索型任務 [02-gao2023-survey.pdf, §II-D, p.5] | 需要模仿特定結構、風格或格式 [02-gao2023-survey.pdf, §II-D, p.5] |
| 更新知識 | – | 可以即時更新 [02-gao2023-survey.pdf, §II-D, p.5] | 比較靜態，要再訓練才能更新 [02-gao2023-survey.pdf, §II-D, p.5] |
| 可解釋性 | – | 高 [02-gao2023-survey.pdf, §II-D, p.5] | – |
| 代價 | – | 延遲較高，資料檢索有倫理考量 [02-gao2023-survey.pdf, §II-D, p.5] | 準備資料和訓練都需要大量運算資源 [02-gao2023-survey.pdf, §II-D, p.5] |

表中的「–」代表綜述沒有明確整理 [02-gao2023-survey.pdf, §II-D, p.5]。

## 重點

- 綜述引用的研究顯示，在多種 knowledge-intensive 任務上，不論是訓練時見過的知識還是全新的知識，RAG 都一致勝過 unsupervised fine-tuning [02-gao2023-survey.pdf, §II-D, p.5]。
- 同一份研究也發現，LLM 很難透過 unsupervised fine-tuning 學到新的事實 [02-gao2023-survey.pdf, §II-D, p.5]。
- Fine-tuning 雖然可以減少 hallucination，但遇到不熟悉的資料時可能出問題 [02-gao2023-survey.pdf, §II-D, p.5]。
- **兩者不是二選一**：RAG 和 FT 可以互補，有時合併使用效果最好 [02-gao2023-survey.pdf, §II-D, p.5]。
- **合併使用的實例：Self-RAG**：它 fine-tune 一個 LLM，讓模型學會何時檢索、怎麼評估文件 [05-asai2023-self-rag.pdf, §3.2, p.4–5]。對照組 Llama2-FT 用相同資料 fine-tune，但沒有學檢索和自我評估，只在測試時加上檢索，表現仍然落後 Self-RAG [05-asai2023-self-rag.pdf, §5.1, p.9]。
- **訓練成本**：Self-RAG 的 critique 是離線算好再插入訓練資料，作者說這比 RLHF 的 PPO 訓練便宜很多 [05-asai2023-self-rag.pdf, §3.2.2, p.6]。
- 要選哪一個，取決於資料多常變動、需要多少客製化，以及有多少運算資源 [02-gao2023-survey.pdf, §II-D, p.5]。

## 相關頁面

- [Closed-book vs open-book](closed-book-vs-open-book.md)
- [比喻集](../analogies.md)
- [三種 RAG 典範比較](rag-paradigms.md)
