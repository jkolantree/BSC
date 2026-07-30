from __future__ import annotations

import re
import unittest
from pathlib import Path


REPOSITORY_ROOT = Path(__file__).resolve().parent.parent
EXPECTED_CLAIM_IDS = (
    "BSC-ZDQ-01",
    "BSC-ZDQ-02a",
    "BSC-ZDQ-02b",
    "BSC-ZDQ-02c",
    "BSC-ZDQ-02d",
    "BSC-ZDQ-02d.1",
    "BSC-ZDQ-02e",
    "BSC-ZDQ-03",
    "BSC-ZDQ-04",
    "BSC-ZDQ-05",
    "BSC-ZDQ-06",
)


class ZetaDQPTCaseIntegrationTests(unittest.TestCase):
    def read(self, relative: str) -> str:
        return (REPOSITORY_ROOT / relative).read_text(encoding="utf-8")

    def test_primary_source_is_pinned_in_bibliography(self) -> None:
        bibliography = self.read(
            "paper/source/On_Boundaries_of_Evidence.bib"
        )
        self.assertIn("@article{wei2026riemanndqpt,", bibliography)
        self.assertIn("10.1038/s41467-026-74935-8", bibliography)

    def test_case_study_and_manuscript_are_cross_linked(self) -> None:
        application = self.read("applications/Riemann_DQPT_Transfer.md")
        manuscript = self.read(
            "paper/source/On_Boundaries_of_Evidence.tex"
        )
        for required in (
            "10.1038/s41467-026-74935-8",
            "305 K",
            "BSC-ZDQ-01",
            "BSC-ZDQ-06",
        ):
            self.assertIn(required, application)
        self.assertIn("wei2026riemanndqpt", manuscript)
        self.assertRegex(
            manuscript,
            re.compile(r"Riemann.*dynamical quantum phase", re.IGNORECASE),
        )

    def test_claim_ids_are_unique_and_complete(self) -> None:
        ledger = self.read("ledgers/Claim_Status_Ledger.md")
        application = self.read("applications/Riemann_DQPT_Transfer.md")
        row_pattern = re.compile(
            r"^\|\s*(BSC-ZDQ-[^ |]+)\s*\|",
            flags=re.MULTILINE,
        )
        ledger_ids = row_pattern.findall(ledger)
        application_ids = row_pattern.findall(application)
        self.assertEqual(ledger_ids, list(EXPECTED_CLAIM_IDS))
        self.assertEqual(application_ids, list(EXPECTED_CLAIM_IDS))

    def test_f9_is_documentary_and_not_an_execution_receipt(self) -> None:
        fixture_index = self.read("fixtures/README.md")
        fixture = self.read(
            "fixtures/F09_zeta_dqpt_transfer/README.md"
        )
        self.assertRegex(
            fixture_index,
            re.compile(r"\|\s*F9\s*\|.*\|\s*Unexecuted", re.IGNORECASE),
        )
        self.assertIn("BSC-ZDQ-01", fixture)
        self.assertIn("BSC-ZDQ-06", fixture)
        self.assertFalse(
            (REPOSITORY_ROOT / "fixtures/F09_zeta_dqpt_transfer"
             / "verification_receipt.json").exists()
        )

    def test_universal_promotions_are_explicitly_blocked(self) -> None:
        application = self.read("applications/Riemann_DQPT_Transfer.md")
        normalized = application.lower()
        for boundary in (
            "does not prove the riemann hypothesis",
            "not the laboratory temperature",
            "finite-size",
            "zero census",
            "recurrence",
            "persistence",
            "quantum advantage",
        ):
            self.assertIn(boundary, normalized)

    def test_fixed_s_rate_bridge_is_present_and_scoped(self) -> None:
        application = self.read("applications/Riemann_DQPT_Transfer.md")
        manuscript = self.read(
            "paper/source/On_Boundaries_of_Evidence.tex"
        )
        for text in (application, manuscript):
            self.assertIn("N=2^d", text.replace(" ", ""))
            self.assertIn("pointwise", text.lower())
            self.assertRegex(
                text,
                re.compile(r"not uniform near a zero", re.IGNORECASE),
            )
        self.assertIn("prop:eta-scaling", manuscript)
        self.assertIn("prop:eta-zero-drift", manuscript)
        self.assertIn("cor:eta-rate-sing", manuscript)
        self.assertIn(r"(1-\beta)\log2", manuscript.replace(" ", ""))
        self.assertIn(r"\beta_0\log2", manuscript.replace(" ", ""))


if __name__ == "__main__":
    unittest.main()
