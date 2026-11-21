---
type: source
title: "Self-RAG: Learning to Retrieve, Generate, and Critique through Self-Reflection"
raw: 05-asai2023-self-rag.pdf
authors: [Akari Asai, Zeqiu Wu, Yizhong Wang, Avirup Sil, Hannaneh Hajishirzi]
year: 2023
tags: [self-rag, adaptive-retrieval, reflection-tokens, self-critique, citation]
sources: [05-asai2023-self-rag.pdf, 01-lewis2020-rag.pdf, 02-gao2023-survey.pdf, 04-liu2023-lost-in-middle.pdf]
updated: 2026-11-22
---

# Self-RAG: Learning to Retrieve, Generate, and Critique through Self-Reflection（Asai et al., 2023）

作者來自 University of Washington、Allen Institute for AI、IBM Research AI [05-asai2023-self-rag.pdf, p.1]。raw 檔是 arXiv 2310.11511 的 v1 版（2023 年 10 月 17 日），標示為 Preprint [05-asai2023-self-rag.pdf, p.1]。

## 一句話摘要

訓練一個 LLM，讓它自己決定「這裡需不需要查資料」，查到之後再自己評分「這份資料相不相關」「我寫的話有沒有根據」「整體回答有沒有用」；評分的方式，是讓模型產生特殊的 reflection tokens [05-asai2023-self-rag.pdf, Abstract, p.1]。詳見 [Self-RAG 方法頁](../methods/self-rag.md)。

## 這篇想解決什麼問題

- 一般的 RAG 不管需不需要都檢索固定數量的文件，可能拖累 LLM 的多樣用途，或產生沒有幫助的回答 [05-asai2023-self-rag.pdf, Abstract, p.1]。
- 不必要或離題的文件會導致低品質的生成 [05-asai2023-self-rag.pdf, §1, p.1]。
- 模型沒有被明確訓練去遵循文件中的事實，所以輸出不一定和檢索到的文件一致 [05-asai2023-self-rag.pdf, §1, p.1]。
- 一般的 RAG 只檢索一次，生成後也不會回頭檢查品質 [05-asai2023-self-rag.pdf, §1, p.2]。

## 核心方法

### 四種 reflection tokens

| 類型 | 問什麼 | 可能的輸出 | 出處 |
|---|---|---|---|
| Retrieve | 現在需要檢索嗎？ | yes／no／continue | [05-asai2023-self-rag.pdf, Table 1, p.4] |
| ISREL | 這份文件對回答問題有用嗎？ | relevant／irrelevant | [05-asai2023-self-rag.pdf, Table 1, p.4] |
| ISSUP | 我寫的這段話，有被文件支持嗎？ | fully／partially／no support | [05-asai2023-self-rag.pdf, Table 1, p.4] |
| ISUSE | 這個回答對問題有用嗎？ | 1–5 分 | [05-asai2023-self-rag.pdf, Table 1, p.4] |

後三種合稱 critique tokens [05-asai2023-self-rag.pdf, Table 1, p.4]。

### 推論時怎麼運作

1. 模型先判斷是否需要檢索 [05-asai2023-self-rag.pdf, §3.1, p.4]。
2. 如果需要，就呼叫 retriever 取回多份文件，並針對**每一份文件平行**產生一段回答 [05-asai2023-self-rag.pdf, §3.1, p.4]。
3. 對每份文件和回答，產生 ISREL、ISSUP、ISUSE 來評分 [05-asai2023-self-rag.pdf, Algorithm 1, p.4]。
4. 依照評分選出最好的那段，再繼續寫下一段（segment-level beam search）[05-asai2023-self-rag.pdf, §3.3, p.6]。
5. 在實驗中，一個 segment 就是一個句子 [05-asai2023-self-rag.pdf, §3.1, p.3]。

### 訓練時怎麼做

