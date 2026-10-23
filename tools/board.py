#!/usr/bin/env python3
"""board.py — 多 agent 共享任务看板的唯一写入口。

数据源：board/tasks.json
生成物：PROJECT_STATUS.md（不要手改，会被覆盖）

设计原则：
  1. 永远不要在 markdown 里手工改状态 —— 那是生成物，下一次 render 就冲掉了。
  2. 所有变更走本脚本，脚本会同时更新 updated 时间戳并重渲染视图。
  3. 同一时刻最多一个「进行中」（可配），冲突时脚本拒绝并告诉你谁占着。

用法见 `python tools/board.py --help`。
"""
from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime
from pathlib import Path

# Windows 默认控制台编码是 GBK，输出中文和 ✓ 会直接炸。强制 UTF-8。
for _stream in (sys.stdout, sys.stderr):
    try:
        _stream.reconfigure(encoding="utf-8")
    except (AttributeError, OSError):
        pass

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "board" / "tasks.json"
VIEW = ROOT / "PROJECT_STATUS.md"

VALID = ["待开始", "进行中", "待确认", "已完成", "已搁置"]
ICON = {"待开始": "·", "进行中": "▶", "待确认": "?", "已完成": "✓", "已搁置": "~"}


# ---------------------------------------------------------------- 读写

def now() -> str:
    return datetime.now().strftime("%Y-%m-%d %H:%M")


def load() -> dict:
    if not DATA.exists():
        return {"schema": 1, "updated": now(), "max_in_progress": 1,
                "tasks": [], "questions": [], "handoff": []}
    with DATA.open(encoding="utf-8") as f:
        return json.load(f)


def save(d: dict) -> None:
    d["updated"] = now()
    DATA.parent.mkdir(parents=True, exist_ok=True)
    with DATA.open("w", encoding="utf-8", newline="\n") as f:
        json.dump(d, f, ensure_ascii=False, indent=2)
        f.write("\n")
    render(d)


def find(d: dict, tid: str) -> dict:
    for t in d["tasks"]:
        if t["id"].lower() == tid.lower():
            return t
    die(f"没有 ID 为 {tid} 的任务。用 `list` 看现有 ID。")


def die(msg: str) -> None:
    print(f"✗ {msg}", file=sys.stderr)
    sys.exit(1)


def ok(msg: str) -> None:
    print(f"✓ {msg}")


# ---------------------------------------------------------------- 渲染

def esc(s: str) -> str:
    return (s or "").replace("|", "\\|").replace("\n", " ")


