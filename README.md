📊 Retail Sales Data Warehouse — SQL & Python

Enterprise-grade Data Warehouse built with SQL Server, Python, and dimensional modeling (Kimball). Includes OLTP modeling, ETL pipelines, SCD Type 2, multi-currency support, and analytical SQL/Python workflows.

🔷 1. Business Context

This project simulates the analytical backbone of a retail cellphone company.

✔ Strategic Objectives

Sales performance analysis across stores, brands, models, channels

RFM segmentation & customer lifecycle insights

ABC/Pareto analysis for product profitability

Seller performance tracking (Top / Medium / Low)

Multi-currency reporting: ARS, USD, EUR, BRL, CNY

BI-ready datasets for Power BI & Python

This architecture is representative of a real Canadian retail BI system.

🔷 2. Architecture Overview

OLTP (Normalized 3NF)
      ↓ ETL
Data Warehouse (Star Schema)
      ↓
SQL Analytics + Python + Power BI

🔷 3. OLTP Model — Transactional Layer

Operational data model used as the source system for the DW.

✔ 9 normalized tables
✔ Referential integrity enforced
✔ Real-time operations
✔ Source for ETL extraction

🖼 ERD

🔷 4. Star Schema — Analytical Data Warehouse

Dimensional model optimized for BI, KPIs, aggregations and advanced analysis.

Dimensions

Date, Customer, Product, Store

Channel, Currency, Payment Method

Seller (SCD Type 2)

Fact Table

FactSales (quantities, revenue, margins, multi-currency metrics)

🖼 ERD

🔷 5. ETL Pipeline & Dimensions

Daily automated ETL ensuring fresh, consistent analytical data.

Pipeline

Extract from OLTP

Transform (business rules, currency conversion)

SCD Type 2 for sellers

Load DW tables (facts & dimensions)

Key Dimensions

DimDate: 10-year temporal attributes

DimChannel: Web / Store / Online

DimCurrency: ARS, USD, EUR, BRL, CNY

🖼 Diagram

🔷 6. Advanced Analytics

Implemented in SQL and Python.

✔ Temporal Analytics

YoY / MoM

Moving averages

Running totals

✔ Segmentation

ABC / Pareto

RFM (Champions, Loyal, At Risk, Lost)

✔ Performance

Best seller

Best store

Top brand/model

✔ Multi-Currency

Correct conversion

Historical exchange rates

Aggregation-safe metrics

🔷 7. Project Structure

├── sql/
│   ├── ddl/
│   ├── dml/
│   └── views/
├── src/
│   ├── etl/
│   └── utils/
├── notebooks/
├── data/
└── docs/

🔷 8. How to Run
SQL Server Setup

1. sql/ddl/00_creacion_bases.sql
2. sql/ddl/01_ddl_oltp.sql
3. sql/dml/02_carga_oltp.sql
4. sql/ddl/03_ddl_dw.sql
5. src/etl/04_etl_dw_inicial.sql

Incremental ETL
src/etl/05_reproceso_diario.sql

Python
pip install -r requirements.txt
jupyter notebook notebooks/Notebook_Estadistica_Ventas.ipynb

🔷 9. Technologies

SQL Server

Python (Pandas, SQLAlchemy, Matplotlib)

T-SQL

Power BI

Jupyter Notebooks

VS Code / SSMS

🔷 10. Author

Ramiro Ottone Villar
MIT License




