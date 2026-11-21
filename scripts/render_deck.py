#!/usr/bin/env python3
"""⑧ 渲染：把 output/<slug>/drafts/*.md 機械式轉成單一自包含的 output/<slug>/deck.html。

用法：python3 scripts/render_deck.py output/<slug>

- 不改任何文字：只移除〔wiki/…〕引用標記（改列在每頁底部的 footer.refs）與 ** 粗體標記（轉成 <strong>）。
- 每頁一個 <section class="slide">，固定 1280×720（16:9），依視窗等比例縮放。
- ← → / PageUp / PageDown / 空白鍵 翻頁；F 全螢幕；N 顯示講稿。
- 不使用任何外部資源（框架、CDN、字型、圖片）。

結束碼：0 = 已產生；1 = 稿件有格式錯誤（請先通過 check_sources.py）；2 = 用法錯誤。
"""
from __future__ import annotations

import html
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from draftlib import ANY_BRACKET_RE, load_drafts, norm_ws  # noqa: E402

W, H, PAD_X = 1280, 720, 72


def inline(raw: str) -> str:
    text = norm_ws(ANY_BRACKET_RE.sub("", raw))
    text = html.escape(text)
    return re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", text)


def diagram_svg(nodes: list[str]) -> str:
    width, height, gap = W - 2 * PAD_X, 132, 56
    n = len(nodes)
    bw = (width - 4 - (n - 1) * gap) / n   # 左右各留 2px，避免方框邊線被裁切
    parts = [f'<svg class="diagram" viewBox="0 0 {width} {height}" width="{width}" height="{height}" '
             f'role="img" aria-label="{html.escape(" → ".join(nodes))}">',
             '<defs><marker id="arrow" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="8" markerHeight="8" '
             'orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="var(--accent)"/></marker></defs>']
    for i, label in enumerate(nodes):
        x = 2 + i * (bw + gap)
        parts.append(f'<g class="node"><rect x="{x:.1f}" y="16" width="{bw:.1f}" height="100" rx="14"/>'
                     f'<text x="{x + bw / 2:.1f}" y="66" dominant-baseline="middle" text-anchor="middle">'
                     f'{html.escape(label)}</text></g>')
        if i < n - 1:
            x1, x2 = x + bw + 6, x + bw + gap - 6
            parts.append(f'<line x1="{x1:.1f}" y1="66" x2="{x2:.1f}" y2="66" marker-end="url(#arrow)"/>')
    parts.append("</svg>")
    return "".join(parts)


def slide_html(d, total: int) -> str:
    refs = "".join(f"<li>{html.escape(p)}</li>" for p in d.cited_pages())
    bullets = "".join(f"<li>{inline(t)}</li>" for _, t in d.bullets)
    diagram = diagram_svg(d.diagram_nodes) if d.diagram else ""
    return f"""
<section class="slide" data-slide="{d.slide}">
  <header>
    <p class="section-label">{html.escape(d.section)}</p>
    <h2>{html.escape(d.title)}</h2>
  </header>
  <div class="content">
    {diagram}
    <ul class="points">{bullets}</ul>
  </div>
  <footer class="refs"><span class="refs-label">出處</span><ul>{refs}</ul><span class="pageno">{d.slide} / {total}</span></footer>
  <aside class="notes">{html.escape(d.notes_text)}</aside>
</section>"""


