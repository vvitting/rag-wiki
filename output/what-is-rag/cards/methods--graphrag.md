---
page: wiki/methods/graphrag.md
---
# 證據卡：GraphRAG

## 重點摘錄
> 先用 LLM 把整批文件整理成 [knowledge graph](../glossary.md)，再把關係緊密的實體分成社群、為每個社群寫好摘要；回答時，把所有社群摘要彙整成一個全局答案 [06-edge2024-graphrag.pdf, Abstract, p.1]。
> | 擅長的問題 | 答案集中在少數幾份文件裡的問題 [06-edge2024-graphrag.pdf, §1, p.2] | 需要理解整批資料的全局問題 [06-edge2024-graphrag.pdf, §1, p.2] |

## 數字
>   - 全面性勝率：Podcast 72%–83%，新聞 72%–80% [06-edge2024-graphrag.pdf, §5.1, p.9]。
> - 在全局問題上，GraphRAG 等全局方法（也包括直接對原文做摘要的 TS）的全面性和多樣性都明顯勝過一般 RAG [06-edge2024-graphrag.pdf, §5.1, p.9]。
> - **建 index 很貴**：約 100 萬 tokens [06-edge2024-graphrag.pdf, §4.1.1, p.8] 的 Podcast 資料，用 gpt-4-turbo 花了 281 分鐘 [06-edge2024-graphrag.pdf, §4.1.3, p.9]。

## 可以用在
- 進階變體（10）：回答全局問題；勝率限「GraphRAG 等全局方法」並分資料集；代價是建 index 很貴
