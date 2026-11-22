#!/usr/bin/env python3
"""topic-slides workflow 的狀態與紀錄工具（讓退回次數的計算是機械式的，而不是靠記憶）。

用法：
  wf_state.py init   <slug> --topic "主題"        建立 output/<slug>/；已存在就印出目前狀態（接續）
  wf_state.py show   <slug>                       印出 state.json
  wf_state.py log    <slug> --node N --result R [--detail 檢查結果] [--reason 退回原因]
                     [--change 修改內容] [--pages 03,05]
        R = pass（通過）| fail（關卡退回）| done（非關卡節點完成）| wait（等使用者）| stop（停止）
        result=fail 且 N 是關卡時，該關卡退回次數 +1；超過該關卡的上限 → 狀態改為 stopped，結束碼 3
  wf_state.py set    <slug> [--node N] [--status running|waiting|stopped|done] [--note 文字]
  wf_state.py report <slug>                       由 rounds.jsonl 產生 report.md
                                                  （保留 report.md 中 <!-- preamble --> … <!-- /preamble --> 的開頭區塊，
                                                    以及 <!-- manual --> 之後的人工內容）

節點編號 N（workflow v2）：0、1、2、2b、3、4、5、6、7、8、9、10（⓪ ① ② ②b ③–⑩）。
關卡與退回上限：⓪ 3、② 3、②b 2、⑤ 3、⑥ 2、⑦ 3、⑨ 3。
結束碼：0 = 正常；2 = 用法錯誤；3 = 停止條件觸發（某關卡退回超過上限）。
"""
from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUTPUT = ROOT / "output"

WORKFLOW_VERSION = "v2"
NODES = {  # 依執行順序
    "0": "⓪ lint 關卡", "1": "① 檢索", "2": "② 覆蓋率關卡", "2b": "②b 相關頁語意檢查",
    "3": "③ 證據卡", "4": "④ 大綱", "5": "⑤ 大綱確認", "6": "⑥ 逐頁稿", "7": "⑦ 忠實度審查",
    "8": "⑧ 渲染", "9": "⑨ 渲染檢查", "10": "⑩ 交件",
}
GATE_LIMITS = {"0": 3, "2": 3, "2b": 2, "5": 3, "6": 2, "7": 3, "9": 3}  # 關卡 → 退回上限
RESULT_LABEL = {"pass": "✅ 通過", "fail": "↩️ 退回", "done": "✔ 完成", "wait": "⏸ 等待使用者", "stop": "⛔ 停止"}
MANUAL_MARK = "<!-- manual -->"
PRE_START, PRE_END = "<!-- preamble -->", "<!-- /preamble -->"


def now() -> str:
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def paths(slug: str) -> tuple[Path, Path, Path]:
    d = OUTPUT / slug
    return d, d / "state.json", d / "rounds.jsonl"


def load(slug: str) -> dict:
    _, sp, _ = paths(slug)
    if not sp.is_file():
        print(f"ERROR {sp} 不存在，請先 init")
        sys.exit(2)
    return json.loads(sp.read_text(encoding="utf-8"))


