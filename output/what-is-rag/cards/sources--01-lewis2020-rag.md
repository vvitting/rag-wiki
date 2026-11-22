---
page: wiki/sources/01-lewis2020-rag.md
---
# 證據卡：01 Lewis et al. 2020（原始 RAG 論文）

## 重點摘錄
> - **Fig.1 的例子：走一遍「Define "middle ear"」**（圖中的問答任務；同一張圖也畫了事實查核和 Jeopardy 出題的例子）[01-lewis2020-rag.pdf, Fig.1, p.2]：
>   1. **輸入問題**：「Define "middle ear"」（定義「中耳」）[01-lewis2020-rag.pdf, Fig.1, p.2]。
>   2. **把問題轉成向量**：Query Encoder 把問題 x 轉成向量 q(x) [01-lewis2020-rag.pdf, Fig.1, p.2]。
>   3. **找資料**：用 MIPS 從 Document Index 中找出最相關的 top-K 份文件，圖中畫的是 z1 到 z4 [01-lewis2020-rag.pdf, Fig.1, p.2]；這個 index 是 Wikipedia 的 dense vector index [01-lewis2020-rag.pdf, §1, p.2]。
>   4. **寫答案**：Generator 根據每一份文件分別產生答案，再把結果合併（marginalize）[01-lewis2020-rag.pdf, Fig.1, p.2]；合併時依每份文件的檢索機率加權 [01-lewis2020-rag.pdf, §2.1, p.3]。
>   5. **輸出**：「The middle ear includes the tympanic cavity and the three ossicles.」（中耳包含鼓室和三塊聽小骨）[01-lewis2020-rag.pdf, Fig.1, p.2]。
>   6. **對照不查資料的模型**：同一個問題，BART 回答「中耳是介於中耳和鼻子之間的部分」，是錯的答案；RAG-Sequence 的答案則和上面步驟 5 相同。Table 3 中這一題屬於 MS-MARCO 生成式問答任務 [01-lewis2020-rag.pdf, Table 3, p.7]。

## 可以用在
- 怎麼運作（07 走一遍）：一個問題從輸入到輸出的完整旅程；對照 BART 不查資料時的錯誤答案
