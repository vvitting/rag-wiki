---
type: analogy
title: "比喻集"
tags: [analogy, teaching]
sources: [01-lewis2020-rag.pdf, 02-gao2023-survey.pdf]
updated: 2026-11-22
---

# 比喻集

> 每個比喻都要包含以下四項。比喻本身不需要引用，但「對應的技術事實」一定要引用。
>
> ```
> ### 比喻名稱
> - **比喻**：…
> - **對應到 RAG 的哪個部分**：…（連到概念頁）
> - **比喻的極限**：…
> - **對應的技術事實**：… [raw 檔名, 位置]
> ```

### 閉書考 vs 開書考

- **比喻**：閉書考只能靠腦袋裡背的東西作答；開書考可以先翻課本找到相關段落，再用自己的話寫答案。RAG 就是讓模型參加開書考。
- **對應到 RAG 的哪個部分**：[Parametric 與 non-parametric memory](concepts/parametric-vs-non-parametric-memory.md)、[Closed-book vs open-book](comparisons/closed-book-vs-open-book.md)
- **比喻的極限**：開書考的學生通常知道該翻哪一章；RAG 的 retriever 是靠向量相似度找資料，可能翻到不相關的頁面。另外，「學生」仍然需要自己的背景知識才看得懂課本。
- **對應的技術事實**：論文本身就把只靠參數的方法稱為「closed-book」，把檢索式方法稱為「open-book」[01-lewis2020-rag.pdf, §4.1, p.5]；而且檢索到的文件沒有答案時，RAG 在 NQ 上仍有 11.8% 答對，靠的是模型自己的知識 [01-lewis2020-rag.pdf, §4.1, p.6]。

### 圖書館員 + 作家

- **比喻**：圖書館員（retriever）聽完你的問題，從書架上拿來幾本最相關的書；作家（generator）讀完這些書，寫出一段回答給你。
- **對應到 RAG 的哪個部分**：[Retriever](concepts/retriever.md) 與 [Generator](concepts/generator.md)
- **比喻的極限**：原始 RAG 的圖書館員和作家是「一起訓練」的，作家寫得好不好會回頭影響圖書館員怎麼找書；真實的圖書館員不會這樣學習。
- **對應的技術事實**：原始 RAG 由 retriever 和 generator 兩個元件組成 [01-lewis2020-rag.pdf, §2, p.2–3]，並且端到端一起訓練 [01-lewis2020-rag.pdf, §2.4, p.3]。

### 換一本新版課本

- **比喻**：課本內容過時了，不用讓學生重新上一整年的課，只要換一本新版課本給他開書考就好。
- **對應到 RAG 的哪個部分**：[Parametric 與 non-parametric memory](concepts/parametric-vs-non-parametric-memory.md)（index hot-swapping）
- **比喻的極限**：如果學生腦中「背的」舊知識和新課本衝突，他不一定會相信課本；這種情況原始 RAG 論文沒有探討。
- **對應的技術事實**：把 index 從 2016 年版換成 2018 年版，就能讓 RAG 答對 2018 年的世界領袖（68%）；index 和年份不對應時只剩 4% [01-lewis2020-rag.pdf, §4.5, p.8]。

### 帶教科書 vs 把知識內化

- **比喻**：RAG 像考試時發給學生一本為這門課量身訂做的教科書，要用時再翻；fine-tuning 像學生花一整學期把知識讀進腦袋、內化成自己的東西。
- **對應到 RAG 的哪個部分**：[RAG vs fine-tuning](comparisons/rag-vs-fine-tuning.md)
- **比喻的極限**：真實的學生內化知識後，通常也記得出處；fine-tuning 後的模型則難以說明知識來自哪裡。而且兩種方法可以同時使用，不是二選一。
- **對應的技術事實**：這個比喻出自綜述本身：RAG 像「provide a model with a tailored textbook」，FT 像「a student internalizing knowledge over time」[02-gao2023-survey.pdf, §II-D, p.5]；而且兩者可以互補 [02-gao2023-survey.pdf, §II-D, p.5]。

### 讀長文章只記得頭尾

- **比喻**：一口氣讀一份很長的講義，最後通常只記得開頭和結尾，中間的內容印象模糊。塞太多文件給 LLM，也會發生類似的事。
- **對應到 RAG 的哪個部分**：[Context window](concepts/context-window.md)、[Reranking](concepts/reranking.md)
- **比喻的極限**：人會累、會分心，LLM 不會；這個現象背後的原因和人不同。Lost in the middle 的原始研究會在 ingest 04 時補充。
- **對應的技術事實**：綜述的描述是「Like humans, LLM tends to only focus on the beginning and end of long texts」[02-gao2023-survey.pdf, §IV-A, p.10]；所以有一種策略是把最相關的內容移到 prompt 的頭尾 [02-gao2023-survey.pdf, §II-B, p.4]。

## 相關頁面
- [目錄](index.md)
- [RAG 總覽](overview.md)
