# iPhone 前置镜头自拍 · 手机掉地 5 秒视频提示词

> 用法：附上男生的三视图（正面 / 侧面 / 背面）作为角色参考图，配合下面任意一版提示词使用。
> 核心难点有三个：**① 角色一致性 ② 前后镜头逻辑（前置视角全程不变）③ 掉落的物理可信度与 iPhone 真实质感**。提示词里都做了针对性约束。

---

## 一、一句话版本（丢给 AI 先试水）

```
Vertical 9:16 selfie video, iPhone front camera. A young man casually holds the phone at arm's length, filming himself: upper body, slightly messy casual clothes, relaxed bored expression, looking at the screen. Real handheld micro-shake. Around 3s the phone slips from his fingers and falls — the camera tumbles, we see ceiling, then it hits the floor with a hard impact shake, framing the underside of his chin and the ceiling. Final ~1 second: the phone is picked up off the floor, the front camera comes back up to his face, slightly tilted and out of focus as it refocuses. Authentic iPhone front camera look: wide 24mm selfie lens, slight fisheye distortion, soft over-sharpened HDR skin, mild sensor noise and motion blur, auto-exposure hunting, no cinematic grading, no vlog filters, no beauty filter.
```

---

## 二、结构化完整版（推荐，配合三视图使用）

```text
TASK
Generate a single continuous ~5-second vertical video (9:16, ~24-30fps) shot entirely
on an iPhone's FRONT camera (selfie camera). The camera is the phone itself — the
entire video is what the front camera records. The character must exactly match the
attached three-view reference images (face, hairstyle, body proportions, clothing).

CHARACTER
Young man, [年龄], [身高体型], wearing [服装]. Face, hair, skin tone, and clothing
must be identical to the reference sheet — same jawline, same hairline, same ear shape.
No identity drift across the shot.

SETTING
[室内：卧室 / 客厅 / 走廊]，[时间：白天自然光 / 晚上顶灯]. Ordinary unremarkable
domestic interior, visible: [地板材质，如浅色木地板/灰色瓷砖], [背景元素：一张床、
一扇窗、门]. Realistic, slightly cluttered, lived-in. No studio lighting.

SHOT TIMELINE (total 5s)

0.0s – 3.0s  — HOLDING / SELFIE
He is holding the phone with one hand at roughly arm's length, casual and unposed —
not vlogging, not performing, just idly filming himself. Framing: upper body from
chest up, head slightly high in frame, a bit off-center. His free arm hangs relaxed.
He looks at the screen, blinks, maybe shifts weight, half-smiles or says something
under his breath. Natural handheld micro-shake: tiny rotational drift, no smooth
gimbal movement, occasional small refocus.

~3.0s – 3.6s — THE DROP (the key beat)
The phone slips out of his hand. His fingers fumble and lose grip — do NOT cut.
The camera falls: rapid tumbling, ceiling / ceiling light / wall / his arm sweeping
through frame, strong motion blur, heavy rolling shutter skew, exposure jumping as
the auto-exposure chases the bright ceiling light.

~3.6s — IMPACT
Hard impact, 2-3 frame violent camera shake, a bounce and settle. Then the camera
lies on the floor: extreme low angle, we see the underside of his chin, his legs and
feet, the ceiling, out-of-focus. Slight tilt. Frame is partially blocked by the floor
edge / a piece of furniture. Audio-visual feel of a real phone hitting the ground.

3.6s – 4.2s — ON THE FLOOR
The camera stays down. He reacts — we see him bend over, a hand reaching down toward
the lens, blurry, growing larger. His face is upside down / from below, distorted.

4.2s – 5.0s — PICKED UP
His hand grabs the phone and lifts it. Camera swings up quickly, the floor streaks
past, then settles in front of his face again — slightly tilted, slightly too close,
out of focus for a beat, then the autofocus snaps onto his eyes. His expression:
mildly annoyed / amused, a small exhale. End on a fraction of a second of stillness.

CAMERA / LENS (must read as iPhone front camera)
- 24mm equivalent ultra-wide selfie lens; obvious perspective distortion, nose and
  forehead slightly enlarged, edges of frame bowed.
- Slight fisheye / barrel distortion on a face close to the lens.
- Vertical 9:16, 1080p, ~30fps, standard iPhone HEVC look.
- Deep depth of field (small sensor) but soft, slightly over-sharpened edges.
- Dynamic range: real iPhone HDR — highlights clipped on the ceiling light,
  shadows lifted and slightly milky, no filmic highlight rolloff.
- Mild luminance noise in shadows, visible in low light; slight motion blur.
- Auto-exposure and auto-focus hunting during the drop and the pickup.
- Slight rolling shutter wobble on fast movement.

LIGHTING
Practical only. [窗光从侧面 / 顶灯偏冷], uneven, some falloff. Auto white balance
occasionally drifts warmer/cooler. No color grading, no teal-orange, no vignette
unless the lens produces one naturally.

STYLE / LOOK — MUST AVOID
NOT cinematic, NOT a music video, NOT a vlog with transitions, NOT a commercial.
No gimbal smoothness, no dolly, no drone, no slow motion, no rack focus artistry.
No beauty filter, no skin smoothing, no face reshaping, no teeth whitening.
No added grain overlay, no letterbox bars, no captions, no UI overlay
(unless [可选：想要的话加上 iPhone 相机界面 / 录制小红点]).
Feels like a random clip someone accidentally filmed, found later in their camera roll.

SOUND (if the model supports it)
Room tone, faint breathing, fabric rustle, the plastic clatter of the phone hitting
the floor, a small "ah" or breath from him, then the scrape of the phone being lifted.

NEGATIVE / 反向提示
cartoon, anime, CGI, 3D render, uncanny valley, plastic skin, waxy face, glowing skin,
professional camera, bokeh balls, shallow depth of field, cinematic teal-orange grade,
stabilized footage, drone shot, slow motion, beauty filter, face swap artifacts,
extra fingers, distorted hands, multiple people, text, watermark, logo, subtitles,
letterbox, oversaturated colors, HDR glow, video game look, AI-generated artifacts,
inconsistent face between frames, floating phone, impossible physics,
mirror-flip errors, back camera (must always be FRONT camera).
```

