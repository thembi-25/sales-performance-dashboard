-- =============================================================
-- Sales Performance Dashboard — SQL Analysis Queries
-- Author: Ernestina Thembi Zah
-- Dataset: cleaned_sales_data (1,850 orders, Jan 2023 - Dec 2024)
-- =============================================================

-- Q1: Which regions generated the highest revenue?
SELECT region,
       COUNT(order_id)            AS total_orders,
       ROUND(SUM(revenue), 2)      AS total_revenue,
       ROUND(AVG(revenue), 2)      AS avg_order_value
FROM sales
GROUP BY region
ORDER BY total_revenue DESC;

-- Q2: Top performing product categories by revenue
SELECT category,
       COUNT(order_id)            AS total_orders,
       ROUND(SUM(revenue), 2)      AS total_revenue,
       ROUND(SUM(revenue) * 100.0 / (SELECT SUM(revenue) FROM sales), 1) AS pct_of_total_revenue
FROM sales
GROUP BY category
ORDER BY total_revenue DESC;

-- Q3: Monthly revenue trend (seasonality check)
SELECT order_month,
       ROUND(SUM(revenue), 2) AS monthly_revenue,
       COUNT(order_id)        AS order_count
FROM sales
GROUP BY order_month
ORDER BY order_month;

-- Q4: Average order value by region and channel
SELECT region, channel,
       ROUND(AVG(revenue), 2) AS avg_order_value,
       COUNT(order_id)        AS order_count
FROM sales
GROUP BY region, channel
ORDER BY region, avg_order_value DESC;

-- Q5: Sales channel performance comparison
SELECT channel,
       COUNT(order_id)            AS total_orders,
       ROUND(SUM(revenue), 2)      AS total_revenue,
       ROUND(AVG(revenue), 2)      AS avg_order_value
FROM sales
GROUP BY channel
ORDER BY total_revenue DESC;

-- Q6: Customer segmentation - repeat vs one-time buyers
SELECT
    CASE WHEN order_count = 1 THEN 'One-time buyer' ELSE 'Repeat buyer' END AS buyer_type,
    COUNT(*) AS customer_count,
    ROUND(SUM(customer_revenue), 2) AS total_revenue,
    ROUND(AVG(customer_revenue), 2) AS avg_revenue_per_customer
FROM (
    SELECT customer_id,
           COUNT(order_id) AS order_count,
           SUM(revenue) AS customer_revenue
    FROM sales
    GROUP BY customer_id
) customer_summary
GROUP BY buyer_type;

-- Q7: Quarter-over-quarter revenue growth
SELECT order_quarter,
       ROUND(SUM(revenue), 2) AS quarterly_revenue,
       COUNT(order_id) AS order_count
FROM sales
GROUP BY order_quarter
ORDER BY order_quarter;

-- Q8: Top 5 highest-value single orders (data quality check)
SELECT order_id, order_date, region, category, unit_price, quantity, revenue
FROM sales
ORDER BY revenue DESC
LIMIT 5;
