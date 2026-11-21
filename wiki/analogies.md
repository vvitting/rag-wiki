---
type: analogy
title: "比喻集"
tags: [analogy, teaching]
sources: [01-lewis2020-rag.pdf, 02-gao2023-survey.pdf, 03-anthropic-contextual-retrieval.pdf, 04-liu2023-lost-in-middle.pdf]
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
- **對應到 RAG 的哪個部分**：[Lost in the middle](concepts/lost-in-the-middle.md)、[Reranking](concepts/reranking.md)
- **比喻的極限**：人會累、會分心，LLM 不會。原始研究的作者也說，Transformer 的 self-attention 理論上能同等地取用任何位置，所以出現這種「像人一樣」的效應其實令人意外，背後的原因還不清楚。
- **對應的技術事實**：心理學稱這個現象為「序列位置效應」（serial-position effect）：人最記得一串項目的第一個和最後一個 [04-liu2023-lost-in-middle.pdf, §6.3, p.10]。04 在 LLM 上也看到類似的 U 形曲線：GPT-3.5-Turbo 在 20 份文件中，答案在第 1 份時是 75.8%，在第 10 份時只有 53.8% [04-liu2023-lost-in-middle.pdf, Table 6, p.18]。對 self-attention 的說明見 [04-liu2023-lost-in-middle.pdf, §6.3, p.11]。

### 書包塞太滿

- **比喻**：考試可以帶參考資料進場，但書包塞了 50 本書，你只會翻最上面和最下面那幾本，中間的根本沒時間看。帶 20 本挑過、排好的書，比帶 50 本亂放的書更有用。
- **對應到 RAG 的哪個部分**：[Context window](concepts/context-window.md)、[Reranking](concepts/reranking.md)
- **比喻的極限**：真人可以慢慢翻；LLM 是一次讀完全部的輸入，問題不在時間不夠，而在中間的資訊用得不好。
- **對應的技術事實**：04 發現取 50 份文件和取 20 份相比，GPT-3.5-Turbo 只多進步約 1.5%，但延遲和成本都增加了；作者建議把相關文件 rerank 到前面，或少取幾份 [04-liu2023-lost-in-middle.pdf, §5, p.10]。

### 從書上撕下來的一頁

- **比喻**：從一本財報裡撕下一頁，上面只寫著「公司營收比上一季成長 3%」。拿到這一頁的人，根本不知道是哪家公司、哪一季。Contextual Retrieval 就是在每一頁的頁首補上一行「本頁出自 ACME 公司 2023 年 Q2 財報」。
- **對應到 RAG 的哪個部分**：[Chunking](concepts/chunking.md)、[Contextual Retrieval](methods/contextual-retrieval.md)
- **比喻的極限**：撕下來的書頁至少還有頁碼和版面可以推敲；chunk 只剩純文字。另外，那行補充說明是由 LLM 寫的，也可能寫錯。
- **對應的技術事實**：「The company's revenue grew by 3%…」這個 chunk 沒有說明公司和時期，所以很難被找到 [03-anthropic-contextual-retrieval.pdf, p.4]；補上 50–100 tokens 的說明後，檢索失敗率降低 35%–49% [03-anthropic-contextual-retrieval.pdf, p.6–7]。

### 用意思找 vs 用字找

- **比喻**：在圖書館問館員「有沒有講心臟病的書」，館員會依「意思」推薦相關的書，這就像 embedding；但如果你要找的是書號「TS-999」，就該直接在目錄裡比對字串，這就像 BM25。兩種找法一起用，最不容易漏掉。
- **對應到 RAG 的哪個部分**：[Retriever](concepts/retriever.md)（hybrid retrieval）
- **比喻的極限**：真的館員會同時用兩種方式思考；RAG 系統則是分開跑兩種檢索，再用 rank fusion 合併結果。
- **對應的技術事實**：embedding 擅長語意，但可能漏掉「TS-999」這類精確比對，BM25 則專門找精確字串 [03-anthropic-contextual-retrieval.pdf, p.3]；兩者合用比只用 embedding 好 [03-anthropic-contextual-retrieval.pdf, p.11]。

## 相關頁面
- [目錄](index.md)
- [RAG 總覽](overview.md)
