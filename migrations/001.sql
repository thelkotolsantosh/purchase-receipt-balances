CREATE TABLE order_line (
    id TEXT NOT NULL PRIMARY KEY,
    ordered INTEGER NOT NULL CHECK(ordered > 0)
);
CREATE TABLE receipt (
    id TEXT NOT NULL PRIMARY KEY,
    line_id TEXT NOT NULL REFERENCES order_line(id),
    units INTEGER NOT NULL CHECK(units > 0)
);
CREATE INDEX receipt_line ON receipt(line_id);
