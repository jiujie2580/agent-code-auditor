from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path

from .models import Finding


@dataclass(frozen=True)
class Rule:
    title: str
    severity: str
    pattern: re.Pattern[str]
    recommendation: str


RULES: tuple[Rule, ...] = (
    Rule(
        title="Possible secret committed to source",
        severity="high",
        pattern=re.compile(r"(?i)(api[_-]?key|secret|token|password)\s*=\s*['\"][^'\"]{8,}['\"]"),
        recommendation="Move credentials to environment variables or a secret manager.",
    ),
    Rule(
        title="Dynamic code execution",
        severity="high",
        pattern=re.compile(r"\b(eval|exec)\s*\("),
        recommendation="Replace dynamic execution with explicit parsing or a restricted interpreter.",
    ),
    Rule(
        title="Broad exception handling",
        severity="medium",
        pattern=re.compile(r"except\s+Exception\s*:"),
        recommendation="Catch the expected exception type and preserve useful error context.",
    ),
    Rule(
        title="Unfinished implementation marker",
        severity="low",
        pattern=re.compile(r"\b(TODO|FIXME|HACK)\b", re.IGNORECASE),
        recommendation="Convert the marker into a tracked task or complete the missing behavior.",
    ),
)


def language_for(path: Path) -> str:
    return {
        ".py": "Python",
        ".js": "JavaScript",
        ".jsx": "React",
        ".ts": "TypeScript",
        ".tsx": "React TypeScript",
    }.get(path.suffix.lower(), "Unknown")


def find_rule_matches(agent: str, path: Path, text: str) -> list[Finding]:
    findings: list[Finding] = []
    for line_number, line in enumerate(text.splitlines(), start=1):
        for rule in RULES:
            if rule.pattern.search(line):
                findings.append(
                    Finding(
                        agent=agent,
                        severity=rule.severity,
                        file=path,
                        line=line_number,
                        title=rule.title,
                        evidence=line.strip(),
                        recommendation=rule.recommendation,
                    )
                )
    return findings
