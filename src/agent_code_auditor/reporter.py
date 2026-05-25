from __future__ import annotations

from datetime import datetime, timezone

from .agents import relative_path, sort_findings
from .models import AuditState


def render_markdown(state: AuditState) -> str:
    root = state.config.root
    lines: list[str] = [
        "# Agent Code Audit Report",
        "",
        f"Generated: {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S UTC')}",
        f"Target: `{root}`",
        "",
        "## Agent Workflow",
    ]

    for index, step in enumerate(state.plan, start=1):
        lines.append(f"{index}. {step}")

    lines.extend(["", "## Scanned Files"])
    if state.scanned_files:
        lines.append("| File | Language | Lines | Risk Markers |")
        lines.append("| --- | --- | ---: | --- |")
        for signal in state.scanned_files:
            markers = ", ".join(signal.risk_markers) if signal.risk_markers else "none"
            lines.append(
                f"| `{relative_path(signal.path, root)}` | {signal.language} | {signal.line_count} | {markers} |"
            )
    else:
        lines.append("No supported source files were found.")

    lines.extend(["", "## Findings"])
    findings = sort_findings(state.findings)
    if findings:
        for finding in findings:
            file_name = relative_path(finding.file, root)
            lines.extend(
                [
                    f"### {finding.severity.upper()}: {finding.title}",
                    f"- Agent: `{finding.agent}`",
                    f"- Location: `{file_name}:{finding.line}`",
                    f"- Evidence: `{finding.evidence}`",
                    f"- Recommendation: {finding.recommendation}",
                    "",
                ]
            )
    else:
        lines.append("No findings were detected.")

    lines.extend(["## Verification"])
    for note in state.verification_notes:
        lines.append(f"- {note}")

    lines.append("")
    return "\n".join(lines)
