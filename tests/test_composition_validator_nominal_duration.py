"""Regression: validator must compare narration with output, not source timecodes."""

import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from tools.analysis.composition_validator import CompositionValidator


class ValidatorDurationIntegrationTests(unittest.TestCase):
    def _validate(self, narration_seconds):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "a.mp4").touch()
            (root / "b.mp4").touch()
            (root / "narration.wav").touch()
            composition = {
                "version": "1.0",
                "render_runtime": "ffmpeg",
                "cuts": [
                    {"id": "shot-1", "source": "a.mp4", "in_seconds": 120, "out_seconds": 125},
                    {"id": "shot-2", "source": "b.mp4", "in_seconds": 380, "out_seconds": 384},
                ],
                "audio": {"narration": {"src": "narration.wav"}},
            }
            spec = root / "edit_decisions.json"
            spec.write_text(json.dumps(composition), encoding="utf-8")
            with patch(
                "tools.analysis.composition_validator.probe_duration",
                return_value=narration_seconds,
            ):
                return CompositionValidator().execute(
                    {"composition_path": str(spec), "assets_root": str(root)}
                )

    def test_overshooting_narration_is_blocked(self):
        # Actual timeline is 5+4=9 seconds. Legacy max(out_seconds)
        # misreported 384 seconds and would incorrectly pass this test.
        result = self._validate(10.5)
        self.assertFalse(result.success)
        self.assertTrue(any(
            "exceeds video" in item for item in result.data["errors"]
        ))

    def test_narration_within_timeline_is_allowed(self):
        result = self._validate(8.5)
        self.assertTrue(result.success, result.error)
        self.assertTrue(any(
            "Nominal video duration: 9" in item for item in result.data["info"]
        ))


if __name__ == "__main__":
    unittest.main()
