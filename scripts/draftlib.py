"""topic-slides workflow 共用的解析工具（只用標準函式庫）。

給 check_coverage.py、check_sources.py、render_deck.py、check_render.py 使用。
逐頁稿格式見 .claude/commands/topic-slides.md 的「逐頁稿格式」。
"""
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
WIKI = ROOT / "wiki"

SECTIONS = ["為什麼需要", "是什麼", "怎麼運作", "進階變體", "怎麼評估", "總結"]
MIN_SLIDES, MAX_SLIDES = 8, 15
MIN_NOTE_SENT, MAX_NOTE_SENT = 2, 4
NOT_CONTENT_PAGES = {"wiki/index.md", "wiki/log.md"}

CITE_RE = re.compile(r"〔(wiki/[A-Za-z0-9_./-]+?\.md)〕")
ANY_BRACKET_RE = re.compile(r"〔([^〔〕]*)〕")
SENT_END = "。！？!?"
DRAFT_NAME_RE = re.compile(r"^(\d{2})-[a-z0-9-]+\.md$")
NUM_RE = re.compile(r"\d+(?:,\d{3})*(?:\.\d+)?(?:\s*[%％])?")   # 帶 % 的數字要連 % 一起比對
SOURCES_LINE_RE = re.compile(r"^\s*-\s+(?:\[[^\]]*\]\()?(wiki/[^\s)]+?\.md)")

# wiki 頁中要先拿掉、避免數字誤配的部分：raw 引用括號與連結目標
WIKI_RAW_CITE_RE = re.compile(r"\[\d{2}-[^\]\n]*?\.pdf[^\]\n]*\]")
WIKI_LINK_TARGET_RE = re.compile(r"\]\([^)\s]*\)")


# ---------- 通用 ----------

def norm_ws(s: str) -> str:
    return re.sub(r"\s+", " ", s).strip()


def strip_cites(s: str) -> str:
    """拿掉〔…〕引用與 ** 粗體標記，得到投影片上真正顯示的文字。"""
    s = ANY_BRACKET_RE.sub("", s)
    s = s.replace("**", "")
    return norm_ws(s)


def cites_in(s: str) -> list[str]:
    return CITE_RE.findall(s)


def bad_brackets(s: str) -> list[str]:
    """〔…〕裡不是合法 wiki 路徑的內容。"""
    return [b for b in ANY_BRACKET_RE.findall(s) if not CITE_RE.fullmatch(f"〔{b}〕")]


def numbers_in(s: str) -> list[str]:
    return [re.sub(r"\s*[%％]$", "%", n.replace(",", "")) for n in NUM_RE.findall(s)]


def split_frontmatter(text: str) -> tuple[dict[str, str] | None, list[str], int]:
    """回傳 (欄位, body 行, body 起始行號 1-based)。"""
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        return None, lines, 1
    fields: dict[str, str] = {}
    for i, line in enumerate(lines[1:], start=1):
        if line.strip() == "---":
            return fields, lines[i + 1:], i + 2
        m = re.match(r"^([A-Za-z_]+)\s*:\s*(.*)$", line)
        if m:
            fields[m.group(1)] = m.group(2).strip().strip('"')
    return None, lines, 1


# ---------- sources.md ----------

def parse_sources_md(path: Path) -> list[tuple[int, str]]:
    """回傳 [(行號, 'wiki/…md')]，依出現順序。

    只讀「相關頁清單」：從檔案開頭讀到第一個 `## ` 標題為止。
    之後的「## 看過但沒選的頁」「## 缺口」等段落即使有 `- wiki/…` 也不算相關頁。
    """
    out = []
    for i, line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
        if line.startswith("## "):
            break
        m = SOURCES_LINE_RE.match(line)
        if m:
            out.append((i, m.group(1)))
    return out


# ---------- wiki 頁文字（給數字比對用） ----------

_wiki_cache: dict[str, str] = {}


def wiki_text_for_numbers(rel_path: str) -> str:
    if rel_path not in _wiki_cache:
        p = ROOT / rel_path
        text = p.read_text(encoding="utf-8") if p.is_file() else ""
        _, body, _ = split_frontmatter(text)
        t = "\n".join(body)
        t = WIKI_RAW_CITE_RE.sub(" ", t)
        t = WIKI_LINK_TARGET_RE.sub("]", t)
        t = re.sub(r"(?<=\d),(?=\d{3})", "", t)
        _wiki_cache[rel_path] = t
    return _wiki_cache[rel_path]


def number_in_pages(num: str, pages: list[str]) -> bool:
    if num.endswith("%"):
        pat = re.compile(r"(?<![\d.])" + re.escape(num[:-1]) + r"\s*[%％]")
    else:
        pat = re.compile(r"(?<![\d.])" + re.escape(num) + r"(?!\.?\d)")
    return any(pat.search(wiki_text_for_numbers(p)) for p in pages)


