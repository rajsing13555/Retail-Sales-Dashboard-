# Power BI Setup Guide — Superstore Retail Sales Dashboard

This guide rebuilds the same dashboard shown in `dashboard/index.html` inside Power BI Desktop, using the same cleaned data and the same KPIs/visuals. Follow it top to bottom — each section maps directly to a section of the HTML dashboard.

## 1. Get the data into Power BI

**Option A — CSV import (simplest):**
1. Open Power BI Desktop → **Home → Get Data → Text/CSV**
2. Select `data/superstore_clean.csv` (already cleaned and column-typed — use this, not the raw file)
3. Click **Transform Data** to open Power Query, verify column types (see Section 2), then **Close & Apply**

**Option B — Connect directly to the SQLite database (`data/retail.db`):**
1. Power BI doesn't have a native SQLite connector, so install the free **SQLite ODBC Driver** (search "SQLite ODBC Driver" — Christian Werner's build is the standard one).
2. In Windows: **ODBC Data Sources (64-bit) → Add → SQLite3 ODBC Driver** → point it at `data/retail.db`.
3. In Power BI: **Get Data → ODBC** → select the DSN you just created → choose the `orders`, `customers`, and `products` tables.
4. This lets you pull all three normalized tables directly, matching the schema in `sql/01_schema.sql` — recommended if you want to show JOIN-based data modeling skills in the interview.

## 2. Verify column types in Power Query

Before loading, check these columns are typed correctly (Power BI sometimes guesses wrong on import):
- `order_date`, `ship_date` → **Date**
- `sales`, `profit`, `discount`, `product_base_margin`, `unit_price`, `shipping_cost` → **Decimal Number**
- `order_quantity`, `days_to_ship`, `postal_code` → **Whole Number**
- Everything else (`category`, `region`, `customer_segment`, etc.) → **Text**

## 3. Build the data model (if using Option B — 3 tables)

1. Go to the **Model** view.
2. Create relationships:
   - `orders[customer_id]` → `customers[customer_id]` (many-to-one)
   - `orders[item_id]` → `products[item_id]` (many-to-one)
3. This mirrors the star-schema structure already defined in `sql/01_schema.sql`.

## 4. Create the DAX measures

Go to **Modeling → New Measure** and add these one at a time (matches the KPI cards in the HTML dashboard):

```dax
Total Revenue = SUM(orders[sales])

Total Profit = SUM(orders[profit])

Profit Margin % = DIVIDE([Total Profit], [Total Revenue], 0)

Total Orders = DISTINCTCOUNT(orders[order_id])

Avg Order Value = DIVIDE([Total Revenue], [Total Orders], 0)
```

For the month-over-month growth chart:

```dax
Revenue MoM % =
VAR CurrentRevenue = [Total Revenue]
VAR PreviousRevenue =
    CALCULATE(
        [Total Revenue],
        DATEADD(orders[order_date], -1, MONTH)
    )
RETURN
    DIVIDE(CurrentRevenue - PreviousRevenue, PreviousRevenue, 0)
```

For the Pareto (top-customer concentration) analysis:

```dax
Customer Revenue Rank =
RANKX(
    ALL(customers[customer_name]),
    CALCULATE([Total Revenue]),
    ,
    DESC
)
```

## 5. Build the report pages

Recreate these visuals (each maps to a chart already built in `dashboard/index.html`, so you can screenshot both side-by-side for your portfolio README):

| Visual | Power BI chart type | Fields |
|---|---|---|
| KPI cards (Revenue, Profit, Margin, Orders, AOV) | **Card** visual ×5 | The 5 measures above |
| Monthly revenue trend | **Line chart** | Axis: `order_date` (Month), Value: `Total Revenue` |
| Revenue by department | **Donut chart** | Legend: `department`, Value: `Total Revenue` |
| Revenue vs. profit by category | **Clustered bar chart** | Axis: `category`, Values: `Total Revenue`, `Total Profit` |
| Profit by region | **Bar chart** | Axis: `region`, Value: `Total Profit` |
| Customer segment profitability | **Clustered bar chart** | Axis: `customer_segment`, Values: `Total Revenue`, `Total Profit` |
| Avg. days to ship by mode | **Bar chart** | Axis: `ship_mode`, Value: Avg of `days_to_ship` |
| Top 10 customers | **Bar chart** (sorted, top N filter) | Axis: `customer_name`, Value: `Total Revenue` |

## 6. Add a page-level filter panel

Add a **Slicer** for `order_year` and `region` at the top of the report page — this is a standard Power BI interactivity feature that the static HTML dashboard doesn't have, and it's worth mentioning explicitly in interviews as something you'd add given more time/a live BI tool.

## 7. Publish & export for your portfolio

1. **File → Export → Export to PDF** — put this PDF in your repo as `powerbi/dashboard_screenshot.pdf` so recruiters without Power BI installed can still see it.
2. If you have a Power BI account: **Publish** to the Power BI Service and add the shareable link to your repo's README.
3. Save the `.pbix` file itself in the `powerbi/` folder so anyone with Power BI Desktop can open and interact with it directly.

## Why this matters for interviews

Being able to say *"I built the same analysis two ways — a lightweight Chart.js dashboard for anyone to view instantly in a browser, and a full Power BI model with DAX measures and a proper star schema"* demonstrates both scrappiness (ship something viewable with zero setup) and BI-tool fluency (the actual tool most Data Analyst job descriptions name explicitly) — in the same project.
