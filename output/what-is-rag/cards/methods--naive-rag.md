---
page: wiki/methods/naive-rag.md
---
# 證據卡：Naive RAG

## 重點摘錄
> 最基本的 RAG 流程：先把文件建成 index，收到問題時找出最相關的 top-k 個 chunk，再把問題和 chunk 一起交給 LLM 產生答案。也被稱為「Retrieve-Read」框架 [02-gao2023-survey.pdf, §II-A, p.3]。
> 2. **Indexing（續）**：因為 language model 的 context 有限制，所以把文字切成較小的 [chunk](../concepts/chunking.md)，用 embedding model 轉成向量，存進 vector database [02-gao2023-survey.pdf, §II-A, p.3]。
> 3. **Retrieval**：用同一個 encoding model 把問題轉成向量，計算它和所有 chunk 向量的相似度，取出最相似的 top K 個 chunk [02-gao2023-survey.pdf, §II-A, p.3]。
> 4. **Generation**：把問題和選出的文件組成一個 prompt，交給 LLM 產生回答 [02-gao2023-survey.pdf, §II-A, p.3]。
> - **檢索的問題**：precision 和 recall 都不夠好，會選到不對或不相關的 chunk，也可能漏掉關鍵資訊 [02-gao2023-survey.pdf, §II-A, p.3]。
> - **生成的問題**：模型可能 [hallucinate](../concepts/hallucination.md)，產生檢索內容沒有支持的說法；輸出也可能離題、有害或帶有偏見 [02-gao2023-survey.pdf, §II-A, p.3]。
> - **回答不了全局問題**：像「這批資料的主要主題是什麼？」這種需要理解整個資料集的問題，一般的 vector RAG 無法回答 [06-edge2024-graphrag.pdf, Abstract, p.1; §1, p.2]。它可能把「抽樣找到的幾個事實」錯誤地當成全局摘要 [06-edge2024-graphrag.pdf, §6.2, p.12]。解法見 [GraphRAG](graphrag.md)。
> 這些缺點正是發展 [Advanced RAG](advanced-rag.md) 和 [Modular RAG](modular-rag.md) 的原因 [02-gao2023-survey.pdf, §II, p.2]。
> **給初學者的理解方式**：兩者都是「先查再寫」。今天大家常說的「RAG」比較接近 Naive RAG，也就是把檢索結果塞進 LLM 的 prompt [02-gao2023-survey.pdf, §II-A, p.3]；原始 RAG 則是把整個系統一起訓練 [01-lewis2020-rag.pdf, §2.4, p.3]。

## ⚠️ 爭議
> > ⚠️ **爭議／更新**：「勝過沒有 RAG 的 LLM」是 02 的整體概括 [02-gao2023-survey.pdf, §II, p.2]，但有兩份實驗顯示並非總是如此：
> > - [04-liu2023-lost-in-middle.pdf, Table 6, p.18; Table 1, p.5]：GPT-3.5-Turbo 在 20 份文件、答案位於中間時，準確率是 53.8%，低於完全不給文件的 56.1%。
> > - [05-asai2023-self-rag.pdf, Table 2, p.8]：ChatGPT 加上檢索後，PubHealth 從 70.1 降到 54.7，TriviaQA 從 74.3 降到 65.7。

## 可以用在
- 怎麼運作（06）：三步驟的細節
- 進階變體（09）：Naive RAG 的缺點
- 總結（12）：⚠️ 不一定勝過不檢索
