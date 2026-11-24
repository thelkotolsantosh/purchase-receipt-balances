# Purchase Receipt Balances

A buyer receives 5 units on Monday and 4 more on Tuesday against an order for 12. How many should the supplier still deliver? This small procurement report joins purchase lines to their receipt events and reports open and excess units separately.

## Run the example

Clone the repository and open its directory with Python 3.10+ and the standard sqlite3 module installed.

    python reconcile.py examples/deliveries.json

PO-41/1 has 3 units outstanding. PO-41/2 has 1 excess unit. Each line is reconciled independently. A surplus on one item cannot conceal a shortage on another.

## Data and workflow

Export one consistent snapshot as UTF-8 JSON. Give each order line a globally unique id and a positive whole-number ordered quantity. Each receipt has its own unique event id, a line_id and positive units in the same unit of measure. Use synthetic data in shared reports.

reconcile.py loads migrations/001.sql into an in-memory SQLite database. One order line has zero or more receipts. The importer validates both arrays in one transaction, rejects duplicate keys and enforces receipt references. The report groups deliveries per line and retains lines without receipts. Invalid inputs exit with status 2. Successful output is a JSON array sorted by line ID.

## Operations and scope

Run python -m unittest discover -s tests -v. For reproducibility archive the dated input snapshot alongside the output and code version. Restore by rerunning that snapshot. The local operating-system account controls file access. Receipt IDs in the input provide the audit trail. This read-only reporting prototype covers whole-unit deliveries. Returns, cancellations, approvals and ledger posting would require additional modules.

See faq.md for the input contract, CONTRIBUTING.md for testing changes and LICENSE for MIT terms.