def render(d: dict | None = None) -> None:
    d = d or load()
    tasks = d["tasks"]
    order = {s: i for i, s in enumerate(VALID)}
    tasks_sorted = sorted(tasks, key=lambda t: (order.get(t.get("status"), 9),
                                                t.get("priority", 5), t["id"]))

    running = [t for t in tasks if t.get("status") == "进行中"]
    lines = [
        "<!-- 本文件由 tools/board.py 自动生成，请勿手工编辑。",
        "     要改状态：python tools/board.py claim|finish|block <ID> --agent <你的名字> -->",
        "",
        "# 项目状态",
        "",
        f"- 最近更新：{d.get('updated', '')}",
        f"- 正在进行的任务数：{len(running)}（上限 {d.get('max_in_progress', 1)}）",
        f"- 任务总数：{len(tasks)}　"
        f"待开始 {sum(1 for t in tasks if t.get('status') == '待开始')}　"
        f"待确认 {sum(1 for t in tasks if t.get('status') == '待确认')}　"
        f"已完成 {sum(1 for t in tasks if t.get('status') == '已完成')}",
        "",
        "## 看板",
        "",
        "| ID | 任务 | 状态 | 负责 | 阻塞 | 证据 |",
        "|---|---|---|---|---|---|",
    ]
    for t in tasks_sorted:
        ev = t.get("evidence") or []
        evs = "<br>".join(f"`{e}`" for e in ev) if ev else "—"
        lines.append(
            f"| {t['id']} | {esc(t.get('title'))} | {ICON[t['status']]} {t['status']} "
            f"| {esc(t.get('owner')) or '—'} | {esc(t.get('blocked')) or '—'} | {evs} |"
        )
    lines += ["", "图例：✓ 已完成　▶ 进行中　? 待确认（卡在人身上）　· 待开始　~ 已搁置", ""]

    # 下一步
    lines += ["## 下一步（每个任务只写一个具体动作）", "",
              "| ID | 下一步 |", "|---|---|"]
    for t in tasks_sorted:
        if t["status"] in ("已完成", "已搁置"):
            continue
        lines.append(f"| {t['id']} | {esc(t.get('next')) or '—'} |")
    lines.append("")

    # 需要人回答
    open_q = [q for q in d.get("questions", []) if not q.get("resolved")]
    if open_q:
        lines += ["## 待确认 · 需要人回答", ""]
        for i, q in enumerate(open_q, 1):
            lines.append(f"{i}. {q['text']}　<sub>({q.get('at', '')} by {q.get('by', '?')})</sub>")
        lines.append("")
        lines.append("> 回答后：`python tools/board.py q --resolve <序号> --answer \"结论\"`")
        lines.append("")

    # 交接
    hist = d.get("handoff", [])[-15:]
    if hist:
        lines += ["## 交接记录（最近 15 条，倒序）", ""]
        for h in reversed(hist):
            lines.append(f"- `{h.get('at', '')}` **{h.get('by', '?')}**：{h.get('text', '')}")
        lines.append("")

    VIEW.write_text("\n".join(lines), encoding="utf-8", newline="\n")


# ---------------------------------------------------------------- 命令

def cmd_render(a) -> None:
    render()
    ok(f"已重新生成 {VIEW.relative_to(ROOT)}")


def cmd_list(a) -> None:
    d = load()
    if a.json:
        print(json.dumps(d, ensure_ascii=False, indent=2))
        return
    print(f"最近更新 {d.get('updated', '')}　进行中上限 {d.get('max_in_progress', 1)}\n")
    print(f"{'ID':<8}{'状态':<7}{'负责':<10}任务")
    print("-" * 76)
    for t in sorted(d["tasks"], key=lambda x: x["id"]):
        mark = "  ← 进行中" if t["status"] == "进行中" else ""
        print(f"{t['id']:<8}{t['status']:<7}{(t.get('owner') or '—'):<10}{t.get('title', '')}{mark}")


def _set_status(t: dict, status: str, agent: str, d: dict) -> None:
    if status not in VALID:
        die(f"状态只能是：{' / '.join(VALID)}")
    if status == "进行中":
        cap = d.get("max_in_progress", 1)
        busy = [x for x in d["tasks"] if x["status"] == "进行中" and x["id"] != t["id"]]
        if len(busy) >= cap:
            names = "、".join(f"{x['id']}（{x.get('owner') or '未知'}）" for x in busy)
            die(f"「进行中」名额已满：{names}。\n"
                f"  要么先让它收工（finish/block），要么你接手一条别的「待开始」。\n"
                f"  确实需要并行时，由人把 board/tasks.json 的 max_in_progress 调大。")
    t["status"] = status
    t["owner"] = agent
    t["updated"] = now()


def cmd_claim(a) -> None:
    d = load()
    t = find(d, a.id)
    if t["status"] == "已完成" and not a.force:
        die(f"{t['id']} 已完成。要重开请加 --force。")
    if t["status"] == "进行中" and t.get("owner") and t["owner"] != a.agent and not a.force:
        die(f"{t['id']} 正被 {t['owner']} 占用。要强行接手加 --force（会覆盖负责字段）。")
    _set_status(t, "进行中", a.agent, d)
    if a.next:
        t["next"] = a.next
    d.setdefault("handoff", []).append(
        {"at": now(), "by": a.agent, "text": f"接手 {t['id']}「{t.get('title', '')}」"})
    save(d)
    ok(f"{t['id']} 已标记为进行中，负责：{a.agent}")


