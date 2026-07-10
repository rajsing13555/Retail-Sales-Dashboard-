-- ============================================================
-- Analysis queries: Superstore Retail Sales
-- Run against data/retail.db, e.g.: sqlite3 data/retail.db < sql/02_analysis_queries.sql
-- ============================================================

-- Q1. Headline KPIs by year
SELECT
    order_year,
    COUNT(DISTINCT order_id)          AS total_orders,
    ROUND(SUM(sales), 0)              AS total_revenue,
    ROUND(SUM(profit), 0)             AS total_profit,
    ROUND(SUM(profit) * 100.0 / SUM(sales), 2) AS profit_margin_pct,
    ROUND(SUM(sales) * 1.0 / COUNT(DISTINCT order_id), 0) AS avg_order_value
FROM orders
GROUP BY order_year
ORDER BY order_year;

-- Q2. Revenue and profit by department and category (JOIN)
SELECT
    p.department,
    p.category,
    COUNT(*)                          AS line_items,
    ROUND(SUM(o.sales), 0)            AS total_revenue,
    ROUND(SUM(o.profit), 0)           AS total_profit,
    ROUND(SUM(o.profit) * 100.0 / NULLIF(SUM(o.sales), 0), 2) AS profit_margin_pct
FROM orders o
JOIN products p ON p.item_id = o.item_id
GROUP BY p.department, p.category
ORDER BY total_revenue DESC;

-- Q3. Top 15 customers by lifetime revenue (JOIN + LIMIT)
SELECT
    c.customer_name,
    c.customer_segment,
    COUNT(DISTINCT o.order_id)        AS orders_placed,
    ROUND(SUM(o.sales), 0)            AS lifetime_revenue,
    ROUND(SUM(o.profit), 0)           AS lifetime_profit
FROM orders o
JOIN customers c ON c.customer_id = o.customer_id
GROUP BY c.customer_id
ORDER BY lifetime_revenue DESC
LIMIT 15;

-- Q4. Month-over-month revenue growth (CTE + window function LAG)
WITH monthly_revenue AS (
    SELECT
        order_year_month,
        SUM(sales) AS revenue
    FROM orders
    GROUP BY order_year_month
)
SELECT
    order_year_month,
    ROUND(revenue, 0) AS revenue,
    ROUND(revenue - LAG(revenue) OVER (ORDER BY order_year_month), 0) AS revenue_change,
    ROUND(
        (revenue - LAG(revenue) OVER (ORDER BY order_year_month)) * 100.0
        / NULLIF(LAG(revenue) OVER (ORDER BY order_year_month), 0), 2
    ) AS mom_growth_pct
FROM monthly_revenue
ORDER BY order_year_month;

-- Q5. Regional performance ranking (window function RANK)
SELECT
    region,
    ROUND(SUM(sales), 0)      AS total_revenue,
    ROUND(SUM(profit), 0)     AS total_profit,
    RANK() OVER (ORDER BY SUM(profit) DESC) AS profit_rank
FROM orders
GROUP BY region
ORDER BY profit_rank;

-- Q6. Pareto analysis — what share of customers drives 80% of revenue?
-- (CTE + window functions: SUM OVER for cumulative revenue, PERCENT_RANK for customer percentile)
WITH customer_revenue AS (
    SELECT
        customer_id,
        SUM(sales) AS revenue
    FROM orders
    GROUP BY customer_id
),
ranked AS (
    SELECT
        customer_id,
        revenue,
        SUM(revenue) OVER (ORDER BY revenue DESC) AS cumulative_revenue,
        SUM(revenue) OVER ()                       AS total_revenue,
        ROW_NUMBER() OVER (ORDER BY revenue DESC)  AS customer_rank,
        COUNT(*) OVER ()                           AS total_customers
    FROM customer_revenue
)
SELECT
    customer_rank,
    total_customers,
    ROUND(customer_rank * 100.0 / total_customers, 1) AS pct_of_customers,
    ROUND(cumulative_revenue * 100.0 / total_revenue, 1) AS pct_of_revenue_captured
FROM ranked
WHERE ROUND(cumulative_revenue * 100.0 / total_revenue, 1) >= 80
ORDER BY customer_rank
LIMIT 1;

-- Q7. Loss-making products — negative profit margin, sorted by total loss (subquery)
SELECT
    p.item_name,
    p.category,
    COUNT(*)                       AS times_sold,
    ROUND(SUM(o.sales), 0)         AS total_revenue,
    ROUND(SUM(o.profit), 0)        AS total_profit_loss
FROM orders o
JOIN products p ON p.item_id = o.item_id
WHERE o.item_id IN (
    SELECT item_id FROM orders
    GROUP BY item_id
    HAVING SUM(profit) < 0
)
GROUP BY p.item_id
ORDER BY total_profit_loss ASC
LIMIT 15;

-- Q8. Average days-to-ship by ship mode and region
SELECT
    ship_mode,
    region,
    ROUND(AVG(days_to_ship), 1) AS avg_days_to_ship,
    COUNT(*)                    AS num_orders
FROM orders
GROUP BY ship_mode, region
ORDER BY ship_mode, avg_days_to_ship;

-- Q9. Customer segment profitability comparison
SELECT
    c.customer_segment,
    COUNT(DISTINCT o.customer_id)   AS num_customers,
    ROUND(SUM(o.sales), 0)          AS total_revenue,
    ROUND(SUM(o.profit), 0)         AS total_profit,
    ROUND(SUM(o.profit) * 100.0 / SUM(o.sales), 2) AS profit_margin_pct,
    ROUND(SUM(o.sales) * 1.0 / COUNT(DISTINCT o.customer_id), 0) AS revenue_per_customer
FROM orders o
JOIN customers c ON c.customer_id = o.customer_id
GROUP BY c.customer_segment
ORDER BY total_profit DESC;

-- Q10. Running total of yearly revenue (window function running SUM)
WITH yearly AS (
    SELECT order_year, SUM(sales) AS revenue
    FROM orders
    GROUP BY order_year
)
SELECT
    order_year,
    ROUND(revenue, 0) AS revenue,
    ROUND(SUM(revenue) OVER (ORDER BY order_year), 0) AS running_total_revenue
FROM yearly
ORDER BY order_year;
