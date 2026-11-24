# FAQ

## 1. What does the report calculate?

Outstanding and excess units for each purchase line.

## 2. Why reconcile at line level?

A surplus of one item cannot fill a shortage of another.

## 3. Who uses the result?

Buyers can follow up on outstanding quantities with suppliers.

## 4. Which deliveries are supported?

Zero, one or multiple positive whole-unit receipts per line.

## 5. Which language is required?

Python runs the importer and report entry point.

## 6. What stores the snapshot?

SQLite holds two related tables in memory during each run.

## 7. What prerequisites are needed?

Use Python 3.10 or later with sqlite3 enabled.

## 8. How do I install it?

Clone the repository and retain migrations alongside reconcile.py.

## 9. Which quantities should I export?

Use the same unit of measure on a line and all its receipts.

## 10. How do I run the example?

Run python reconcile.py examples/deliveries.json.

## 11. Where is the database schema?

migrations/001.sql defines order_line, receipt and the lookup index.

## 12. How are partial deliveries combined?

The query sums receipt units grouped by purchase line.

## 13. What input does it accept?

A JSON object with lines and receipts arrays.

## 14. What does excess mean?

It counts delivered units above the ordered quantity.

## 15. Can I use my own identifiers?

Yes. Supply unique nonblank strings for purchase lines and receipt events.

## 16. What happens to an unknown line reference?

The foreign key rejects the receipt and the whole import rolls back.

## 17. Can I reuse one delivery slip number across items?

Include the slip line number to make each event ID unique.

## 18. How do I investigate a mismatch?

Filter the archived receipts by line_id and total their units against the order.

## 19. How do I run the tests?

Run python -m unittest discover -s tests -v.

## 20. How do I contribute a rule?

Submit a synthetic example and test for its expected outstanding and excess quantities.

## 21. Can it handle negative return events?

The current schema accepts positive receipts. Returns need a separate event type.

## 22. Does this replace an operational ERP?

It is an offline report. Warehouse posting and approvals belong in the source ERP.

## 23. What could a future version add?

Return events and dated order revisions would support more complex histories.

## 24. How do I protect procurement records?

Limit access to local snapshots and archive them using your normal data controls.

## 25. How do I recover a previous report?

Run the archived snapshot against its recorded code version as described in README.md.