def cmd_finish(a) -> None:
    d = load()
    t = find(d, a.id)
    status = a.status or "已完成"
    _set_status(t, status, a.agent, d)
    if a.evidence:
        t.setdefault("evidence", [])
        for e in a.evidence:
            if e not in t["evidence"]:
                t["evidence"].append(e)
    if a.note:
        t["note"] = a.note
    t["next"] = a.next or ""
    if status == "已完成" and not t.get("evidence"):
        print("⚠ 已完成但没有证据路径，另一个 agent 无法核实。建议补 --evidence。", file=sys.stderr)
    if status == "待确认" and not a.note:
        print("⚠ 待确认需要在 --note 里写清人需要回答什么。", file=sys.stderr)
    d.setdefault("handoff", []).append(
        {"at": now(), "by": a.agent,
         "text": f"{t['id']} → {status}。{a.note or ''}".strip()})
    save(d)
    ok(f"{t['id']} → {status}")


def cmd_block(a) -> None:
    d = load()
    t = find(d, a.id)
    _set_status(t, "待确认", a.agent, d)
    t["blocked"] = a.reason
    d.setdefault("questions", []).append(
        {"text": f"[{t['id']}] {a.reason}", "at": now(), "by": a.agent, "resolved": False})
    d.setdefault("handoff", []).append(
        {"at": now(), "by": a.agent, "text": f"{t['id']} 阻塞：{a.reason}"})
    save(d)
    ok(f"{t['id']} → 待确认，问题已记入看板")


def cmd_add(a) -> None:
    d = load()
    if any(t["id"].lower() == a.id.lower() for t in d["tasks"]):
        die(f"{a.id} 已存在。")
    d["tasks"].append({
        "id": a.id, "title": a.title, "status": a.status or "待开始",
        "owner": a.owner or "", "blocked": "", "evidence": [],
        "next": a.next or "", "created": now(), "updated": now(),
    })
    d.setdefault("handoff", []).append(
        {"at": now(), "by": a.agent, "text": f"新建 {a.id}「{a.title}」"})
    save(d)
    ok(f"已新建 {a.id}")


def cmd_note(a) -> None:
    d = load()
    d.setdefault("handoff", []).append({"at": now(), "by": a.agent, "text": a.text})
    save(d)
    ok("已记入交接记录")


def cmd_q(a) -> None:
    d = load()
    if a.resolve:
        open_q = [q for q in d.get("questions", []) if not q.get("resolved")]
        idx = a.resolve - 1
        if idx < 0 or idx >= len(open_q):
            die(f"没有第 {a.resolve} 个待回答问题。")
        open_q[idx]["resolved"] = True
        open_q[idx]["answer"] = a.answer or ""
        open_q[idx]["resolved_at"] = now()
        save(d)
        ok(f"已关闭问题：{open_q[idx]['text'][:40]}")
        return
    if a.text:
        d.setdefault("questions", []).append(
            {"text": a.text, "at": now(), "by": a.agent or "?", "resolved": False})
        save(d)
        ok("问题已记录")


def cmd_check(a) -> None:
    d = load()
    problems = []
    running = [t for t in d["tasks"] if t["status"] == "进行中"]
    if len(running) > d.get("max_in_progress", 1):
        problems.append(f"进行中的任务有 {len(running)} 个，超过上限："
                        + "、".join(t["id"] for t in running))
    for t in d["tasks"]:
        if t["status"] not in VALID:
            problems.append(f"{t['id']} 状态非法：{t['status']}")
        if t["status"] == "已完成" and not t.get("evidence"):
            problems.append(f"{t['id']} 已完成但没有证据路径")
        for e in t.get("evidence", []):
            if e.startswith("外链"):
                continue
            if not (ROOT / e.split("#")[0]).exists():
                problems.append(f"{t['id']} 证据文件不存在：{e}")
        if t["status"] == "待确认" and not t.get("blocked"):
            problems.append(f"{t['id']} 待确认但没写阻塞原因")
    if problems:
        for p in problems:
            print(f"✗ {p}")
        sys.exit(1)
    ok(f"看板一致：{len(d['tasks'])} 个任务，{len(running)} 个进行中")