TEMPLATE = """<!doctype html>
<html lang="zh-Hant">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>__TITLE__</title>
<style>
:root {
  --bg: #1d2129; --paper: #ffffff; --ink: #1f2933; --muted: #6b7785;
  --accent: #2f6fde; --accent-soft: #e8f0fd; --line: #d9dee5;
  --font: "PingFang TC", "Noto Sans TC", "Microsoft JhengHei", "Heiti TC", system-ui, sans-serif;
}
* { box-sizing: border-box; }
html, body { margin: 0; height: 100%; background: var(--bg); overflow: hidden; font-family: var(--font); }
#stage { position: absolute; left: 50%; top: 50%; width: 1280px; height: 720px; transform-origin: center center; }
.slide { display: none; position: absolute; inset: 0; width: 1280px; height: 720px; overflow: hidden;
  background: var(--paper); color: var(--ink); padding: 48px 72px 0; flex-direction: column; }
.slide.active { display: flex; }
header { flex: none; }
.section-label { margin: 0 0 8px; font-size: 18px; font-weight: 600; letter-spacing: .08em; color: var(--accent); }
h2 { margin: 0; font-size: 40px; line-height: 52px; }
.content { flex: 1; min-height: 0; overflow: hidden; padding-top: 28px; }
.points { margin: 0; padding-left: 1.2em; font-size: 27px; line-height: 1.55; }
.points li { margin-bottom: 14px; }
.points li::marker { color: var(--accent); }
strong { color: var(--accent); }
.diagram { display: block; margin: 0 0 24px; overflow: visible; }
.diagram rect { fill: var(--accent-soft); stroke: var(--accent); stroke-width: 2; }
.diagram text { font-family: var(--font); font-size: 24px; font-weight: 600; fill: var(--ink); }
.diagram line { stroke: var(--accent); stroke-width: 3; }
.refs { flex: none; height: 64px; display: flex; align-items: center; gap: 12px; border-top: 1px solid var(--line);
  font-size: 13px; color: var(--muted); overflow: hidden; }
.refs-label { flex: none; font-weight: 600; }
.refs ul { flex: 1; display: flex; flex-wrap: wrap; gap: 2px 14px; margin: 0; padding: 0; list-style: none;
  font-family: ui-monospace, Menlo, monospace; }
.pageno { flex: none; font-size: 14px; }
aside.notes { display: none; }
#notes-panel { display: none; position: fixed; left: 0; right: 0; bottom: 0; max-height: 40vh; overflow: auto;
  background: rgba(20, 24, 31, .94); color: #f1f3f5; font: 20px/1.6 var(--font); padding: 18px 28px; }
body.show-notes #notes-panel { display: block; }
</style>
</head>
<body>
<div id="stage">__SLIDES__
</div>
<div id="notes-panel" aria-live="polite"></div>
<script>
(function () {
  var slides = Array.prototype.slice.call(document.querySelectorAll("section.slide"));
  var stage = document.getElementById("stage");
  var panel = document.getElementById("notes-panel");
  var cur = 0;
  function fit() {
    var s = Math.min(window.innerWidth / 1280, window.innerHeight / 720);
    stage.style.transform = "translate(-50%, -50%) scale(" + s + ")";
  }
  function go(i) {
    cur = Math.max(0, Math.min(slides.length - 1, i));
    slides.forEach(function (el, k) { el.classList.toggle("active", k === cur); });
    panel.textContent = slides[cur].querySelector("aside.notes").textContent;
    if (location.hash !== "#" + (cur + 1)) history.replaceState(null, "", "#" + (cur + 1));
  }
  document.addEventListener("keydown", function (e) {
    var k = e.key;
    if (k === "ArrowRight" || k === "PageDown" || k === " ") { e.preventDefault(); go(cur + 1); }
    else if (k === "ArrowLeft" || k === "PageUp") { e.preventDefault(); go(cur - 1); }
    else if (k === "Home") { go(0); }
    else if (k === "End") { go(slides.length - 1); }
    else if (k === "f" || k === "F") {
      if (!document.fullscreenElement) document.documentElement.requestFullscreen();
      else document.exitFullscreen();
    }
    else if (k === "n" || k === "N") { document.body.classList.toggle("show-notes"); }
  });
  window.addEventListener("resize", fit);
  window.deck = { go: go, count: slides.length };
  fit();
  go((parseInt(location.hash.slice(1), 10) || 1) - 1);
})();
</script>
</body>
</html>
"""


def main() -> int:
    if len(sys.argv) != 2:
        print(__doc__)
        return 2
    out_dir = Path(sys.argv[1]).resolve()
    drafts = load_drafts(out_dir)
    if not drafts:
        print(f"ERROR {out_dir}/drafts/ 沒有稿件")
        return 1
    bad = [f"drafts/{d.name} {e}" for d in drafts for e in d.errors]
    if bad:
        for e in bad:
            print(f"ERROR {e}")
        return 1
    title = drafts[0].title
    body = "".join(slide_html(d, len(drafts)) for d in drafts)
    out = out_dir / "deck.html"
    out.write_text(TEMPLATE.replace("__TITLE__", html.escape(title)).replace("__SLIDES__", body), encoding="utf-8")
    print(f"已產生 {out}（{len(drafts)} 頁）")
    return 0


if __name__ == "__main__":
    sys.exit(main())
