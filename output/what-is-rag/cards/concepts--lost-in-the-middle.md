---
page: wiki/concepts/lost-in-the-middle.md
---
# 證據卡：Lost in the middle

## 重點摘錄
> 把一堆文件塞進 [prompt](../glossary.md) 時，[LLM](../glossary.md) 最會利用放在**開頭**和**結尾**的資訊，放在**中間**的資訊最容易被忽略。把「答案的位置」和「準確率」畫成圖，會是一條 U 形曲線 [04-liu2023-lost-in-middle.pdf, Fig.1, p.1]。

## 數字
> - 最糟的時候，給模型文件反而比完全不給還差：GPT-3.5-Turbo 在 20 份文件、答案位於中間時，準確率是 53.8%，不給文件時則是 56.1% [04-liu2023-lost-in-middle.pdf, Table 6, p.18; Table 1, p.5]。
> | 第 1 份（開頭） | 75.8% | [04-liu2023-lost-in-middle.pdf, Table 6, p.18] |
> | 第 10 份（中間） | 53.8% | [04-liu2023-lost-in-middle.pdf, Table 6, p.18] |
> | 第 20 份（結尾） | 63.2% | [04-liu2023-lost-in-middle.pdf, Table 6, p.18] |
> | 不給文件（closed-book） | 56.1% | [04-liu2023-lost-in-middle.pdf, Table 1, p.5] |

## 可以用在
- 總結（13）：位置也有影響——答案在開頭或結尾用得好、在中間最容易被忽略（GPT-3.5-Turbo，20 份文件）
