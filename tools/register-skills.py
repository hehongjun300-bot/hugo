#!/usr/bin/env python3
"""register-skills.py — 把 skills/ 里下载好的 skill 登记到 Codex 的扫描目录。

为什么需要这一步：Codex 只会扫描 ~/.codex/skills/ 下"第一层文件夹里有 SKILL.md"
的 skill。下载到 D 盘 skills/ 里的仓库，SKILL.md 往往藏在子目录，Codex 看不到。
本脚本找出每个真正的 SKILL.md，在扫描目录里建一个指向它的入口（Windows 目录联接，
几乎不占空间，也不需要管理员权限）。没有 SKILL.md 的仓库会被跳过并说明。

用法：
  python tools/register-skills.py             # 登记
  python tools/register-skills.py --dry-run   # 只看会做什么
  python tools/register-skills.py --copy      # 联接失败时改为复制
  python tools/register-skills.py --target X  # 指定扫描目录（测试用）
"""
import argparse, os, re, shutil, stat, subprocess, sys
from pathlib import Path

for s in (sys.stdout, sys.stderr):
    try: s.reconfigure(encoding="utf-8")
    except Exception: pass

ROOT = Path(__file__).resolve().parent.parent
SKIP_DIRS = {".git", "node_modules"}


def is_link(p: Path) -> bool:
    try:
        st = os.lstat(p)
    except OSError:
        return False
    return stat.S_ISLNK(st.st_mode) or bool(getattr(st, "st_file_attributes", 0) & 0x400)


def find_skills(src: Path):
    for dp, dns, fns in os.walk(src):
        dns[:] = [d for d in dns if d not in SKIP_DIRS]
        if "SKILL.md" in fns:
            yield Path(dp)


def read_meta(skill_dir: Path):
    text = (skill_dir / "SKILL.md").read_text(encoding="utf-8", errors="replace")
    m = re.match(r"---\s*\n(.*?)\n---", text, re.S)
    head = m.group(1) if m else ""
    name = re.search(r"^name:\s*(.+)$", head, re.M)
    desc = re.search(r"^description:\s*(.+)$", head, re.M)
    return (name.group(1).strip().strip("\"'") if name else None), bool(desc)


def link(src: Path, dst: Path, copy: bool) -> str:
    if not copy:
        r = subprocess.run(["cmd", "/c", "mklink", "/J", str(dst), str(src)],
                           capture_output=True)
        if r.returncode == 0 and dst.exists():
            return "联接"
    shutil.copytree(src, dst, ignore=shutil.ignore_patterns(".git", "node_modules"))
    return "复制"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--src", default=str(ROOT / "skills"))
    ap.add_argument("--target", default=str(Path.home() / ".codex" / "skills"))
    ap.add_argument("--copy", action="store_true")
    ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args()
    src, target = Path(a.src), Path(a.target)
    if not src.is_dir():
        sys.exit(f"✗ 找不到 {src}，先运行 bash tools/install-skills.sh")
    target.mkdir(parents=True, exist_ok=True)

    found = list(find_skills(src))
    repos = [p for p in src.iterdir() if p.is_dir()]
    ok = skipped = 0
    for repo in repos:
        if not any(repo in d.parents or d == repo for d in found):
            print(f"· 跳过 {repo.name}：仓库里没有 SKILL.md，不是 skill（只是资料/样片）")
    for d in found:
        name, has_desc = read_meta(d)
        name = name or d.name
        rel = d.relative_to(src)
        if not has_desc:
            print(f"✗ 跳过 {rel}：SKILL.md 缺少 description，Codex 无法匹配"); skipped += 1; continue
        dst = target / name
        if dst.exists() or is_link(dst):
            print(f"· 已存在 {name}，不覆盖（来源 {rel}）"); skipped += 1; continue
        if a.dry_run:
            print(f"[预演] {name}  <-  {rel}"); ok += 1; continue
        how = link(d, dst, a.copy)
        good = (dst / "SKILL.md").is_file()
        print(f"{'✓' if good else '✗'} {name}  <-  {rel}  ({how})")
        ok += good
        skipped += not good
    print(f"\n登记 {ok} 个，跳过 {skipped} 个。扫描目录：{target}")
    print("扫描目录当前内容：", ", ".join(sorted(p.name for p in target.iterdir())) or "(空)")
    print("提示：登记后需要重启 Codex（关闭窗口再打开）才会重新扫描。")


if __name__ == "__main__":
    main()
