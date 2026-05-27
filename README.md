# Agent Code Auditor

这是一个可运行的多 Agent 代码审查演示项目。它会扫描本地代码目录，按安全性和可维护性规则检查常见风险，并生成一份可以追踪过程的 Markdown 报告。

## 这个项目解决什么问题

团队在提交代码前经常需要重复检查：有没有误提交密钥、有没有未完成标记、有没有动态执行代码、有没有过宽的异常捕获。这个项目把这些步骤拆成一个简单的 Agent 流程，让检查结果更稳定，也更容易展示。

## 工作流程

1. Planner Agent 生成审查计划。
2. Scanner Agent 扫描支持的源码文件并记录风险标记。
3. Reviewer Agent 按规则检查具体问题。
4. Verification Agent 汇总结果并检查是否有重复发现。

## 快速运行

```bash
python scripts/run_audit.py demo/sample_project --output reports/demo-report.md
```

如果希望发现高风险问题时让命令失败，可以加上：

```bash
python scripts/run_audit.py demo/sample_project --fail-on-high
```

## 运行测试

```bash
python -m unittest discover tests
```

## 示例报告包含什么

- Agent 审查流程
- 已扫描文件和风险标记
- 问题位置、证据和修复建议
- 结果验证说明

## 后续可以扩展的方向

- 增加更多项目自定义规则。
- 接入大模型，让 Reviewer Agent 做更深层的语义审查。
- 增加 Fixer Agent，根据发现的问题生成修复建议。
- 接入 GitHub Actions，在 Pull Request 中自动生成审查报告。

## 项目定位

这个仓库适合作为一个小而完整的 Agent 工作流演示：能运行、能测试、能输出报告，也方便继续扩展。