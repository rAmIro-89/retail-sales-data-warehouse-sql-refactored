-- Create Fact Tables
-- Data Warehouse DDL Script

-- ============================================================
-- Sales Fact Table
-- ============================================================
CREATE TABLE fact_sales (
    sale_id BIGINT PRIMARY KEY,
    date_key INT NOT NULL,
    product_key INT NOT NULL,
    customer_key INT NOT NULL,
    store_key INT NOT NULL,
    quantity INT NOT NULL,
    unit_price DECIMAL(10,2) NOT NULL,
    unit_cost DECIMAL(10,2) NOT NULL,
    total_amount DECIMAL(12,2) NOT NULL,
    discount_amount DECIMAL(10,2) DEFAULT 0,
    net_amount DECIMAL(12,2) NOT NULL,
    profit DECIMAL(12,2),
    profit_margin DECIMAL(5,2),
    created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    -- Foreign Keys
    CONSTRAINT fk_fact_date FOREIGN KEY (date_key) REFERENCES dim_date(date_key),
    CONSTRAINT fk_fact_product FOREIGN KEY (product_key) REFERENCES dim_product(product_key),
    CONSTRAINT fk_fact_customer FOREIGN KEY (customer_key) REFERENCES dim_customer(customer_key),
    CONSTRAINT fk_fact_store FOREIGN KEY (store_key) REFERENCES dim_store(store_key),
    
    -- Check Constraints
    CONSTRAINT chk_quantity CHECK (quantity > 0),
    CONSTRAINT chk_amount CHECK (total_amount >= 0)
);

-- ============================================================
-- Indexes for Fact Table Performance
-- ============================================================
CREATE INDEX idx_fact_sales_date ON fact_sales(date_key);
CREATE INDEX idx_fact_sales_product ON fact_sales(product_key);
CREATE INDEX idx_fact_sales_customer ON fact_sales(customer_key);
CREATE INDEX idx_fact_sales_store ON fact_sales(store_key);
CREATE INDEX idx_fact_sales_composite ON fact_sales(date_key, product_key, customer_key);

-- ============================================================
-- Partitioning (Optional - for large datasets)
-- ============================================================
-- Uncomment and modify based on your database system
-- Example for PostgreSQL:
-- CREATE TABLE fact_sales_2024 PARTITION OF fact_sales
-- FOR VALUES FROM ('2024-01-01') TO ('2025-01-01');

-- ============================================================
-- Comments for Documentation
-- ============================================================
COMMENT ON TABLE fact_sales IS 'Fact table storing sales transactions';
COMMENT ON COLUMN fact_sales.profit IS 'Calculated as (unit_price - unit_cost) * quantity';
COMMENT ON COLUMN fact_sales.profit_margin IS 'Calculated as (profit / total_amount) * 100';
