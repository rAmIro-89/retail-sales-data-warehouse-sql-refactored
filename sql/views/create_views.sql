-- Analytical Views for Business Intelligence
-- Data Warehouse View Definitions

-- ============================================================
-- Sales Summary View
-- ============================================================
CREATE OR REPLACE VIEW view_sales_summary AS
SELECT 
    d.year,
    d.quarter,
    d.month_name,
    p.category,
    p.subcategory,
    c.customer_segment,
    s.store_name,
    s.store_type,
    COUNT(f.sale_id) as transaction_count,
    SUM(f.quantity) as total_units_sold,
    SUM(f.total_amount) as total_revenue,
    SUM(f.discount_amount) as total_discounts,
    SUM(f.net_amount) as net_revenue,
    SUM(f.profit) as total_profit,
    AVG(f.profit_margin) as avg_profit_margin,
    AVG(f.total_amount) as avg_transaction_value
FROM fact_sales f
INNER JOIN dim_date d ON f.date_key = d.date_key
INNER JOIN dim_product p ON f.product_key = p.product_key
INNER JOIN dim_customer c ON f.customer_key = c.customer_key
INNER JOIN dim_store s ON f.store_key = s.store_key
GROUP BY 
    d.year, d.quarter, d.month_name,
    p.category, p.subcategory,
    c.customer_segment,
    s.store_name, s.store_type;

-- ============================================================
-- Monthly Sales Trend View
-- ============================================================
CREATE OR REPLACE VIEW view_monthly_sales_trend AS
SELECT 
    d.year,
    d.month_number,
    d.month_name,
    COUNT(f.sale_id) as transactions,
    SUM(f.total_amount) as revenue,
    SUM(f.profit) as profit,
    AVG(f.total_amount) as avg_order_value,
    LAG(SUM(f.total_amount)) OVER (ORDER BY d.year, d.month_number) as prev_month_revenue,
    (SUM(f.total_amount) - LAG(SUM(f.total_amount)) OVER (ORDER BY d.year, d.month_number)) / 
        NULLIF(LAG(SUM(f.total_amount)) OVER (ORDER BY d.year, d.month_number), 0) * 100 as mom_growth_pct
FROM fact_sales f
INNER JOIN dim_date d ON f.date_key = d.date_key
GROUP BY d.year, d.month_number, d.month_name
ORDER BY d.year, d.month_number;

-- ============================================================
-- Product Performance View
-- ============================================================
CREATE OR REPLACE VIEW view_product_performance AS
SELECT 
    p.product_key,
    p.product_name,
    p.category,
    p.brand,
    COUNT(f.sale_id) as times_sold,
    SUM(f.quantity) as total_units,
    SUM(f.total_amount) as total_revenue,
    SUM(f.profit) as total_profit,
    AVG(f.profit_margin) as avg_margin,
    RANK() OVER (PARTITION BY p.category ORDER BY SUM(f.total_amount) DESC) as category_rank
FROM fact_sales f
INNER JOIN dim_product p ON f.product_key = p.product_key
WHERE p.is_current = TRUE
GROUP BY p.product_key, p.product_name, p.category, p.brand
ORDER BY total_revenue DESC;

-- ============================================================
-- Customer Segmentation View (RFM Analysis)
-- ============================================================
CREATE OR REPLACE VIEW view_customer_rfm AS
WITH customer_metrics AS (
    SELECT 
        c.customer_key,
        c.customer_name,
        c.customer_segment,
        MAX(d.date) as last_purchase_date,
        CURRENT_DATE - MAX(d.date) as recency_days,
        COUNT(DISTINCT f.sale_id) as frequency,
        SUM(f.total_amount) as monetary
    FROM fact_sales f
    INNER JOIN dim_customer c ON f.customer_key = c.customer_key
    INNER JOIN dim_date d ON f.date_key = d.date_key
    WHERE c.is_current = TRUE
    GROUP BY c.customer_key, c.customer_name, c.customer_segment
),
rfm_scores AS (
    SELECT 
        *,
        NTILE(5) OVER (ORDER BY recency_days) as recency_score,
        NTILE(5) OVER (ORDER BY frequency DESC) as frequency_score,
        NTILE(5) OVER (ORDER BY monetary DESC) as monetary_score
    FROM customer_metrics
)
SELECT 
    *,
    recency_score + frequency_score + monetary_score as rfm_total,
    CASE 
        WHEN recency_score >= 4 AND frequency_score >= 4 AND monetary_score >= 4 THEN 'Champions'
        WHEN recency_score >= 3 AND frequency_score >= 3 THEN 'Loyal Customers'
        WHEN recency_score >= 4 AND frequency_score <= 2 THEN 'New Customers'
        WHEN recency_score <= 2 AND frequency_score >= 3 THEN 'At Risk'
        WHEN recency_score <= 2 AND frequency_score <= 2 THEN 'Lost'
        ELSE 'Regular'
    END as customer_category
FROM rfm_scores;

-- ============================================================
-- Store Performance View
-- ============================================================
CREATE OR REPLACE VIEW view_store_performance AS
SELECT 
    s.store_key,
    s.store_name,
    s.store_type,
    s.city,
    s.state,
    s.region,
    COUNT(f.sale_id) as transaction_count,
    SUM(f.total_amount) as total_revenue,
    SUM(f.profit) as total_profit,
    AVG(f.profit_margin) as avg_margin,
    COUNT(DISTINCT f.customer_key) as unique_customers,
    SUM(f.total_amount) / NULLIF(COUNT(DISTINCT f.customer_key), 0) as revenue_per_customer
FROM fact_sales f
INNER JOIN dim_store s ON f.store_key = s.store_key
WHERE s.is_active = TRUE
GROUP BY s.store_key, s.store_name, s.store_type, s.city, s.state, s.region
ORDER BY total_revenue DESC;

-- ============================================================
-- Daily Sales Dashboard View
-- ============================================================
CREATE OR REPLACE VIEW view_daily_dashboard AS
SELECT 
    d.date,
    d.day_of_week,
    d.is_weekend,
    COUNT(f.sale_id) as transactions,
    SUM(f.quantity) as units_sold,
    SUM(f.total_amount) as revenue,
    SUM(f.profit) as profit,
    AVG(f.total_amount) as avg_order_value,
    COUNT(DISTINCT f.customer_key) as unique_customers,
    COUNT(DISTINCT f.product_key) as unique_products
FROM fact_sales f
INNER JOIN dim_date d ON f.date_key = d.date_key
GROUP BY d.date, d.day_of_week, d.is_weekend
ORDER BY d.date DESC;

-- ============================================================
-- Grant Access to Views (adjust roles as needed)
-- ============================================================
-- GRANT SELECT ON view_sales_summary TO reporting_role;
-- GRANT SELECT ON view_monthly_sales_trend TO reporting_role;
-- GRANT SELECT ON view_product_performance TO reporting_role;
-- GRANT SELECT ON view_customer_rfm TO reporting_role;
-- GRANT SELECT ON view_store_performance TO reporting_role;
-- GRANT SELECT ON view_daily_dashboard TO reporting_role;
