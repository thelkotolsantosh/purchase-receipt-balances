"""Reconcile one purchase-order snapshot with its goods receipts."""
import argparse
import json
import sqlite3
from contextlib import closing
from pathlib import Path


def identifier(value):
    if not isinstance(value, str) or not value.strip():
        raise ValueError("Identifiers must be nonempty strings")
    return value.strip()


def quantity(value):
    if type(value) is not int or value <= 0:
        raise ValueError("Expected a positive integer quantity")
    return value


def report(snapshot):
    lines, receipts = snapshot["lines"], snapshot["receipts"]
    if not isinstance(lines, list) or not isinstance(receipts, list):
        raise ValueError("Expected arrays for lines and receipts")
    with closing(sqlite3.connect(":memory:")) as db:
        db.execute("PRAGMA foreign_keys = ON")
        db.executescript((Path(__file__).parent / "migrations/001.sql").read_text())
        with db:
            for line in lines:
                db.execute("INSERT INTO order_line VALUES (?, ?)",
                           (identifier(line["id"]), quantity(line["ordered"])))
            for receipt in receipts:
                db.execute("INSERT INTO receipt VALUES (?, ?, ?)",
                           (identifier(receipt["id"]), identifier(receipt["line_id"]),
                            quantity(receipt["units"])))
        rows = db.execute("""
            SELECT l.id, l.ordered, COALESCE(SUM(r.units), 0)
            FROM order_line l LEFT JOIN receipt r ON r.line_id = l.id
            GROUP BY l.id, l.ordered ORDER BY l.id
        """)
        return [dict(line_id=key, ordered=ordered, received=received,
                     outstanding=max(0, ordered-received), excess=max(0, received-ordered))
                for key, ordered, received in rows]


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("snapshot", type=Path)
    args = parser.parse_args()
    try:
        print(json.dumps(report(json.loads(args.snapshot.read_text(encoding="utf-8"))), indent=2))
    except (OSError, ValueError, TypeError, KeyError, OverflowError, sqlite3.Error) as error:
        parser.exit(2, f"Invalid snapshot: {error}\n")
