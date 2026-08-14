from __future__ import annotations

import json
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
SCAFFOLD_ROOT = REPO_ROOT / "Hermit"


def _load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def test_roadmap_has_required_phases_in_order() -> None:
    roadmap = _load_json(SCAFFOLD_ROOT / "manifests" / "roadmap.phases.json")
    phase_names = [phase["name"] for phase in roadmap["phases"]]
    assert phase_names == [
        "rust_taxonomy",
        "evidence_collection",
        "graph_schema",
        "completeness_scoring",
        "verification_grounding",
        "composition_synthesis",
    ]


def test_indexes_reference_existing_schemas() -> None:
    index_dir = SCAFFOLD_ROOT / "indexes"
    for index_name in ["taxonomy.index.json", "evidence.index.json", "relationships.index.json"]:
        index = _load_json(index_dir / index_name)
        schema = (index_dir / index["schema"]).resolve()
        assert schema.is_file(), f"Missing schema for {index_name}: {schema}"


def test_project_manifest_declares_machine_readable_principles() -> None:
    manifest = _load_json(SCAFFOLD_ROOT / "manifests" / "project.manifest.json")
    assert manifest["name"] == "Hermit"
    assert manifest["visibility"] == "private"
    assert "machine_readable_first" in manifest["design_principles"]
