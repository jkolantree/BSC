from __future__ import annotations

import copy
import json
import os
import re
import subprocess
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
GRAPH = ROOT / "ledgers" / "BSC_Core_v1_5_Claim_Graph.json"
GRAPH_RECEIPT = ROOT / "ledgers" / "BSC_Core_v1_5_Claim_Graph.receipt.json"
REGISTRY = ROOT / "ledgers" / "BSC_Core_v1_5_Claim_Registry.json"
PACKAGE_RECEIPT = ROOT / "ledgers" / "BSC_Core_v1_5_Claim_Package.receipt.json"
ALLOWED_VERDICTS = {"N/A", "false", "ill-posed", "open", "true"}


def load_json(path: Path) -> object:
    return json.loads(path.read_text(encoding="utf-8"))


def run_python(*arguments: str) -> subprocess.CompletedProcess[str]:
    environment = dict(os.environ)
    environment.update(
        {
            "PYTHONDONTWRITEBYTECODE": "1",
            "PYTHONHASHSEED": "0",
            "PYTHONPATH": "",
        }
    )
    return subprocess.run(
        [sys.executable, "-I", "-B", *arguments],
        cwd=ROOT,
        env=environment,
        text=True,
        capture_output=True,
        check=False,
    )


class BscCoreV15IntegrationTests(unittest.TestCase):
    def test_registry_and_graph_are_exactly_aligned(self) -> None:
        registry = load_json(REGISTRY)
        graph = load_json(GRAPH)
        assert isinstance(registry, dict)
        assert isinstance(graph, dict)
        self.assertEqual(registry["coverage"], "selected-milestone-claims")
        expected_package_artifacts = {
            ".github/workflows/verify-release.yml",
            "BSC_CORE_V1_5.md",
            "Makefile",
            "REPRODUCING.md",
            "fixtures/F15_cyclic_readiness/receipt.schema.json",
            "formal/bsc_core/BscCore.lean",
            "formal/bsc_core/BscCore/Examples.lean",
            "formal/bsc_core/BscCore/Tests.lean",
            "formal/bsc_core/README.md",
            "formal/bsc_core/lake-manifest.json",
            "formal/bsc_core/lakefile.toml",
            "formal/bsc_core/lean-toolchain",
            "schemas/bsc-claim-readiness-graph-v1.schema.json",
            "schemas/bsc-core-v1.5-claim-registry.schema.json",
            "tests/test_bsc_core_v1_5.py",
        }
        self.assertEqual(set(registry["package_artifacts"]), expected_package_artifacts)
        self.assertEqual(
            registry["package_artifacts"], sorted(registry["package_artifacts"])
        )

        claims = registry["claims"]
        nodes = graph["nodes"]
        claim_ids = [claim["id"] for claim in claims]
        node_ids = [node["id"] for node in nodes]
        self.assertEqual(claim_ids, sorted(set(claim_ids)))
        self.assertEqual(node_ids, sorted(set(node_ids)))
        self.assertEqual(claim_ids, node_ids)

        claims_by_id = {claim["id"]: claim for claim in claims}
        nodes_by_id = {node["id"]: node for node in nodes}
        self.assertEqual(
            {identifier: claim["verdict"] for identifier, claim in claims_by_id.items()},
            {identifier: node["verdict"] for identifier, node in nodes_by_id.items()},
        )
        self.assertTrue(
            all(claim["verdict"] in ALLOWED_VERDICTS for claim in claims)
        )

        dependencies = {
            (dependency, claim["id"])
            for claim in claims
            for dependency in claim["dependencies"]
        }
        edges = {(edge["source"], edge["target"]) for edge in graph["edges"]}
        self.assertEqual(dependencies, edges)
        self.assertEqual(len(claims), 12)
        self.assertEqual(len(edges), 10)

        for claim in claims:
            for relative in claim["sources"] + claim["evidence"]:
                self.assertTrue((ROOT / relative).is_file(), relative)
        for relative in registry["package_artifacts"]:
            self.assertTrue((ROOT / relative).is_file(), relative)

    def test_verdict_is_not_a_maturity_or_epistemic_status(self) -> None:
        graph = load_json(GRAPH)
        assert isinstance(graph, dict)
        nodes = {node["id"]: node for node in graph["nodes"]}
        self.assertEqual(nodes["BSC-AIR-01"]["verdict"], "N/A")
        self.assertEqual(nodes["BSC-CAU-01"]["verdict"], "N/A")
        self.assertEqual(nodes["BSC-CAT-01"]["verdict"], "open")
        self.assertEqual(nodes["BSC-NOV-01"]["verdict"], "open")

        mutated = copy.deepcopy(graph)
        mutated["nodes"][0]["verdict"] = "proposed"
        result = run_python(
            "tools/bsc_claim_readiness.py", "evaluate", str(GRAPH)
        )
        self.assertEqual(result.returncode, 0, result.stderr)

        temporary = ROOT / "tests" / ".bsc-v15-invalid-verdict.json"
        try:
            temporary.write_text(json.dumps(mutated), encoding="utf-8")
            rejected = run_python(
                "tools/bsc_claim_readiness.py", "evaluate", str(temporary)
            )
            self.assertNotEqual(rejected.returncode, 0)
            self.assertIn("closed vocabulary", rejected.stderr)
            self.assertNotIn("Traceback", rejected.stderr)
        finally:
            temporary.unlink(missing_ok=True)

    def test_package_loader_rejects_duplicate_keys_and_large_integers(self) -> None:
        raw = REGISTRY.read_text(encoding="utf-8")
        cases = {
            "duplicate": raw.replace(
                '"schema": "bsc.core.v1.5.claim-registry.v1",',
                '"schema": "bsc.core.v1.5.claim-registry.v1",\n'
                '  "schema": "bsc.core.v1.5.claim-registry.v1",',
                1,
            ),
            "large-integer": raw.replace(
                '"coverage": "selected-milestone-claims",',
                '"coverage": "selected-milestone-claims",\n'
                '  "oversized": 12345678901234567890,',
                1,
            ),
        }
        for label, content in cases.items():
            with self.subTest(label=label):
                temporary = ROOT / "tests" / f".bsc-v15-invalid-{label}.json"
                try:
                    temporary.write_text(content, encoding="utf-8")
                    rejected = run_python(
                        "tools/bsc_core_claim_package.py",
                        "evaluate",
                        str(temporary),
                    )
                    self.assertNotEqual(rejected.returncode, 0)
                    self.assertNotIn("Traceback", rejected.stderr)
                    self.assertNotIn(str(temporary), rejected.stderr)
                finally:
                    temporary.unlink(missing_ok=True)

    def test_formal_scope_and_human_scope_are_not_conflated(self) -> None:
        graph = load_json(GRAPH)
        assert isinstance(graph, dict)
        nodes = {node["id"]: node for node in graph["nodes"]}
        self.assertEqual(
            nodes["BSC-RDY-02"]["initial"]["FORMAL"],
            "human-proof-recorded",
        )
        self.assertEqual(
            nodes["BSC-RDY-03"]["initial"]["FORMAL"],
            "kernel-check-added",
        )

        formal_readme = (ROOT / "formal" / "bsc_core" / "README.md").read_text(
            encoding="utf-8"
        )
        self.assertIn("This is not the heterogeneous-lattice theorem", formal_readme)
        self.assertIn("Weighted optimization and complexity are not formalized", formal_readme)
        self.assertIn("tightening every selected natural-valued tolerance", formal_readme)

    def test_formal_source_projection_and_prohibited_constructs(self) -> None:
        project = ROOT / "formal" / "bsc_core"
        lean_files = sorted(
            [project / "BscCore.lean", *(project / "BscCore").glob("*.lean")]
        )
        self.assertEqual(len(lean_files), 9)
        prohibited = re.compile(
            r"\bsorry\b|\badmit\b|"
            r"^\s*(?:(?:private|protected|local)\s+)*axiom\b|"
            r"\bunsafe\b|\bnative_decide\b|\bbv_decide\b|"
            r"maxHeartbeats\s+0",
            re.MULTILINE,
        )
        for path in lean_files:
            self.assertIsNone(prohibited.search(path.read_text(encoding="utf-8")), path)

        root_module = (project / "BscCore.lean").read_text(encoding="utf-8")
        for module in (
            "Readiness",
            "CapSystem",
            "Identifiability",
            "PairSeparation",
            "Oscillation",
            "Examples",
        ):
            self.assertIn(f"import BscCore.{module}", root_module)

    def test_retained_graph_and_package_receipts_match(self) -> None:
        graph = run_python(
            "tools/bsc_claim_readiness.py", "check", str(GRAPH), str(GRAPH_RECEIPT)
        )
        self.assertEqual(graph.returncode, 0, graph.stderr)
        self.assertIn("receipt matches exact graph bytes", graph.stdout)

        package = run_python(
            "tools/bsc_core_claim_package.py",
            "check",
            str(REGISTRY),
            str(PACKAGE_RECEIPT),
        )
        self.assertEqual(package.returncode, 0, package.stderr)
        self.assertIn("receipt matches exact package bytes", package.stdout)

    def test_fixtures_replay_with_honest_evidence_labels(self) -> None:
        f14 = run_python(
            "fixtures/F14_intervention_identifiability/check_fixture.py"
        )
        self.assertEqual(f14.returncode, 0, f14.stderr)
        self.assertIn("families=8 minimum_cost=2 minimizers=2", f14.stdout)
        f15 = run_python("fixtures/F15_cyclic_readiness/check_fixture.py")
        self.assertEqual(f15.returncode, 0, f15.stderr)
        self.assertIn("84 feasible assignments", f15.stdout)

        fixtures = (ROOT / "fixtures" / "README.md").read_text(encoding="utf-8")
        self.assertIn("same-implementation replay", fixtures)
        self.assertIn("not described as an independent implementation", fixtures)
        f15_checker = (
            ROOT / "fixtures" / "F15_cyclic_readiness" / "check_fixture.py"
        ).read_text(encoding="utf-8")
        self.assertIn("validate_receipt_schema", f15_checker)
        self.assertIn("receipt.schema.json", f15_checker)

    def test_public_navigation_and_validation_boundary(self) -> None:
        required = {
            "README.md": "BSC Core v1.5 executive summary",
            "BSC_CORE_V1_5.md": "internal adversarial validation report",
            "CHANGELOG.md": "BSC Core v1.5 research milestone",
            "SOURCE_AVAILABILITY.md": "every artifact required to replay",
            "DISCLOSURE.md": "correlated internal development",
            "ROADMAP.md": "BSC Core v1.5",
            "REPRODUCING.md": "selected-claim package",
            "synopsis/Reader_Map.md": "Formal methods and AI-assisted mathematics",
            "revision/Revision_Memorandum.md": "partially",
            "ledgers/Claim_Status_Ledger.md": "BSC-RDY-03",
        }
        for relative, phrase in required.items():
            text = (ROOT / relative).read_text(encoding="utf-8")
            self.assertIn(phrase, " ".join(text.split()), relative)

        hub = (ROOT / "BSC_CORE_V1_5.md").read_text(encoding="utf-8")
        self.assertIn("Novelty status:** unknown", hub)
        self.assertIn("not labeled an\nindependent implementation", hub)
        self.assertIn("curator-supplied premises", hub)

    def test_ci_and_makefile_cover_the_public_boundary(self) -> None:
        workflow = (ROOT / ".github" / "workflows" / "verify-release.yml").read_text(
            encoding="utf-8"
        )
        for phrase in (
            "working-directory: formal/bsc_core",
            "lake build",
            "lake env leanchecker BscCore",
            "lake env lean BscCore/Tests.lean",
            "lake env lean BscCore/AxiomAudit.lean",
            "Reject prohibited proof shortcuts",
            "BscCore BscCore.lean",
        ):
            self.assertIn(phrase, workflow)

        makefile = (ROOT / "Makefile").read_text(encoding="utf-8")
        self.assertIn("bsc-core:", makefile)
        self.assertRegex(makefile, r"verify:.*bsc-core")


if __name__ == "__main__":
    unittest.main()
