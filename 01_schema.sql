-- ============================================================
-- Schema: Superstore Retail Sales (normalized 3-table model)
-- ============================================================
-- Built by notebook/01_clean_and_build_db.py from the raw CSV export.
-- This file documents the schema; the tables already exist in data/retail.db.

CREATE TABLE customers (
    customer_id       INTEGER PRIMARY KEY,
    customer_name     TEXT,
    customer_segment  TEXT   -- Consumer, Corporate, Home Office, Small Business
);

CREATE TABLE products (
    item_id               INTEGER PRIMARY KEY,
    item_name             TEXT,
    category              TEXT,   -- e.g. Paper, Tables, Chairs & Chairmats
    department            TEXT,   -- Office Supplies, Furniture, Technology
    container             TEXT,
    unit_price            REAL,
    product_base_margin   REAL
);

CREATE TABLE orders (              -- fact table, one row per order line item
    order_line_id       INTEGER PRIMARY KEY,
    order_id            INTEGER,
    customer_id         INTEGER REFERENCES customers(customer_id),
    item_id             INTEGER REFERENCES products(item_id),
    order_date          TEXT,      -- ISO date
    ship_date           TEXT,
    order_year          INTEGER,
    order_month         INTEGER,
    order_year_month    TEXT,      -- 'YYYY-MM', for easy monthly grouping
    days_to_ship        INTEGER,
    ship_mode           TEXT,
    order_priority      TEXT,
    region              TEXT,
    state               TEXT,
    city                TEXT,
    postal_code         INTEGER,
    order_quantity      INTEGER,
    discount            REAL,
    sales               REAL,
    profit              REAL,
    profit_margin_pct   REAL,
    shipping_cost       REAL
);

CREATE INDEX idx_orders_customer ON orders(customer_id);
CREATE INDEX idx_orders_item ON orders(item_id);
CREATE INDEX idx_orders_date ON orders(order_date);
