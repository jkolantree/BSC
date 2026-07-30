from __future__ import annotations

import unittest
from pathlib import Path


REPOSITORY_ROOT = Path(__file__).resolve().parent.parent
DEVELOPMENT_VERSION = "1.1.0-dev"
PRIOR_VERSION_DOI = "10.5281/zenodo.21541561"


class DevelopmentMetadataTests(unittest.TestCase):
    def read(self, relative: str) -> str:
        return (REPOSITORY_ROOT / relative).read_text(encoding="utf-8")

    def test_development_version_is_consistent_on_active_surfaces(self) -> None:
        expected_fragments = {
            "README.md": "version 1.1.0-development draft",
            "paper/source/On_Boundaries_of_Evidence.tex": (
                rf"\newcommand{{\BSCVersion}}{{{DEVELOPMENT_VERSION}}}"
            ),
            "synopsis/Technical_Synopsis.md": (
                "version 1.1.0-development draft"
            ),
            "synopsis/source/Technical_Synopsis.tex": (
                rf"\newcommand{{\BSCVersion}}{{{DEVELOPMENT_VERSION}}}"
            ),
            "CITATION.cff": f'version: "{DEVELOPMENT_VERSION}"',
            ".zenodo.json": f'"version": "{DEVELOPMENT_VERSION}"',
            "Makefile": f"VERSION ?= {DEVELOPMENT_VERSION}",
            "tools/build_archives.py": (
                f'DEFAULT_VERSION = "{DEVELOPMENT_VERSION}"'
            ),
            "CHANGELOG.md": f"## {DEVELOPMENT_VERSION} - Unreleased",
        }
        for relative, fragment in expected_fragments.items():
            with self.subTest(path=relative):
                self.assertIn(fragment, self.read(relative))

    def test_development_artifacts_do_not_claim_the_prior_version_doi(self) -> None:
        for relative in (
            "paper/source/On_Boundaries_of_Evidence.tex",
            "synopsis/source/Technical_Synopsis.tex",
        ):
            with self.subTest(path=relative):
                text = self.read(relative)
                self.assertIn(
                    r"\newcommand{\BSCDOI}{Unreleased development draft}",
                    text,
                )
                self.assertNotIn(
                    f"pdfsubject={{Version 1.0.1; DOI {PRIOR_VERSION_DOI}",
                    text,
                )

    def test_prior_release_provenance_remains_visible(self) -> None:
        for relative in ("README.md", "CHANGELOG.md", "REPRODUCING.md"):
            with self.subTest(path=relative):
                self.assertIn(PRIOR_VERSION_DOI, self.read(relative))

    def test_development_citation_has_no_release_date(self) -> None:
        citation = self.read("CITATION.cff")
        self.assertNotIn("date-released:", citation)
        self.assertIn("unreleased development draft", citation.lower())

    def test_preferred_citation_routes_to_latest_released_preprint(self) -> None:
        citation = self.read("CITATION.cff")
        _, separator, preferred = citation.partition("preferred-citation:")
        self.assertTrue(separator)
        self.assertIn(f'doi: "{PRIOR_VERSION_DOI}"', preferred)
        self.assertIn(
            f'url: "https://doi.org/{PRIOR_VERSION_DOI}"',
            preferred,
        )
        self.assertIn("Version 1.0.1 preprint", preferred)
        self.assertNotIn(DEVELOPMENT_VERSION, preferred)

    def test_development_zenodo_metadata_claims_no_prior_deposit(self) -> None:
        metadata = self.read(".zenodo.json")
        self.assertNotIn('"doi":', metadata)
        self.assertNotIn('"publication_date":', metadata)
        self.assertNotIn("/releases/tag/v1.0.1", metadata)
        self.assertIn("claims no DOI or publication date", metadata)

    def test_development_page_counts_are_consistent(self) -> None:
        self.assertIn("PAPER_PAGES ?= 50", self.read("Makefile"))
        self.assertIn(
            'parser.add_argument("--paper-pages", type=int, default=50)',
            self.read("tools/verify_build.py"),
        )
        self.assertIn(
            "The expected page count is 50.",
            self.read("REPRODUCING.md"),
        )


if __name__ == "__main__":
    unittest.main()
