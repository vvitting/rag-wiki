---
type: source
title: "From Local to Global: A GraphRAG Approach to Query-Focused Summarization"
raw: 06-edge2024-graphrag.pdf
authors: [Darren Edge, Ha Trinh, Newman Cheng, Joshua Bradley, Alex Chao, Apurva Mody, Steven Truitt, Dasha Metropolitansky, Robert Osazuwa Ness, Jonathan Larson]
year: 2024
tags: [graphrag, knowledge-graph, global-questions, summarization, llm-as-a-judge]
sources: [06-edge2024-graphrag.pdf, 02-gao2023-survey.pdf, 03-anthropic-contextual-retrieval.pdf, 04-liu2023-lost-in-middle.pdf, 07-es2023-ragas.pdf]
updated: 2026-11-22
---

# From Local to Global: A GraphRAG Approach to Query-Focused Summarization（Edge et al., 2024）

作者來自 Microsoft Research 等 Microsoft 團隊 [06-edge2024-graphrag.pdf, p.1]。raw 檔是 arXiv 2404.16130 的 v2 版（2025 年 2 月 19 日），標示為「Preprint. Under review.」[06-edge2024-graphrag.pdf, p.1]。

## 一句話摘要

一般的 RAG 很難回答「這整批資料的主要主題是什麼？」這種需要看完全部資料的問題。GraphRAG 先用 LLM 把文件整理成 knowledge graph，再把關係緊密的實體分群並寫好摘要；回答時，把所有群組的摘要彙整成答案 [06-edge2024-graphrag.pdf, Abstract, p.1]。詳見 [GraphRAG 方法頁](../methods/graphrag.md)。

## 這篇想解決什麼問題

- 一般的 RAG（作者稱為 vector RAG）適合回答「答案集中在少數幾份文件裡」的問題 [06-edge2024-graphrag.pdf, §1, p.2]。
- 但它無法回答 sensemaking（理解全局）類的問題，也就是需要理解整個資料集的問題，例如「資料集的主要主題是什麼？」[06-edge2024-graphrag.pdf, Abstract, p.1; §1, p.2]。
- 這類問題本質上是「針對問題做摘要」（query-focused summarization，QFS），不是單純的檢索 [06-edge2024-graphrag.pdf, Abstract, p.1]。
- 過去的 QFS 方法又無法擴展到 RAG 系統通常處理的資料量 [06-edge2024-graphrag.pdf, Abstract, p.1]。

## 核心方法

詳見 [GraphRAG 方法頁](../methods/graphrag.md)。

### 建立 index（事前準備）

1. 把文件切成 text chunk [06-edge2024-graphrag.pdf, §3.1.1, p.4]。
2. 用 LLM 從每個 chunk 抽出實體（entity）、實體之間的關係（relationship），以及關於實體的事實陳述（claim），並各自寫一段簡短描述 [06-edge2024-graphrag.pdf, §3.1.2, p.4–5]。
3. 把它們組成 knowledge graph：實體是節點，關係是邊 [06-edge2024-graphrag.pdf, §3.1.3, p.5]。
4. 用 Leiden 演算法把圖分成階層式的社群（community），也就是一群群關係緊密的實體 [06-edge2024-graphrag.pdf, §3.1.4, p.5]。
5. 用 LLM 為每個社群寫一份報告式的摘要，由下往上，高層的摘要會整合低層的摘要 [06-edge2024-graphrag.pdf, §3.1.5, p.6]。

### 回答問題（map-reduce）

1. **準備**：把社群摘要隨機打亂，切成固定大小的塊；這樣相關資訊會分散在各塊中，而不是集中在單一個 context window 裡（可能因此被漏掉）[06-edge2024-graphrag.pdf, §3.1.6, p.6]。
2. **Map**：每一塊平行產生一個部分答案，並讓 LLM 為這個答案的幫助程度打 0–100 分，0 分的直接丟掉 [06-edge2024-graphrag.pdf, §3.1.6, p.6]。
3. **Reduce**：依分數由高到低，把部分答案放進新的 context window，直到放滿，再產生最終的全局答案 [06-edge2024-graphrag.pdf, §3.1.6, p.6]。

