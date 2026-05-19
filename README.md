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

1. 修改 `SKILL.md`、`references/`、`assets/templates/` 或 `scripts/`。
2. 本地检查 skill 是否能被识别：

   ```bash
   npx skills add /path/to/idtpptx -l
   ```

3. 提交并推送到 GitHub。别人再运行 `npx skills update idtpptx -g -y` 就能拿到更新。

## 这个 skill 提供什么

- 清理过业务内容的公司风格 PPTX 模板，位于 `assets/templates/`
- 简单务实的白底蓝色企业风格规则
- 封面、章节页、正文说明页、对比表页、截图步骤页、建议页、问题处理页等常用版式映射
- 默认微软雅黑字体、不同内容密度下的字号、行距和表格对齐规则
- 更适合中文内部汇报和培训材料的写法指导
- 针对占位符清理、封面冗余白色面板、logo 安全区 / 版心一致性、截图可读性、OpenXML 结构校验和 PowerPoint 兼容性等公司级 QA 检查规则
- 可复用的 PPT QA playbook 和机械检查脚本 `scripts/pptx_quality_gate.py`

## 注意事项

- `idtpptx` 不替代基础 `pptx` skill。
- 基础 `pptx` skill 负责 PPTX 文件读取、拆包、复制页面、XML 编辑、打包、渲染和通用 QA。
- `idtpptx` 只负责公司风格和模板约束。
- 交付前必须完成内容、视觉、压缩包、OpenXML 结构和 PowerPoint 兼容性检查；不能只以 LibreOffice 成功渲染作为最终依据。
- 如果依赖安装在另一个 Python 环境里，可追加 `--python python` 或设置 `IDTPPTX_PYTHON=python`。
- 模板中可能包含公司品牌元素，只应在授权场景下使用和分享。
