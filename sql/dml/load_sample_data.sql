-- DML Sample Data Loading Scripts
-- Data Warehouse Data Manipulation

-- ============================================================
-- Load Date Dimension (Sample for 2024)
-- ============================================================
-- This is a simplified example. In production, use a date generation script
-- to populate the entire date range (e.g., 2020-2030)

INSERT INTO dim_date (date_key, date, day_of_week, day_of_month, day_of_year, 
                     week_of_year, month_number, month_name, quarter, year, 
                     is_weekend, is_holiday, fiscal_year, fiscal_quarter)
SELECT
    TO_CHAR(d, 'YYYYMMDD')::INT as date_key,
    d as date,
    TO_CHAR(d, 'Day') as day_of_week,
    EXTRACT(DAY FROM d) as day_of_month,
    EXTRACT(DOY FROM d) as day_of_year,
    EXTRACT(WEEK FROM d) as week_of_year,
    EXTRACT(MONTH FROM d) as month_number,
    TO_CHAR(d, 'Month') as month_name,
    EXTRACT(QUARTER FROM d) as quarter,
    EXTRACT(YEAR FROM d) as year,
    CASE WHEN EXTRACT(DOW FROM d) IN (0, 6) THEN TRUE ELSE FALSE END as is_weekend,
    FALSE as is_holiday,
    EXTRACT(YEAR FROM d) as fiscal_year,
    EXTRACT(QUARTER FROM d) as fiscal_quarter
FROM generate_series('2024-01-01'::date, '2024-12-31'::date, '1 day'::interval) d;

-- ============================================================
-- Load Sample Products
-- ============================================================
INSERT INTO dim_product (product_key, product_id, product_name, category, 
                        subcategory, brand, unit_cost, unit_price, valid_from)
VALUES
    (1, 'PROD001', 'Laptop Pro 15"', 'Electronics', 'Computers', 'TechBrand', 800.00, 1200.00, '2024-01-01'),
    (2, 'PROD002', 'Wireless Mouse', 'Electronics', 'Accessories', 'TechBrand', 15.00, 25.00, '2024-01-01'),
    (3, 'PROD003', 'Office Chair Deluxe', 'Furniture', 'Seating', 'ComfortCo', 120.00, 250.00, '2024-01-01'),
    (4, 'PROD004', 'Desk Lamp LED', 'Furniture', 'Lighting', 'BrightLight', 30.00, 55.00, '2024-01-01'),
    (5, 'PROD005', 'Notebook Set', 'Stationery', 'Writing', 'PaperPlus', 5.00, 12.00, '2024-01-01');

-- ============================================================
-- Load Sample Customers
-- ============================================================
INSERT INTO dim_customer (customer_key, customer_id, customer_name, customer_segment,
                         email, city, state, country, valid_from)
VALUES
    (1, 'CUST001', 'John Smith', 'Premium', 'john.smith@email.com', 'New York', 'NY', 'USA', '2024-01-01'),
    (2, 'CUST002', 'Mary Johnson', 'Standard', 'mary.j@email.com', 'Los Angeles', 'CA', 'USA', '2024-01-01'),
    (3, 'CUST003', 'Robert Brown', 'Premium', 'r.brown@email.com', 'Chicago', 'IL', 'USA', '2024-01-01'),
    (4, 'CUST004', 'Patricia Davis', 'Standard', 'p.davis@email.com', 'Houston', 'TX', 'USA', '2024-01-01'),
    (5, 'CUST005', 'Michael Wilson', 'Basic', 'm.wilson@email.com', 'Phoenix', 'AZ', 'USA', '2024-01-01');

-- ============================================================
-- Load Sample Stores
-- ============================================================
INSERT INTO dim_store (store_key, store_id, store_name, store_type, manager_name,
                      city, state, country, region, open_date, is_active)
VALUES
    (1, 'STORE001', 'Downtown Store', 'Retail', 'Alice Cooper', 'New York', 'NY', 'USA', 'Northeast', '2020-01-01', TRUE),
    (2, 'STORE002', 'Mall Store', 'Retail', 'Bob Martin', 'Los Angeles', 'CA', 'USA', 'West', '2020-06-01', TRUE),
    (3, 'STORE003', 'Online Store', 'E-commerce', 'Carol White', NULL, NULL, 'USA', 'National', '2019-01-01', TRUE),
    (4, 'STORE004', 'Suburban Store', 'Retail', 'David Lee', 'Chicago', 'IL', 'USA', 'Midwest', '2021-03-01', TRUE);

-- ============================================================
-- Load Sample Sales Transactions
-- ============================================================
INSERT INTO fact_sales (sale_id, date_key, product_key, customer_key, store_key,
                       quantity, unit_price, unit_cost, total_amount, discount_amount,
                       net_amount, profit, profit_margin)
VALUES
    (1, 20240115, 1, 1, 1, 2, 1200.00, 800.00, 2400.00, 100.00, 2300.00, 800.00, 33.33),
    (2, 20240115, 2, 2, 1, 5, 25.00, 15.00, 125.00, 0.00, 125.00, 50.00, 40.00),
    (3, 20240116, 3, 3, 2, 1, 250.00, 120.00, 250.00, 25.00, 225.00, 130.00, 52.00),
    (4, 20240116, 4, 4, 2, 3, 55.00, 30.00, 165.00, 0.00, 165.00, 75.00, 45.45),
    (5, 20240117, 5, 5, 3, 10, 12.00, 5.00, 120.00, 10.00, 110.00, 70.00, 58.33);

-- ============================================================
-- Update Statistics
-- ============================================================
ANALYZE dim_date;
ANALYZE dim_product;
ANALYZE dim_customer;
ANALYZE dim_store;
ANALYZE fact_sales;
