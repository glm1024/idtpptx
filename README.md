# idtpptx

`idtpptx` 是一个用于生成和编辑 IDT / 浪潮风格 PowerPoint 的 Codex skill。

它不是独立的 PPTX 处理引擎，而是一个覆盖层 skill：底层 PPTX 读写、拆包、复制页面、打包和渲染 QA 依赖成熟的 `pptx` skill；`idtpptx` 负责补充公司风格、模板选择、版式映射、中文内部文档口径和公司级检查规则。

## 安装

先安装基础 `pptx` skill：

```bash
npx skills add anthropics/skills@pptx -g -y
```

再安装 `idtpptx`：

```bash
npx skills add https://github.com/glm1024/idtpptx -g -y
```

## 更新

如果是按上面的全局方式安装，后续更新 `idtpptx`：

```bash
npx skills update idtpptx -g -y
```

建议同时更新基础 `pptx` skill：

```bash
npx skills update pptx -g -y
```

也可以一次更新全部全局 skills：

```bash
npx skills update -g -y
```

如果是项目级安装，把 `-g` 改成 `-p`，或在对应项目目录下运行更新命令。

维护这个仓库时，流程是：

1. 修改 `SKILL.md`、`references/`、`assets/templates/`、`scripts/` 或 `evals/`。
2. 如果改动会影响触发规则、版式选择、主题约束或 QA 行为，同步检查并更新 `evals/evals.json`。
3. 本地检查 skill 是否能被识别：

   ```bash
   npx skills add /path/to/idtpptx -l
   ```

4. 提交并推送到 GitHub。别人再运行 `npx skills update idtpptx -g -y` 就能拿到更新。

## 这个 skill 提供什么

- 清理过业务内容的公司风格 PPTX 模板，位于 `assets/templates/`
- 简单务实的白底蓝色企业风格规则
- 固定的 IDT/Inspur 主题 contract：颜色 token、字体 contract、场景变体和禁止用途
- 封面、章节页、正文说明页、对比表页、截图步骤页、建议页、问题处理页等常用页面意图映射
- `COV-01`、`SS-02`、`TBL-02` 等受控版式 ID 登记表，作为页面配方而不是整页克隆指令
- 组件系统和组合语法：把 logo、标题、表格、流程、架构图、截图框、结论条等有限元素组合成不同页面
- 登记版式优先、组件组合优先、截图槽位优先的稳定生成规则，减少不同模型自由发挥造成的偏差
- 模板派生组合的生成路线：默认复用公司模板母版和品牌元素，但不把 V1 样例页逐页复制成最终 PPT
- 截图和生成配图的保真、裁切、比例和素材边界规则
- 默认微软雅黑字体、标题系统、不同内容密度下的字号、行距和表格对齐规则
- 卡片、结论框、说明框、标注框等“有外框文字”的内框计算、换行和溢出检查规则
- 默认黑色/近黑色文字、红色重点提示和受控语义色规则
- 更适合中文内部汇报和培训材料的写法指导
- 针对占位符清理、PowerPoint 默认标题提示、标题区域匹配、封面冗余白色面板、文本框超出可见外框、模板克隆风险、logo 本体防遮挡 / 版心一致性、截图可读性、主题漂移、OpenXML 结构校验和 PowerPoint 兼容性等公司级 QA 检查规则
- 可复用的 PPT QA playbook 和机械检查脚本 `scripts/pptx_quality_gate.py`
- 用于回归检查的轻量 eval 场景，位于 `evals/evals.json`

## 资产边界

`idtpptx` 仓库只分发生成 PPT 所必需的小型资产：

- `assets/templates/`：唯一的公司 V1 主模板和必要品牌资产。
- `references/`：版式、主题、文案、截图和 QA 规则。
- `scripts/`：机械检查或辅助脚本。

不要把原始参考 PPT 库、客户/项目 deck、素材研究语料或几十 MB 的内部资料放进 skill 根目录。它们可以保存在本地 sibling 目录，例如：

```text
../ppt-reference/
```

参考 PPT 的作用是研究和提炼，不是作为 skill 安装包内容。需要吸收时，先把结论写入 `references/reference-deck-inventory.md`、`references/reference-layout-extraction.md`、`references/component-system.md`、`references/composition-grammar.md`、`references/layout-map.md` 或 `references/layout-registry.md`，再用 `references/cleaned-layout-sample-specs.md` 约束清洗样例页，最后通过 `scripts/build_template.py` 重建唯一的 V1 主模板。

当前内置模板 `assets/templates/inspur-pragmatic-template-v1.pptx` 是唯一给 AI 使用的 V1 主模板。它包含已登记、清洗、验证过的 `COV-02A` 正式评审封面、`DIR-01A` 目录进度页、`PRC-03A` 阶段推进页、`SS-02A` 多截图步骤页、`SS-03A` 故障排查截图页、`ARC-01A` 左说明右技术图页、`ARC-02A` 全宽技术架构图页、`ARC-03A` 左图右文 / 右图左文拆分架构页、`TBL-02A` 密集证据表页、`TBL-03A` 指标/评估表页和 `SUM-02A` 决策复盘页。不要再让 AI 在多个 PPT 模板之间选择，也不要把这些样例页当成固定成品页序列；它们是风格标尺、组件样本和兜底参考。

## 注意事项

- `idtpptx` 不替代基础 `pptx` skill。
- 基础 `pptx` skill 负责 PPTX 文件读取、拆包、复制页面、XML 编辑、打包、渲染和通用 QA。
- `idtpptx` 只负责公司风格和模板约束。
- 有公司模板时，默认走模板派生组合和 XML 编辑路线；PptxGenJS/from-scratch 只用于没有可用模板、用户明确要求从零生成，或模板无法表达目标结构的例外场景。
- `idtpptx` 不生成 HTML 网页 PPT，不引入 WebGL、浏览器动效、Swiss poster 或杂志风模板；这些应作为独立 web deck workflow 处理。
- `idtpptx` 不提供通用主题库，不复制或依赖 `theme-factory` 的 10 套主题、字体或 showcase PDF；默认只使用固定公司主题。
- 交付前必须完成内容、视觉、压缩包、图片/media 关系、OpenXML 结构和 PowerPoint 兼容性检查；不能只以 LibreOffice 成功渲染作为最终依据。
- 如果 PowerPoint 提示“发现内容有问题/需要修复”，或修复后图片变成附件/包对象图标，视为未交付成功，需要回到 PPTX 包结构和媒体关系继续修。
- 如果依赖安装在另一个 Python 环境里，可追加 `--python python` 或设置 `IDTPPTX_PYTHON=python`。
- 模板中可能包含公司品牌元素，只应在授权场景下使用和分享。

改动主题规则后，除常规检查外，还要运行 QA helper 并刷新本机安装副本，确认后续会话能读取最新 `theme-contract`。