---

## 三、分段提示词版（如果模型支持分镜 / 首尾帧）

有些工具（可灵、Veo、Sora、Runway 等）对**单段 5 秒复杂动作**容易翻车，建议拆成 3 段生成再拼接，一致性会明显更好。

### 镜头 1（0–3s）：举着手机自拍

```text
Vertical 9:16, iPhone front camera selfie shot, 24mm. A young man [描述] holds the
phone at arm's length, upper body in frame, relaxed and unposed, looking into the lens,
casual handheld micro-shake. Real domestic interior, natural light. Authentic iPhone
front camera look: wide-angle face distortion, HDR highlights, light sensor noise,
no filter, no grading. Continuous single take, no cuts.
```

### 镜头 2（3–4s）：手机掉落 + 触地

```text
POV of a phone falling to the floor. The camera tumbles downward, ceiling and arms
sweeping through frame, heavy motion blur and rolling shutter skew, exposure
flickering. Impact: violent 2-3 frame shake, a bounce, then the phone lies flat on
[地板材质]. Now shooting from floor level: the underside of the man's chin above,
his feet, out of focus, ceiling light blown out.
```

### 镜头 3（4–5s）：被捡起，回到脸上

```text
The phone is lifted off the floor from below. A hand enters and grabs it, the camera
swings up fast — floor and legs streaking past — and settles into a selfie angle in
front of the man's face, slightly tilted and too close. Autofocus hunts, then snaps
onto his eyes. His face: mildly annoyed/amused. iPhone front camera look maintained.
```

> 拼接提示：镜头 2 的最后一帧和镜头 3 的第一帧尽量同机位（都是贴地平视），接缝最好藏在那次"手伸进来"的瞬间。

---

## 四、参考图使用建议

1. **三视图怎么喂**：正面图最关键，用来锁脸；侧面图锁鼻梁和下颌线；背面图锁发型后脑勺。大多数模型只看正面就够，但侧面能显著减少后半段"抬头/低头"时的脸崩。
2. **加一句锚定**：在提示词最前面加 `Use the character from the reference images exactly as shown. Do not change his face, hairstyle, or clothing.` 这类硬约束。
3. **负面清单里一定要有** `face changes between shots`、`different person`、`face morphing`。
4. 如果模型支持 **角色参考 / 首帧 + 尾帧**，最稳的做法是：截一张他举手机自拍的图当首帧，截一张"躺地视角"图当中段，尾帧是"捡起来对着脸"。

---

## 五、几个容易翻车的点（实测经验）

| 问题 | 解决 |
|---|---|
| 手机掉地后画面变成"第三视角" | 提示词里反复强调 `the camera IS the phone, the frame is always the front camera` |
| 模型自动切到后置镜头（拍地面） | 负面里写死 `back camera`，正面写 `front camera at all times` |
| 掉地过程太平滑，像无人机 | 强调 `tumbling, motion blur, rolling shutter, exposure flicker` |
| 皮肤太干净，一眼 AI | 加 `skin texture pores, slight oiliness, no beauty filter, no smoothing` |
| 画面太"电影感" | 加 `ungraded, no log, no LUT, straight-out-of-iPhone` |
| 脸在低头/仰头时变形 | 用三视图的侧面 + 负面 `face morphing` |
| 最后捡起来时运镜太"顺" | 加 `slightly too close, tilted, autofocus hunting, one-handed grab` |

---

## 六、参数建议

- 画幅：9:16（竖屏），1080×1920 或 2160×3840
- 帧率：24 或 30fps（想更像手机就 30）
- 时长：5s（模型上限不足时，按上面拆成 3 段）
- 运镜强度：如果有"手持感"参数，调到**中高**；有"稳定性"参数，调到**低**
- 风格强度 / CFG：偏低一些，让画面"平凡"一点，别被模型往"电影感"拽