def save(slug: str, st: dict) -> None:
    _, sp, _ = paths(slug)
    st["updated"] = now()
    sp.write_text(json.dumps(st, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def read_rounds(slug: str) -> list[dict]:
    _, _, rp = paths(slug)
    if not rp.is_file():
        return []
    return [json.loads(l) for l in rp.read_text(encoding="utf-8").splitlines() if l.strip()]


def cmd_init(a) -> int:
    d, sp, _ = paths(a.slug)
    if sp.is_file():
        print("RESUME")
        print(sp.read_text(encoding="utf-8"))
        return 0
    d.mkdir(parents=True, exist_ok=True)
    save(a.slug, {"topic": a.topic, "slug": a.slug, "workflow": WORKFLOW_VERSION, "node": "0",
                  "status": "running", "rejections": {g: 0 for g in GATE_LIMITS}, "stop_reason": "",
                  "note": "", "created": now()})
    print(f"NEW {d}")
    return 0


def cmd_show(a) -> int:
    print(json.dumps(load(a.slug), ensure_ascii=False, indent=2))
    return 0


def cmd_log(a) -> int:
    st = load(a.slug)
    rounds = read_rounds(a.slug)
    rnd = sum(1 for r in rounds if str(r["node"]) == a.node) + 1
    entry = {"time": now(), "node": a.node, "round": rnd, "result": a.result, "detail": a.detail or "",
             "reason": a.reason or "", "change": a.change or "", "pages": a.pages or ""}
    _, _, rp = paths(a.slug)
    with rp.open("a", encoding="utf-8") as f:
        f.write(json.dumps(entry, ensure_ascii=False) + "\n")
    st["node"] = a.node
    code = 0
    if a.result == "fail" and a.node in GATE_LIMITS:
        k, limit = a.node, GATE_LIMITS[a.node]
        st["rejections"][k] = st["rejections"].get(k, 0) + 1
        n = st["rejections"][k]
        print(f"{NODES[k]} 退回累計 {n} 輪（上限 {limit}）")
        if n > limit and st["status"] != "stopped":
            st["status"] = "stopped"
            st["stop_reason"] = f"{NODES[k]} 退回累計 {n} 輪，超過 {limit} 輪：{a.reason or a.detail}"
            print(f"STOP {st['stop_reason']}")
        if n > limit:
            code = 3
    elif a.result == "stop":
        st["status"] = "stopped"
        st["stop_reason"] = f"{NODES[a.node]}：{a.reason or a.detail}"
    elif a.result == "wait":
        st["status"] = "waiting"
    else:
        st["status"] = "running" if st["status"] != "done" else "done"
    save(a.slug, st)
    print(f"已記錄 {NODES[a.node]} 第 {rnd} 輪：{a.result}")
    return code


def cmd_set(a) -> int:
    st = load(a.slug)
    if a.node is not None:
        st["node"] = a.node
    if a.status:
        st["status"] = a.status
    if a.note is not None:
        st["note"] = a.note
    save(a.slug, st)
    print(json.dumps(st, ensure_ascii=False, indent=2))
    return 0


def cell(s: str) -> str:
    return (s or "—").replace("|", "\\|").replace("\n", "<br>")


def cmd_report(a) -> int:
    st = load(a.slug)
    rounds = read_rounds(a.slug)
    d, _, _ = paths(a.slug)
    rp = d / "report.md"
    manual, preamble = "", ""
    if rp.is_file():
        old = rp.read_text(encoding="utf-8")
        if MANUAL_MARK in old:
            manual = old.split(MANUAL_MARK, 1)[1].strip("\n")
        if PRE_START in old and PRE_END in old.split(PRE_START, 1)[1]:
            preamble = old.split(PRE_START, 1)[1].split(PRE_END, 1)[0].strip("\n")
    status_label = {"running": "進行中", "waiting": "等待使用者", "stopped": "⛔ 已停止", "done": "✅ 完成"}
    deck = d / "deck.html"
    shots = sorted((d / "screenshots").glob("slide-*.png")) if (d / "screenshots").is_dir() else []
    lines = [f"# topic-slides 報告：{st['topic']}", ""]
    if preamble:
        lines += [PRE_START, preamble, PRE_END, ""]
    lines += [
        f"- slug：`{st['slug']}`（workflow {st.get('workflow', 'v1')}）",
        f"- 狀態：{status_label.get(st['status'], st['status'])}",
        f"- 目前節點：{NODES[str(st['node'])]}",
        f"- 建立：{st.get('created', '')}；最後更新：{now()}",
        f"- 簡報：{'`deck.html`（' + str(len(shots)) + ' 張截圖）' if deck.is_file() else '尚未產生'}",
    ]
    if st.get("stop_reason"):
        lines.append(f"- **停止原因**：{st['stop_reason']}")
    if st.get("note"):
        lines.append(f"- 備註：{st['note']}")
    lines += ["", "## 關卡退回統計", "", "| 關卡 | 退回輪數 | 上限 |", "|---|---|---|"]
    for g, limit in GATE_LIMITS.items():
        lines.append(f"| {NODES[g]} | {st['rejections'].get(g, 0)} | {limit} |")
    lines += ["", "## 逐節點紀錄", "",
              "| 時間 | 節點 | 輪次 | 結果 | 檢查結果 | 退回原因 | 修改內容 | 涉及頁面 |",
              "|---|---|---|---|---|---|---|---|"]
    for r in rounds:
        lines.append(f"| {r['time']} | {NODES[str(r['node'])]} | {r['round']} | {RESULT_LABEL.get(r['result'], r['result'])} "
                     f"| {cell(r['detail'])} | {cell(r['reason'])} | {cell(r['change'])} | {cell(r['pages'])} |")
    lines += ["", MANUAL_MARK, manual or "## 補充說明\n\n（由 agent 補充：未解決的問題、需要使用者決定的事項。）", ""]
    rp.write_text("\n".join(lines), encoding="utf-8")
    print(f"已產生 {rp}")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description="topic-slides 狀態工具")
    sub = ap.add_subparsers(dest="cmd", required=True)
    p = sub.add_parser("init"); p.add_argument("slug"); p.add_argument("--topic", required=True)
    p = sub.add_parser("show"); p.add_argument("slug")
    p = sub.add_parser("log"); p.add_argument("slug")
    p.add_argument("--node", required=True, choices=list(NODES))
    p.add_argument("--result", required=True, choices=sorted(RESULT_LABEL))
    for opt in ("--detail", "--reason", "--change", "--pages"):
        p.add_argument(opt)
    p = sub.add_parser("set"); p.add_argument("slug")
    p.add_argument("--node", choices=list(NODES))
    p.add_argument("--status", choices=["running", "waiting", "stopped", "done"])
    p.add_argument("--note")
    p = sub.add_parser("report"); p.add_argument("slug")
    a = ap.parse_args()
    return {"init": cmd_init, "show": cmd_show, "log": cmd_log, "set": cmd_set, "report": cmd_report}[a.cmd](a)


if __name__ == "__main__":
    sys.exit(main())
