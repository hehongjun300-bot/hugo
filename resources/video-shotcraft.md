# video-shotcraft

- **真实出处**：https://github.com/Vincentwei1021/video-shotcraft
- 星标：约 13,200（2026-10-23 查）
- 资源形态：Agent Skill + 工程/镜头库（TypeScript + Remotion）
- 许可：**Apache-2.0**（已核实仓库 LICENSE）
- 演示站：https://vincentwei1021.github.io/video-shotcraft/
- 本地副本：`projects/P-001-5s-splash/tool-src/video-shotcraft-main/`（未入库，被 .gitignore 排除）

## 能做什么

用**代码**（React/Remotion）逐帧渲染出产品宣传片。核心资产：

- 158 张镜头配方卡，附 demo 源码和动态样片
- 一支已验收的完整宣传片模板（Ink Press）
- 真实页面截图 + 2.5D 运镜 + 节奏卡点 + 声音设计
- 六阶段工作流，三种使用模式（模板 / 自主创作 / 共同创作）

**典型用途**：把 App、网站、前端项目做成产品宣传片。

## 不能做什么

**不能生成真人影像。** 画面全部由代码画出（几何图形、文字、UI 截图），没有视频生成模型。
要拍真人、实拍感的画面，必须用另外的视频生成服务（Runway / Sora / 可灵等）。

已核实：仓库内没有引用任何视频生成模型。

## 为什么用它

P-001（5 秒动效宣传片）就是用它做的，成片 `projects/P-001-5s-splash/out/v1.mp4`。

## 使用前检查

- 部分音效来源不明，商用前需逐个核对 `assets/audio/ATTRIBUTION.md`
- 依赖 Remotion，Remotion 对商业用途另有许可条件，接商业项目前需确认
- 字体按各自许可核查
