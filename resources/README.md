# 视频制作资源目录

下表用于快速选型。**链接已于 2026-10-23 核实并修正**——原记录把作者名错写成了本地账号 `hehongjun300-bot`，7 条链接全部 404。

## 关键事实：这些 skill 全是「用代码画画面」，没有一个是 AI 生成真人视频

如果你要做真人出镜、实拍感的视频（如 P-005 的 iPhone 自拍），这 7 个都**做不到**，
需要另外接入视频生成服务（Runway / Sora / 可灵等）。它们能做的都是几何图形、
文字、UI 截图、数据图表这类由代码绘制的内容。

| 项目 | 真实出处 | 星标 | 能做什么 | 许可证 | 详情 |
|---|---|---|---|---|---|
| video-shotcraft | [Vincentwei1021](https://github.com/Vincentwei1021/video-shotcraft) | 13.2k | 产品/UI 宣传片，158 张镜头卡 | Apache-2.0 | [条目](video-shotcraft.md) |
| lemo-opuscar | [lemomo-ai](https://github.com/lemomo-ai/lemo-opuscar) | 6.0k | 59 种电影风格的艺术短片 | MIT | [条目](lemo-opuscar.md) |
| huashu-art-motion | [alchaincyf](https://github.com/alchaincyf/huashu-art-motion) | 5.0k | 35 种艺术风格，口播/白板/数据 | MIT | [条目](huashu-art-motion.md) |
| mg-styles-15 | [Vincentwei1021](https://github.com/Vincentwei1021/mg-styles-15) | 1.9k | 15 种动态图形风格参考 | MIT | [条目](mg-styles-15.md) |
| xilo-opus-video | [Kianzzz](https://github.com/Kianzzz/xilo-opus-video) | 250 | 通用视频，先出 3 个方案再定稿 | MIT | [条目](xilo-opus-video.md) |
| dashi-animationstyle | [chuspeeism](https://github.com/chuspeeism/dashi-animationstyle) | 118 | 中文口播 → 7 种画风讲解动画 | **待人工核实** | [条目](dashi-animationstyle.md) |
| wtt-code-animation-studio | **来源无法核实** | — | 中文旁白代码动画（未证实） | 无法核实 | [条目](wtt-code-animation-studio.md) |

## 选型建议

| 你要做什么 | 用哪个 |
|---|---|
| App / 网站 / 产品宣传片 | **video-shotcraft**（已在本地，P-001 就是它做的） |
| 有强烈视觉风格的艺术短片 | lemo-opuscar |
| 中文口播的知识讲解 | dashi-animationstyle 或 huashu-art-motion |
| 品牌片头、转场、信息图动效 | mg-styles-15 |
| 要「先看方案再定稿」的正式项目 | xilo-opus-video |
| **真人出镜 / 实拍感画面** | **以上都不行**，需接视频生成服务 |

## 核查状态

- 6 个项目的出处、星标、许可证已核实（2026-10-23）
- `dashi-animationstyle` 的 LICENSE 存在但无法自动识别，商用前需人工读原文
- `wtt-code-animation-studio` 在 GitHub 上已找不到，**不要依据原记录使用**
- 接入顺序与选择由实际项目需求决定
