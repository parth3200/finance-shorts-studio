"""Command line interface for Finance Shorts Studio."""

from __future__ import annotations

import argparse
from pathlib import Path

from .engine import load_market_facts, write_content_packs

DEFAULT_INPUT = Path(__file__).resolve().parents[2] / "examples" / "market_facts.csv"


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Generate local YouTube Shorts finance script packs from CSV market facts."
    )
    parser.add_argument(
        "--input",
        default=str(DEFAULT_INPUT),
        help="Path to a local CSV with symbol,price,change_percent,as_of columns.",
    )
    parser.add_argument(
        "--out",
        default="output",
        help="Directory where JSON content packs should be written.",
    )
    return parser


def main() -> int:
    args = build_parser().parse_args()
    facts = load_market_facts(args.input)
    paths = write_content_packs(facts, args.out)
    print(f"Wrote {len(paths)} content pack(s) to {Path(args.out).resolve()}")
    for path in paths:
        print(path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
