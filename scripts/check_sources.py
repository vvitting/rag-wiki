#!/usr/bin/env python3
"""⑥ 逐頁稿檢查：output/<slug>/drafts/*.md。

用法：python3 scripts/check_sources.py output/<slug>

檢查項目：
  - 頁數 8–15；檔名 NN-slug.md；frontmatter slide 與檔名編號一致、從 1 連號
  - section 是六段之一，順序為 為什麼需要→是什麼→怎麼運作→進階變體→怎麼評估→總結，且六段都有
  - 投影片每個項目、流程圖、講稿每一句都有〔wiki/…md〕出處
  - 引用的 wiki 頁存在，且列在 sources.md
  - 講稿 2–4 句
  - 每個數字都能在「同一行／同一句引用的 wiki 頁」中找到（標題的數字比對整頁引用的 wiki 頁）

結束碼：0 = 通過；1 = 失敗（印出哪一頁、第幾行、什麼問題）；2 = 用法錯誤。
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from draftlib import (  # noqa: E402
    DRAFT_NAME_RE, MAX_NOTE_SENT, MAX_SLIDES, MIN_NOTE_SENT, MIN_SLIDES, ROOT, SECTIONS,
    bad_brackets, cites_in, load_drafts, number_in_pages, numbers_in, parse_sources_md, strip_cites,
)


def main() -> int:
    if len(sys.argv) != 2:
        print(__doc__)
        return 2
    out_dir = Path(sys.argv[1]).resolve()
    errors: list[str] = []

    src = out_dir / "sources.md"
    allowed = {p for _, p in parse_sources_md(src)} if src.is_file() else set()
    if not src.is_file():
        errors.append("sources.md 不存在，無法確認引用的頁是否在相關頁清單內")

    drafts = load_drafts(out_dir)
    n = len(drafts)
    if not MIN_SLIDES <= n <= MAX_SLIDES:
        errors.append(f"drafts/：共 {n} 頁（必須 {MIN_SLIDES}–{MAX_SLIDES} 頁）")

    last_sec = -1
    seen_secs: set[str] = set()
    for idx, d in enumerate(drafts, start=1):
        tag = f"drafts/{d.name}"
        for e in d.errors:
            errors.append(f"{tag} {e}")

        m = DRAFT_NAME_RE.match(d.name)
        if not m:
            errors.append(f"{tag}：檔名要是 NN-英文-slug.md")
        elif int(m.group(1)) != idx:
            errors.append(f"{tag}：檔名編號應為 {idx:02d}（頁面要從 01 連號）")
        if d.slide is not None and d.slide != idx:
            errors.append(f"{tag}：frontmatter slide={d.slide}，應為 {idx}")

        if d.section:
            if d.section not in SECTIONS:
                errors.append(f"{tag}：section「{d.section}」不是 {'／'.join(SECTIONS)} 之一")
            else:
                si = SECTIONS.index(d.section)
                if si < last_sec:
                    errors.append(f"{tag}：section「{d.section}」出現在「{SECTIONS[last_sec]}」之後，順序錯誤")
                last_sec = max(last_sec, si)
                seen_secs.add(d.section)

        def check_line(ln: int, raw: str, kind: str, need_cite: bool = True) -> None:
            for b in bad_brackets(raw):
                errors.append(f"{tag} 第 {ln} 行：引用格式錯誤〔{b}〕（要寫成〔wiki/路徑.md〕）")
            cites = cites_in(raw)
            if need_cite and not cites:
                short = strip_cites(raw)
                short = short if len(short) <= 30 else short[:30] + "…"
                errors.append(f"{tag} 第 {ln} 行：{kind}沒有出處：「{short}」")
            for c in cites:
                if not (ROOT / c).is_file():
                    errors.append(f"{tag} 第 {ln} 行：引用的 {c} 不存在")
                elif allowed and c not in allowed:
                    errors.append(f"{tag} 第 {ln} 行：引用的 {c} 不在 sources.md 中")
            existing = [c for c in cites if (ROOT / c).is_file()]
            if existing:
                for num in numbers_in(strip_cites(raw)):
                    if not number_in_pages(num, existing):
                        errors.append(f"{tag} 第 {ln} 行：數字 {num} 在引用的 {'、'.join(existing)} 中找不到")

        for ln, t in d.bullets:
            check_line(ln, t, "投影片項目")
        for ln, t in d.diagram:
            check_line(ln, t, "流程圖")
        for ln, s in d.notes:
            if not strip_cites(s):
                errors.append(f"{tag} 第 {ln} 行：講稿中有單獨的引用標記「{s}」（引用要放在句號之前）")
                continue
            check_line(ln, s, "講稿句子")
        n_sent = sum(1 for _, s in d.notes if strip_cites(s))
        if d.notes and not MIN_NOTE_SENT <= n_sent <= MAX_NOTE_SENT:
            errors.append(f"{tag}：講稿 {n_sent} 句（必須 {MIN_NOTE_SENT}–{MAX_NOTE_SENT} 句）")
        if not d.notes:
            errors.append(f"{tag}：缺少「## 講稿」或講稿為空")

        all_pages = [c for c in d.cited_pages() if (ROOT / c).is_file()]
        for num in numbers_in(d.title):
            if not number_in_pages(num, all_pages):
                errors.append(f"{tag} 第 {d.title_line} 行：標題的數字 {num} 在本頁引用的 wiki 頁中找不到")
        for b in bad_brackets(d.title):
            errors.append(f"{tag} 第 {d.title_line} 行：標題不要放引用〔{b}〕")

    if drafts:
        missing = [s for s in SECTIONS if s not in seen_secs]
        if missing:
            errors.append(f"drafts/：缺少段落 {'、'.join(missing)}")

    for e in errors:
        print(f"ERROR {e}")
    print(f"逐頁稿：{n} 頁")
    print("結果：" + ("通過" if not errors else f"{len(errors)} 個問題"))
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