# ---------- 逐頁稿 ----------

class Draft:
    def __init__(self, path: Path):
        self.path = path
        self.name = path.name
        self.errors: list[str] = []          # 格式錯誤（解析階段就發現的）
        self.fields: dict[str, str] = {}
        self.slide: int | None = None
        self.section = ""
        self.title = ""
        self.title_line = 0
        self.bullets: list[tuple[int, str]] = []     # (行號, 原始文字，不含 "- ")
        self.diagram: list[tuple[int, str]] = []     # (行號, 原始文字)
        self.notes: list[tuple[int, str]] = []       # (起始行號, 一句，含引用)
        self._parse()

    # 顯示用文字（拿掉引用後）
    @property
    def bullet_texts(self) -> list[str]:
        return [strip_cites(t) for _, t in self.bullets]

    @property
    def diagram_nodes(self) -> list[str]:
        if not self.diagram:
            return []
        return [strip_cites(n) for n in self.diagram[0][1].split("→") if strip_cites(n)]

    @property
    def notes_text(self) -> str:
        return norm_ws("".join(strip_cites(s) for _, s in self.notes))

    def cited_pages(self) -> list[str]:
        seen: list[str] = []
        for _, t in self.bullets + self.diagram + self.notes:
            for c in cites_in(t):
                if c not in seen:
                    seen.append(c)
        return seen

    def _parse(self) -> None:
        text = self.path.read_text(encoding="utf-8")
        fields, body, start = split_frontmatter(text)
        if fields is None:
            self.errors.append("第 1 行：缺少 frontmatter（--- 開頭、--- 結束）")
            return
        self.fields = fields
        for k in ("slide", "section", "title"):
            if not fields.get(k):
                self.errors.append(f"frontmatter 缺少 {k}")
        try:
            self.slide = int(fields.get("slide", ""))
        except ValueError:
            self.errors.append(f"frontmatter slide 不是整數：{fields.get('slide')!r}")
        self.section = fields.get("section", "")
        self.title = fields.get("title", "")
        lines = text.splitlines()
        self.title_line = next((i for i, l in enumerate(lines, 1) if l.startswith("title:")), 1)

        block = None
        note_buf: list[tuple[int, str]] = []
        for offset, line in enumerate(body):
            ln = start + offset
            s = line.strip()
            if s.startswith("## "):
                head = s[3:].strip()
                block = {"投影片": "points", "圖": "diagram", "講稿": "notes"}.get(head)
                if block is None:
                    self.errors.append(f"第 {ln} 行：未知的區塊「{head}」（只能有 投影片／圖／講稿）")
                continue
            if not s:
                continue
            if block is None:
                self.errors.append(f"第 {ln} 行：內容不在任何 ## 區塊內")
            elif block == "points":
                if not s.startswith("- "):
                    self.errors.append(f"第 {ln} 行：投影片區塊每行都要用「- 」開頭")
                    continue
                self.bullets.append((ln, s[2:].strip()))
            elif block == "diagram":
                self.diagram.append((ln, s))
            else:
                note_buf.append((ln, s))

        if not self.bullets:
            self.errors.append("「## 投影片」區塊沒有任何項目")
        if len(self.diagram) > 1:
            self.errors.append(f"第 {self.diagram[1][0]} 行：「## 圖」只能有一行（A → B → C〔…〕）")
        if self.diagram:
            ln, t = self.diagram[0]
            nodes = [n for n in t.split("→") if strip_cites(n)]
            if not 2 <= len(nodes) <= 5:
                self.errors.append(f"第 {ln} 行：流程圖要有 2–5 個節點，用「→」分隔（目前 {len(nodes)} 個）")
            for n in nodes:
                if len(strip_cites(n)) > 12:
                    self.errors.append(f"第 {ln} 行：流程圖節點「{strip_cites(n)}」超過 12 字")
        self.notes = split_sentences(note_buf)


def split_sentences(lines: list[tuple[int, str]]) -> list[tuple[int, str]]:
    """把講稿切成句子。引用〔…〕必須放在句號前；句號後緊接的〔…〕會變成獨立片段（之後報錯）。"""
    out: list[tuple[int, str]] = []
    buf, buf_ln = "", 0
    for ln, text in lines:
        for ch in text:
            if not buf.strip():
                buf_ln = ln
            buf += ch
            if ch in SENT_END:
                out.append((buf_ln, buf.strip()))
                buf = ""
        buf += " "
    if buf.strip():
        out.append((buf_ln, buf.strip()))
    return out


def load_drafts(out_dir: Path) -> list[Draft]:
    d = out_dir / "drafts"
    return [Draft(p) for p in sorted(d.glob("*.md"))] if d.is_dir() else []