### 評估方法

- **出題**：沒有標準答案，所以先讓 LLM 依資料集的描述，想像 5 種使用者、每人 5 個任務、每個任務 5 個問題，每個資料集共 125 題 [06-edge2024-graphrag.pdf, §3.2, p.6–7]。
- **評分**：用 LLM 當評審（LLM-as-a-judge），兩兩比較兩個系統的答案 [06-edge2024-graphrag.pdf, §3.3, p.7]。
- **四個標準**：comprehensiveness（全面性）、diversity（多樣性）、empowerment（幫助讀者做判斷）、directness（直接、簡潔；這是對照用的標準）[06-edge2024-graphrag.pdf, §3.3, p.7–8]。
- **驗證**：再用另一種方法驗證：從答案中抽出事實陳述（claim），以 claim 的數量衡量全面性，以 claim 的群集數衡量多樣性 [06-edge2024-graphrag.pdf, §4.2, p.9]。

## 關鍵結果（數字務必附出處）

### 資料與規模

| 資料集 | 規模 | 圖的大小 | 出處 |
|---|---|---|---|
| Podcast 逐字稿 | 1669 個 600-token chunk，約 100 萬 tokens | 8,564 個節點、20,691 條邊 | [06-edge2024-graphrag.pdf, §4.1.1, p.8; §5.1, p.9] |
| 新聞文章 | 3197 個 600-token chunk，約 170 萬 tokens | 15,754 個節點、19,520 條邊 | [06-edge2024-graphrag.pdf, §4.1.1, p.8; §5.1, p.9] |

- 為 Podcast 資料集建 index，花了 281 分鐘（使用 gpt-4-turbo）[06-edge2024-graphrag.pdf, §4.1.3, p.9]。

### GraphRAG vs 一般 RAG（實驗一：LLM 評審的勝率）

- **全面性**：GraphRAG 等全局方法對一般 RAG 的勝率，在 Podcast 上是 72%–83%，在新聞上是 72%–80% [06-edge2024-graphrag.pdf, §5.1, p.9]。
- **多樣性**：勝率在 Podcast 上是 75%–82%，在新聞上是 62%–71% [06-edge2024-graphrag.pdf, §5.1, p.9]。
- **直接性**：一般 RAG 的答案在所有比較中都最直接 [06-edge2024-graphrag.pdf, §5.1, p.9]。
- **幫助判斷（empowerment）**：結果好壞參半 [06-edge2024-graphrag.pdf, §5.1, p.9]。分析顯示，能否提供具體例子、引言和引用，是關鍵 [06-edge2024-graphrag.pdf, §5.1, p.10]。

### 用 claim 驗證（實驗二）

| 方法 | 新聞：平均 claim 數 | Podcast：平均 claim 數 | 出處 |
|---|---|---|---|
| GraphRAG 根層摘要（C0） | 34.18 | 32.21 | [06-edge2024-graphrag.pdf, Table 3, p.11] |
| 直接對原文做摘要（TS） | 32.89 | 31.39 | [06-edge2024-graphrag.pdf, Table 3, p.11] |
| 一般 RAG（SS） | 25.23 | 26.50 | [06-edge2024-graphrag.pdf, Table 3, p.11] |

- 所有全局方法的全面性都高於一般 RAG，差異都達到統計顯著 [06-edge2024-graphrag.pdf, §5.2, p.11]。
- 在雙方有明確勝負的比較中，LLM 評審和 claim 指標的判斷一致：全面性是 78%，多樣性是 69%–70% [06-edge2024-graphrag.pdf, §5.2, p.11]。

### 成本

