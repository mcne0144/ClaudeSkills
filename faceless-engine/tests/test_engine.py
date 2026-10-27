import json
import os
import shutil
import sys
import tempfile
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))

# isolate state and work dirs for the whole test run
TMP = Path(tempfile.mkdtemp(prefix="faceless-test-"))
os.environ["FACELESS_WORK"] = str(TMP / "work")
from engine import common  # noqa: E402

common.STATE = TMP / "state"
from engine import ff_report, ledger, niche_score, script_tools, tts  # noqa: E402

ff_report.STATE = common.STATE
ledger.STATE = common.STATE
ledger.VIDEOS = common.STATE / "videos"
niche_score.STATE = common.STATE
script_tools.STATE = common.STATE

FIXTURE = (HERE / "fixtures_report_2026-07-05.html").read_text()
SAMPLE = (HERE.parent / "docs" / "examples" / "sample-script.md").read_text()


class ReportParser(unittest.TestCase):
    def test_parses_all_niches(self):
        r = ff_report.parse_html(FIXTURE)
        self.assertEqual(r["week_of"], "2026-07-05")
        self.assertEqual(r["videos_scanned"], 1800)
        self.assertEqual(r["niches_tracked"], 40)
        self.assertEqual(len(r["niches"]), 40)
        first = r["niches"][0]
        self.assertEqual(first["name"], "Crypto News & Explainers")
        self.assertEqual(first["rpm_tier"], "HIGH")
        self.assertEqual(first["effort"], "mid")
        self.assertAlmostEqual(first["rising"], 1.92)
        self.assertEqual(first["outliers"], 19)
        self.assertAlmostEqual(first["cpc"], 3.86)
        self.assertEqual(first["seed_demand_per_month"], 27000)
        self.assertEqual(first["breakouts"][0]["video_id"], "eyyDNAj6K_c")
        self.assertEqual(first["breakouts"][0]["views"], 210000)
        self.assertEqual(first["breakouts"][0]["age_days"], 1)

    def test_shorts_flag_and_empty_niche(self):
        r = ff_report.parse_html(FIXTURE)
        celeb = r["niches"][4]
        self.assertTrue(any(b["is_short"] for b in celeb["breakouts"]))
        last = r["niches"][-1]
        self.assertEqual(last["breakouts"], [])
        self.assertEqual(last["rpm_tier"], "LOW")

    def test_staleness(self):
        from datetime import date

        r = ff_report.parse_html(FIXTURE)
        self.assertFalse(ff_report.staleness(r, reference=date(2026, 7, 10))["stale"])
        self.assertTrue(ff_report.staleness(r, reference=date(2026, 10, 27))["stale"])

    def test_human_number(self):
        self.assertEqual(common.human_number("2.6K"), 2600)
        self.assertEqual(common.human_number("1.0M"), 1000000)
        self.assertEqual(common.human_number("460"), 460)
        self.assertIsNone(common.human_number("n/a"))


class NicheScoring(unittest.TestCase):
    def test_policy_penalty_demotes_finance(self):
        r = ff_report.parse_html(FIXTURE)
        board = niche_score.score(r)
        names = [row["name"] for row in board["rows"]]
        self.assertLess(names.index("AI News & Tools"), names.index("Crypto News & Explainers"))
        crypto = next(row for row in board["rows"] if row["name"] == "Crypto News & Explainers")
        self.assertIn("policy-risk", crypto["flags"])
        self.assertEqual(board["rows"][0]["rank"], 1)


class Ledger(unittest.TestCase):
    def test_lifecycle_and_no_backwards(self):
        rec = ledger.new("A test video", "AI News & Tools")
        self.assertEqual(rec["status"], "idea")
        ledger.set_status(rec, "approved", "ok")
        ledger.set_status(rec, "scripted")
        with self.assertRaises(ValueError):
            ledger.set_status(rec, "approved")
        again = ledger.load(rec["id"])
        self.assertEqual(again["status"], "scripted")
        self.assertEqual(len(ledger.by_status("scripted")), 1)
        rec2 = ledger.new("A test video", "AI News & Tools")
        self.assertNotEqual(rec2["id"], rec["id"])


class ScriptGates(unittest.TestCase):
    def test_sample_passes(self):
        res = script_tools.check(SAMPLE)
        self.assertTrue(res["ok"], res["problems"])
        self.assertGreaterEqual(res["minutes"], 8)
        self.assertGreaterEqual(res["pov_sentences"], 6)

    def test_templated_script_fails(self):
        d = common.STATE / "scripts"
        d.mkdir(parents=True, exist_ok=True)
        (d / "prev.md").write_text(SAMPLE)
        res = script_tools.check(SAMPLE.replace("CRM", "ERP"), path="new.md")
        self.assertFalse(res["ok"])
        self.assertTrue(any("too similar" in p for p in res["problems"]))
        (d / "prev.md").unlink()

    def test_missing_pov_and_banned(self):
        bad = SAMPLE.replace(" I ", " one ").replace("I think", "one thinks").replace("my ", "the ")
        bad = bad.replace("Thanks for watching.", "Let's dive in. In conclusion, thanks.")
        res = script_tools.check(bad)
        self.assertFalse(res["ok"])
        joined = " ".join(res["problems"])
        self.assertIn("banned phrase", joined)

    def test_chunks_and_parse(self):
        doc = script_tools.parse(SAMPLE)
        self.assertEqual(doc["scenes"][0]["kind"], "hook")
        self.assertEqual(doc["scenes"][-1]["kind"], "outro")
        self.assertEqual(len(doc["sources"]), 4)
        self.assertEqual(doc["scenes"][1]["keywords"], "office at night, computer screen glowing")
        self.assertEqual(doc["scenes"][1]["fallback"], "software dashboard close up")
        chunks = script_tools.tts_chunks(doc, max_chars=2000)
        self.assertGreater(len(chunks), 1)
        self.assertTrue(all(len(c) <= 2000 for c in chunks))


class Captions(unittest.TestCase):
    def test_srt_grouping(self):
        words = [{"w": f"w{i}", "s": i * 0.3, "e": i * 0.3 + 0.25} for i in range(20)]
        srt = tts.build_srt(words, max_words=7, max_seconds=2.8)
        blocks = [b for b in srt.strip().split("\n\n") if b]
        self.assertEqual(len(blocks), 3)
        self.assertIn("00:00:00,000 -->", blocks[0])

    def test_alignment_to_words(self):
        al = {"characters": list("hi yo"), "character_start_times_seconds": [0, 0.1, 0.2, 0.3, 0.4],
              "character_end_times_seconds": [0.1, 0.2, 0.3, 0.4, 0.5]}
        w = tts.words_from_alignment(al, 10.0)
        self.assertEqual([x["w"] for x in w], ["hi", "yo"])
        self.assertAlmostEqual(w[1]["s"], 10.3)


def tearDownModule():
    shutil.rmtree(TMP, ignore_errors=True)


if __name__ == "__main__":
    unittest.main()
