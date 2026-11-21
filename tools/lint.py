#!/usr/bin/env python3
"""RAG Wiki 機械性健康檢查（規則見 AGENTS.md 第 7、9.3、10 節）。

用法：python3 tools/lint.py
有 error 時回傳 exit code 1。只使用 Python 標準函式庫。
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
WIKI = ROOT / "wiki"
RAW = ROOT / "raw"
SLIDES = ROOT / "slides" / "rag-intro.html"

NO_FRONTMATTER = {"index.md", "log.md"}          # 不需要 frontmatter 與引用檢查
NO_ORPHAN_CHECK = {"index.md"}
REQUIRED_FIELDS = ["type", "title", "tags", "sources", "updated"]
SOURCE_FIELDS = ["raw", "authors", "year"]
VALID_TYPES = {"source", "concept", "method", "comparison", "question",
               "glossary", "analogy", "overview"}

LINK_RE = re.compile(r"(?<!!)\[([^\]]*)\]\(([^)\s]+)\)")
CITE_RE = re.compile(r"\[(\d{2}-[^,\]\s]+\.pdf)\s*,\s*([^\]]+)\]")
BARE_PDF_RE = re.compile(r"\[(\d{2}-[^,\]\s]+\.pdf)\s*\](?!\()")   # 後面接 ( 是 Markdown 連結，不是引用
TODO_MARK = "[待補來源]"
WIKILINK_RE = re.compile(r"\[\[[^\]]+\]\]")
LABEL_ONLY_RE = re.compile(r"^-\s*\*\*(比喻|對應到 RAG 的哪個部分|比喻的極限)\*\*")

errors: list[str] = []
warnings: list[str] = []
infos: list[str] = []


def rel(p: Path) -> str:
    return str(p.relative_to(ROOT))


def parse_frontmatter(text: str) -> tuple[dict[str, str] | None, int]:
    """回傳 (欄位 dict, body 起始行號)。只做簡單的 key: value 解析。"""
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        return None, 0
    fields: dict[str, str] = {}
    for i, line in enumerate(lines[1:], start=1):
        if line.strip() == "---":
            return fields, i + 1
        m = re.match(r"^([A-Za-z_]+)\s*:\s*(.*)$", line)
        if m:
            fields[m.group(1)] = m.group(2).strip()
    return None, 0


def parse_list(value: str) -> list[str]:
    value = value.strip()
    if value.startswith("[") and value.endswith("]"):
        return [v.strip().strip("'\"") for v in value[1:-1].split(",") if v.strip()]
    return [value] if value else []


def iter_blocks(lines: list[str], offset: int):
    """把 body 切成需要檢查引用的區塊，產生 (行號, 文字)。"""
    in_code = in_comment = skip_section = False
    para: list[str] = []
    para_start = 0

    def flush():
        nonlocal para
        if para:
            yield para_start, " ".join(para)
        para = []

    for idx, raw_line in enumerate(lines):
        lineno = idx + offset + 1
        line = raw_line.strip()
        if line.startswith("```"):
            in_code = not in_code
            yield from flush()
            continue
        if in_code:
            continue
        if "<!--" in line:
            in_comment = "-->" not in line
            yield from flush()
            continue
        if in_comment:
            in_comment = "-->" not in line
            continue
        if line.startswith("#"):
            yield from flush()
            skip_section = line.lstrip("#").strip() == "相關頁面"
            continue
        if skip_section or not line:
            yield from flush()
            continue
        if line.startswith(">") and "⚠️" not in line:
            yield from flush()
            continue
        if re.match(r"^\|?\s*:?-{3,}", line):          # 表格分隔列
            continue
        if line.startswith("|"):
            yield from flush()
            nxt = lines[idx + 1].strip() if idx + 1 < len(lines) else ""
            if re.match(r"^\|?\s*:?-{3,}", nxt):         # 表頭
                continue
            yield lineno, line
            continue
        if re.match(r"^([-*+]|\d+\.)\s", line):
            yield from flush()
            if LABEL_ONLY_RE.match(line):
                continue
            yield lineno, line
            continue
        # 一般段落：每一行獨立檢查（寫作慣例是一行一段），避免同段其他行的引用掩護沒引用的數字
        yield lineno, line
    yield from flush()


def check_block(path: Path, lineno: int, block: str):
    for m in BARE_PDF_RE.finditer(block):
        errors.append(f"{rel(path)}:{lineno} 引用缺少章節／頁碼：[{m.group(1)}]")
    for m in CITE_RE.finditer(block):
        if not (RAW / m.group(1)).exists():
            errors.append(f"{rel(path)}:{lineno} 引用的 raw 檔不存在：{m.group(1)}")
    cited = bool(CITE_RE.search(block)) or TODO_MARK in block
    stripped = CITE_RE.sub("", block)
    stripped = LINK_RE.sub("", stripped)                # 連結是導覽用途，不算主張
    stripped = re.sub(r"`[^`]*`", "", stripped)
    stripped = re.sub(r"^([-*+]|\d+\.)\s+", "", stripped)
    content = re.sub(r"[\s|*_\-—–:：,，。.()（）]", "", stripped)
    if len(content) < 8:                               # 只有連結或標籤
        return
    if cited:
        return
    preview = block[:60] + ("…" if len(block) > 60 else "")
    if re.search(r"\d", stripped):
        errors.append(f"{rel(path)}:{lineno} 含數字但沒附引用：{preview}")
    else:
        warnings.append(f"{rel(path)}:{lineno} 段落沒附引用：{preview}")


def check_wiki() -> None:
    pages = sorted(WIKI.rglob("*.md"))
    inbound: dict[Path, int] = {p.resolve(): 0 for p in pages}
    todo_count = 0

    for path in pages:
        text = path.read_text(encoding="utf-8")
        lines = text.splitlines()

        for i, line in enumerate(lines, start=1):
            if WIKILINK_RE.search(line) and not line.strip().startswith(">"):
                errors.append(f"{rel(path)}:{i} 使用了 [[wikilink]]，請改用標準 Markdown 連結")

        # 連結
        in_code = False
        for i, line in enumerate(lines, start=1):
            if line.strip().startswith("```"):
                in_code = not in_code
            if in_code:
                continue
            for m in LINK_RE.finditer(re.sub(r"`[^`]*`", "", line)):
                target = m.group(2)
                if re.match(r"^[a-z]+:", target) or target.startswith("#"):
                    continue
                dest = (path.parent / target.split("#")[0]).resolve()
                if not dest.exists():
                    errors.append(f"{rel(path)}:{i} 壞連結：{target}")
                elif dest in inbound and dest != path.resolve():
                    inbound[dest] += 1

        if path.name in NO_FRONTMATTER and path.parent == WIKI:
            continue

        # frontmatter
        fm, body_start = parse_frontmatter(text)
        if fm is None:
            errors.append(f"{rel(path)} 缺少 YAML frontmatter")
        else:
            for f in REQUIRED_FIELDS:
                if f not in fm:
                    errors.append(f"{rel(path)} frontmatter 缺少必填欄位：{f}")
            if fm.get("type") and fm["type"] not in VALID_TYPES:
                errors.append(f"{rel(path)} frontmatter type 不合法：{fm['type']}")
            if fm.get("type") == "source":
                for f in SOURCE_FIELDS:
                    if f not in fm:
                        errors.append(f"{rel(path)} 來源頁 frontmatter 缺少：{f}")
                if fm.get("raw") and not (RAW / fm["raw"].strip("'\"")).exists():
                    errors.append(f"{rel(path)} frontmatter raw 檔不存在：{fm['raw']}")
            for s in parse_list(fm.get("sources", "")):
                if not (RAW / s).exists():
                    errors.append(f"{rel(path)} frontmatter sources 的檔案不存在：{s}")
            if fm.get("updated") and not re.match(r"^\d{4}-\d{2}-\d{2}$", fm["updated"]):
                errors.append(f"{rel(path)} frontmatter updated 格式應為 YYYY-MM-DD")

        # 相關頁面
        if not any(l.strip().lstrip("#").strip() == "相關頁面" for l in lines if l.startswith("#")):
            warnings.append(f"{rel(path)} 缺少「## 相關頁面」區塊")

        # 引用
        todo_count += text.count(TODO_MARK)
        for lineno, block in iter_blocks(lines[body_start:], body_start):
            check_block(path, lineno, block)

    for p, n in inbound.items():
        if n == 0 and p.name not in NO_ORPHAN_CHECK and not (p.name == "log.md" and p.parent == WIKI):
            errors.append(f"{rel(p)} 是孤立頁面（沒有其他頁面連進來）")

    # ingest 進度
    raws = sorted(RAW.glob("*.pdf"))
    missing = [r.name for r in raws if not (WIKI / "sources" / (r.stem + ".md")).exists()]
    infos.append(f"wiki 頁面數：{len(pages)}；[待補來源] 標記：{todo_count} 處")
    if missing:
        infos.append(f"尚未 ingest（沒有來源頁）：{len(missing)}/{len(raws)} — " + ", ".join(missing))


def check_slides() -> None:
    if not SLIDES.exists():
        infos.append("slides/rag-intro.html 尚未產生，略過簡報檢查")
        return
    html = SLIDES.read_text(encoding="utf-8")
    name = rel(SLIDES)

    ext = re.findall(r"""(?:src|href)\s*=\s*["']\s*((?:https?:)?//[^"']+)""", html, re.I)
    ext += re.findall(r"""url\(\s*["']?((?:https?:)?//[^)"']+)""", html, re.I)
    ext += re.findall(r"""@import\s+["']?([^;"']+)""", html, re.I)
    for u in ext:
        errors.append(f"{name} 引用外部資源（必須完全自包含）：{u}")
    if re.search(r"reveal(\.min)?\.(js|css)", html, re.I):
        errors.append(f"{name} 不可使用 reveal.js")

    sections = re.findall(r"<section\b[^>]*class=[\"'][^\"']*\bslide\b[^\"']*[\"'][^>]*>(.*?)</section>",
                          html, re.S | re.I)
    n = len(sections)
    if not 8 <= n <= 15:
        errors.append(f"{name} 投影片數 {n} 張，必須在 8–15 張之間")
    for i, sec in enumerate(sections, start=1):
        if not re.search(r"<aside\b[^>]*class=[\"'][^\"']*\bnotes\b", sec, re.I):
            errors.append(f"{name} 第 {i} 張缺少講者備註 <aside class=\"notes\">")
        foot = re.search(r"<footer\b[^>]*class=[\"'][^\"']*\brefs\b[^>]*>(.*?)</footer>", sec, re.S | re.I)
        if not foot:
            errors.append(f"{name} 第 {i} 張缺少引用 footer <footer class=\"refs\">")
            continue
        refs = re.findall(r"wiki/[\w./-]+\.md", foot.group(1))
        if not refs:
            errors.append(f"{name} 第 {i} 張的 footer 沒有列出 wiki 頁面")
        for r in refs:
            if not (ROOT / r).exists():
                errors.append(f"{name} 第 {i} 張引用的 wiki 頁面不存在：{r}")
    for key, label in [("ArrowRight", "方向鍵翻頁"), ("requestFullscreen", "全螢幕")]:
        if key not in html:
            warnings.append(f"{name} 似乎沒有實作{label}（找不到 {key}）")
    if "16 / 9" not in html and "16/9" not in html and "1920" not in html:
        warnings.append(f"{name} 找不到 16:9 比例設定")
    infos.append(f"投影片：{n} 張")


def main() -> int:
    check_wiki()
    check_slides()
    for title, items in [("ERROR", errors), ("WARNING", warnings), ("INFO", infos)]:
        if items:
            print(f"\n== {title} ({len(items)}) ==")
            for it in items:
                print(f"  - {it}")
    print(f"\n結果：{len(errors)} error, {len(warnings)} warning")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
