from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path


@dataclass(frozen=True)
class AuditConfig:
    root: Path
    include_extensions: tuple[str, ...] = (".py", ".js", ".ts", ".tsx", ".jsx")
    max_file_kb: int = 256


@dataclass(frozen=True)
class FileSignal:
    path: Path
    language: str
    line_count: int
    risk_markers: tuple[str, ...]


@dataclass(frozen=True)
class Finding:
    agent: str
    severity: str
    file: Path
    line: int
    title: str
    evidence: str
    recommendation: str


@dataclass
class AuditState:
    config: AuditConfig
    plan: list[str] = field(default_factory=list)
    scanned_files: list[FileSignal] = field(default_factory=list)
    findings: list[Finding] = field(default_factory=list)
    verification_notes: list[str] = field(default_factory=list)
