# 可选 Blender 子技能的分工

先读任务需要的那一行。按表中的技能名在当前会话技能目录找到并打开相应的 `SKILL.md`；具体脚本相对该技能目录解析。若环境只装了总控包，仍可按本包中的量图、造型和验收说明工作。下表的子技能是可选的专业入口。

| 遇到什么任务 | 优先使用 | 交给下一步的结果 |
| --- | --- | --- |
| 选 Blender 后端、确认连接的是目标场景 | `text-to-blender` | 实际运行时、文件、可用操作和受支持的执行路径。 |
| 跨多个工序、需要协调已有流程 | `blender-pro-workflow`、`blender-skill-harmonizer` | 本次阶段顺序和交接条件；以用户交付阶段作为终点。 |
| 整理艺术图、图纸、线稿的依据 | `reference-analysis-validator`、`reference-to-3d` | 图集角色、可见部件、需求与候选蒙版。 |
| 多张图需要统一坐标或彼此矛盾 | `orthographic-registration`、`multiview-constraint-solver` | 每视图像素变换、单位、共同基准和冲突处置。 |
| 线条相接、部件覆盖，或已有可用轮廓 | `source-part-segmentation`、`contour-to-mesh`；工程正交线稿用 `wireframe-to-3d` | 带孔洞的部件轮廓、深度约束和对应截面。 |
| 品牌标志、吉祥物有严格的轮廓和配色要求 | `mascot-logo-reconstruction` | 各部件的形状、前后层次及图集对应关系。 |
| 分面、壳体、实体缺口、组装及局部返修 | `image-to-blender-production`、`blender-modeling` | 可编辑几何及对应的截面/连接/光轴检查；前者附组件审核脚本。 |
| UV、贴花或给定的纹理图集 | `blender-uv-texturing`、`atlas-uv-fitting` | 稳定几何上的材质槽、独立 UV 岛和图集分区。 |
| 贴图与形状不符、侧壁或背面缺图 | `texture-driven-mesh-fitting`、`closed-surface-uv-coverage` | 修正后的边界对应关系以及前、后、侧的覆盖证据。 |
| 比较同机位造型 | `blender-cameras`、`multiview-fit-loop`、`landmark-fit-repair` | 锁定的对照相机、分视角差异和具体到地标的修改量。 |
| 形体接近但质感、透明件或发光效果不对 | `blender-materials`、`blender-lighting`、`reference-look-calibration` | 同一形体、机位、曝光条件下复测的材质及照明。 |
| 活动结构、表情或纹理状态变化 | `blender-animation`；纹理驱动变化用 `texture-state-animation`；关键帧和动作接触表用 `animation-quality-gate` | 时间轴、关键姿势、运动净空和帧间稳定性。只有参考或委托要求环形动态 HUD 时才用 `orbital-hud-motion`。 |
| 反复返修，外观或多个交付指标退化 | `fit-repair-optimizer`、`quality-refinement-autoloop` | 按相机、几何、材质等原因排定的修复顺序与回归证据。 |
| 从已保存母版出图，或明确需要下游格式 | `blender-rendering`；另有导出要求时接 `blender-export` | 从交付母版渲染的图件；如需导出，再回读导出物验证材质、单位和动作。 |

**使用旧工具时检查输入语义。** 有些旧比较器会自动改变不同尺寸输入的宽高，有些只实现四个固定视角，或把轮廓线稿与实体面积遮罩混作一种模式。先生成已配准的同画幅输入，覆盖实际要求的每个方向。局部开放边、遮挡区或基线回归可用本包的比较脚本。项目约定优先于子技能示例中的阈值、机位数、输出格式和默认文件名。

## 可以直接复用的工具

下列路径均相对对应子技能目录。执行前先读该技能的输入约定，输出交给表中下一环节。

| 工具 | 输入与用途 |
| --- | --- |
| `reference-analysis-validator/scripts/reference_manifest_compiler.py` | 输入图片或目录，通过 `--out` 输出图像测量清单。人工补上造型仲裁图、部件语义和状态关系。 |
| `orthographic-registration/scripts/register_views.py` | 输入已分开的正交视图，输出初始边界记录；再用物理锚点、视向和左右手校正配准。 |
| `multiview-constraint-solver/scripts/view_constraint_report.py` | 读取含各视图 `bbox=[x,y,w,h]` 的 JSON，检验共用轴的一致性。先确认图像尺度可比，再解释数值冲突。 |
| `image-to-blender-production/scripts/audit_blender.py` | 在 Blender 中打开指定母版，用 `--spec 检查规格.json --out 检查结果.json` 检查命名部件、截面、圆环或光轴；按项目运行器传递脚本参数。 |
| `animation-quality-gate/scripts/animation_contact_sheet.py` | 输入已渲染的帧文件，通过 `--out-image` 和 `--out-report` 生成接触表与记录。机构干涉及姿态回归另从三维数据验证。 |
