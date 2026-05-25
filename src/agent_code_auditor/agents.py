from __future__ import annotations

from collections import Counter
from pathlib import Path

from .models import AuditState, FileSignal, Finding
from .rules import find_rule_matches, language_for


class PlannerAgent:
    name = "planner"

    def run(self, state: AuditState) -> AuditState:
        state.plan = [
            "Map source files and choose audit scope",
            "Scan each file for risk markers and implementation signals",
            "Review risky lines with focused security and maintainability rules",
            "Verify that the audit result is internally consistent",
        ]
        return state


class ScannerAgent:
    name = "scanner"

    def run(self, state: AuditState) -> AuditState:
        root = state.config.root
        max_bytes = state.config.max_file_kb * 1024

        for path in sorted(root.rglob("*")):
            if not path.is_file() or path.suffix.lower() not in state.config.include_extensions:
                continue
            if path.stat().st_size > max_bytes:
                continue

            text = path.read_text(encoding="utf-8", errors="ignore")
            markers = tuple(marker for marker in ("TODO", "FIXME", "eval", "secret") if marker.lower() in text.lower())
            state.scanned_files.append(
                FileSignal(
                    path=path,
                    language=language_for(path),
                    line_count=len(text.splitlines()),
                    risk_markers=markers,
                )
            )
        return state


class ReviewerAgent:
    name = "reviewer"

    def run(self, state: AuditState) -> AuditState:
        for signal in state.scanned_files:
            text = signal.path.read_text(encoding="utf-8", errors="ignore")
            state.findings.extend(find_rule_matches(self.name, signal.path, text))
        return state


class VerificationAgent:
    name = "verifier"

    def run(self, state: AuditState) -> AuditState:
        counts = Counter(finding.severity for finding in state.findings)
        files_with_findings = {finding.file for finding in state.findings}

        state.verification_notes.append(f"Scanned {len(state.scanned_files)} source files.")
        state.verification_notes.append(f"Found {len(state.findings)} issues across {len(files_with_findings)} files.")
        state.verification_notes.append(
            "Severity summary: "
            + ", ".join(f"{severity}={count}" for severity, count in sorted(counts.items()))
            if counts
            else "Severity summary: no issues detected"
        )

        duplicate_keys = [
            (finding.file, finding.line, finding.title)
            for finding in state.findings
        ]
        if len(duplicate_keys) != len(set(duplicate_keys)):
            state.verification_notes.append("Verifier warning: duplicate findings were detected.")
        else:
            state.verification_notes.append("Verifier check passed: no duplicate findings.")
        return state


def relative_path(path: Path, root: Path) -> str:
    try:
        return str(path.relative_to(root)).replace("\\", "/")
    except ValueError:
        return str(path)


def sort_findings(findings: list[Finding]) -> list[Finding]:
    severity_rank = {"high": 0, "medium": 1, "low": 2}
    return sorted(findings, key=lambda item: (severity_rank.get(item.severity, 9), str(item.file), item.line))
