-- Create Dimension Tables
-- Data Warehouse DDL Script

-- ============================================================
-- Date Dimension
-- ============================================================
CREATE TABLE dim_date (
    date_key INT PRIMARY KEY,
    date DATE NOT NULL,
    day_of_week VARCHAR(10),
    day_of_month INT,
    day_of_year INT,
    week_of_year INT,
    month_number INT,
    month_name VARCHAR(20),
    quarter INT,
    year INT,
    is_weekend BOOLEAN,
    is_holiday BOOLEAN,
    fiscal_year INT,
    fiscal_quarter INT
);

-- ============================================================
-- Product Dimension
-- ============================================================
CREATE TABLE dim_product (
    product_key INT PRIMARY KEY,
    product_id VARCHAR(50),
    product_name VARCHAR(200) NOT NULL,
    category VARCHAR(100),
    subcategory VARCHAR(100),
    brand VARCHAR(100),
    supplier VARCHAR(200),
    unit_cost DECIMAL(10,2),
    unit_price DECIMAL(10,2),
    valid_from DATE NOT NULL,
    valid_to DATE,
    is_current BOOLEAN DEFAULT TRUE,
    version INT DEFAULT 1
);

-- ============================================================
-- Customer Dimension
-- ============================================================
CREATE TABLE dim_customer (
    customer_key INT PRIMARY KEY,
    customer_id VARCHAR(50),
    customer_name VARCHAR(200) NOT NULL,
    customer_segment VARCHAR(50),
    email VARCHAR(200),
    phone VARCHAR(50),
    city VARCHAR(100),
    state VARCHAR(100),
    country VARCHAR(100),
    postal_code VARCHAR(20),
    valid_from DATE NOT NULL,
    valid_to DATE,
    is_current BOOLEAN DEFAULT TRUE,
    version INT DEFAULT 1
);

-- ============================================================
-- Store Dimension
-- ============================================================
CREATE TABLE dim_store (
    store_key INT PRIMARY KEY,
    store_id VARCHAR(50),
    store_name VARCHAR(200) NOT NULL,
    store_type VARCHAR(50),
    manager_name VARCHAR(200),
    city VARCHAR(100),
    state VARCHAR(100),
    country VARCHAR(100),
    region VARCHAR(100),
    open_date DATE,
    square_footage INT,
    is_active BOOLEAN DEFAULT TRUE
);

-- ============================================================
-- Unknown Records (for referential integrity)
-- ============================================================
INSERT INTO dim_date (date_key, date, day_of_week, month_name, year)
VALUES (-1, '1900-01-01', 'Unknown', 'Unknown', 1900);

INSERT INTO dim_product (product_key, product_id, product_name, category, valid_from)
VALUES (-1, 'UNK', 'Unknown Product', 'Unknown', '1900-01-01');

INSERT INTO dim_customer (customer_key, customer_id, customer_name, customer_segment, valid_from)
VALUES (-1, 'UNK', 'Unknown Customer', 'Unknown', '1900-01-01');

INSERT INTO dim_store (store_key, store_id, store_name, store_type, open_date)
VALUES (-1, 'UNK', 'Unknown Store', 'Unknown', '1900-01-01');

-- ============================================================
-- Indexes for Performance
-- ============================================================
CREATE INDEX idx_dim_product_name ON dim_product(product_name);
CREATE INDEX idx_dim_product_category ON dim_product(category);
CREATE INDEX idx_dim_customer_name ON dim_customer(customer_name);
CREATE INDEX idx_dim_customer_segment ON dim_customer(customer_segment);
CREATE INDEX idx_dim_date_year_month ON dim_date(year, month_number);
