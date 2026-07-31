from __future__ import annotations

import hashlib
import unittest
from pathlib import Path


REPOSITORY_ROOT = Path(__file__).resolve().parent.parent
RELEASE_VERSION = "1.2.0"
DEVELOPMENT_VERSION = "1.3.0-dev"
RELEASE_DATE = "2026-07-30"
RELEASE_URL = "https://github.com/jkolantree/BSC/releases/tag/v1.2.0"
CONCEPT_DOI = "10.5281/zenodo.21541160"
RELEASE_VERSION_DOI = "10.5281/zenodo.21711341"
PRIOR_RELEASE_VERSION_DOI = "10.5281/zenodo.21710743"
PRIOR_VERSION_DOI = "10.5281/zenodo.21541561"


class ReleaseMetadataTests(unittest.TestCase):
    def read(self, relative: str) -> str:
        return (REPOSITORY_ROOT / relative).read_text(encoding="utf-8")

    def sha256(self, relative: str) -> str:
        return hashlib.sha256((REPOSITORY_ROOT / relative).read_bytes()).hexdigest()

    def test_release_and_development_versions_are_separated(self) -> None:
        expected_fragments = {
            "README.md": "Latest released version:** v1.2.0",
            "CITATION.cff": f'version: "{RELEASE_VERSION}"',
            ".zenodo.json": f'"version": "{RELEASE_VERSION}"',
            "CHANGELOG.md": "## 1.2.0",
            "framework/Operational_Channel_Core.md": (
                f"version `{DEVELOPMENT_VERSION}`"
            ),
            "framework/Simulation_Evidence_Profile.md": (
                "part of the released `1.2.0` framework"
            ),
            "fixtures/README.md": (
                "Version 1.2.0 defines ten exact reference fixtures"
            ),
            "paper/source/On_Boundaries_of_Evidence.tex": (
                rf"\newcommand{{\BSCVersion}}{{{DEVELOPMENT_VERSION}}}"
            ),
            "synopsis/Technical_Synopsis.md": (
                f"Repository state:** version {DEVELOPMENT_VERSION}"
            ),
            "synopsis/source/Technical_Synopsis.tex": (
                rf"\newcommand{{\BSCVersion}}{{{DEVELOPMENT_VERSION}}}"
            ),
            "Makefile": f"VERSION ?= {DEVELOPMENT_VERSION}",
            "tools/build_archives.py": (
                f'DEFAULT_VERSION = "{DEVELOPMENT_VERSION}"'
            ),
        }
        for relative, fragment in expected_fragments.items():
            with self.subTest(path=relative):
                self.assertIn(fragment, self.read(relative))

    def test_release_documents_use_concept_doi_not_prior_version_doi(
        self,
    ) -> None:
        for relative in (
            "paper/source/On_Boundaries_of_Evidence.tex",
            "synopsis/source/Technical_Synopsis.tex",
        ):
            with self.subTest(path=relative):
                text = self.read(relative)
                self.assertIn(
                    rf"\newcommand{{\BSCDOI}}{{Concept DOI {CONCEPT_DOI}}}",
                    text,
                )
                self.assertNotIn(PRIOR_VERSION_DOI, text)
                self.assertIn(DEVELOPMENT_VERSION, text)

    def test_prior_release_doi_provenance_remains_visible(self) -> None:
        for relative in ("README.md", "CHANGELOG.md", "REPRODUCING.md"):
            with self.subTest(path=relative):
                text = self.read(relative)
                self.assertIn(RELEASE_VERSION_DOI, text)
                self.assertIn(PRIOR_RELEASE_VERSION_DOI, text)
                self.assertIn(PRIOR_VERSION_DOI, text)

    def test_release_citation_is_final_and_doi_honest(self) -> None:
        citation = self.read("CITATION.cff")
        self.assertIn(f"date-released: {RELEASE_DATE}", citation)
        self.assertIn(f'value: "{CONCEPT_DOI}"', citation)
        self.assertIn(f'repository-artifact: "{RELEASE_URL}"', citation)
        self.assertNotIn(DEVELOPMENT_VERSION, citation)
        self.assertNotIn("unreleased development draft", citation.lower())
        _, separator, preferred = citation.partition("preferred-citation:")
        self.assertTrue(separator)
        self.assertIn(f'url: "{RELEASE_URL}"', preferred)
        self.assertIn("Version 1.2.0 preprint", preferred)
        self.assertNotIn(PRIOR_VERSION_DOI, preferred)

    def test_zenodo_metadata_requests_new_version_without_inventing_doi(self) -> None:
        metadata = self.read(".zenodo.json")
        self.assertNotIn('"doi":', metadata)
        self.assertIn(f'"publication_date": "{RELEASE_DATE}"', metadata)
        self.assertIn(f'"identifier": "{RELEASE_URL}"', metadata)
        self.assertNotIn("/releases/tag/v1.0.1", metadata)
        self.assertNotIn(DEVELOPMENT_VERSION, metadata)
        self.assertNotIn("unreleased", metadata.lower())

    def test_release_fixture_inventory_is_explicit(self) -> None:
        fixture_index = self.read("fixtures/README.md")
        self.assertIn(
            "Version 1.2.0 defines ten exact reference fixtures",
            fixture_index,
        )
        self.assertIn("F8 and F10 are executable", fixture_index)
        self.assertIn("F10_coupled_surrogate", fixture_index)

    def test_page_counts_are_consistent(self) -> None:
        self.assertIn("PAPER_PAGES ?= 63", self.read("Makefile"))
        self.assertIn(
            'parser.add_argument("--paper-pages", type=int, default=63)',
            self.read("tools/verify_build.py"),
        )
        self.assertIn(
            "The expected page count is 63.",
            self.read("REPRODUCING.md"),
        )

    def test_release_metadata_has_no_development_markers(self) -> None:
        release_metadata = (
            "CITATION.cff",
            ".zenodo.json",
        )
        for relative in release_metadata:
            text = self.read(relative).lower()
            with self.subTest(path=relative):
                self.assertNotIn(DEVELOPMENT_VERSION, text)
                self.assertNotIn("unreleased", text)

    def test_development_surfaces_are_explicit(self) -> None:
        development_surfaces = (
            "README.md",
            "CHANGELOG.md",
            "ROADMAP.md",
            "framework/Operational_Channel_Core.md",
            "ledgers/Claim_Status_Ledger.md",
            "ledgers/Symbol_and_Notation_Ledger.md",
            "revision/Revision_Memorandum.md",
            "synopsis/Technical_Synopsis.md",
            "synopsis/Reader_Map.md",
            "paper/source/On_Boundaries_of_Evidence.tex",
            "synopsis/source/Technical_Synopsis.tex",
        )
        for relative in development_surfaces:
            with self.subTest(path=relative):
                self.assertIn(DEVELOPMENT_VERSION, self.read(relative))

    def test_recorded_release_pdf_hashes_match_tracked_bytes(self) -> None:
        reproducing = self.read("REPRODUCING.md")
        for relative in (
            "paper/On_Boundaries_of_Evidence.pdf",
            "synopsis/Technical_Synopsis.pdf",
        ):
            with self.subTest(path=relative):
                self.assertIn(f"`{self.sha256(relative)}`", reproducing)


if __name__ == "__main__":
    unittest.main()
