# Wiki 維護流程 — sources/01、sources/05 補 Fig.1 例子（reviewer 模式 A）

- 觸發：⑤ 第 1 次退回，使用者批准從 raw-text/ 補 Lewis Fig.1、Self-RAG Fig.1 的完整例子
- 允許讀取：wiki/sources/01、wiki/sources/05、raw-text/01–06、issues.md；實際讀取皆在清單內（有效）
- 結果：嚴重 0、輕微 5（V2-18–V2-22）→ 通過；V2-18、V2-19、V2-20、V2-22 已當場修正，V2-21 不修（理由見 issues.md）

## reviewer 回報摘要（全文要點）

1. [輕微｜引用] sources/01 步驟 3「Document Index（Wikipedia）」、步驟 4「加權合併」只引 Fig.1, p.2；Wikipedia 在 §1 p.2 內文，「加權」在 §2.1 p.3。→ 已補引用。
2. [輕微｜限定條件] sources/01 步驟 6：Table 3 的 middle ear 屬於 MS-MARCO 任務，RAG-S 答案與 Fig.1 輸出相同，建議註明。→ 已補。
3. [輕微｜簡化] sources/05 Self-RAG 步驟 1「先判斷這個問題需要檢索」：實際上每個 segment 之前都判斷（§3.1 p.4），圖中第一句沒有檢索。→ 已改寫。
4. [輕微｜需要更多資料] sources/05 一般 RAG 步驟 3：圖中另有「Contradictory」「No information in passages」標籤，抽出的文字看不出標在哪一句，需要看原圖。→ 不修。
5. [輕微｜可讀性] sources/05：Relevant／Supported 等標籤沒有說明是 ISREL／ISSUP；步驟 3 沒說選中哪一段（§3.1 p.4：d1 被選中）。→ 已補。
