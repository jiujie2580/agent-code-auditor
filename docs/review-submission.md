# AI Agent 使用证明提交说明

## 建议提交材料

提交类型选择：GitHub 项目链接。

建议填写链接：上传本仓库后，填写仓库首页链接，例如：

```text
https://github.com/<your-github-name>/agent-code-auditor
```

## 项目简介

Agent Code Auditor 是一个可运行的多 Agent 代码审查项目。它用于模拟 AI Agent 在真实研发场景中的工作流：接收一个代码目录，自动规划审查步骤，扫描源码，识别安全和维护风险，并生成可追溯的 Markdown 报告。

## 核心痛点

这个项目解决的是研发团队中常见的代码理解和质量检查问题。历史代码通常文件多、上下文分散，人工检查容易漏掉明显风险，例如误提交密钥、动态执行代码、宽泛异常处理、未完成标记等。Agent 工作流可以把这些重复工作自动化，让开发者在提交前更快得到结构化反馈。

## 核心逻辑流

项目包含四个协作 Agent：

1. Planner Agent：生成审查计划。
2. Scanner Agent：扫描目标目录并提取文件信息。
3. Reviewer Agent：根据安全性和可维护性规则生成问题清单。
4. Verification Agent：汇总结果并验证报告一致性。

这体现了长链推理和多 Agent 协作：先规划，再收集上下文，然后审查，最后自检。

## 可验证内容

- `demo/sample_project`：示例输入代码库。
- `docs/demo-report.md`：Agent 运行后生成的示例报告。
- `tests/test_unittest.py`：自动化测试，证明核心流程可运行。
- `README.md`：项目说明和运行方法。

## 本地验证命令

```bash
python scripts/run_audit.py demo/sample_project --output docs/demo-report.md
python -m unittest discover tests
```

## 审核表单可填写文案

我提交的是一个 GitHub 项目链接：Agent Code Auditor。它是一个可运行的多 Agent 代码审查演示项目，主要解决研发团队在维护存量代码时遇到的代码理解成本高、人工检查容易遗漏、提交前验证不足等问题。项目会接收一个代码目录，先由 Planner Agent 生成审查计划，再由 Scanner Agent 扫描文件和风险标记，随后由 Reviewer Agent 生成安全性和可维护性问题，最后由 Verification Agent 汇总结果并检查报告一致性。仓库中包含示例输入代码、生成后的 Agent 报告、自动化测试和运行说明，审核方可以直接运行命令复现完整工作流。
