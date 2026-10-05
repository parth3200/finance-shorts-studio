import json
import os
import subprocess
import sys
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest import TestCase, main


PROJECT_ROOT = Path(__file__).resolve().parents[1]


class CliTests(TestCase):
    def test_cli_generates_content_packs_from_local_csv(self):
        with TemporaryDirectory() as temp_dir:
            env = os.environ.copy()
            env["PYTHONPATH"] = str(PROJECT_ROOT / "src")
            result = subprocess.run(
                [
                    sys.executable,
                    "-m",
                    "finance_shorts",
                    "--input",
                    str(PROJECT_ROOT / "examples" / "market_facts.csv"),
                    "--out",
                    temp_dir,
                ],
                cwd=PROJECT_ROOT,
                env=env,
                text=True,
                capture_output=True,
                timeout=30,
            )

            self.assertEqual(0, result.returncode, result.stderr)
            output_files = sorted(Path(temp_dir).glob("*.json"))
            self.assertEqual(["hdfcbank.json", "niftybees.json"], [p.name for p in output_files])
            payload = json.loads((Path(temp_dir) / "niftybees.json").read_text(encoding="utf-8"))
            self.assertEqual("NIFTYBEES market snapshot", payload["title"])
            self.assertIn("Wrote 2 content pack(s)", result.stdout)


if __name__ == "__main__":
    main()