def cmd_pick(a) -> None:
    d = load()
    cap = d.get("max_in_progress", 1)
    running = [t for t in d["tasks"] if t["status"] == "进行中"]
    if len(running) >= cap:
        t = running[0]
        print(f"当前只有 {t['id']}「{t.get('title', '')}」在进行中（{t.get('owner') or '未知'}）。")
        print(f"要么接手它，要么等它收工。它的下一步：{t.get('next') or '（没写）'}")
        return
    todo = [t for t in d["tasks"] if t["status"] == "待开始"]
    if not todo:
        print("没有待开始的任务。用 `add` 新建，或处理待确认的问题。")
        return
    # priority 小 = 更优先；没写 priority 的当 5
    todo.sort(key=lambda t: (t.get("priority", 5), t["id"]))
    t = todo[0]
    p = t.get("priority", 5)
    print(f"建议接手：{t['id']}「{t.get('title', '')}」" + (f"  （优先级 {p}）" if p != 5 else ""))
    print(f"下一步：{t.get('next') or '（没写）'}")
    if len(todo) > 1:
        others = "、".join(f"{x['id']}({x.get('priority', 5)})" for x in todo[1:4])
        print(f"其它待开始：{others}")
    print(f"\n接手指令：python tools/board.py claim {t['id']} --agent <你的名字>")


# ---------------------------------------------------------------- 入口

def main() -> None:
    p = argparse.ArgumentParser(
        prog="board.py", description="多 agent 共享任务看板（数据源 board/tasks.json）")
    sub = p.add_subparsers(dest="cmd", required=True)

    s = sub.add_parser("render", help="重新生成 PROJECT_STATUS.md")
    s.set_defaults(fn=cmd_render)

    s = sub.add_parser("list", help="列出所有任务")
    s.add_argument("--json", action="store_true")
    s.set_defaults(fn=cmd_list)

    s = sub.add_parser("pick", help="建议下一个该做什么")
    s.set_defaults(fn=cmd_pick)

    s = sub.add_parser("claim", help="接手一个任务（标记进行中）")
    s.add_argument("id")
    s.add_argument("--agent", required=True)
    s.add_argument("--next", default="")
    s.add_argument("--force", action="store_true")
    s.set_defaults(fn=cmd_claim)

    s = sub.add_parser("finish", help="收工（默认已完成）")
    s.add_argument("id")
    s.add_argument("--agent", required=True)
    s.add_argument("--status", default="已完成", choices=VALID)
    s.add_argument("--evidence", action="append", default=[])
    s.add_argument("--note", default="")
    s.add_argument("--next", default="")
    s.set_defaults(fn=cmd_finish)

    s = sub.add_parser("block", help="卡住了，转待确认并登记问题")
    s.add_argument("id")
    s.add_argument("--agent", required=True)
    s.add_argument("--reason", required=True)
    s.set_defaults(fn=cmd_block)

    s = sub.add_parser("add", help="新建任务")
    s.add_argument("id")
    s.add_argument("--title", required=True)
    s.add_argument("--status", default="待开始", choices=VALID)
    s.add_argument("--owner", default="")
    s.add_argument("--next", default="")
    s.add_argument("--agent", default="?")
    s.set_defaults(fn=cmd_add)

    s = sub.add_parser("note", help="只追加一条交接记录")
    s.add_argument("text")
    s.add_argument("--agent", default="?")
    s.set_defaults(fn=cmd_note)

    s = sub.add_parser("q", help="登记/关闭「需要人回答」的问题")
    s.add_argument("text", nargs="?", default="")
    s.add_argument("--agent", default="?")
    s.add_argument("--resolve", type=int)
    s.add_argument("--answer", default="")
    s.set_defaults(fn=cmd_q)

    s = sub.add_parser("check", help="一致性自检（CI / 收工前跑）")
    s.set_defaults(fn=cmd_check)

    a = p.parse_args()
    a.fn(a)


if __name__ == "__main__":
    main()
