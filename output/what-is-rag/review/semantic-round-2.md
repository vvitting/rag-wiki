# ②b 相關頁語意檢查 — 第 2 次（⑤ 退回、重新檢索後；reviewer 模式 A）

- 範圍：新加入的 3 頁（sources/01、sources/05、lost-in-the-middle）完整檢查；其餘 14 頁未修改，只用於比對矛盾
- 允許讀取：sources.md 的 17 頁、raw-text/01–07、issues.md；實際讀取皆在清單內（有效）
- 判定：嚴重 0、輕微 12（V2-23–V2-34）→ 通過
- 舊問題：3 頁中沒有「待修」條目；V2-18、V2-19、V2-20、V2-22 確認已修，V2-21 維持不修
- 跨頁：75.8／53.8／56.1、2% 與 11.8% 的 ⚠️、reranking／文件數量 ⚠️、Fig.1「3 份文件選第 1 份」與其他 14 頁一致；無 [待補來源]

## 新問題（全部輕微）
1. sources/01 第 69–70 行：42.7% 的人工評估比的是 BART vs RAG-Token，頁面只寫「RAG」。
2. sources/01：seq2seq、DPR、BART、bi-encoder、MIPS、FAISS、marginalize、EM、NQ／TriviaQA／FEVER／MS-MARCO、BLEU、ROUGE-L、tri-gram 沒有連結；Fig.1 例子第 3 步的「MIPS」「top-K」初學者看不懂。
3. sources/05 第 25 行：「只檢索一次」出自 §2 p.3，不是 §1 p.2。
4. sources/05 第 103 行：2% 是 Self-RAG 7B、TriviaQA 和 PopQA 上的結果，沒有寫明。
5. sources/05 第 128 行：「04 發現文件放錯位置時比不給還差」少了 GPT-3.5-Turbo、20／30 份文件、最差位置的限定（同 Q03 修正前）。
6. sources/05 第 50 行：「每一類 4k–20k 筆」與附錄 utility 3,831 筆不一致，未在「其他小瑕疵」註明。
7. sources/05 第 113 行：「PopQA 和傳記各只抽 50 筆」，原文「50 samples from PopQA and Bio results」可能是合計（需要更多資料）。
8. sources/05 第 77 行：用一般文字寫「注意：…詳見 Self-RAG 的 ⚠️」，沒用標準 ⚠️ 區塊。
9. sources/05：LLM、reflection tokens、critic、RLHF／PPO、beam search、MAUVE、引用 precision 沒有連結。
10. lost-in-the-middle 第 42 行：「測試過的模型都有這個現象」和同頁第 44–45 行的兩個例外（Llama-2 7B、encoder-decoder）對不上；§2.3 指的是主實驗的 6 個模型。
11. lost-in-the-middle 第 17 行：「正確的文件很可能剛好落在中間 [§1, p.2]」是推論，原文沒這樣說。
12. lost-in-the-middle：primacy／recency bias、key-value 檢索、encoder-decoder、ranked list truncation、self-attention、Transformer 沒有連結或白話說明。