1. 先用 GPT-4 為訓練資料標出 reflection tokens，每一類收集 4k 到 20k 筆 [05-asai2023-self-rag.pdf, §3.2.1, p.5]。
2. 用這些資料訓練一個 critic 模型（以 Llama 2-7B 初始化），學會模仿 GPT-4 的判斷 [05-asai2023-self-rag.pdf, §3.2.1, p.5]。
3. 用 critic 模型離線地把 reflection tokens 和檢索到的文件插入訓練語料 [05-asai2023-self-rag.pdf, §3.2.2, p.5]。
4. 用一般的 next-token 目標訓練 generator，讓它自己學會產生 reflection tokens；推論時就不需要 critic 了 [05-asai2023-self-rag.pdf, §3, p.4]。
5. 作者說，這比 RLHF 的 PPO 訓練便宜很多，因為 critique 是離線算好的 [05-asai2023-self-rag.pdf, §3.2.2, p.6]。

### 推論時可以調整行為

- **檢索頻率**：可以設一個門檻，「需要檢索」的機率超過門檻才檢索 [05-asai2023-self-rag.pdf, §3.3, p.6]。
- **評分權重**：ISREL、ISSUP、ISUSE 的權重可以在推論時調整，不需要重新訓練 [05-asai2023-self-rag.pdf, §3.3, p.6]。
- **硬性限制**：例如只要產生 ISSUP=No support，就直接丟掉那段回答 [05-asai2023-self-rag.pdf, §3.3, p.6]。

## 關鍵結果（數字務必附出處）

### 主要結果（Table 2）

| 模型 | PopQA | TriviaQA | PubHealth | ARC-C | ASQA 引用 precision | 出處 |
|---|---|---|---|---|---|---|
| ChatGPT（不檢索） | 29.3 | 74.3 | 70.1 | 75.3 | – | [05-asai2023-self-rag.pdf, Table 2, p.8] |
| ChatGPT（加上檢索） | 50.8 | 65.7 | 54.7 | 75.3 | 65.1 | [05-asai2023-self-rag.pdf, Table 2, p.8] |
| Llama2-13B（加上檢索） | 45.7 | 47.0 | 30.2 | 26.0 | 2.3 | [05-asai2023-self-rag.pdf, Table 2, p.8] |
| Self-RAG 7B | 54.9 | 66.4 | 72.4 | 67.3 | 66.9 | [05-asai2023-self-rag.pdf, Table 2, p.8] |
| Self-RAG 13B | 55.8 | 69.3 | 74.5 | 73.1 | 70.3 | [05-asai2023-self-rag.pdf, Table 2, p.8] |

- 在所有任務上，Self-RAG 都是非商用模型中表現最好的 [05-asai2023-self-rag.pdf, §5.1, p.8]。
- 在 PubHealth、PopQA、傳記生成、ASQA（Rouge 和 MAUVE）上，甚至勝過 ChatGPT [05-asai2023-self-rag.pdf, §5.1, p.8]。
- 在 ASQA 的引用 precision 上也勝過 ChatGPT，這個指標衡量的是「模型的說法是否完全被引用的證據支持」[05-asai2023-self-rag.pdf, §5.1, p.8]。
- Llama2-FT 7B 用和 Self-RAG 相同的資料訓練，但沒有 reflection tokens，只在測試時加上檢索，表現仍然落後 Self-RAG；作者據此認為，進步不只是來自訓練資料 [05-asai2023-self-rag.pdf, §5.1, p.9]。

### 檢索不一定有幫助

- 在 PubHealth 和 ARC-Challenge 上，加上檢索的基準模型，並沒有比不檢索的版本明顯進步 [05-asai2023-self-rag.pdf, §5.1, p.8]。
- 例如 ChatGPT 加上檢索後，TriviaQA 從 74.3 降到 65.7，PubHealth 從 70.1 降到 54.7 [05-asai2023-self-rag.pdf, Table 2, p.8]。
- 作者認為，對於不能直接從文件中「複製或擷取片段」的任務，這些基準模型的幫助有限 [05-asai2023-self-rag.pdf, §5.1, p.8]。

### 消融實驗（7B，用 50k 筆訓練資料）

