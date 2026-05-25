from __future__ import annotations

import argparse
from pathlib import Path

from .pipeline import run_audit
from .reporter import render_markdown


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Run a local multi-agent code audit demo.")
    parser.add_argument("target", type=Path, help="Source folder to audit")
    parser.add_argument("--output", "-o", type=Path, help="Write markdown report to this path")
    parser.add_argument(
        "--fail-on-high",
        action="store_true",
        help="Return a non-zero exit code when high severity issues are found",
    )
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()

    if not args.target.exists() or not args.target.is_dir():
        parser.error(f"target must be an existing directory: {args.target}")

    state = run_audit(args.target)
    report = render_markdown(state)

    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(report, encoding="utf-8")
        print(f"Report written to {args.output}")
    else:
        print(report)

    high_count = sum(1 for finding in state.findings if finding.severity == "high")
    return 2 if args.fail_on_high and high_count else 0


if __name__ == "__main__":
    raise SystemExit(main())
