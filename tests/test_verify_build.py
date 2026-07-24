from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from tools.verify_build import Artifact, verify_artifact


class BuildVerifierTests(unittest.TestCase):
    def make_artifact(
        self, log_text: str, expected_pages: int = 2
    ) -> tuple[tempfile.TemporaryDirectory[str], Artifact]:
        temporary = tempfile.TemporaryDirectory(prefix="bsc-build-test-")
        root = Path(temporary.name)
        pdf = root / "artifact.pdf"
        log = root / "artifact.log"
        pdf.write_bytes(b"%PDF-1.5\nsynthetic test fixture\n")
        log.write_text(log_text, encoding="utf-8")
        return temporary, Artifact("test", pdf, log, expected_pages)

    def test_clean_log_and_expected_pages_pass(self) -> None:
        temporary, artifact = self.make_artifact(
            "Output written on artifact.pdf (2 pages, 123 bytes).\n"
        )
        self.addCleanup(temporary.cleanup)
        self.assertEqual(verify_artifact(artifact), [])

    def test_wrapped_output_path_passes(self) -> None:
        temporary, artifact = self.make_artifact(
            "Output written on /a/very/long/release/path/that/tex/wrapped/\n"
            "artifact.pdf (2 pages, 123 bytes).\n"
        )
        self.addCleanup(temporary.cleanup)
        self.assertEqual(verify_artifact(artifact), [])

    def test_page_drift_is_rejected(self) -> None:
        temporary, artifact = self.make_artifact(
            "Output written on artifact.pdf (3 pages, 123 bytes).\n"
        )
        self.addCleanup(temporary.cleanup)
        errors = verify_artifact(artifact)
        self.assertIn("test: expected 2 pages, got 3", errors)

    def test_warning_is_rejected(self) -> None:
        temporary, artifact = self.make_artifact(
            "Package natbib Warning: Citation `missing' undefined.\n"
            "Output written on artifact.pdf (2 pages, 123 bytes).\n"
        )
        self.addCleanup(temporary.cleanup)
        errors = verify_artifact(artifact)
        self.assertIn("test: final log contains package warning", errors)
        self.assertIn(
            "test: final log contains undefined reference/citation", errors
        )

    def test_non_pdf_is_rejected(self) -> None:
        temporary, artifact = self.make_artifact(
            "Output written on artifact.pdf (2 pages, 123 bytes).\n"
        )
        self.addCleanup(temporary.cleanup)
        artifact.pdf.write_bytes(b"not a PDF\n")
        self.assertIn(
            "test: output does not have a PDF header",
            verify_artifact(artifact),
        )


if __name__ == "__main__":
    unittest.main()
