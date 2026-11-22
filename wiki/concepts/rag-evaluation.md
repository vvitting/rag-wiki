---
type: concept
title: "RAG 評估"
tags: [concept, evaluation, metrics, benchmark]
sources: [02-gao2023-survey.pdf, 01-lewis2020-rag.pdf, 03-anthropic-contextual-retrieval.pdf, 04-liu2023-lost-in-middle.pdf, 05-asai2023-self-rag.pdf, 06-edge2024-graphrag.pdf, 07-es2023-ragas.pdf]
updated: 2026-11-22
---

# RAG 評估

## 白話說明

評估 RAG 要分開看兩件事：「找得好不好」（retrieval quality）和「寫得好不好」（generation quality）[02-gao2023-survey.pdf, §VI-B, p.12]。

## 為什麼重要

- 過去評估 RAG，多半只看它在特定任務上的表現，專門評估 RAG 特性的研究很少 [02-gao2023-survey.pdf, §VI-B, p.12]。
- 評估檢索品質，是判斷 retriever 找來的 context 是否有效的關鍵 [02-gao2023-survey.pdf, §VI-B, p.12]。

## 評估方式總覽

> 下表是 wiki 依 raw/ 的來源整理的評估方式比較，每一列都附上出處。

| 評估方式 | 需要標準答案嗎 | 評估什麼 | 用過的來源 |
|---|---|---|---|
| 任務指標（EM、F1、BLEU、ROUGE、Accuracy） | 需要 [02-gao2023-survey.pdf, §VI-B, p.12] | 最終答案和標準答案的吻合程度 | 01 [01-lewis2020-rag.pdf, §3, p.4–5] |
| 只評估檢索（recall@k） | 需要知道哪些文件相關 [03-anthropic-contextual-retrieval.pdf, p.7] | 相關文件有沒有被找到 | 03 [03-anthropic-contextual-retrieval.pdf, p.7] |
| 位置效應測試 | 需要 [04-liu2023-lost-in-middle.pdf, §2.1, p.3] | 相關資訊放在不同位置時，表現差多少 | 04 [04-liu2023-lost-in-middle.pdf, §1, p.3] |
| 引用品質（citation precision／recall、FactScore） | 需要證據或參考資料 [05-asai2023-self-rag.pdf, §4.1, p.7] | 說法有沒有被引用的證據支持 | 05 [05-asai2023-self-rag.pdf, §4.1, p.7] |
| RAGAS（拆成小步驟讓 LLM 評分） | 不需要 [07-es2023-ragas.pdf, Abstract, p.1] | faithfulness、answer relevance、context relevance | 07 [07-es2023-ragas.pdf, §3, p.3] |
| LLM 兩兩比較（LLM-as-a-judge） | 不需要 [06-edge2024-graphrag.pdf, §2.4, p.4] | 全面性、多樣性等相對好壞 | 06 [06-edge2024-graphrag.pdf, §3.3, p.7] |
| 人工評估 | 不需要，但需要人力 [07-es2023-ragas.pdf, §4, p.4] | 依研究設計而定 | 01、05、07 [01-lewis2020-rag.pdf, §3.3, p.5] [05-asai2023-self-rag.pdf, §5.2, p.10] [07-es2023-ragas.pdf, §4, p.4] |

## 運作方式

### 兩個評估目標

| 目標 | 看什麼 | 常用指標 | 出處 |
|---|---|---|---|
| Retrieval quality | retriever 找來的 context 有沒有用 | Hit Rate、MRR、NDCG | [02-gao2023-survey.pdf, §VI-B, p.12] |
| Generation quality | generator 能不能根據 context 寫出連貫、相關的答案 | 沒有標準答案時看 faithfulness、relevance、是否有害；有標準答案時看準確度 | [02-gao2023-survey.pdf, §VI-B, p.12] |

### 三個品質分數（quality scores）

- **Context relevance**：檢索到的 context 是否精確、切題 [02-gao2023-survey.pdf, §VI-C, p.12]。
- **Answer faithfulness**：答案是否忠於檢索到的 context，沒有互相矛盾 [02-gao2023-survey.pdf, §VI-C, p.12]。
- **Answer relevance**：答案是否直接回答了問題 [02-gao2023-survey.pdf, §VI-C, p.12]。

