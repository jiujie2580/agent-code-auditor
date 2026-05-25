# Agent Code Auditor

这是一个可运行的多 Agent 代码审查演示项目，可作为 AI / Agent 使用证明提交给审核。它模拟一个研发团队常见的工作流：AI Agent 接收一个代码目录，自动规划检查步骤，扫描代码文件，识别潜在风险，并输出一份可追溯的审查报告。

## 项目解决的核心痛点

很多团队在维护历史项目时，会遇到几个重复问题：新人理解代码慢，手动排查风险容易遗漏，代码审查依赖个人经验，提交前验证不够稳定。这个项目把这些重复工作拆成可自动执行的 Agent 流程，用程序化规则模拟 AI Agent 的长链工作方式，帮助团队更快发现明显风险，例如误提交密钥、动态执行代码、过宽的异常处理、未完成标记等。

## 核心 Agent 流程

项目包含四个协作角色：

1. Planner Agent：分析任务目标，生成审查计划。
2. Scanner Agent：遍历目标代码库，识别语言、文件规模和风险标记。
3. Reviewer Agent：根据安全性和可维护性规则生成具体问题。
4. Verification Agent：汇总结果，检查重复发现，并生成验证说明。

这条流程体现了长链推理的基本结构：先规划，再收集上下文，然后审查，最后验证结果。真实业务中可以把 Reviewer Agent 替换为大模型调用，也可以增加测试 Agent、修复 Agent 或 PR Agent，让它自动生成修改并运行测试。

## 快速运行

```bash
python scripts/run_audit.py demo/sample_project --output reports/demo-report.md
```

报告会写入 `reports/demo-report.md`。如果需要在 CI 中遇到高风险问题就失败，可以额外加上 `--fail-on-high`。

## 运行测试

```bash
python -m unittest discover tests
```

## 示例输出

演示代码位于 `demo/sample_project`。运行后会生成一份 Markdown 报告，包含：

- Agent 工作流
- 已扫描文件列表
- 风险发现、位置和建议
- 验证结果

## 可扩展方向

- 接入 OpenAI API，把 Reviewer Agent 从规则检查升级为语义审查。
- 增加 Fixer Agent，根据审查结果自动生成补丁。
- 增加 Test Agent，在修改后自动运行单元测试并根据失败信息继续修复。
- 接入 GitHub Actions，在每次 Pull Request 中自动生成审查报告。

## 用于审核时的说明

这个仓库可以作为“GitHub 项目链接或产品在线演示地址”提交。审核方可以通过 README 了解项目目标，通过 `demo/sample_project` 查看输入样例，通过运行命令得到 Agent 工作流报告，通过测试结果确认项目可运行。
