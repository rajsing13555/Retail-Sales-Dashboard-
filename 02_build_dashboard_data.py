"""
Precompute all aggregates needed for the interactive HTML dashboard,
so the dashboard itself stays a static file (no server/backend needed).
Run: python3 02_build_dashboard_data.py
"""
import pandas as pd
import json

df = pd.read_csv("../data/superstore_clean.csv", parse_dates=["order_date", "ship_date"])

data = {}

# KPI cards
data["kpis"] = {
    "total_revenue": round(df["sales"].sum()),
    "total_profit": round(df["profit"].sum()),
    "total_orders": int(df["order_id"].nunique()),
    "profit_margin_pct": round(df["profit"].sum() / df["sales"].sum() * 100, 1),
    "avg_order_value": round(df["sales"].sum() / df["order_id"].nunique()),
}

# Revenue & profit by year
yearly = df.groupby("order_year").agg(revenue=("sales", "sum"), profit=("profit", "sum")).reset_index()
data["yearly"] = {
    "years": yearly["order_year"].astype(str).tolist(),
    "revenue": yearly["revenue"].round().tolist(),
    "profit": yearly["profit"].round().tolist(),
}

# Monthly revenue trend
monthly = df.groupby("order_year_month").agg(revenue=("sales", "sum")).reset_index().sort_values("order_year_month")
data["monthly"] = {
    "months": monthly["order_year_month"].tolist(),
    "revenue": monthly["revenue"].round().tolist(),
}

# Revenue & profit by department
dept = df.groupby("department").agg(revenue=("sales", "sum"), profit=("profit", "sum")).reset_index().sort_values("revenue", ascending=False)
data["by_department"] = {
    "labels": dept["department"].tolist(),
    "revenue": dept["revenue"].round().tolist(),
    "profit": dept["profit"].round().tolist(),
}

# Revenue & profit by category (top 12 by revenue)
cat = df.groupby("category").agg(revenue=("sales", "sum"), profit=("profit", "sum")).reset_index().sort_values("revenue", ascending=False).head(12)
data["by_category"] = {
    "labels": cat["category"].tolist(),
    "revenue": cat["revenue"].round().tolist(),
    "profit": cat["profit"].round().tolist(),
}

# Revenue by region
region = df.groupby("region").agg(revenue=("sales", "sum"), profit=("profit", "sum")).reset_index().sort_values("revenue", ascending=False)
data["by_region"] = {
    "labels": region["region"].tolist(),
    "revenue": region["revenue"].round().tolist(),
    "profit": region["profit"].round().tolist(),
}

# Customer segment
seg = df.groupby("customer_segment").agg(
    revenue=("sales", "sum"), profit=("profit", "sum"), customers=("customer_id", "nunique")
).reset_index().sort_values("revenue", ascending=False)
data["by_segment"] = {
    "labels": seg["customer_segment"].tolist(),
    "revenue": seg["revenue"].round().tolist(),
    "profit": seg["profit"].round().tolist(),
    "customers": seg["customers"].tolist(),
}

# Ship mode avg days to ship
ship = df.groupby("ship_mode").agg(avg_days=("days_to_ship", "mean"), orders=("order_id", "nunique")).reset_index().sort_values("avg_days")
data["ship_mode"] = {
    "labels": ship["ship_mode"].tolist(),
    "avg_days": ship["avg_days"].round(1).tolist(),
}

# Top 10 customers by revenue
top_cust = df.groupby(["customer_id"]).agg(revenue=("sales", "sum")).reset_index().sort_values("revenue", ascending=False).head(10)
top_cust = top_cust.merge(df[["customer_id", "customer_name"]].drop_duplicates(), on="customer_id")
data["top_customers"] = {
    "names": top_cust["customer_name"].tolist(),
    "revenue": top_cust["revenue"].round().tolist(),
}

# Loss-making categories (for callout)
cat_margin = df.groupby("category").agg(revenue=("sales", "sum"), profit=("profit", "sum")).reset_index()
cat_margin["margin_pct"] = (cat_margin["profit"] / cat_margin["revenue"] * 100).round(1)
losers = cat_margin[cat_margin["profit"] < 0].sort_values("profit")
data["loss_categories"] = losers.to_dict("records")

with open("../dashboard/data.json", "w") as f:
    json.dump(data, f, indent=2)

print("Dashboard data written -> ../dashboard/data.json")
print(json.dumps(data["kpis"], indent=2))
print("Loss-making categories:", [r["category"] for r in data["loss_categories"]])
