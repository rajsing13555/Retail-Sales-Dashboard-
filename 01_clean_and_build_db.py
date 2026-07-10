"""
Data cleaning + normalization + SQLite DB build for the Superstore Retail Sales project.
Run: python3 01_clean_and_build_db.py
"""
import pandas as pd
import sqlite3
import os

RAW_PATH = "../data/superstore_raw.csv"
CLEAN_PATH = "../data/superstore_clean.csv"
DB_PATH = "../data/retail.db"

def clean():
    df = pd.read_csv(RAW_PATH, encoding='latin1')

    # --- Data quality issue found during EDA: the "Row ID" column contains
    # date-like strings (e.g. "11/18/1951"), not a real identifier — likely a
    # column-mapping error upstream in the source export. We drop it and
    # generate a clean surrogate key instead of trusting it. ---
    df = df.drop(columns=["Row ID"])
    df = df.reset_index(drop=True)
    df.insert(0, "order_line_id", df.index + 1)

    # Standardize column names to snake_case for SQL friendliness
    rename_map = {
        "Category": "category", "City": "city", "Container": "container",
        "Customer ID": "customer_id", "Customer Name": "customer_name",
        "Customer Segment": "customer_segment", "Department": "department",
        "Item ID": "item_id", "Item": "item_name", "Order Date": "order_date",
        "Order ID": "order_id", "Order Priority": "order_priority",
        "Postal Code": "postal_code", "Region": "region", "Ship Date": "ship_date",
        "Ship Mode": "ship_mode", "State": "state", "Discount": "discount",
        "Order Quantity": "order_quantity", "Product Base Margin": "product_base_margin",
        "Profit": "profit", "Sales": "sales", "Shipping Cost": "shipping_cost",
        "Unit Price": "unit_price",
    }
    df = df.rename(columns=rename_map)

    # Parse dates
    df["order_date"] = pd.to_datetime(df["order_date"], format="%m/%d/%Y")
    df["ship_date"] = pd.to_datetime(df["ship_date"], format="%m/%d/%Y")

    # Derived columns used repeatedly downstream (compute once, not per-query)
    df["order_year"] = df["order_date"].dt.year
    df["order_month"] = df["order_date"].dt.month
    df["order_year_month"] = df["order_date"].dt.to_period("M").astype(str)
    df["days_to_ship"] = (df["ship_date"] - df["order_date"]).dt.days
    df["profit_margin_pct"] = (df["profit"] / df["sales"] * 100).round(2)

    # Sanity checks
    assert df["order_line_id"].is_unique
    assert (df["days_to_ship"] >= 0).all(), "Found ship_date before order_date"
    assert df["sales"].min() >= 0, "Found negative sales after cleaning"

    df.to_csv(CLEAN_PATH, index=False)
    print(f"Cleaned data saved: {df.shape[0]} rows, {df.shape[1]} columns -> {CLEAN_PATH}")
    return df

def build_db(df):
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)
    conn = sqlite3.connect(DB_PATH)

    customers = (
        df[["customer_id", "customer_name", "customer_segment"]]
        .drop_duplicates(subset=["customer_id"])
        .reset_index(drop=True)
    )
    products = (
        df[["item_id", "item_name", "category", "department", "container",
            "unit_price", "product_base_margin"]]
        .drop_duplicates(subset=["item_id"])
        .reset_index(drop=True)
    )
    orders_fact = df[[
        "order_line_id", "order_id", "customer_id", "item_id", "order_date",
        "ship_date", "order_year", "order_month", "order_year_month",
        "days_to_ship", "ship_mode", "order_priority", "region", "state",
        "city", "postal_code", "order_quantity", "discount", "sales",
        "profit", "profit_margin_pct", "shipping_cost",
    ]]

    customers.to_sql("customers", conn, index=False, if_exists="replace")
    products.to_sql("products", conn, index=False, if_exists="replace")
    orders_fact.to_sql("orders", conn, index=False, if_exists="replace")

    conn.execute("CREATE INDEX idx_orders_customer ON orders(customer_id)")
    conn.execute("CREATE INDEX idx_orders_item ON orders(item_id)")
    conn.execute("CREATE INDEX idx_orders_date ON orders(order_date)")
    conn.commit()

    print(f"SQLite DB built -> {DB_PATH}")
    print(f"  customers: {len(customers)} rows")
    print(f"  products:  {len(products)} rows")
    print(f"  orders:    {len(orders_fact)} rows")
    conn.close()

if __name__ == "__main__":
    df = clean()
    build_db(df)
