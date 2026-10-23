<!-- 本文件由 tools/board.py 自动生成，请勿手工编辑。
     要改状态：python tools/board.py claim|finish|block <ID> --agent <你的名字> -->

# 项目状态

- 最近更新：2026-10-23 21:25
- 正在进行的任务数：0（上限 3）
- 任务总数：5　待开始 2　待确认 1　已完成 1

## 看板

| ID | 任务 | 状态 | 负责 | 阻塞 | 证据 |
|---|---|---|---|---|---|
| P-003 | 建 Remotion 最小渲染链路 | · 待开始 | — | — | — |
| P-002 | 资源条目上游核查（7 项许可证与素材来源） | · 待开始 | — | — | `resources/` |
| P-005 | iPhone 前置自拍掉地 5 秒视频 | ? 待确认 | Codex | 当前会话未连接 Runway 或其他视频生成工具；需要先连接可用的视频生成服务才能依据三视图渲染 MP4 | — |
| P-001 | 5 秒动效宣传片 v1（16:9 / 1920×1080） | ✓ 已完成 | Codex | — | `projects/P-001-5s-splash/out/v1.mp4`<br>`projects/P-001-5s-splash/out/last-frame.png`<br>`projects/P-001-5s-splash/PROMPT.md` |
| P-004 | 竖屏版 1080×1920 宣传片（如需） | ~ 已搁置 | — | — | — |

图例：✓ 已完成　▶ 进行中　? 待确认（卡在人身上）　· 待开始　~ 已搁置

## 下一步（每个任务只写一个具体动作）

| ID | 下一步 |
|---|---|
| P-003 | 在 projects/P-003-remotion-smoke/ 出 1 秒纯色测试片，验证 ffmpeg 与 Node 版本可用 |
| P-002 | 从 video-shotcraft 开始核原文 LICENSE、音效 ATTRIBUTION.md，把结论回填 resources/video-shotcraft.md |
| P-005 | 连接 Runway 或其他视频生成工具后，按 RUNWAY_PROMPT.md 出 out/v1.mp4 并用 ffprobe 核对 |

## 待确认 · 需要人回答

1. P-001 的 v1.mp4 观感是否可用？主文案「一起，向前」和品牌色 #E85A2C 仍是占位，要给正式的吗？　<sub>(2026-10-23 20:20 by Claude)</sub>
2. 仓库本地有大量未提交改动（12 个跟踪文件 + projects/ 全部未跟踪），要不要现在提交并 push 到 GitHub？　<sub>(2026-10-23 20:20 by Claude)</sub>
3. projects/P-001-5s-splash/tool-src/ 是 302MB / 11825 个文件的上游 video-shotcraft 副本，放进仓库会让 clone 变慢。改成 .gitignore 排除、或改为 git submodule？　<sub>(2026-10-23 20:20 by Claude)</sub>
4. [P-005] 当前会话未连接 Runway 或其他视频生成工具；需要先连接可用的视频生成服务才能依据三视图渲染 MP4　<sub>(2026-10-23 21:21 by Codex)</sub>

> 回答后：`python tools/board.py q --resolve <序号> --answer "结论"`

## 交接记录（最近 15 条，倒序）

- `2026-10-23 21:25` **Codex**：P-005 → 待确认。三视图已复制，生成提示词已补全；待连接视频生成工具
- `2026-10-23 21:21` **Codex**：P-005 阻塞：当前会话未连接 Runway 或其他视频生成工具；需要先连接可用的视频生成服务才能依据三视图渲染 MP4
- `2026-10-23 21:19` **Codex**：接手 P-005「iPhone 前置自拍掉地 5 秒视频」
- `2026-10-23 20:55` **Claude**：给任务加 priority 字段（数字小=优先），让 pick 先推荐真实视频工作而不是内务核查。
- `2026-10-23 20:51` **Claude**：新建 P-005：iPhone 前置自拍 5 秒视频（自拍→掉地→捡起），提示词已备好，等 Codex 接手出片
- `2026-10-23 20:51` **Claude**：新建 P-005「iPhone 前置自拍掉地 5 秒视频」
- `2026-10-23 20:45` **Claude**：P-001 的 NOTES.md 仍写「进行中」（看板早已改成已完成），这是 Codex 说 P-001 占着名额的真实原因；已改正。同时把进行中上限从 1 调到 3。
- `2026-10-23 20:20` **Claude**：把 PROJECT_STATUS.md 从手改表格改为 board/tasks.json 单一数据源 + tools/board.py 生成视图；按 ffprobe 实测把 P-001 从进行中更正为已完成。