| 設定 | PopQA | PubHealth | ASQA（em） | 出處 |
|---|---|---|---|---|
| Self-RAG（完整） | 45.5 | 73.5 | 32.1 | [05-asai2023-self-rag.pdf, Fig.3a, p.9] |
| 訓練時不用 retriever | 43.6 | 67.8 | 31.0 | [05-asai2023-self-rag.pdf, Fig.3a, p.9] |
| 訓練時不用 critic | 42.6 | 72.0 | 18.1 | [05-asai2023-self-rag.pdf, Fig.3a, p.9] |
| 推論時不檢索 | 24.7 | 73.0 | – | [05-asai2023-self-rag.pdf, Fig.3a, p.9] |
| 一律只用第 1 份文件（像一般 RAG） | 41.8 | 73.1 | 28.6 | [05-asai2023-self-rag.pdf, Fig.3a, p.9] |

- 每個元件都很重要 [05-asai2023-self-rag.pdf, §5.2, p.9]。
- 像一般 RAG 那樣不管相關性、直接用最前面的文件，會讓 PopQA 和 ASQA 的表現大幅下降 [05-asai2023-self-rag.pdf, §5.2, p.9]。

### 其他發現

- **答案幾乎都有根據**：在答對的題目中，Self-RAG 只有 2% 的答案不在提供的文件裡；Llama2-chat 13B 是 18%，Alpaca 是 15% [05-asai2023-self-rag.pdf, App. C.1, p.20]。
- **文件不相關時會標示出來**：Self-RAG 會產生 ISREL=Irrelevant，其他 instruction-tuned 模型則繼續產生看似合理的答案 [05-asai2023-self-rag.pdf, App. C.1, p.20]。
- **權重的取捨**：提高 ISSUP 的權重，引用 precision 上升，但流暢度（MAUVE）下降 [05-asai2023-self-rag.pdf, §5.2, p.9–10]。
- **檢索頻率的取捨**：少檢索時，PubHealth 的表現下降較少，PopQA 下降較多 [05-asai2023-self-rag.pdf, §5.2, p.10]。
- **訓練資料**：資料越多，表現通常越好，在 PopQA 和 ASQA 上進步尤其明顯 [05-asai2023-self-rag.pdf, §5.2, p.10]。

## 限制與後續爭議

- **仍可能沒有根據**：Self-RAG 仍可能產生沒有被引用完全支持的輸出 [05-asai2023-self-rag.pdf, Ethical Concerns, p.11]。
- **依賴 GPT-4**：critic 的訓練資料是由 GPT-4 產生的；作者也承認，依賴商用 LLM 會增加 API 成本、降低可重現性 [05-asai2023-self-rag.pdf, §3.2.1, p.5]。
- **人工評估規模小**：PopQA 和傳記各只抽 50 筆 [05-asai2023-self-rag.pdf, §5.2, p.10]。
- **現成 retriever 的限制**：主要為 knowledge-intensive 任務訓練的現成 retriever，用在開放式生成上效果有限 [05-asai2023-self-rag.pdf, App. B.2, p.20]。
- **需要訓練**：要訓練 critic 和 generator 兩個模型，訓練時用了 4 張 A100 80GB [05-asai2023-self-rag.pdf, App. B.1, p.19]。

> ⚠️ **爭議／更新（原文內部不一致）**：正文說 critic 和 GPT-4 的判斷「在大多數類別上」一致度超過 90% [05-asai2023-self-rag.pdf, §3.2.1, p.5]；但附錄的表格中，Llama2-7B critic 只有 Retrieve（93.8）和 ISSUP（93.5）超過 90%，ISREL 是 80.2、ISUSE 是 73.5 [05-asai2023-self-rag.pdf, App. A.2, p.18]。附錄的文字則改說「大多數類別超過 80%」[05-asai2023-self-rag.pdf, App. A.2, p.18]。

> ⚠️ **爭議／更新（原文內部不一致）**：附錄 C.1 提到「Alpaca 30B」有 20% 的正確答案不在文件中 [05-asai2023-self-rag.pdf, App. C.1, p.20]，但同一段前面說評估的是 Alpaca 7B 和 13B，主實驗也沒有 30B 的模型 [05-asai2023-self-rag.pdf, App. C.1, p.20; Table 2, p.8]。引用這個 20% 時要註明。