- 根層社群摘要（C0）每次查詢需要的 tokens，比直接對原文做摘要少 97% 以上 [06-edge2024-graphrag.pdf, §5.1, p.10]。
- C0 仍保有對一般 RAG 的優勢：全面性勝率 72%、多樣性勝率 62% [06-edge2024-graphrag.pdf, §5.1, p.10]。

### Context window 越大越好嗎？

- gpt-4-turbo 有 128k tokens 的 context window，但考慮到「lost in the middle」，作者在一般 RAG（SS）上測試了 8k、16k、32k、64k 四種大小，再把最好的大小統一用在所有方法上 [06-edge2024-graphrag.pdf, App. C, p.19]。
- 結果最小的 8k 在全面性上全面勝出（平均勝率 58.1%），在多樣性和幫助判斷上則差不多 [06-edge2024-graphrag.pdf, App. C, p.19]。

## 限制與後續爭議

- **評估範圍**：只測了兩個約 100 萬 tokens 的資料集 [06-edge2024-graphrag.pdf, §6.1, p.11]。
- **沒有比較捏造率**：作者說，比較 fabrication rate 能讓分析更完整 [06-edge2024-graphrag.pdf, §6.1, p.11]。
- **用 LLM 評審**：沒有標準答案，所以靠 LLM 兩兩比較 [06-edge2024-graphrag.pdf, §3.3, p.7]。
- **實體比對很粗糙**：用完全相同的字串來比對實體，不過作者說，重複的實體通常會在後面的步驟被歸在一起 [06-edge2024-graphrag.pdf, §3.1.3, p.5]。
- **輸出的風險**：如果答案沒有正確反映原始資料，就會對後續的判斷造成風險；使用時應清楚揭露 AI 的使用和可能出錯 [06-edge2024-graphrag.pdf, §6.2, p.12]。
- **相較之下的好處**：對全局問題，一般 RAG 可能把「抽樣找到的幾個事實」錯誤地當成全局摘要來呈現；GraphRAG 有機會減輕這種風險 [06-edge2024-graphrag.pdf, §6.2, p.12]。

> ⚠️ **爭議／更新**：本篇說較長的 chunk 會讓「出現在 chunk **前段**的資訊」比較難被找到，並引用了 04 和 Kuratov et al. 2024 [06-edge2024-graphrag.pdf, §3.1.1, p.4; References, p.14]。但 04 的發現是：開頭的資訊用得最好（primacy bias），**中間**的資訊最容易被忽略 [04-liu2023-lost-in-middle.pdf, Abstract, p.1]。Kuratov et al. 不在 raw/ 中，無法核對它是否支持「前段」的說法。

> ⚠️ **爭議／更新**：本篇說 RAGAS 的 context relevance、faithfulness、answer relevance 是「一般 vector RAG 適用、但和全局理解無關」的評估標準 [06-edge2024-graphrag.pdf, §2.4, p.4]；02 則把這三個列為 RAG 的主要品質分數 [02-gao2023-survey.pdf, §VI-C, p.12]。RAGAS 原始論文的設定確實是標準 RAG [07-es2023-ragas.pdf, §3, p.2]。兩者適用的問題類型不同。詳見 [RAG 評估](../concepts/rag-evaluation.md)。

> ⚠️ **爭議／更新**：本篇的主要結果靠 LLM 兩兩比較答案得出；但 [07-es2023-ragas.pdf, Table 1, p.5] 發現，直接讓 ChatGPT 從兩個答案中挑選，和人類判斷一致的比例只有 0.40–0.54，而且答案的順序會影響判斷 [07-es2023-ragas.pdf, §2, p.2]。本篇的 raw 檔中沒有找到處理答案順序的說明。不過本篇用的是 GPT-4 [06-edge2024-graphrag.pdf, §1, p.2]（實驗用的是 gpt-4-turbo [06-edge2024-graphrag.pdf, §4.1.3, p.9]），也用 claim 指標交叉驗證過（69%–78% 一致）[06-edge2024-graphrag.pdf, §5.2, p.11]。詳見 [RAG 評估](../concepts/rag-evaluation.md)。

