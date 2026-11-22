#!/usr/bin/env python3
"""把 raw/*.pdf 轉成 raw-text/<同檔名>.md，給人和 reviewer 核對原文用。

用法：
  .venv/bin/python tools/pdf2text.py            # 轉換全部 PDF
  .venv/bin/python tools/pdf2text.py 05         # 只轉換檔名以 05 開頭的 PDF

- 每頁開頭插入 <!-- page N -->，N 從 1 開始，等於 PDF 的第 N 頁（也就是 wiki 引用中的 p.N）。
- raw-text/ 是衍生檔：不可手動編輯；要更新就重跑本工具。引用一律寫原始 PDF 的檔名和頁碼。
- 需要 pymupdf（版本見 requirements.txt）。

結束碼：0 = 成功；1 = 轉換失敗或頁數不符；2 = 缺少 pymupdf。
"""
from __future__ import annotations

import sys
from pathlib import Path

try:
    import pymupdf
except ImportError:
    print("ERROR 缺少 pymupdf：請先執行 python3 -m venv .venv && .venv/bin/pip install -r requirements.txt")
    sys.exit(2)

ROOT = Path(__file__).resolve().parent.parent
RAW = ROOT / "raw"
OUT = ROOT / "raw-text"
# PDF 的數學符號有時會被抽成控制字元（例如 01 p.3 的括號），讓檔案被當成二進位檔；換成空白
CONTROL = {c: " " for c in range(32) if chr(c) not in "\n\t"} | {0x7F: " "}
HEADER = (
    "<!-- 本檔由 tools/pdf2text.py 從 raw/{name} 自動產生，不可手動編輯。"
    "引用時請寫原始 PDF 的檔名與頁碼（p.N = 下方的 page N）。 -->\n"
)


def convert(pdf: Path) -> int:
    doc = pymupdf.open(pdf)
    parts = [HEADER.format(name=pdf.name)]
    for i, page in enumerate(doc, start=1):
        parts.append(f"\n<!-- page {i} -->\n\n{page.get_text().translate(CONTROL).rstrip()}\n")
    n = doc.page_count
    doc.close()
    out = OUT / (pdf.stem + ".md")
    out.write_text("".join(parts), encoding="utf-8")
    written = out.read_text(encoding="utf-8").count("<!-- page ")
    if written != n:
        print(f"ERROR {out.relative_to(ROOT)}：頁碼標記 {written} 個，PDF 有 {n} 頁")
        return 1
    print(f"{pdf.name} → {out.relative_to(ROOT)}（{n} 頁）")
    return 0


def main() -> int:
    prefix = sys.argv[1] if len(sys.argv) > 1 else ""
    pdfs = sorted(p for p in RAW.glob("*.pdf") if p.name.startswith(prefix))
    if not pdfs:
        print(f"ERROR raw/ 中找不到符合「{prefix}*.pdf」的檔案")
        return 1
    OUT.mkdir(exist_ok=True)
    return 1 if any(convert(p) for p in pdfs) else 0


if __name__ == "__main__":
    sys.exit(main())
