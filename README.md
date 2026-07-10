# Superstore Retail Sales — SQL + Power BI + Interactive Dashboard
### End-to-end retail analytics: raw CSV → cleaned SQLite database → SQL analysis → interactive dashboard → business insights report

**Role:** Solo Data Analyst (full pipeline) | **Dataset:** Superstore retail sales, 2013–2016 (6,455 orders, $8.95M revenue)

---

## 🧭 TL;DR

This project takes a raw retail sales export and turns it into a complete analytics deliverable: a cleaned, normalized SQLite database; 10 SQL analysis queries (including CTEs, window functions, and multi-table joins); an interactive browser dashboard; a Power BI rebuild guide; and a written business insights report with prioritized recommendations.

**Headline finding:** revenue grew ~10x from 2013 to 2016, but profit margin peaked in 2014 and has been declining since — with a small number of specific, fixable causes (see [`reports/insights_report.md`](./reports/insights_report.md)).

## 📁 What's inside

| Path | What it is |
|---|---|
| [`data/`](./data) | Raw CSV, cleaned CSV, and the final SQLite database (`retail.db`) |
| [`notebook/01_clean_and_build_db.py`](./notebook/01_clean_and_build_db.py) | Cleans the raw export and builds the normalized `customers` / `products` / `orders` schema |
| [`notebook/02_build_dashboard_data.py`](./notebook/02_build_dashboard_data.py) | Runs the aggregation queries and exports `dashboard/data.json` for the frontend |
| [`sql/01_schema.sql`](./sql/01_schema.sql) | Documented schema for the 3-table model |
| [`sql/02_analysis_queries.sql`](./sql/02_analysis_queries.sql) | 10 analysis queries — KPIs, joins, CTEs, window functions (Pareto analysis, MoM growth, running totals) |
| [`dashboard/index.html`](./dashboard/index.html) | Interactive Chart.js dashboard — open directly in any browser, no server needed |
| [`powerbi/POWER_BI_INSTRUCTIONS.md`](./powerbi/POWER_BI_INSTRUCTIONS.md) | Step-by-step guide to rebuild the same dashboard in Power BI with DAX measures |
| [`reports/insights_report.md`](./reports/insights_report.md) | Written business insights report with prioritized recommendations |

## 🖥️ View the dashboard

Open `dashboard/index.html` directly in any browser — it reads `dashboard/data.json` and renders instantly, no server or install needed.

## 🗄️ Rebuild the database from scratch

```bash
cd notebook
python 01_clean_and_build_db.py     # raw CSV → cleaned data/retail.db
python 02_build_dashboard_data.py   # retail.db → dashboard/data.json
```

Then run the SQL analysis directly:
```bash
sqlite3 -header -column ../data/retail.db < ../sql/02_analysis_queries.sql
```

## 📊 Key numbers

| Metric | Value |
|---|---|
| Total revenue (2013–2016) | $8.95M |
| Total profit | $1.31M |
| Overall profit margin | 14.7% |
| Total orders | 6,455 |
| Top-20%-of-customers revenue share | 80% (from the top 27.3% of customers) |

Full breakdown and recommendations in [`reports/insights_report.md`](./reports/insights_report.md).

## 🛠️ Tools & techniques used

`Python (pandas)` · `SQLite` · `SQL (CTEs, window functions, joins)` · `Chart.js` · `Power BI (DAX)` · `Pareto/cohort analysis` · `KPI dashboard design`

---
*Built by Raj Singh — [LinkedIn](https://linkedin.com/in/rajsingh-dataanalyst) · [GitHub](https://github.com/rajsing13555)*
