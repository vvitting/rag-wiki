---
page: wiki/sources/05-asai2023-self-rag.md
---
# 證據卡：05 Asai et al. 2023（Self-RAG）

## 重點摘錄
> - **Fig.1 的例子：走一遍「How did US states get their names?」**（美國各州的名字怎麼來的？）[05-asai2023-self-rag.pdf, Fig.1, p.2]：
>     1. 不管需不需要，先取回 K 份文件，例如「California 的名字來自一本西班牙書中的虛構島嶼」「Texas 常見的嬰兒名字是 Emma」「50 個州中有 11 個以人名命名」[05-asai2023-self-rag.pdf, Fig.1, p.2]。
>     3. 產生的答案寫「California 是以 Christopher Columbus 命名」，和取回的文件（來自西班牙書中的虛構島嶼）不一致 [05-asai2023-self-rag.pdf, Fig.1, p.2]。
>     1. 模型寫完開頭一句後，判斷下一段需要檢索（Retrieve）[05-asai2023-self-rag.pdf, Fig.1, p.2]；Self-RAG 每寫一段之前，都會重新判斷要不要檢索 [05-asai2023-self-rag.pdf, §3.1, p.4]。
>     3. 評分後選出最好的段落：選中「11 個州以人名命名」那段，因為它的文件相關、內容也完全被支持；Texas 那段的文件不相關，California 那段只有部分被支持 [05-asai2023-self-rag.pdf, §3.1, p.4]。接著再重複「判斷要不要檢索 → 生成 → 評分」寫下一段 [05-asai2023-self-rag.pdf, Fig.1, p.2; §3.1, p.4]。

## 可以用在
- 進階變體（11）：Self-RAG 和一般 RAG 處理同一個問題的差別（一般 RAG 答案和文件不一致；Self-RAG 評分後挑出有根據的段落）
