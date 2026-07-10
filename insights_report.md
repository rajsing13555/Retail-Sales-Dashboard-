# Insights Report — Superstore Retail Sales (2013–2016)

*All figures below are pulled directly from the SQL queries in [`sql/02_analysis_queries.sql`](../sql/02_analysis_queries.sql) run against `data/retail.db`.*

## Executive Summary

Between 2013 and 2016, the business grew revenue nearly 10x (from $372K to $3.71M annually) — but profit margin has been sliding since 2014, and a small set of structural problems (specific loss-making categories, slow Central-region shipping, and margin-thin Consumer segment) are quietly eating into that growth. The headline numbers:

| Metric | Value |
|---|---|
| Total revenue (2013–2016) | $8.95M |
| Total profit | $1.31M |
| Overall profit margin | 14.7% |
| Total orders | 6,455 |
| Average order value | $1,387 |

## Finding 1 — Growth is real, but margin is eroding

Revenue grew every year, but profit margin peaked in 2014 (19.2%) and has declined since — down to 12.3% by 2016.

| Year | Revenue | Profit | Margin |
|---|---|---|---|
| 2013 | $371,971 | $42,796 | 11.5% |
| 2014 | $1,717,979 | $330,341 | **19.2%** |
| 2015 | $3,152,871 | $483,181 | 15.3% |
| 2016 | $3,709,206 | $456,097 | 12.3% |

**Read:** the business is scaling revenue faster than it's protecting profitability. This is the single most important trend for leadership to see — growth alone is masking a margin problem that would otherwise be a headline concern.

## Finding 2 — Tables is the single biggest profit leak

The Tables category generated $1.06M in revenue but **lost $72,506** (-6.8% margin) — the largest dollar loss of any category. Bookcases (-$7,714), Rubber Bands (-32.7% margin), and Scissors/Rulers/Trimmers (-4.8% margin) round out the loss-making list.

At the product level, the worst offenders are concentrated in **Office Machines** (printers, videoconferencing units) and **Tables** — e.g., the Okidata Pacemark 4410N printer lost $39,743 on just $27,214 of revenue sold. This pattern (high unit price, deep discounting, likely high shipping cost) suggests these SKUs are being discounted below a sustainable margin, not simply low-demand products.

**Recommendation:** Audit discount policy specifically for Tables and Office Machines — this looks like a pricing/discounting problem, not a demand problem, since both categories still generate meaningful revenue.

## Finding 3 — Regional profit gap is wider than the revenue gap suggests

| Region | Revenue | Profit | Rank |
|---|---|---|---|
| East | $3.14M | $475,024 | 1 |
| Central | $2.29M | $458,668 | 2 |
| West | $2.00M | $271,578 | 3 |
| South | $1.51M | $107,145 | 4 |

South generates 48% of East's revenue but only 23% of East's profit — a disproportionate margin gap worth investigating region-by-region (likely a mix of discount policy and shipping cost differences by region).

## Finding 4 — Customer concentration is moderate, not extreme

The top **27.3%** of customers drive **80%** of total revenue. This is a healthier distribution than a classic 80/20 Pareto pattern (where ~20% of customers would drive 80%) — the customer base is relatively well-diversified, which is a genuine strength worth highlighting, not just a risk to manage.

## Finding 5 — Consumer segment is the largest but least profitable

| Segment | Customers | Revenue | Profit | Margin |
|---|---|---|---|---|
| Corporate | 948 | $3.25M | $473,992 | 14.6% |
| Home Office | 618 | $2.11M | $314,760 | 14.9% |
| Small Business | 600 | $1.70M | $286,216 | **16.9%** |
| Consumer | 537 | $1.90M | $237,447 | **12.5%** |

Small Business customers are the most profitable per rupee of revenue, while Consumer — despite the highest revenue-per-customer ($3,531) — has the lowest margin. A segment-specific pricing or promotion review for Consumer could recover meaningful margin without needing new customer acquisition.

## Finding 6 — Central region shipping is a quiet operational drag

Average days-to-ship for Delivery Truck orders in the Central region is **23.1 days** — roughly 70% slower than the same ship mode in the East (13.5 days). This is worth flagging to operations independent of the profit analysis, since shipping delays are a common (if under-measured) driver of customer churn.

## Recommendations, prioritized

1. **Immediate:** Review discount depth on Tables and Office Machines SKUs — this is the single largest, most fixable profit leak identified.
2. **Short-term:** Investigate why South region's margin lags so far behind its revenue — likely candidates are region-specific discount policy or higher shipping cost.
3. **Medium-term:** Pilot a targeted pricing or bundling strategy for the Consumer segment, which has the largest revenue base but weakest margin.
4. **Operational:** Flag Central-region Delivery Truck shipping times to logistics/ops — a 23-day average is an outlier worth explaining.
