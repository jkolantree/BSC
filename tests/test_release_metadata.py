from __future__ import annotations

import hashlib
import unittest
from pathlib import Path


REPOSITORY_ROOT = Path(__file__).resolve().parent.parent
RELEASE_VERSION = "1.4.0"
RELEASE_DATE = "2026-07-31"
RELEASE_URL = "https://github.com/jkolantree/BSC/releases/tag/v1.4.0"
CONCEPT_DOI = "10.5281/zenodo.21541160"
PRIOR_RELEASE_VERSION_DOI = "10.5281/zenodo.21713285"
PRIOR_RELEASE_2_VERSION_DOI = "10.5281/zenodo.21711341"
PRIOR_RELEASE_3_VERSION_DOI = "10.5281/zenodo.21710743"
PRIOR_VERSION_DOI = "10.5281/zenodo.21541561"


class ReleaseMetadataTests(unittest.TestCase):
    def read(self, relative: str) -> str:
        return (REPOSITORY_ROOT / relative).read_text(encoding="utf-8")

    def sha256(self, relative: str) -> str:
        return hashlib.sha256(
            (REPOSITORY_ROOT / relative).read_bytes()
        ).hexdigest()

    def test_release_version_is_consistent_on_active_surfaces(self) -> None:
        expected_fragments = {
            "README.md": "Latest released version:** v1.4.0",
            "CITATION.cff": f'version: "{RELEASE_VERSION}"',
            ".zenodo.json": f'"version": "{RELEASE_VERSION}"',
            "CHANGELOG.md": "## 1.4.0",
            "framework/Operational_Channel_Core.md": (
                "part of the released `1.3.0` framework"
            ),
            "framework/Electromagnetic_Evidence_Bridge.md": (
                "part of the released `1.3.0` framework"
            ),
            "framework/Simulation_Evidence_Profile.md": (
                "part of the released `1.2.0` framework"
            ),
            "fixtures/README.md": (
                "Version 1.4.0 contains eleven exact reference fixtures"
            ),
            "paper/source/On_Boundaries_of_Evidence.tex": (
                rf"\newcommand{{\BSCVersion}}{{{RELEASE_VERSION}}}"
            ),
            "synopsis/Technical_Synopsis.md": (
                "Repository state:** version 1.4.0 release"
            ),
            "synopsis/source/Technical_Synopsis.tex": (
                rf"\newcommand{{\BSCVersion}}{{{RELEASE_VERSION}}}"
            ),
            "Makefile": f"VERSION ?= {RELEASE_VERSION}",
            "tools/build_archives.py": (
                f'DEFAULT_VERSION = "{RELEASE_VERSION}"'
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
                self.assertNotIn(PRIOR_RELEASE_VERSION_DOI, text)
                self.assertNotIn("development version", text.lower())

    def test_prior_release_doi_provenance_remains_visible(self) -> None:
        for relative in ("README.md", "CHANGELOG.md", "REPRODUCING.md"):
            text = self.read(relative)
            with self.subTest(path=relative, doi=PRIOR_RELEASE_VERSION_DOI):
                self.assertIn(PRIOR_RELEASE_VERSION_DOI, text)
            with self.subTest(path=relative, doi=PRIOR_RELEASE_2_VERSION_DOI):
                self.assertIn(PRIOR_RELEASE_2_VERSION_DOI, text)
            with self.subTest(path=relative, doi=PRIOR_RELEASE_3_VERSION_DOI):
                self.assertIn(PRIOR_RELEASE_3_VERSION_DOI, text)
            with self.subTest(path=relative, doi=PRIOR_VERSION_DOI):
                self.assertIn(PRIOR_VERSION_DOI, text)

    def test_release_citation_is_final_and_doi_honest(self) -> None:
        citation = self.read("CITATION.cff")
        self.assertIn(f"date-released: {RELEASE_DATE}", citation)
        self.assertIn(f'value: "{CONCEPT_DOI}"', citation)
        self.assertIn(f'repository-artifact: "{RELEASE_URL}"', citation)
        self.assertNotIn("unreleased", citation.lower())
        self.assertNotIn("development version", citation.lower())
        _, separator, preferred = citation.partition("preferred-citation:")
        self.assertTrue(separator)
        self.assertIn(f'url: "{RELEASE_URL}"', preferred)
        self.assertIn("Version 1.4.0 preprint", preferred)
        self.assertNotIn(PRIOR_RELEASE_VERSION_DOI, preferred)

    def test_zenodo_metadata_requests_new_version_without_inventing_doi(
        self,
    ) -> None:
        metadata = self.read(".zenodo.json")
        self.assertNotIn('"doi":', metadata)
        self.assertIn(f'"publication_date": "{RELEASE_DATE}"', metadata)
        self.assertIn(f'"identifier": "{RELEASE_URL}"', metadata)
        self.assertNotIn("/releases/tag/v1.2.0", metadata)
        self.assertNotIn("unreleased", metadata.lower())

    def test_release_fixture_inventory_is_explicit(self) -> None:
        fixture_index = self.read("fixtures/README.md")
        self.assertIn(
            "Version 1.4.0 contains eleven exact reference fixtures",
            fixture_index,
        )
        self.assertIn(
            "F8, F10, and F11 are executable in version 1.4.0",
            fixture_index,
        )
        self.assertIn("F10_coupled_surrogate", fixture_index)
        self.assertIn("F11_collatz_recursive_sieve", fixture_index)

    def test_page_counts_are_consistent(self) -> None:
        self.assertIn("PAPER_PAGES ?= 75", self.read("Makefile"))
        self.assertIn(
            'parser.add_argument("--paper-pages", type=int, default=75)',
            self.read("tools/verify_build.py"),
        )
        self.assertIn(
            "The build gate requires a 75-page paper",
            self.read("REPRODUCING.md"),
        )
        self.assertIn("SOURCE_DATE_EPOCH ?= 1785456000", self.read("Makefile"))
        self.assertIn("export SOURCE_DATE_EPOCH", self.read("Makefile"))
        self.assertIn(
            "DEFAULT_SOURCE_DATE_EPOCH = 1785456000",
            self.read("tools/build_archives.py"),
        )

    def test_active_surfaces_have_no_release_development_markers(self) -> None:
        active_surfaces = (
            "README.md",
            "CHANGELOG.md",
            "REPRODUCING.md",
            "ROADMAP.md",
            "CITATION.cff",
            ".zenodo.json",
            "framework/Operational_Channel_Core.md",
            "framework/Electromagnetic_Evidence_Bridge.md",
            "fixtures/README.md",
            "ledgers/Claim_Status_Ledger.md",
            "ledgers/Symbol_and_Notation_Ledger.md",
            "revision/Revision_Memorandum.md",
            "synopsis/Technical_Synopsis.md",
            "synopsis/Reader_Map.md",
            "paper/source/On_Boundaries_of_Evidence.tex",
            "synopsis/source/Technical_Synopsis.tex",
        )
        forbidden = (
            "1.4.0-dev",
            "unreleased 1.4.0",
            "development version 1.4.0",
            "1.4.0 development tree",
        )
        for relative in active_surfaces:
            text = self.read(relative).lower()
            for marker in forbidden:
                with self.subTest(path=relative, marker=marker):
                    self.assertNotIn(marker, text)

    def test_recorded_release_pdf_hashes_match_tracked_bytes(self) -> None:
        reproducing = self.read("REPRODUCING.md")
        _, marker, active_release = reproducing.partition(
            "## Release v1.4.0 render"
        )
        self.assertTrue(marker, "missing active v1.4.0 PDF record")
        active_release = active_release.partition(
            "## Refresh and verify the release tree"
        )[0]
        for relative in (
            "paper/On_Boundaries_of_Evidence.pdf",
            "synopsis/Technical_Synopsis.pdf",
        ):
            with self.subTest(path=relative):
                self.assertIn(f"`{self.sha256(relative)}`", active_release)


if __name__ == "__main__":
    unittest.main()
