import json
import unittest
from copy import deepcopy

from app.producer.main import row_to_json


class TestProducer(unittest.TestCase):
  def __str__(self):
        return f"Producer: {self._testMethodName}"

  def test_timestamps_and_does_not_mutate(self):
    row = {"Waterbody Name": "A", "County": "X"}
    original = deepcopy(row)
    js = row_to_json(row)
    produced = json.loads(js)
    # Original row unchanged
    self.assertEqual(row, original)
    # Fields present
    self.assertIn("ts", produced)
    self.assertIn("ts_iso", produced)
    self.assertIsInstance(produced["ts"], int)
    self.assertIn("T", produced["ts_iso"])  # crude ISO check
    # Original data still present
    self.assertEqual(produced["Waterbody Name"], "A")
    self.assertEqual(produced["County"], "X")


if __name__ == '__main__':  # pragma: no cover
  unittest.main()