### 四種能力（required abilities）

- **Noise robustness**：遇到和問題有關、但沒有實質資訊的文件時，能不能不被干擾 [02-gao2023-survey.pdf, §VI-C, p.12]。
- **Negative rejection**：檢索到的文件沒有答案時，能不能拒絕回答 [02-gao2023-survey.pdf, §VI-C, p.12]。
- **Information integration**：能不能整合多份文件的資訊，回答複雜的問題 [02-gao2023-survey.pdf, §VI-C, p.12]。
- **Counterfactual robustness**：能不能辨認並忽略文件中已知的錯誤 [02-gao2023-survey.pdf, §VI-C, p.12]。

Context relevance 和 noise robustness 用來評估檢索；其餘五項用來評估生成 [02-gao2023-survey.pdf, §VI-C, p.12]。

### 三個品質分數怎麼自動算？RAGAS

RAGAS 讓 LLM 計算上面三個品質分數，不需要標準答案 [07-es2023-ragas.pdf, Abstract, p.1; §3, p.3]：

- **Faithfulness**：把答案拆成小陳述，算有幾成能從 context 推論出來 [07-es2023-ragas.pdf, §3, p.3]。
- **Answer relevance**：根據答案反推問題，再和原始問題比對 embedding 相似度 [07-es2023-ragas.pdf, §3, p.3]。
- **Context relevance**：算 context 中有幾成句子是回答問題必要的 [07-es2023-ragas.pdf, §3, p.4]。

和人類判斷的一致度分別是 0.95、0.78、0.70，都高於直接讓 ChatGPT 打分數或挑選 [07-es2023-ragas.pdf, Table 1, p.5]。詳見 [RAGAS](ragas.md)。

### 實例：只評估檢索

- 03 用「1 − recall@20」當評估指標，也就是「相關文件沒出現在前 20 個 chunk 裡」的比例 [03-anthropic-contextual-retrieval.pdf, p.7]。
- 這個指標只衡量檢索，不衡量最終答案。03 主張檢索準確度的提升會直接轉化為下游任務更好的表現 [03-anthropic-contextual-retrieval.pdf, p.2]，但 raw 檔中沒有附上答案品質的數字 [03-anthropic-contextual-retrieval.pdf, p.7–11]。
- 03 的建議是：一定要做評估（always run evals）[03-anthropic-contextual-retrieval.pdf, p.9]。

### 實例：評估「模型會不會用 context」

- 04 提出一種評估方式：要宣稱模型能好好使用長 context，就必須證明相關資訊放在哪個位置都不太影響表現，也就是最好和最差情況的差距要很小 [04-liu2023-lost-in-middle.pdf, §1, p.3]。
- 04 也把結果和兩個基準比較：closed-book（不給文件）和 oracle（只給答案文件）[04-liu2023-lost-in-middle.pdf, §2.3, p.5]。
- **Noise robustness 的實例**：用「和問題相關但沒有答案」的文件當干擾時，模型表現比用隨機文件當干擾還差 [04-liu2023-lost-in-middle.pdf, App. B, p.14]。這正對應 02 對 noise robustness 的定義：處理「相關但沒有實質資訊」的文件 [02-gao2023-survey.pdf, §VI-C, p.12]。

### 實例：評估「有沒有根據」與引用品質

Self-RAG 論文用了幾個衡量「有沒有根據」的指標 [05-asai2023-self-rag.pdf, §4.1, p.7]：

- **FactScore**：評估傳記生成的事實性 [05-asai2023-self-rag.pdf, §4.1, p.7]。
- **引用 precision 和 recall**：用在長篇問答 ASQA；precision 衡量「模型的說法是否完全被引用的證據支持」[05-asai2023-self-rag.pdf, §4.1, p.7; §5.1, p.8]。
- **短答案的判分方式**：只要標準答案出現在模型輸出中就算對，不要求完全一致（不是 Exact Match）[05-asai2023-self-rag.pdf, §4.1, p.7]。
- **人工評估 S&P**：答案是否合理（plausible），以及證據是否足以驗證答案（supported）[05-asai2023-self-rag.pdf, §5.2, p.10]。

