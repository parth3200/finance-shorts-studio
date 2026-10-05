# Finance Shorts Studio

A local-first Python tool that turns CSV market facts into YouTube Shorts script packs.

## Why this project exists

- **Local-first:** reads only local CSV/JSON-style project files; no credentials or personal data required.
- **Compliance guardrails:** generated finance content includes an educational disclaimer and avoids guarantees or personalized financial advice.
- **Automation-ready:** emits JSON content packs that can be used by your local editing, TTS, or upload workflows.
- **Free to run:** uses only the Python standard library.

## Input format

Create a CSV with these columns:

```csv
symbol,price,change_percent,as_of
NIFTYBEES,252.35,1.8,2026-01-15T15:30:00+05:30
```

## Run

```bash
cd finance-shorts-studio
PYTHONPATH=src python3 -m finance_shorts \
  --input examples/market_facts.csv \
  --out output
```

Generated files land in `output/` as one JSON pack per symbol.

## Test

```bash
PYTHONPATH=src python3 -m unittest discover -s tests -v
```

## Safety notes

- Do not enter API keys, account IDs, client data, portfolio data, or personal identifiers.
- Market data shown in examples is placeholder data for local development.
- Publish only original/authorized assets and follow YouTube, finance-content, and local law requirements.
