# hehongjun300-bot / hugo

视频制作的工作台：一个统一的 agent 协作约定 + 按项目分目录的真实产出 + 可复用资源登记。

## 开始

**读 [AGENTS.md](AGENTS.md)，只读这一页。** 它包含三条协作规矩、开工/收工协议和文件地图。
其他文档都从那一页链接出去，不维护第二份规则。

```bash
python tools/board.py pick     # 看现在该做什么
python tools/board.py list     # 看全部任务
python tools/board.py check    # 收工前自检
```

## 目录

```
AGENTS.md            唯一入口：协作规则 + 开工/收工协议
board/tasks.json     唯一的进度数据源（任务、状态、证据、待回答问题）
PROJECT_STATUS.md    看板的人类可读视图（自动生成，勿手改）
tools/board.py       看板唯一写入口
DECISIONS.md         重要选择及其理由
WORKFLOW.md          从评估到交付的四个阶段
projects/<ID>/       每个真实项目一个目录：PROMPT / NOTES / 工程 / out
resources/           可复用工具与素材的登记（含许可筛查）
```

## 当前

- **进行中：无**（上限 1）
- P-001 5 秒动效宣传片 v1 **已完成** —— `projects/P-001-5s-splash/out/v1.mp4`
  实测 1920×1080 / 60fps / 300 帧 / 5.000s。
- 下一条可接手：P-002 资源许可证核查，或 P-003 Remotion 最小链路。

完整状态与待确认事项见 [PROJECT_STATUS.md](PROJECT_STATUS.md)。
