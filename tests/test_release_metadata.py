from __future__ import annotations

import hashlib
import json
import unittest
from datetime import UTC, datetime
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

    def active_release(self) -> tuple[str, str, str]:
        specification = json.loads(self.read("release/release-spec.json"))
        version = specification["intended_version"]
        epoch = specification["build_epoch"]
        if version is None:
            return RELEASE_VERSION, RELEASE_DATE, RELEASE_URL
        self.assertIsInstance(version, str)
        self.assertIsInstance(epoch, int)
        release_date = datetime.fromtimestamp(epoch, tz=UTC).date().isoformat()
        release_url = f"https://github.com/jkolantree/BSC/releases/tag/v{version}"
        return version, release_date, release_url

    def test_release_version_is_consistent_on_active_surfaces(self) -> None:
        active_version, _, _ = self.active_release()
        expected_fragments = {
            "README.md": f"Latest released version:** v{active_version}",
            "CITATION.cff": f'version: "{active_version}"',
            ".zenodo.json": f'"version": "{active_version}"',
            "CHANGELOG.md": f"## {active_version}",
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
                f"Version {active_version} contains eleven exact reference fixtures"
            ),
            "paper/source/On_Boundaries_of_Evidence.tex": (
                rf"\newcommand{{\BSCVersion}}{{{active_version}}}"
            ),
            "synopsis/Technical_Synopsis.md": (
                f"Repository state:** version {active_version} release"
            ),
            "synopsis/source/Technical_Synopsis.tex": (
                rf"\newcommand{{\BSCVersion}}{{{active_version}}}"
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
        active_version, active_date, active_url = self.active_release()
        citation = self.read("CITATION.cff")
        self.assertIn(f"date-released: {active_date}", citation)
        self.assertIn(f'value: "{CONCEPT_DOI}"', citation)
        self.assertIn(f'repository-artifact: "{active_url}"', citation)
        self.assertNotIn("unreleased", citation.lower())
        self.assertNotIn("development version", citation.lower())
        _, separator, preferred = citation.partition("preferred-citation:")
        self.assertTrue(separator)
        self.assertIn(f'url: "{active_url}"', preferred)
        self.assertIn(f"Version {active_version} preprint", preferred)
        self.assertNotIn(PRIOR_RELEASE_VERSION_DOI, preferred)

    def test_zenodo_metadata_requests_new_version_without_inventing_doi(
        self,
    ) -> None:
        _, active_date, active_url = self.active_release()
        metadata = self.read(".zenodo.json")
        self.assertNotIn('"doi":', metadata)
        self.assertIn(f'"publication_date": "{active_date}"', metadata)
        self.assertIn(f'"identifier": "{active_url}"', metadata)
        self.assertNotIn("/releases/tag/v1.2.0", metadata)
        self.assertNotIn("unreleased", metadata.lower())

    def test_release_fixture_inventory_is_explicit(self) -> None:
        active_version, _, _ = self.active_release()
        fixture_index = self.read("fixtures/README.md")
        self.assertIn(
            f"Version {active_version} contains eleven exact reference fixtures",
            fixture_index,
        )
        self.assertIn(
            f"F8, F10, and F11 are executable in version {active_version}",
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

    def test_post_release_archive_defaults_are_fail_closed(self) -> None:
        makefile = self.read("Makefile")
        builder = self.read("tools/build_archives.py")
        specification = self.read("release/release-spec.json")
        self.assertNotIn("VERSION ?= 1.4.0", makefile)
        self.assertNotIn("SOURCE_DATE_EPOCH ?= 1785456000", makefile)
        self.assertNotIn('DEFAULT_VERSION = "1.4.0"', builder)
        self.assertNotIn("DEFAULT_SOURCE_DATE_EPOCH", builder)
        self.assertIn("--development", makefile)
        self.assertIn("--candidate-version", makefile)
        self.assertIn("--release-version", makefile)
        self.assertIn("VERSION is no longer accepted", makefile)
        self.assertIn(
            "SOURCE_DATE_EPOCH ?= $(shell $(PYTHON) tools/release_identity.py --print-build-epoch)",
            makefile,
        )
        self.assertIn("export SOURCE_DATE_EPOCH", makefile)
        parsed = json.loads(specification)
        self.assertEqual(parsed["schema"], "bsc.release-spec.v1")
        version = parsed["intended_version"]
        epoch = parsed["build_epoch"]
        self.assertEqual(version is None, epoch is None)
        if version is not None:
            self.assertIsInstance(version, str)
            self.assertIsInstance(epoch, int)

    def test_ci_verifies_real_tag_authority_without_write_permissions(self) -> None:
        workflow = self.read(".github/workflows/verify-release.yml")
        self.assertIn("permissions:\n  contents: read", workflow)
        self.assertIn("fetch-depth: 0", workflow)
        self.assertIn("fetch-tags: true", workflow)
        self.assertIn('${GITHUB_REF_NAME#v}', workflow)
        self.assertIn('--candidate-version "${version}"', workflow)
        self.assertIn('--release-version "${version}"', workflow)
        self.assertEqual(workflow.count("make fixture-full"), 2)

    def test_f11_certificate_has_canonical_checkout_eol(self) -> None:
        attributes = self.read(".gitattributes").splitlines()
        self.assertIn("*.tsv text eol=lf", attributes)

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
        active_version, _, _ = self.active_release()
        reproducing = self.read("REPRODUCING.md")
        _, marker, active_release = reproducing.partition(
            f"## Release v{active_version} render"
        )
        self.assertTrue(marker, f"missing active v{active_version} PDF record")
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