> ⚠️ **爭議／更新**：本篇的核心就是「以摘要為基礎的 index」，而且在全局問題上勝過一般 RAG [06-edge2024-graphrag.pdf, §5.1, p.9]；但 [03-anthropic-contextual-retrieval.pdf, p.5] 發現以摘要為基礎的 indexing 表現很差。兩者的任務不同：03 衡量的是「能不能找到特定的 chunk」，本篇衡量的是「全局問題的答案夠不夠全面」。詳見 [Chunking](../concepts/chunking.md)。

## 和既有頁面的關係

- **呼應 04**：作者因為考慮到 lost in the middle，才為一般 RAG 測試不同大小的 context window；結果 8k 在全面性上最好，其他標準則差不多 [06-edge2024-graphrag.pdf, App. C, p.19]。回答問題時把社群摘要打亂、分散到多個 context window，也是為了避免相關資訊集中在單一 context window 而被漏掉 [06-edge2024-graphrag.pdf, §3.1.6, p.6]。
- **對 02 的 knowledge graph 的補充**：02 說 knowledge graph 這類結構化資料「通常經過驗證、資訊較精確」[02-gao2023-survey.pdf, §III-A, p.7]；GraphRAG 的 knowledge graph 則是 LLM 從文字中抽出來的，作者自己稱之為一種摘要 [06-edge2024-graphrag.pdf, §3.1.3, p.5]，兩者性質不同。
- **把一般 RAG 稱為 naive RAG**：本篇的圖表把一般 RAG（SS）稱為「naïve RAG」[06-edge2024-graphrag.pdf, Fig.2, p.10]。

## 關鍵圖表說明

- **Fig.1**：GraphRAG 的流程。從原始文件 → chunk → 實體與關係 → knowledge graph → 社群 → 社群摘要 → 社群答案 → 全局答案 [06-edge2024-graphrag.pdf, Fig.1, p.4]。**最適合放進簡報的圖。**
- **Table 1**：LLM 產生的使用者、任務和問題範例 [06-edge2024-graphrag.pdf, Table 1, p.7]。
- **Fig.2**：六種方法兩兩比較的勝率 [06-edge2024-graphrag.pdf, Fig.2, p.10]。
- **Table 2**：各層級社群摘要的數量和 token 數 [06-edge2024-graphrag.pdf, Table 2, p.10]。
- **Table 5**：同一題「哪些公眾人物在娛樂新聞中反覆出現？」，GraphRAG 和一般 RAG 的答案對照 [06-edge2024-graphrag.pdf, App. D, p.20]。**很適合用來說明兩者的差別。**

## 對初學者的重點

1. 一般 RAG 擅長「找特定事實」，不擅長「看完整批資料再總結」[06-edge2024-graphrag.pdf, §1, p.2]。
2. GraphRAG 先把資料整理成「誰和誰有關係」的圖，再分群寫摘要 [06-edge2024-graphrag.pdf, §1, p.2]。
3. 回答全局問題時，GraphRAG 的答案更全面、更多元；但一般 RAG 的答案更直接 [06-edge2024-graphrag.pdf, §5.1, p.9]。
4. 代價是建 index 很花時間和 LLM 呼叫：約 100 萬 tokens [06-edge2024-graphrag.pdf, §4.1.1, p.8] 的資料，花了 281 分鐘 [06-edge2024-graphrag.pdf, §4.1.3, p.9]。

## 相關頁面

- [GraphRAG（方法）](../methods/graphrag.md)
- [Naive RAG](../methods/naive-rag.md)
- [RAG 評估](../concepts/rag-evaluation.md)
- [Context window](../concepts/context-window.md)
- [Chunking](../concepts/chunking.md)
- [04 Lost in the Middle](04-liu2023-lost-in-middle.md)
- [術語表](../glossary.md)
