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

## 使用示例

```text
用 idtpptx 风格帮我做一份项目汇报 PPT。
```

```text
用 idtpptx 风格帮我做一份内部培训 PPT。
```

```text
把这份大纲整理成 IDT / 浪潮风格的 PowerPoint。
```

## 这个 skill 提供什么

- 清理过业务内容的公司风格 PPTX 模板，位于 `assets/templates/`
- 简单务实的白底蓝色企业风格规则
- 封面、章节页、正文说明页、对比表页、截图步骤页、建议页、问题处理页等常用版式映射
- 更适合中文内部汇报和培训材料的写法指导
- 针对占位符清理、logo / 版心一致性、截图可读性等公司级 QA 检查规则

## 注意事项

- `idtpptx` 不替代基础 `pptx` skill。
- 基础 `pptx` skill 负责 PPTX 文件读取、拆包、复制页面、XML 编辑、打包、渲染和通用 QA。
- `idtpptx` 只负责公司风格和模板约束。
- 模板中可能包含公司品牌元素，只应在授权场景下使用和分享。
