#!/usr/bin/env python3
"""② 覆蓋率關卡：檢查 output/<slug>/sources.md。

用法：
  python3 scripts/check_coverage.py output/<slug>           # ② sources.md 頁數 ≥ 3 且都存在
  python3 scripts/check_coverage.py output/<slug> --cards   # ③ 另外檢查證據卡

sources.md 每個相關頁一行：`- wiki/concepts/chunking.md — 和主題的關係`
（也接受 `- [標題](wiki/concepts/chunking.md) — …`）

--cards 會檢查：每個相關頁都有一張卡 cards/<目錄>--<檔名>.md，
卡片 frontmatter 的 page 與相關頁一致，且卡片裡每一行「> 」摘錄都逐字出現在該 wiki 頁。

結束碼：0 = 通過；1 = 失敗（印出具體問題）；2 = 用法錯誤。
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from draftlib import NOT_CONTENT_PAGES, ROOT, norm_ws, parse_sources_md, split_frontmatter  # noqa: E402

MIN_PAGES = 3


def card_name(page: str) -> str:
    rel = page[len("wiki/"):-len(".md")]
    return rel.replace("/", "--") + ".md"


def check_sources(out_dir: Path, errors: list[str]) -> list[str]:
    src = out_dir / "sources.md"
    if not src.is_file():
        errors.append(f"{src.relative_to(ROOT)} 不存在")
        return []
    entries = parse_sources_md(src)
    pages: list[str] = []
    for ln, page in entries:
        where = f"sources.md 第 {ln} 行"
        p = (ROOT / page).resolve()
        if not str(p).startswith(str((ROOT / "wiki").resolve()) + "/"):
            errors.append(f"{where}：{page} 不在 wiki/ 內")
        elif page in NOT_CONTENT_PAGES:
            errors.append(f"{where}：{page} 是目錄／紀錄頁，不能當作相關頁")
        elif not p.is_file():
            errors.append(f"{where}：{page} 不存在")
        elif page in pages:
            errors.append(f"{where}：{page} 重複列出")
        else:
            pages.append(page)
    if len(pages) < MIN_PAGES:
        errors.append(f"sources.md：有效的相關頁只有 {len(pages)} 頁（需要 ≥ {MIN_PAGES}）")
    return pages


def check_cards(out_dir: Path, pages: list[str], errors: list[str]) -> None:
    cards_dir = out_dir / "cards"
    expected = {card_name(p): p for p in pages}
    if cards_dir.is_dir():
        for extra in sorted(cards_dir.glob("*.md")):
            if extra.name not in expected:
                errors.append(f"cards/{extra.name}：對應的頁面不在 sources.md 中")
    for name, page in expected.items():
        card = cards_dir / name
        where = f"cards/{name}"
        if not card.is_file():
            errors.append(f"{where}：缺少（{page} 的證據卡）")
            continue
        fields, body, start = split_frontmatter(card.read_text(encoding="utf-8"))
        if not fields or fields.get("page") != page:
            errors.append(f"{where}：frontmatter 的 page 應為 {page}（目前 {fields.get('page') if fields else '無 frontmatter'}）")
        page_text = norm_ws((ROOT / page).read_text(encoding="utf-8"))
        quotes = 0
        for offset, line in enumerate(body):
            if not line.startswith(">"):
                continue
            q = norm_ws(line[1:])
            if not q:
                continue
            quotes += 1
            if q not in page_text:
                short = q if len(q) <= 40 else q[:40] + "…"
                errors.append(f"{where} 第 {start + offset} 行：摘錄不是 {page} 的原文：「{short}」")
        if quotes == 0:
            errors.append(f"{where}：沒有任何「> 」原文摘錄")


def main() -> int:
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    if len(args) != 1:
        print(__doc__)
        return 2
    out_dir = Path(args[0]).resolve()
    errors: list[str] = []
    pages = check_sources(out_dir, errors)
    if "--cards" in sys.argv and pages:
        check_cards(out_dir, pages, errors)
    for e in errors:
        print(f"ERROR {e}")
    print(f"相關頁：{len(pages)} 頁" + ("、證據卡已檢查" if "--cards" in sys.argv else ""))
    print("結果：" + ("通過" if not errors else f"{len(errors)} 個問題"))
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
