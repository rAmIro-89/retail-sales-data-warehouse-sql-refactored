# 📊 Retail Sales Data Warehouse - SQL & Python

[![SQL Server](https://img.shields.io/badge/SQL%20Server-2016%2B-CC2927.svg)](https://www.microsoft.com/sql-server/)
[![Python](https://img.shields.io/badge/python-3.8%2B-blue.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

Production-ready Data Warehouse implementation with star schema, SCD Type 2, ETL pipelines, and advanced business analytics. Designed for Canadian retail market analysis with multi-currency support.

## Business Problem

**Objective:** Build an enterprise-grade Business Intelligence system that transforms transactional retail sales data into actionable insights for strategic decision-making.

**Real-World Applications:**
- **Retail Analytics:** Track sales performance across stores, products, and sales representatives
- **Customer Segmentation:** RFM (Recency, Frequency, Monetary) analysis to identify high-value customers
- **Inventory Optimization:** ABC/Pareto analysis to focus on top 20% products driving 80% revenue
- **Sales Performance:** Automated categorization of sales representatives (Top/Medium/Low performers)
- **Multi-Market Support:** Handle multi-currency transactions (ARS, USD, EUR, BRL, CNY) with historical exchange rates
- **Trend Analysis:** Year-over-Year (YoY), Month-over-Month (MoM), moving averages, and seasonality detection

**Target Audience:**
- Retail companies needing data-driven decision support
- Business analysts requiring self-service BI tools
- Data engineers building scalable data warehouses
- Canadian market with English documentation standards

**Technical Challenge:** Implement a complete BI solution with normalized OLTP source system, dimensional data warehouse with Slowly Changing Dimensions (SCD Type 2), incremental ETL processes, data quality validation, and cross-platform analytics (SQL + Python).

## Architecture

```
OLTP_Celulares (Normalized 3NF)
     ↓ ETL Pipeline
DW_Celulares (Star Schema)
     ↓ Business Analytics
SQL Queries + Python Notebooks + Power BI
```

### Dimensional Model (Star Schema)

**Dimensions:**
- `DimFecha` (Date) - Complete calendar 2020-2030 with fiscal attributes
- `DimCliente` (Customer) - Customer demographics
- `DimProducto` (Product) - Mobile phone brands and models
- `DimLocal` (Store) - Store locations (province, city)
- `DimVendedor` (Salesperson) - **SCD Type 2** with automated monthly performance categorization
- `DimFormaPago` (Payment Method) - Payment types
- `DimCanal` (Channel) - Junk dimension (Online/In-Store)
- `DimMoneda` (Currency) - Supported currencies (ARS, USD, EUR, BRL, CNY ¥)
- `DimExchangeRate` - Monthly exchange rates

**Facts:**
- `FactVentas` (Sales) - Grain: 1 row per sale with metrics: `quantity`, `amount`, `margin`, `margin_percentage`, `exchange_rate`

## Key Features

### 1. Star Schema Implementation
- **7 Dimensions + 1 Fact Table** optimized for query performance
- **Surrogate Keys** (`sk_*`) for independence from source systems
- **Unknown Records** (SK=-1) for referential integrity
- **Slowly Changing Dimensions Type 2:** Historical tracking of salesperson performance

### 2. ETL Pipeline
- **Initial Load:** Full dimension and fact population from OLTP
- **Incremental Load:** Daily processing of new transactions
- **SCD Type 2 Automation:** Automatic versioning when performance changes
- **Data Quality:** Built-in validation for integrity

### 3. Multi-Currency Support
- **5 Currencies:** ARS (base), USD, EUR, BRL, CNY (Yuan ¥)
- **Historical Exchange Rates:** Monthly rates in `DimExchangeRate`
- **Automatic Conversion:** All queries return amounts in all 5 currencies
- **Correct Aggregation:** CTE pattern prevents row multiplication

### 4. Advanced Analytics
- **Temporal Analysis:** YoY, MoM, moving averages, running totals
- **ABC/Pareto:** 80/20 product segmentation
- **RFM Segmentation:** Customer classification (Champions, Loyal, At Risk, Lost)
- **Performance Tracking:** Automated salesperson categorization

### 5. Cross-Platform Validation
- **SQL Server** for production reporting
- **Python/Pandas** for data science workflows
- **100% Validation:** Automated comparison between SQL and Python results

## Project Structure

```
retail-sales-data-warehouse-sql/
├── sql/
│   ├── ddl/                      # Database and table creation
│   │   ├── 00_creacion_bases.sql
│   │   ├── 01_ddl_oltp.sql
│   │   └── 03_ddl_dw.sql
│   ├── dml/                      # Data loading
│   │   └── 02_carga_oltp.sql
│   └── views/                    # Analytical queries
│       ├── 01_marca_mas_vendida.sql
│       ├── 08_analisis_temporal.sql
│       ├── 09_analisis_abc_pareto.sql
│       └── 10_analisis_rfm.sql
├── src/
│   ├── etl/                      # ETL scripts
│   │   ├── 04_etl_dw_inicial.sql
│   │   ├── 05_reproceso_diario.sql
│   │   ├── extract.py
│   │   ├── transform.py
│   │   └── load.py
│   └── utils/                    # Helper scripts
│       └── db_connection.py
├── notebooks/
│   ├── Notebook_Estadistica_Ventas.ipynb
│   ├── 01_exploratory_analysis.ipynb
│   └── 02_reporting_kpis.ipynb
├── data/
│   ├── raw/                      # Source data
│   └── processed/                # Analytical datasets
│       └── DW_Dataset_Aplanado.xlsx
├── docs/
│   ├── architecture.md
│   ├── star_schema.png
│   └── Presentacion_Proyecto_DW_Celulares.pptx
└── requirements.txt
```

## How to Run

### Initial Setup

Execute scripts in SQL Server Management Studio (SSMS) in this order:

```sql
-- 1. Create databases
sql/ddl/00_creacion_bases.sql

-- 2. Create OLTP structure
sql/ddl/01_ddl_oltp.sql

-- 3. Load sample data
sql/dml/02_carga_oltp.sql

-- 4. Create DW structure
sql/ddl/03_ddl_dw.sql

-- 5. Run initial ETL
src/etl/04_etl_dw_inicial.sql
```

### Incremental ETL

Simulate daily processing:

```sql
-- 1. Add new sales to OLTP
src/utils/ALTAS_SIMPLES.sql

-- 2. Run incremental ETL
src/etl/05_reproceso_diario.sql
```

### Python Analysis

```bash
# Install dependencies
pip install -r requirements.txt

# Run Jupyter notebook
jupyter notebook notebooks/Notebook_Estadistica_Ventas.ipynb
```

## Available Analytics

### Basic Queries (Multi-Currency)
- Top-selling brand by units and revenue (5 currencies)
- Best-performing salesperson
- Most profitable store
- Most used payment method
- Quarterly sales analysis

### Advanced Analytics

**Temporal Analysis (`08_analisis_temporal.sql`):**
- Year-over-Year (YoY) growth
- Month-over-Month (MoM) trends
- 3-month moving averages
- Running totals
- Day-of-week seasonality

**ABC/Pareto Analysis (`09_analisis_abc_pareto.sql`):**
- Product classification (A: 80% revenue, B: 15%, C: 5%)
- Customer segmentation (VIP, Regular, Occasional)
- Salesperson ranking

**RFM Segmentation (`10_analisis_rfm.sql`):**
- Customer classification into 10 segments
- Champions, Loyal, At Risk, Lost, etc.
- Action recommendations per segment

## Python Notebook Features

`Notebook_Estadistica_Ventas.ipynb` includes:

- **Direct SQL Server Connection:** SQLAlchemy with auto-reconnection
- **Star Schema in Pandas:** Build dimensional model in-memory
- **Temporal Visualizations:** Salesperson performance trends by category
- **Statistical Analysis:** Distribution histograms with KDE curves
- **Multi-Currency Validation:** 5 queries compared SQL vs Pandas
- **Unicode Support:** Correct ¥, €, R$ symbols in all charts
- **Automated Validation Table:** ✅/❌ comparison by currency and query

**Requirements:**
```bash
pandas>=1.5.0
numpy>=1.24.0
sqlalchemy>=2.0.0
pyodbc>=4.0.0
matplotlib>=3.5.0
seaborn>=0.12.0
scipy>=1.10.0
```

## Data Quality Validation

Script: `07_validacion/06_validacion_calidad.sql`

Validates:
- ✅ Referential integrity (no orphaned FKs except Unknown)
- ✅ Unique primary keys
- ✅ No duplicate business keys in SCD2
- ✅ Consistent metrics (margin = quantity × (price - cost))
- ✅ Valid SCD2 dates (end_date > start_date)
- ✅ No nulls in critical columns

## Implemented Concepts

### Data Warehousing
- **Kimball Dimensional Modeling:** Star schema with 7 dimensions
- **Slowly Changing Dimensions Type 2:** Historical versioning with start/end dates
- **Junk Dimension:** Low-cardinality attributes (channel)
- **Unknown Pattern:** SK=-1 for late-arriving dimensions
- **Surrogate Keys:** Artificial keys independent of source systems

### ETL
- **Initial Load:** Full historical data migration
- **Incremental Load:** Daily delta processing
- **SCD Type 2 Automation:** Automatic row versioning on changes
- **Data Quality Checks:** Validation at each ETL stage

### Advanced SQL
- **Window Functions:** RANK, ROW_NUMBER, LAG, LEAD, SUM OVER
- **CTEs:** Complex multi-currency aggregations
- **PERCENTILE_CONT:** Customer segmentation
- **DATEPART/DATEADD:** Temporal analysis

### Business Intelligence
- **KPIs:** Revenue, margin, units sold, customer count
- **Segmentation:** ABC/Pareto, RFM
- **Performance Tracking:** Automated salesperson categorization
- **Multi-Currency Reporting:** Historical exchange rates

## Technologies Used

- **SQL Server 2016+** (Azure SQL, SQL Server 2019/2022 compatible)
- **Transact-SQL (T-SQL)** for ETL and queries
- **Python 3.8+** with Pandas, Matplotlib, Seaborn, Scipy
- **Jupyter Notebooks** for interactive analysis
- **SQLAlchemy** for Python-SQL integration
- **VS Code / SSMS / Azure Data Studio** as development tools

## Troubleshooting

### Yuan symbol (¥) not displaying in SSMS

**Solution:**
1. Go to `Tools > Options > Environment > Fonts and Colors`
2. Change font to **Consolas** or **Courier New**
3. Restart SSMS

The symbol always displays correctly in Python notebooks (UTF-8 native).

### "Database already exists" error

```sql
-- Full reset (OLTP + DW)
sql/ddl/00_reset_databases.sql

-- DW only reset (keeps OLTP)
sql/ddl/00_reset_dw.sql
```

### Salespeople show as 'Inicial' category

**Cause:** Initial ETL assigns `categoria='Inicial'`. Actual categorization happens in daily processing.

**Solution:**
```sql
src/etl/05_reproceso_diario.sql
```

## License

MIT License - See LICENSE file for details.

**Author:** Ramiro Ottone Villar  
**Portfolio Project:** Canadian Tech Market  
**Version:** 2.1  
**Status:** Production-ready with multi-currency support and full validation
