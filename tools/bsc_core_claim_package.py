#!/usr/bin/env python3
"""Validate and bind the selected BSC Core v1.5 claim package.

The JSON Schemas are structural aids.  This checker supplies the semantic
cross-checks: exact graph/registry identifier agreement, verdict agreement,
dependency-edge agreement, safe repository-relative artifact paths, and
SHA-256 binding of every referenced source and evidence file.

A PASS validates those package relationships and bytes.  It does not prove
the curator-supplied verdicts or readiness premises.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from pathlib import Path, PurePosixPath
from typing import Any

TOOLS_DIR = Path(__file__).resolve().parent
if str(TOOLS_DIR) not in sys.path:
    sys.path.insert(0, str(TOOLS_DIR))

import bsc_claim_readiness as readiness


REGISTRY_SCHEMA = "bsc.core.v1.5.claim-registry.v1"
RECEIPT_SCHEMA = "bsc.core.v1.5.claim-package-receipt.v1"
ALLOWED_VERDICTS = frozenset({"N/A", "false", "ill-posed", "open", "true"})
IDENTIFIER = re.compile(r"^[A-Z][A-Z0-9]*(?:-[A-Z0-9]+)*$")
MAX_DOCUMENT_BYTES = 2_000_000
MAX_ARTIFACT_BYTES = 20_000_000
MAX_RECEIPT_BYTES = 4_000_000
REPO_ROOT = Path(__file__).resolve().parent.parent


class PackageError(ValueError):
    """Raised when the claim package is structurally or semantically invalid."""


def canonical_json(value: Any) -> bytes:
    return (
        json.dumps(value, ensure_ascii=True, sort_keys=True, separators=(",", ":"))
        + "\n"
    ).encode("utf-8")


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def load_document(path: Path, label: str) -> tuple[bytes, Any]:
    try:
        return readiness.load_json_bytes(
            path, maximum=MAX_DOCUMENT_BYTES, label=label
        )
    except readiness.ReadinessError as exc:
        raise PackageError(str(exc)) from None


def read_bounded(path: Path, maximum: int, label: str) -> bytes:
    try:
        with path.open("rb") as stream:
            content = stream.read(maximum + 1)
    except OSError:
        raise PackageError(f"cannot read {label}") from None
    if len(content) > maximum:
        raise PackageError(f"{label} exceeds the {maximum}-byte bound")
    return content


def exact_object(value: Any, keys: set[str], label: str) -> dict[str, Any]:
    if not isinstance(value, dict):
        raise PackageError(f"{label} must be an object")
    if set(value) != keys:
        raise PackageError(
            f"{label} keys differ: missing={sorted(keys - set(value))}, "
            f"extra={sorted(set(value) - keys)}"
        )
    return value


def nonempty_string(value: Any, label: str) -> str:
    if not isinstance(value, str) or not value:
        raise PackageError(f"{label} must be a nonempty string")
    return value


def claim_identifier(value: Any, label: str) -> str:
    text = nonempty_string(value, label)
    if not IDENTIFIER.fullmatch(text):
        raise PackageError(f"{label} is not a portable claim identifier")
    return text


def string_list(
    value: Any,
    label: str,
    *,
    identifiers: bool = False,
    allow_empty: bool = True,
) -> tuple[str, ...]:
    if not isinstance(value, list) or (not allow_empty and not value):
        raise PackageError(f"{label} must be an array")
    result = tuple(
        claim_identifier(item, f"{label}[{index}]")
        if identifiers
        else nonempty_string(item, f"{label}[{index}]")
        for index, item in enumerate(value)
    )
    if result != tuple(sorted(set(result))):
        raise PackageError(f"{label} must be sorted and duplicate-free")
    return result


def safe_repository_file(value: str, label: str) -> tuple[str, Path]:
    if "\\" in value:
        raise PackageError(f"{label} must use repository-relative POSIX separators")
    pure = PurePosixPath(value)
    if pure.is_absolute() or not pure.parts or any(
        part in {"", ".", ".."} for part in pure.parts
    ):
        raise PackageError(f"{label} is not a safe repository-relative path")
    resolved = (REPO_ROOT / Path(*pure.parts)).resolve()
    try:
        resolved.relative_to(REPO_ROOT)
    except ValueError as exc:
        raise PackageError(f"{label} escapes the repository") from exc
    if not resolved.is_file():
        raise PackageError(f"{label} does not name a repository file")
    return value, resolved


def build_receipt(registry_path: Path) -> dict[str, Any]:
    registry_raw, registry_document = load_document(registry_path, "registry")
    registry = exact_object(
        registry_document,
        {
            "schema",
            "milestone",
            "coverage",
            "readiness_graph",
            "package_artifacts",
            "claims",
        },
        "registry",
    )
    if registry["schema"] != REGISTRY_SCHEMA:
        raise PackageError("registry schema mismatch")
    milestone = nonempty_string(registry["milestone"], "registry.milestone")
    if registry["coverage"] != "selected-milestone-claims":
        raise PackageError("registry coverage must be selected-milestone-claims")
    graph_name, graph_path = safe_repository_file(
        nonempty_string(registry["readiness_graph"], "registry.readiness_graph"),
        "registry.readiness_graph",
    )
    graph_raw, graph_document = load_document(graph_path, "readiness graph")
    graph = readiness.validate_graph(graph_document)
    graph_receipt = readiness.evaluate(graph_raw, graph_document)
    package_artifacts = string_list(
        registry["package_artifacts"],
        "registry.package_artifacts",
        allow_empty=False,
    )

    raw_claims = registry["claims"]
    if not isinstance(raw_claims, list) or not raw_claims:
        raise PackageError("registry.claims must be a nonempty array")

    claims: list[dict[str, Any]] = []
    artifact_paths: set[str] = {graph_name, *package_artifacts}
    for index, raw_claim in enumerate(raw_claims):
        claim = exact_object(
            raw_claim,
            {
                "id",
                "statement",
                "verdict",
                "authority_ceiling",
                "dependencies",
                "sources",
                "evidence",
            },
            f"claims[{index}]",
        )
        identifier = claim_identifier(claim["id"], f"claims[{index}].id")
        statement = nonempty_string(
            claim["statement"], f"claims[{index}].statement"
        )
        verdict = nonempty_string(claim["verdict"], f"claims[{index}].verdict")
        if verdict not in ALLOWED_VERDICTS:
            raise PackageError(
                f"claims[{index}].verdict is outside the closed vocabulary"
            )
        ceiling = nonempty_string(
            claim["authority_ceiling"], f"claims[{index}].authority_ceiling"
        )
        dependencies = string_list(
            claim["dependencies"],
            f"claims[{index}].dependencies",
            identifiers=True,
        )
        sources = string_list(
            claim["sources"], f"claims[{index}].sources", allow_empty=False
        )
        evidence = string_list(
            claim["evidence"], f"claims[{index}].evidence"
        )
        artifact_paths.update(sources)
        artifact_paths.update(evidence)
        claims.append(
            {
                "authority_ceiling_sha256": sha256(ceiling.encode("utf-8")),
                "dependencies": list(dependencies),
                "evidence": list(evidence),
                "id": identifier,
                "sources": list(sources),
                "statement_sha256": sha256(statement.encode("utf-8")),
                "verdict": verdict,
            }
        )

    identifiers = tuple(claim["id"] for claim in claims)
    if identifiers != tuple(sorted(set(identifiers))):
        raise PackageError("claim identifiers must be sorted and duplicate-free")
    identifier_set = set(identifiers)
    if identifier_set != set(graph.nodes):
        raise PackageError("registry claim identifiers differ from graph nodes")

    dependency_pairs: set[tuple[str, str]] = set()
    for claim in claims:
        for dependency in claim["dependencies"]:
            if dependency not in identifier_set:
                raise PackageError(
                    f"claim {claim['id']} has unknown dependency {dependency}"
                )
            if dependency == claim["id"]:
                raise PackageError(f"claim {claim['id']} depends on itself")
            dependency_pairs.add((dependency, claim["id"]))
        if claim["verdict"] != graph.nodes[claim["id"]].verdict:
            raise PackageError(f"claim {claim['id']} verdict differs from graph")

    edge_pairs = {(edge.source, edge.target) for edge in graph.edges}
    if dependency_pairs != edge_pairs:
        raise PackageError(
            "registry dependency pairs differ from readiness graph edges"
        )

    artifact_sha256: dict[str, str] = {}
    for path_text in sorted(artifact_paths):
        _, path = safe_repository_file(path_text, f"artifact {path_text}")
        artifact_sha256[path_text] = sha256(
            read_bounded(path, MAX_ARTIFACT_BYTES, f"artifact {path_text}")
        )

    graph_receipt_sha256 = sha256(readiness.canonical_json(graph_receipt))
    return {
        "artifact_sha256": artifact_sha256,
        "checks": {
            "artifact_paths_exist": True,
            "dependencies_equal_edges": True,
            "graph_fixed_point": graph_receipt["checks"]["fixed_point"],
            "ids_equal_graph_nodes": True,
            "verdicts_equal_graph": True,
        },
        "claim_count": len(claims),
        "coverage": registry["coverage"],
        "claims": claims,
        "generator_sha256": sha256(Path(__file__).read_bytes()),
        "graph_edge_count": len(graph.edges),
        "graph_node_count": len(graph.nodes),
        "graph_receipt_sha256": graph_receipt_sha256,
        "milestone": milestone,
        "package_artifacts": list(package_artifacts),
        "readiness_graph_sha256": sha256(graph_raw),
        "registry_sha256": sha256(registry_raw),
        "schema": RECEIPT_SCHEMA,
        "status": "PASS",
    }


def write_new(path: Path, content: bytes) -> None:
    try:
        with path.open("xb") as stream:
            stream.write(content)
    except FileExistsError as exc:
        raise PackageError("refusing to overwrite existing receipt") from exc
    except OSError:
        raise PackageError("cannot write receipt") from None


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="command", required=True)
    evaluate = subparsers.add_parser("evaluate")
    evaluate.add_argument("registry", type=Path)
    write = subparsers.add_parser("write-new")
    write.add_argument("registry", type=Path)
    write.add_argument("receipt", type=Path)
    check = subparsers.add_parser("check")
    check.add_argument("registry", type=Path)
    check.add_argument("receipt", type=Path)
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        expected = canonical_json(build_receipt(args.registry))
        if args.command == "evaluate":
            sys.stdout.buffer.write(expected)
        elif args.command == "write-new":
            write_new(args.receipt, expected)
            print(f"BSC CORE CLAIM PACKAGE: PASS: wrote {args.receipt}")
        else:
            if read_bounded(
                args.receipt, MAX_RECEIPT_BYTES, "retained receipt"
            ) != expected:
                raise PackageError(
                    "receipt is stale, noncanonical, or identity-mismatched"
                )
            print("BSC CORE CLAIM PACKAGE: PASS: receipt matches exact package bytes")
    except (
        PackageError,
        readiness.ReadinessError,
        OSError,
        UnicodeError,
        RecursionError,
        ValueError,
        OverflowError,
    ) as exc:
        print(f"BSC CORE CLAIM PACKAGE: FAIL: {exc}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
