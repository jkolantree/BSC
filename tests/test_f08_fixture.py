from __future__ import annotations

import json
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


REPOSITORY_ROOT = Path(__file__).resolve().parent.parent
FIXTURE = REPOSITORY_ROOT / "fixtures" / "F08_sqrt_square_sign"


class F08FixtureTests(unittest.TestCase):
    def run_program(
        self, program: Path, *arguments: Path
    ) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [sys.executable, str(program), *(str(argument) for argument in arguments)],
            cwd=program.parent,
            check=False,
            capture_output=True,
            text=True,
        )

    def make_mutant(self) -> tuple[tempfile.TemporaryDirectory[str], Path]:
        temporary = tempfile.TemporaryDirectory(prefix="bsc-f8-mutant-")
        fixture = Path(temporary.name) / "fixture"
        shutil.copytree(FIXTURE, fixture)
        return temporary, fixture

    def generate_retained_receipt(self, fixture: Path) -> None:
        generated = fixture / "mutant_receipt.json"
        completed = self.run_program(
            fixture / "verify_counterexample.py", generated
        )
        self.assertEqual(completed.returncode, 0, completed.stderr)
        shutil.copyfile(generated, fixture / "verification_receipt.json")

    def test_released_fixture_passes(self) -> None:
        completed = self.run_program(FIXTURE / "check_fixture.py")
        self.assertEqual(completed.returncode, 0, completed.stderr)
        self.assertIn("F8-SQRT-SQUARE-SIGN: PASS", completed.stdout)

    def test_schema_invalid_interpreter_mutant_is_rejected(self) -> None:
        temporary, fixture = self.make_mutant()
        self.addCleanup(temporary.cleanup)
        script = fixture / "verify_counterexample.py"
        source = script.read_text(encoding="utf-8")
        source = source.replace(
            '"implementation": platform.python_implementation(),',
            '"implementation": 123,',
        )
        self.assertIn('"implementation": 123,', source)
        script.write_text(source, encoding="utf-8")
        self.generate_retained_receipt(fixture)

        completed = self.run_program(fixture / "check_fixture.py")
        self.assertNotEqual(completed.returncode, 0)
        self.assertIn(
            "$.interpreter.implementation: value does not match declared constant",
            completed.stderr,
        )

    def test_semantically_false_output_mutant_is_rejected(self) -> None:
        temporary, fixture = self.make_mutant()
        self.addCleanup(temporary.cleanup)

        script = fixture / "verify_counterexample.py"
        source = script.read_text(encoding="utf-8")
        source = source.replace("lhs = math.isqrt(x * x)", "lhs = 0")
        self.assertIn("lhs = 0", source)
        script.write_text(source, encoding="utf-8")

        schema_path = fixture / "receipt.schema.json"
        schema = json.loads(schema_path.read_text(encoding="utf-8"))
        schema["properties"]["output"]["properties"]["sqrt_x_squared"]["const"] = 0
        schema_path.write_text(
            json.dumps(schema, indent=2, sort_keys=False) + "\n",
            encoding="utf-8",
        )
        self.generate_retained_receipt(fixture)

        completed = self.run_program(fixture / "check_fixture.py")
        self.assertNotEqual(completed.returncode, 0)
        self.assertIn(
            "recorded square root differs from independent exact arithmetic",
            completed.stderr,
        )

    def test_generator_cannot_overwrite_retained_receipt(self) -> None:
        retained = FIXTURE / "verification_receipt.json"
        before = retained.read_bytes()
        completed = self.run_program(
            FIXTURE / "verify_counterexample.py", retained
        )
        self.assertNotEqual(completed.returncode, 0)
        self.assertIn(
            "refusing to overwrite the retained verification receipt",
            completed.stderr,
        )
        self.assertEqual(retained.read_bytes(), before)

    def test_generator_refuses_any_existing_output(self) -> None:
        with tempfile.TemporaryDirectory(prefix="bsc-f8-existing-") as temporary:
            output = Path(temporary) / "already_exists.json"
            output.write_text("do not overwrite\n", encoding="utf-8")
            completed = self.run_program(
                FIXTURE / "verify_counterexample.py", output
            )
            self.assertNotEqual(completed.returncode, 0)
            self.assertIn("refusing to overwrite existing output", completed.stderr)
            self.assertEqual(output.read_text(encoding="utf-8"), "do not overwrite\n")


if __name__ == "__main__":
    unittest.main()