**和綜述的三個品質分數對照**（wiki 的整理，依兩篇的定義比對 [02-gao2023-survey.pdf, §VI-C, p.12] [05-asai2023-self-rag.pdf, Table 1, p.4]）：

| 02 的品質分數 | 定義 | 05 的對應 reflection token | 定義 |
|---|---|---|---|
| Context relevance | 檢索到的 context 是否精確、切題 [02-gao2023-survey.pdf, §VI-C, p.12] | ISREL | 文件是否提供解決問題的有用資訊 [05-asai2023-self-rag.pdf, Table 1, p.4] |
| Answer faithfulness | 答案是否忠於 context [02-gao2023-survey.pdf, §VI-C, p.12] | ISSUP | 輸出中值得查證的說法，是否都被文件支持 [05-asai2023-self-rag.pdf, Table 1, p.4] |
| Answer relevance | 答案是否直接回答問題 [02-gao2023-survey.pdf, §VI-C, p.12] | ISUSE | 回答對問題是否有用（不論是否符合事實）[05-asai2023-self-rag.pdf, App. A.1, p.17] |

差別在於：02 列的是「評估者」用的指標；Self-RAG 則讓模型在生成過程中**自己**評估這些面向 [05-asai2023-self-rag.pdf, §3.1, p.4]。

### 實例：沒有標準答案時怎麼評估（LLM-as-a-judge）

GraphRAG 論文要評估「這批資料的主要主題是什麼？」這類全局問題，但這種問題沒有標準答案 [06-edge2024-graphrag.pdf, §3.3, p.7]。

- **自動出題**：讓 LLM 依資料集的描述，想像使用者和他們的任務，再產生問題 [06-edge2024-graphrag.pdf, §3.2, p.6]。
- **兩兩比較**：讓 LLM 看同一題的兩個答案，依標準選出比較好的那個，或判定平手；每次比較重複 5 次再平均 [06-edge2024-graphrag.pdf, §3.3, p.8; Fig.2, p.10]。
- **四個標準**：comprehensiveness（全面性）、diversity（多樣性）、empowerment（幫助讀者做判斷），以及當作對照組的 directness（直接、簡潔）[06-edge2024-graphrag.pdf, §3.3, p.7–8]。
- **為什麼要有對照組**：directness 和全面性、多樣性本來就互相衝突，所以不應該有任何方法四項全勝；用它來檢查結果是否合理 [06-edge2024-graphrag.pdf, §3.3, p.8]。
- **用另一種方法驗證**：從答案中抽出事實陳述（claim），用 claim 的數量和群集數重新衡量；在雙方有明確勝負的比較中，和 LLM 評審的判斷一致的比例是 78%（全面性）和 69%–70%（多樣性）[06-edge2024-graphrag.pdf, §5.2, p.11]。

> ⚠️ **爭議／更新**：[02-gao2023-survey.pdf, §VI-C, p.12] 把 context relevance、answer faithfulness、answer relevance 列為 RAG 的三個主要品質分數；[06-edge2024-graphrag.pdf, §2.4, p.4] 則認為這三個（以 RAGAS 為例）只適用於一般的 vector RAG，和全局理解類的問題無關。RAGAS 原始論文的設定也確實是「一個問題 → 檢索 context → 生成答案」的標準 RAG [07-es2023-ragas.pdf, §3, p.2]。兩者適用的問題類型不同：找特定事實時用前者，理解整批資料時則需要全面性、多樣性這類標準。

### LLM 當評審，可靠嗎？

