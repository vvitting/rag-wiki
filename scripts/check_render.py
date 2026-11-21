#!/usr/bin/env python3
"""⑨ 渲染檢查：用 Playwright 開啟 output/<slug>/deck.html。

用法：python3 scripts/check_render.py output/<slug>

檢查項目：
  - 頁數 8–15
  - 每頁沒有內容溢出：標題超過兩行、內容區超出可用高度／寬度、元素超出 16:9 投影片邊界、
    流程圖文字超出方框、出處列塞不下
  - 每頁都有 aside.notes 與 footer.refs
  - 文字與 drafts/ 一字不差（標題、段落標籤、項目、流程圖、講稿、出處清單）
  - 沒有外部資源；有左右鍵翻頁
  - 每頁截圖存到 output/<slug>/screenshots/slide-NN.png

結束碼：0 = 通過；1 = 失敗（印出哪一頁、什麼問題）；2 = 用法錯誤或沒有安裝 Playwright。
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from draftlib import MAX_SLIDES, MIN_SLIDES, load_drafts, norm_ws  # noqa: E402

EXTERNAL_RE = re.compile(r"""(?:src|href)\s*=\s*["']?\s*(?:https?:)?//|@import|url\(\s*["']?(?:https?:)?//""", re.I)

MEASURE_JS = """
(i) => {
  window.deck.go(i);
  const s = document.querySelectorAll('section.slide')[i];
  const sr = s.getBoundingClientRect();
  const issues = [];
  const over = (el, label) => {
    if (!el) return;
    const dy = el.scrollHeight - el.clientHeight, dx = el.scrollWidth - el.clientWidth;
    if (dy > 2) issues.push(`${label}垂直溢出 ${dy}px`);
    if (dx > 2) issues.push(`${label}水平溢出 ${dx}px`);
  };
  const h2 = s.querySelector('h2');
  if (h2) {
    const lines = Math.round(h2.getBoundingClientRect().height / parseFloat(getComputedStyle(h2).lineHeight));
    if (lines > 2) issues.push(`標題有 ${lines} 行（最多 2 行）`);
  }
  over(s.querySelector('.content'), '內容區');
  over(s.querySelector('footer.refs'), '出處列');
  over(s.querySelector('footer.refs ul'), '出處清單');
  for (const el of s.querySelectorAll('*')) {
    if (el.closest('aside.notes') || el.closest('defs')) continue;
    const r = el.getBoundingClientRect();
    if (r.width === 0 && r.height === 0) continue;
    const out = [];
    if (r.right > sr.right + 1) out.push(`右 ${Math.round(r.right - sr.right)}px`);
    if (r.bottom > sr.bottom + 1) out.push(`下 ${Math.round(r.bottom - sr.bottom)}px`);
    if (r.left < sr.left - 1) out.push(`左 ${Math.round(sr.left - r.left)}px`);
    if (r.top < sr.top - 1) out.push(`上 ${Math.round(sr.top - r.top)}px`);
    if (out.length) {
      const t = (el.textContent || '').trim().slice(0, 20);
      issues.push(`<${el.tagName.toLowerCase()}> 超出投影片邊界（${out.join('、')}）「${t}」`);
    }
  }
  for (const g of s.querySelectorAll('.diagram g.node')) {
    const rb = g.querySelector('rect').getBBox(), tb = g.querySelector('text').getBBox();
    if (tb.width > rb.width - 16) issues.push(`流程圖節點「${g.textContent}」文字超出方框`);
  }
  const txt = sel => Array.from(s.querySelectorAll(sel)).map(e => e.textContent.replace(/\\s+/g, ' ').trim());
  return {
    issues,
    text: {
      section: txt('.section-label')[0] || '',
      title: txt('h2')[0] || '',
      bullets: txt('.points > li'),
      nodes: txt('.diagram g.node text'),
      notes: txt('aside.notes'),
      refs: txt('footer.refs ul li'),
    },
  };
}
"""


def main() -> int:
    if len(sys.argv) != 2:
        print(__doc__)
        return 2
    out_dir = Path(sys.argv[1]).resolve()
    deck = out_dir / "deck.html"
    if not deck.is_file():
        print(f"ERROR {deck} 不存在（先執行 render_deck.py）")
        return 1
    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        print("ERROR 沒有安裝 Playwright：python3 -m pip install playwright && python3 -m playwright install chromium")
        return 2

    errors: list[str] = []
    src = deck.read_text(encoding="utf-8")
    for m in EXTERNAL_RE.finditer(src):
        errors.append(f"deck.html：使用了外部資源「{src[m.start():m.start() + 40]}」")
    if "ArrowRight" not in src or "ArrowLeft" not in src:
        errors.append("deck.html：沒有左右方向鍵翻頁")

    drafts = load_drafts(out_dir)
    shots = out_dir / "screenshots"
    shots.mkdir(exist_ok=True)
    for old in shots.glob("slide-*.png"):
        old.unlink()

    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page(viewport={"width": 1280, "height": 720})
        page.goto(deck.as_uri())
        page.evaluate("document.fonts.ready")
        n = page.locator("section.slide").count()
        if not MIN_SLIDES <= n <= MAX_SLIDES:
            errors.append(f"deck.html：共 {n} 頁（必須 {MIN_SLIDES}–{MAX_SLIDES} 頁）")
        if n != len(drafts):
            errors.append(f"deck.html 有 {n} 頁，但 drafts/ 有 {len(drafts)} 頁")
        for i in range(n):
            tag = f"第 {i + 1} 頁"
            res = page.evaluate(MEASURE_JS, i)
            page.screenshot(path=str(shots / f"slide-{i + 1:02d}.png"))
            for issue in res["issues"]:
                errors.append(f"{tag}：{issue}")
            t = res["text"]
            if not t["notes"]:
                errors.append(f"{tag}：缺少 aside.notes")
            if not t["refs"]:
                errors.append(f"{tag}：footer.refs 沒有列出 wiki 頁")
            if i >= len(drafts):
                continue
            d = drafts[i]
            name = f"drafts/{d.name}"
            expect = {
                "section": norm_ws(d.section),
                "title": norm_ws(d.title),
                "bullets": d.bullet_texts,
                "nodes": d.diagram_nodes,
                "notes": [d.notes_text],
                "refs": d.cited_pages(),
            }
            got = dict(t)
            labels = {"section": "段落標籤", "title": "標題", "bullets": "項目", "nodes": "流程圖",
                      "notes": "講稿", "refs": "出處清單"}
            for key, exp in expect.items():
                if got[key] != exp:
                    errors.append(f"{tag}：{labels[key]}和 {name} 不一致（稿件：{exp!r}；簡報：{got[key]!r}）")
        browser.close()

    for e in errors:
        print(f"ERROR {e}")
    print(f"截圖：{shots}")
    print("結果：" + ("通過" if not errors else f"{len(errors)} 個問題"))
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
