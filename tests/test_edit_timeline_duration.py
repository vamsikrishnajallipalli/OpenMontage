"""Regression tests for source trim vs output-timeline semantics."""

import unittest
from lib.edit_timeline_duration import nominal_duration_seconds


def cut(name, a, b, *, speed=1, layer="primary"):
    return {"id": name, "source": "irrelevant.mp4", "in_seconds": a,
            "out_seconds": b, "speed": speed, "layer": layer}


class NominalDurationTests(unittest.TestCase):
    def test_source_offsets_not_timeline_positions(self):
        self.assertEqual(nominal_duration_seconds([
            cut("a", 120, 125), cut("b", 380, 384)]), 9)

    def test_playback_speed(self):
        self.assertEqual(nominal_duration_seconds([
            cut("a", 25, 37, speed=2), cut("b", 5, 8, speed=.5)]), 12)

    def test_overlays_do_not_extend_duration(self):
        self.assertEqual(nominal_duration_seconds([
            cut("a", 0, 5), cut("title", 90, 150, layer="overlay")]), 5)

    def test_background_only_is_accepted(self):
        self.assertEqual(nominal_duration_seconds([cut("bg", 8, 18, layer="background")]), 10)

    def test_rejects_invalid_timing(self):
        for invalid in [
            [cut("a", 3, 3)], [cut("a", 4, 3)],
            [cut("a", 0, 2, speed=0)], [cut("a", float('nan'), 4)],
            [cut("a", 0, 3), cut("a", 10, 12)],
            [cut("overlay", 0, 5, layer="overlay")],
        ]:
            with self.subTest(invalid=invalid), self.assertRaises(ValueError):
                nominal_duration_seconds(invalid)


if __name__ == "__main__":
    unittest.main()
