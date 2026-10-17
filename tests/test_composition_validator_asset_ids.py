"""Canonical asset-manifest IDs are filesystem-backed in pre-render validation."""

import json
import tempfile
import unittest
from pathlib import Path

from tools.analysis.composition_validator import CompositionValidator


class CanonicalManifestValidationTests(unittest.TestCase):
    def test_resolves_asset_ids_from_sibling_manifest(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            artifacts = root / "artifacts"
            artifacts.mkdir()
            (root / "assets").mkdir()
            (root / "assets" / "shot.mp4").touch()
            manifest = {
                "version": "1.0",
                "assets": [{
                    "id": "shot-id", "type": "video", "path": "assets/shot.mp4",
                    "source_tool": "stock", "scene_id": "s1",
                }],
            }
            (artifacts / "asset_manifest.json").write_text(json.dumps(manifest))
            composition = {
                "version": "1.0", "render_runtime": "ffmpeg",
                "cuts": [{"id": "shot", "source": "shot-id",
                          "in_seconds": 20, "out_seconds": 23}],
            }
            spec = artifacts / "edit_decisions.json"
            spec.write_text(json.dumps(composition))
            result = CompositionValidator().execute({"composition_path": str(spec)})
            self.assertTrue(result.success, result.error)

    def test_unknown_id_is_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            spec = root / "edit_decisions.json"
            spec.write_text(json.dumps({
                "version": "1.0", "render_runtime": "ffmpeg",
                "cuts": [{"id": "a", "source": "nonexistent",
                          "in_seconds": 0, "out_seconds": 3}],
            }))
            result = CompositionValidator().execute({"composition_path": str(spec)})
            self.assertFalse(result.success)
            self.assertTrue(any("Missing asset" in e for e in result.data["errors"]))


if __name__ == "__main__":
    unittest.main()
