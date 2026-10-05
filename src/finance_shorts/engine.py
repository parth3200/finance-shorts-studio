"""Core finance shorts generation engine."""

import csv
import json
import re
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import List, Union


@dataclass(frozen=True)
class MarketFact:
    """A local or user-provided market data point."""

    symbol: str
    price: float
    change_percent: float
    as_of: str


@dataclass(frozen=True)
class ShortScript:
    """A YouTube Shorts-ready script package."""

    title: str
    hook: str
    body: str
    cta: str
    hashtags: tuple[str, ...]
    disclaimer: str
    estimated_duration_seconds: int


def generate_short_script(fact: MarketFact) -> ShortScript:
    """Generate an educational finance Short script from a market fact."""

    direction = "up" if fact.change_percent >= 0 else "down"
    change = f"{abs(fact.change_percent):.1f}%"
    title = f"{fact.symbol} market snapshot"

    hook = f"{fact.symbol} moved {change} today."
    body = (
        f"As of {fact.as_of}, {fact.symbol} is trading at ₹{fact.price:,.2f}, "
        f"{direction} by {change}. Watch the trend, compare it with your plan, "
        "and avoid making impulsive decisions from one price move."
    )
    cta = "Follow for daily finance explainers."
    disclaimer = "Educational content only, not financial advice."

    return ShortScript(
        title=title,
        hook=hook,
        body=body,
        cta=cta,
        hashtags=("#finance", "#stockmarket", "#shorts"),
        disclaimer=disclaimer,
        estimated_duration_seconds=35,
    )


def load_market_facts(path: Union[Path, str]) -> List[MarketFact]:
    """Load local market facts from a CSV file without any network calls."""

    csv_path = Path(path)
    with csv_path.open("r", encoding="utf-8", newline="") as handle:
        rows = csv.DictReader(handle)
        required = {"symbol", "price", "change_percent", "as_of"}
        if rows.fieldnames is None or not required.issubset(rows.fieldnames):
            raise ValueError("CSV must include symbol, price, change_percent, and as_of columns")

        return [
            MarketFact(
                symbol=row["symbol"].strip(),
                price=float(row["price"]),
                change_percent=float(row["change_percent"]),
                as_of=row["as_of"].strip(),
            )
            for row in rows
        ]


def write_content_packs(facts: List[MarketFact], output_dir: Union[Path, str]) -> List[Path]:
    """Write one JSON content pack per market fact."""

    target_dir = Path(output_dir)
    target_dir.mkdir(parents=True, exist_ok=True)
    paths: List[Path] = []

    for fact in facts:
        script = generate_short_script(fact)
        safe_symbol = re.sub(r"[^a-z0-9]+", "-", fact.symbol.lower()).strip("-") or "market"
        output_path = target_dir / f"{safe_symbol}.json"
        output_path.write_text(
            json.dumps(asdict(script), ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )
        paths.append(output_path)

    return paths