> ⚠️ **爭議／更新**：[07-es2023-ragas.pdf, Table 1, p.5] 發現，直接讓 ChatGPT 從兩個答案中挑出比較好的那個（GPT Ranking），和人類判斷一致的比例只有 0.40–0.54；07 也提醒，答案的**順序**會影響 LLM 的判斷 [07-es2023-ragas.pdf, §2, p.2]。而 [06-edge2024-graphrag.pdf, §3.3, p.7–8] 的主要結果，正是用 LLM 兩兩比較答案得出的，06 的 raw 檔中沒有找到處理答案順序的說明。
> 但兩者條件不同：06 使用 GPT-4 [06-edge2024-graphrag.pdf, §1, p.2]（實驗用的是 gpt-4-turbo [06-edge2024-graphrag.pdf, §4.1.3, p.9]），07 的基準用的是 ChatGPT [07-es2023-ragas.pdf, §5, p.5]；06 也另外用 claim 指標驗證過，兩種方法判斷一致的比例是 69%–78% [06-edge2024-graphrag.pdf, §5.2, p.11]。

> 可以得到的實用原則（每一點都有出處）：

1. **把判斷拆成小步驟**，比直接要 LLM 打分數或挑選準確 [07-es2023-ragas.pdf, §5, p.5]。
2. **加入對照標準**，檢查結果是否合理，例如 06 的 directness [06-edge2024-graphrag.pdf, §3.3, p.8]。
3. **重複多次再平均**，以應對 LLM 輸出的隨機性 [06-edge2024-graphrag.pdf, §3.3, p.8]。
4. **用另一種方法交叉驗證**，例如人工標註 [07-es2023-ragas.pdf, §4, p.4] 或 claim 指標 [06-edge2024-graphrag.pdf, §4.2, p.9]。

### 傳統的任務指標

- 問答常用 EM 和 F1，事實查核常用 Accuracy，答案品質也常用 BLEU 和 ROUGE [02-gao2023-survey.pdf, §VI-B, p.12]。
- 原始 RAG 就是用 Exact Match、BLEU、ROUGE-L、Label Accuracy，再加上人工評估 [01-lewis2020-rag.pdf, §3, p.4–5]。

### Benchmark 與工具

| 名稱 | 類型 | 評估面向 | 出處 |
|---|---|---|---|
| RGB | benchmark | noise robustness、negative rejection、information integration、counterfactual robustness | [02-gao2023-survey.pdf, Table IV, p.15] |
| RECALL | benchmark | counterfactual robustness | [02-gao2023-survey.pdf, Table IV, p.15] |
| CRUD | benchmark | 創意生成、知識問答、錯誤修正、摘要 | [02-gao2023-survey.pdf, Table IV, p.15] |
| RAGAS | 工具 | context relevance、faithfulness、answer relevance | [02-gao2023-survey.pdf, Table IV, p.15] |
| ARES | 工具 | context relevance、faithfulness、answer relevance | [02-gao2023-survey.pdf, Table IV, p.15] |
| TruLens | 工具 | context relevance、faithfulness、answer relevance | [02-gao2023-survey.pdf, Table IV, p.15] |

- RAGAS、ARES、TruLens 這類自動化工具，是用 LLM 來評判品質分數 [02-gao2023-survey.pdf, §VI-D, p.14]。RAGAS 的原始論文見 [RAGAS](ragas.md)。
- RAGAS 也整合進 LlamaIndex 和 LangChain，方便開發者放進既有的流程 [07-es2023-ragas.pdf, §1, p.2]。

## 各論文怎麼說

- **[02-gao2023-survey.pdf](../sources/02-gao2023-survey.md)**：作者坦承，這些指標都是從相關研究借來的傳統指標，還不是成熟或標準化的 RAG 評估方式 [02-gao2023-survey.pdf, §VI-C, p.14]。
- **[01-lewis2020-rag.pdf](../sources/01-lewis2020-rag.md)**：用人工評估比較事實性（factuality）和具體性（specificity）[01-lewis2020-rag.pdf, §3.3, p.5]。
- **[07-es2023-ragas.pdf](../sources/07-es2023-ragas.md)**：常見的評估方式各有問題：perplexity 不一定能預測實際任務的表現，封閉模型也拿不到機率；問答資料集多半只有簡短的擷取式答案，不一定能代表實際使用情況 [07-es2023-ragas.pdf, §1, p.1]。

## 相關頁面

- [RAGAS](ragas.md)
- [Hallucination](hallucination.md)
- [Retriever](retriever.md)
- [Generator](generator.md)
- [術語表](../glossary.md)
