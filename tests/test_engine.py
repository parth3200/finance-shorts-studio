from pathlib import Path
from tempfile import TemporaryDirectory
from unittest import TestCase, main

from finance_shorts.engine import MarketFact, generate_short_script, load_market_facts, write_content_packs


class ShortScriptTests(TestCase):
    def test_generate_short_script_contains_market_snapshot_and_compliance_disclaimer(self):
        fact = MarketFact(
            symbol="NIFTYBEES",
            price=252.35,
            change_percent=1.8,
            as_of="2026-01-15T15:30:00+05:30",
        )

        script = generate_short_script(fact)

        self.assertIn("NIFTYBEES", script.title)
        self.assertIn("1.8%", script.hook)
        self.assertIn("₹252.35", script.body)
        self.assertIn("Educational content only", script.disclaimer)
        self.assertLessEqual(script.estimated_duration_seconds, 45)

    def test_load_market_facts_reads_local_csv_without_network(self):
        csv_text = "symbol,price,change_percent,as_of\nHDFCBANK,1700.25,-0.4,2026-01-15T15:30:00+05:30\n"

        with TemporaryDirectory() as temp_dir:
            path = Path(temp_dir) / "facts.csv"
            path.write_text(csv_text, encoding="utf-8")

            facts = load_market_facts(path)

        self.assertEqual(1, len(facts))
        self.assertEqual("HDFCBANK", facts[0].symbol)
        self.assertEqual(1700.25, facts[0].price)
        self.assertEqual(-0.4, facts[0].change_percent)

    def test_write_content_packs_creates_json_script_files_without_personal_data(self):
        facts = [
            MarketFact(
                symbol="RELIANCE",
                price=2450.1,
                change_percent=0.9,
                as_of="2026-01-15T15:30:00+05:30",
            )
        ]

        with TemporaryDirectory() as temp_dir:
            output_paths = write_content_packs(facts, temp_dir)

            self.assertEqual(1, len(output_paths))
            output_path = Path(output_paths[0])
            self.assertTrue(output_path.exists())
            self.assertEqual("reliance.json", output_path.name)
            content = output_path.read_text(encoding="utf-8")
            self.assertIn('"title": "RELIANCE market snapshot"', content)
            self.assertIn('"disclaimer": "Educational content only, not financial advice."', content)
            self.assertNotIn("parth", content.lower())


if __name__ == "__main__":
    main()
