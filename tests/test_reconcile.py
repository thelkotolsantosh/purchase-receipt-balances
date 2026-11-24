import sqlite3
import unittest
from reconcile import report


class ReceiptBalance(unittest.TestCase):
    def snapshot(self, quantities):
        return {"lines": [{"id": "L", "ordered": 5}], "receipts": [
            {"id": str(i), "line_id": "L", "units": n} for i, n in enumerate(quantities)]}

    def test_balances(self):
        for units, open_qty, excess in [([], 5, 0), ([2], 3, 0), ([2, 3], 0, 0), ([7], 0, 2)]:
            row, = report(self.snapshot(units))
            self.assertEqual((row["outstanding"], row["excess"]), (open_qty, excess))

    def test_unknown_line(self):
        data = self.snapshot([2])
        data["lines"] = []
        with self.assertRaises(sqlite3.IntegrityError):
            report(data)

    def test_duplicate_receipt(self):
        data = self.snapshot([2])
        data["receipts"] *= 2
        with self.assertRaises(sqlite3.IntegrityError):
            report(data)

    def test_invalid_units(self):
        for value in [0, -1, 1.2, True]:
            with self.assertRaises(ValueError):
                report(self.snapshot([value]))
