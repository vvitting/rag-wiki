---
page: wiki/comparisons/closed-book-vs-open-book.md
---
# 證據卡：Closed-book vs open-book

## 重點摘錄
> ## Open-domain QA 成績（NQ，Exact Match）
> 原始 RAG 論文用「closed-book」形容只靠參數記憶的方法，用「open-book」形容會去檢索資料的方法 [01-lewis2020-rag.pdf, §4.1, p.5]。
> RAG 結合了兩邊的優點：closed-book 能自由生成文字，open-book 有檢索帶來的表現 [01-lewis2020-rag.pdf, §4.1, p.5]。
> - 所以開書考要考得好，不只要「帶對書」，還要「把重點翻到前面」。詳見 [Lost in the middle](../concepts/lost-in-the-middle.md) [04-liu2023-lost-in-middle.pdf, §5, p.10]。

## 數字
> | T5-11B | closed-book | 11B | 34.5 | [01-lewis2020-rag.pdf, Table 1, p.6; App. G, p.19] |
> | RAG-Sequence | open-book | 626M | 44.5 | [01-lewis2020-rag.pdf, Table 1, p.6; App. G, p.18–19] |
> - 參數少很多的 open-book 模型，可以勝過參數多很多的 closed-book 模型；作者據此認為，結合兩種記憶的模型只需要少得多的可訓練參數 [01-lewis2020-rag.pdf, App. G, p.19]。
> | Closed-book（不給文件） | 56.1% | [04-liu2023-lost-in-middle.pdf, Table 1, p.5] |
> | 20 份文件，答案在第 1 份 | 75.8% | [04-liu2023-lost-in-middle.pdf, Table 6, p.18] |
> | 20 份文件，答案在第 10 份 | 53.8% | [04-liu2023-lost-in-middle.pdf, Table 6, p.18] |
> - 在 20 和 30 份文件的設定中，答案放在最差的位置時（例如 20 份中的第 10 份，見上表），open-book 的表現反而**低於** closed-book [04-liu2023-lost-in-middle.pdf, §2.3, p.5]。

## 可以用在
- 是什麼（04）：閉書考 vs 開書考；RAG-Sequence 44.5 vs T5-11B 34.5
- 總結（13）：開書考不一定比較好（53.8% < 56.1%，限 20／30 份文件的最差位置）
- 是什麼（04）：44.5／34.5 是 NQ 上的 Exact Match（修正輕微問題時補）