- **其他小瑕疵**：訓練資料總數在正文是「150k」[05-asai2023-self-rag.pdf, §4.3, p.7]，附錄是 145,619 筆 [05-asai2023-self-rag.pdf, App. A.2, p.17]，應該是四捨五入的差異；Retrieve 的資料數寫成「1,2594」[05-asai2023-self-rag.pdf, App. A.1, p.17]，數字格式有誤。

> ⚠️ **爭議／更新**：[01-lewis2020-rag.pdf, §4.1, p.6] 把「檢索到的文件沒有答案時，仍有 11.8% 答對」視為生成式 RAG 的**優點**（能用上 parametric knowledge）；本篇則把「只有 2% 的正確答案不在文件中」視為**優點**，代表答案有根據、容易驗證 [05-asai2023-self-rag.pdf, App. C.1, p.20]。兩篇對「用模型自己的知識回答」的價值判斷不同。詳見 [Parametric 與 non-parametric memory](../concepts/parametric-vs-non-parametric-memory.md)。

## 和既有頁面的關係

- **02 的描述與本篇一致**：02 說 Self-RAG 用 retrieve 和 critic 兩類 reflection tokens，讓模型自己決定何時檢索 [02-gao2023-survey.pdf, §V-C, p.12]，和本篇相符 [05-asai2023-self-rag.pdf, Table 1, p.4]。
- **呼應 04**：04 發現文件放錯位置時，LLM 拿到文件反而比不給還差 [04-liu2023-lost-in-middle.pdf, §2.3, p.5]；本篇也觀察到，加上檢索後部分任務反而退步 [05-asai2023-self-rag.pdf, Table 2, p.8]。詳見 [Closed-book vs open-book](../comparisons/closed-book-vs-open-book.md)。
- **把 01 當作「傳統 RAG」**：本篇引用 Lewis et al. 2020 作為傳統 RAG 的代表 [05-asai2023-self-rag.pdf, §1, p.1]。

## 關鍵圖表說明

- **Fig.1**：左邊是一般 RAG（固定取 K 份文件），右邊是 Self-RAG（需要時才檢索、平行生成、評分後選最好的）；下方的「寫一篇暑假作文」例子不需要檢索 [05-asai2023-self-rag.pdf, Fig.1, p.2]。**最適合放進簡報的圖。**
- **Table 1**：四種 reflection tokens 的定義 [05-asai2023-self-rag.pdf, Table 1, p.4]。
- **Algorithm 1**：推論流程 [05-asai2023-self-rag.pdf, Algorithm 1, p.4]。
- **Table 2**：六個任務的主要結果 [05-asai2023-self-rag.pdf, Table 2, p.8]。
- **Fig.3**：消融實驗、權重調整的效果、檢索頻率和準確率的關係 [05-asai2023-self-rag.pdf, Fig.3, p.9]。

## 對初學者的重點

1. 不是每個問題都需要查資料，例如寫暑假作文就不用 [05-asai2023-self-rag.pdf, Fig.1, p.2]。
2. Self-RAG 讓模型自己判斷「要不要查」「查到的有沒有用」「我寫的有沒有根據」[05-asai2023-self-rag.pdf, Table 1, p.4]。
3. 每段回答都附上引用和「有沒有根據」的自我評估，讓人更容易查核事實 [05-asai2023-self-rag.pdf, §1, p.2]。
4. 檢索不一定有幫助，有時甚至讓 ChatGPT 表現變差 [05-asai2023-self-rag.pdf, Table 2, p.8]。

## 相關頁面

- [Self-RAG（方法）](../methods/self-rag.md)
- [Modular RAG](../methods/modular-rag.md)
- [Hallucination](../concepts/hallucination.md)
- [RAG 評估](../concepts/rag-evaluation.md)
- [Closed-book vs open-book](../comparisons/closed-book-vs-open-book.md)
- [Parametric 與 non-parametric memory](../concepts/parametric-vs-non-parametric-memory.md)
