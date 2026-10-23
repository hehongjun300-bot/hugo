# 从评估到交付

> 协作规则（谁先读什么、怎么交接）在 [AGENTS.md](AGENTS.md)，这里只写**每个阶段做什么**。

## 阶段 1 · 选与核查

1. 从 [resources/](resources/README.md) 按成片目标筛候选。
2. 只读与当前任务相关的条目：README、许可证、依赖、素材来源。
3. 结论回填到该条目：核查日期、版本/提交号、许可结论、风险。
4. 许可冲突或素材权利不明 → 条目标 `待确认`，不用于对外交付。

## 阶段 2 · 接入

1. 建 `projects/<ID>/`，写 `NOTES.md`（目标、受众、规格、所用资源及版本）。
2. 第三方代码放 `projects/<ID>/tool-src/`（已在 `.gitignore` 排除），**保留上游 LICENSE 与版权声明**。
   需要固定版本时改用 git submodule，不要直接提交上游副本。
3. 不动已有项目；先 `git status` 再装依赖。
4. `.gitignore` 排除：本机配置、密钥、缓存、成片大文件、`tool-src/`。

## 阶段 3 · 制作与复核

1. **先出 1 秒小样**验证渲染链路、字体、授权，再铺全长。5 秒片尤其如此：第 1 秒不对，后 4 秒白做。
2. 交付前核对：画面、时长、画幅、导出规格、素材许可、署名。
3. 保存可复现工程（锁版本）与最终导出目录。
4. **用命令验证，不靠肉眼**：

   ```bash
   ffprobe -v error -select_streams v:0 \
     -show_entries stream=width,height,r_frame_rate,nb_frames,duration \
     -of default=nw=1 path/to/out.mp4
   ```

   把实测值写进 `finish --note`，这样下一个人不用重跑。

## 阶段 4 · 归档

- 产物放 `projects/<ID>/out/`，大文件不入库（`.gitignore` 已排除 mp4/mov），在 `NOTES.md` 写清位置。
- 收工走脚本，不要手改 markdown：

  ```bash
  python tools/board.py finish P-00X --agent <名字> \
    --evidence projects/P-00X/out/v1.mp4 \
    --note "实测 5.000s / 300 帧 / 60fps" \
    --next "等人确认"
  python tools/board.py check
  ```

- 状态从 `进行中` → `已完成`，释放名额。
