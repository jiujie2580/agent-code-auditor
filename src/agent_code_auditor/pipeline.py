from __future__ import annotations

from pathlib import Path

from .agents import PlannerAgent, ReviewerAgent, ScannerAgent, VerificationAgent
from .models import AuditConfig, AuditState


def run_audit(root: Path) -> AuditState:
    state = AuditState(config=AuditConfig(root=root.resolve()))
    for agent in (PlannerAgent(), ScannerAgent(), ReviewerAgent(), VerificationAgent()):
        state = agent.run(state)
    return state
