import sys
import csv
import time
import json
import unittest
import tempfile
from io import StringIO
from pathlib import Path
from copy import deepcopy

from app.producer.main import row_to_json


class TestRowToJson(unittest.TestCase):
    def test_enriches_with_timestamps_and_does_not_mutate(self):
        row = {"Waterbody Name": "A", "County": "X"}
        original = deepcopy(row)
        js = row_to_json(row)
        parsed = json.loads(js)
        # Original row unchanged
        self.assertEqual(row, original)
        # Fields present
        self.assertIn("ts", parsed)
        self.assertIn("ts_iso", parsed)
        self.assertIsInstance(parsed["ts"], int)
        self.assertIn("T", parsed["ts_iso"])  # crude ISO check
        # Original data still present
        self.assertEqual(parsed["Waterbody Name"], "A")
        self.assertEqual(parsed["County"], "X")

    def test_blank_fields_and_lines(self):
        # Create a temp CSV with header, normal row, row with empty fields, and a blank line
        tmp = tempfile.NamedTemporaryFile(mode='w+', delete=False, newline='', encoding='utf-8')
        path = Path(tmp.name)
        tmp.write('Waterbody Name,County,Comments\n')
        tmp.write('A,X,ok comment\n')
        tmp.write('B,,\n')  # empty County and Comments
        tmp.write('\n')     # blank line
        tmp.flush(); tmp.close()

        emitted = []
        with path.open('r', encoding='utf-8', newline='') as f:
            reader = csv.DictReader(f)
            for row in reader:
                # Skip completely empty dicts (can happen if blank line has fewer columns)
                if not any(v.strip() for v in row.values() if v is not None):
                    continue
                js = row_to_json(row)
                emitted.append(json.loads(js))

        # Expect 2 valid rows (blank line ignored)
        self.assertEqual(len(emitted), 2)
        # First row preserved
        self.assertEqual(emitted[0]['Waterbody Name'], 'A')
        self.assertEqual(emitted[0]['County'], 'X')
        self.assertIn('ts', emitted[0])
        # Second row has empty County; ensure key exists and is empty string
        self.assertIn('County', emitted[1])
        self.assertEqual(emitted[1]['County'], '')
        self.assertIn('ts_iso', emitted[1])


if __name__ == '__main__':  # pragma: no cover
    unittest.main()
