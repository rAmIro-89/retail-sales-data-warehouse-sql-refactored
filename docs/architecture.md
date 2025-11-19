# Retail Sales Data Warehouse - Architecture Documentation

## Overview

This document describes the architecture and design of the Retail Sales Data Warehouse system.

## Architecture Components

### 1. Data Sources

The data warehouse integrates data from multiple sources:

- **OLTP Database**: Transactional data from the operational retail system
- **CSV Files**: Historical sales data, product catalogs, customer information
- **External APIs**: Third-party data sources (payment providers, shipping services)
- **Web Analytics**: Customer behavior tracking data

### 2. ETL Pipeline

The Extract, Transform, Load (ETL) pipeline is implemented using Python and consists of three main modules:

#### Extract (`src/etl/extract.py`)
- Connects to multiple data sources
- Reads raw data from databases, CSV files, and APIs
- Performs initial data validation
- Handles connection errors and retries

#### Transform (`src/etl/transform.py`)
- Data cleaning and standardization
- Business rule application
- Data quality checks
- Dimension and fact table preparation
- Surrogate key generation

#### Load (`src/etl/load.py`)
- Loads transformed data into the data warehouse
- Implements Slowly Changing Dimension (SCD) strategies
- Handles incremental updates
- Maintains data lineage and audit trails

### 3. Data Warehouse Design

#### Star Schema Model

The data warehouse follows a star schema design pattern for optimal query performance:

```
                    ┌─────────────────┐
                    │   dim_date      │
                    ├─────────────────┤
                    │ date_key (PK)   │
                    │ date            │
                    │ day_of_week     │
                    │ month           │
                    │ quarter         │
                    │ year            │
                    └─────────────────┘
                            │
                            │
    ┌───────────────┐      │      ┌───────────────┐
    │  dim_product  │      │      │  dim_customer │
    ├───────────────┤      │      ├───────────────┤
    │ product_key   │      │      │ customer_key  │
    │ product_name  │      │      │ customer_name │
    │ category      │──────┼──────│ segment       │
    │ brand         │      │      │ location      │
    │ price         │      │      │ join_date     │
    └───────────────┘      │      └───────────────┘
                           │
                    ┌──────▼──────┐
                    │ fact_sales  │
                    ├─────────────┤
                    │ sale_id     │
                    │ date_key FK │
                    │ product_key │
                    │ customer_key│
                    │ store_key   │
                    │ quantity    │
                    │ unit_price  │
                    │ total_amount│
                    │ discount    │
                    └─────────────┘
                           │
                    ┌──────▼──────┐
                    │  dim_store  │
                    ├─────────────┤
                    │ store_key   │
                    │ store_name  │
                    │ store_type  │
                    │ location    │
                    │ manager     │
                    └─────────────┘
```

#### Dimension Tables

**dim_date**
- Complete date dimension with calendar attributes
- Supports time-based analysis and trending
- Includes fiscal calendar if needed

**dim_product**
- Product master data
- Hierarchical structure (Category → Subcategory → Product)
- SCD Type 2 for price history

**dim_customer**
- Customer demographic and behavioral attributes
- Segmentation information
- SCD Type 2 for tracking customer changes

**dim_store**
- Store/location information
- Store type and characteristics
- Geographic hierarchy

#### Fact Table

**fact_sales**
- Grain: One row per sales transaction line item
- Measures: quantity, unit_price, total_amount, discount
- Foreign keys to all dimension tables
- Additive measures for aggregation

### 4. Data Storage

#### PostgreSQL Database
- Primary data warehouse storage
- Optimized with indexes and partitioning
- Regular vacuum and analyze operations
- Backup and recovery procedures

#### File Storage
- Raw data stored in `data/raw/`
- Processed data stored in `data/processed/`
- Archived data for audit trails

### 5. Analytics Layer

#### SQL Views (`sql/views/`)
- Pre-aggregated views for common queries
- Business-specific calculations
- Performance optimization through materialized views

#### Reporting Layer
- Jupyter notebooks for ad-hoc analysis
- Automated KPI reports
- Dashboard integration capabilities

## Data Flow

```
┌──────────────┐    ┌──────────────┐    ┌──────────────┐    ┌──────────────┐
│ Data Sources │───▶│   Extract    │───▶│  Transform   │───▶│     Load     │
└──────────────┘    └──────────────┘    └──────────────┘    └──────────────┘
                                                                      │
                                                                      ▼
                    ┌──────────────┐    ┌──────────────┐    ┌──────────────┐
                    │  Reporting   │◀───│     Views    │◀───│ Data Warehouse│
                    └──────────────┘    └──────────────┘    └──────────────┘
```

## Technology Stack

- **Programming Language**: Python 3.8+
- **Database**: PostgreSQL 12+
- **ETL Framework**: Custom Python scripts with SQLAlchemy
- **Data Processing**: Pandas, NumPy
- **Visualization**: Matplotlib, Seaborn
- **Analytics**: Jupyter Notebooks
- **Version Control**: Git

## Performance Considerations

### Indexing Strategy
- Primary keys on all dimension tables
- Foreign keys in fact table
- Composite indexes on frequently queried columns
- Date-based partitioning on fact tables

### Query Optimization
- Materialized views for complex aggregations
- Query result caching
- Statistics collection and maintenance

### Data Volume Management
- Incremental loading strategy
- Archival of historical data
- Partitioning by date for fact tables

## Security

### Access Control
- Role-based access control (RBAC)
- Separate read-only user for reporting
- ETL service account with limited permissions

### Data Privacy
- PII data masking for non-production environments
- Encryption at rest and in transit
- Audit logging for sensitive data access

## Monitoring and Maintenance

### ETL Monitoring
- Job execution logs
- Data quality checks
- Error notification system
- Performance metrics

### Database Maintenance
- Regular backups (daily incremental, weekly full)
- Index maintenance
- Statistics updates
- Disk space monitoring

## Disaster Recovery

### Backup Strategy
- Automated daily backups
- Off-site backup storage
- Point-in-time recovery capability
- Recovery Time Objective (RTO): 4 hours
- Recovery Point Objective (RPO): 24 hours

### Testing
- Quarterly DR drills
- Backup restoration testing
- Failover procedure documentation

## Future Enhancements

1. **Real-time Data Integration**: Implement streaming ETL for near real-time analytics
2. **Machine Learning Integration**: Predictive analytics and forecasting models
3. **Cloud Migration**: Evaluate cloud-based data warehouse solutions
4. **Advanced Analytics**: Implement OLAP cube for multi-dimensional analysis
5. **Self-Service BI**: Integrate with BI tools (Power BI, Tableau)

## References

- [Star Schema Design](https://en.wikipedia.org/wiki/Star_schema)
- [Kimball Dimensional Modeling](https://www.kimballgroup.com)
- [SQLAlchemy Documentation](https://www.sqlalchemy.org)
- [PostgreSQL Performance Tuning](https://www.postgresql.org/docs/current/performance-tips.html)

## Change Log

| Date | Version | Changes | Author |
|------|---------|---------|--------|
| 2025-11-19 | 1.0 | Initial architecture documentation | Data Engineering Team |

---

**Document Owner**: Data Engineering Team  
**Last Updated**: November 19, 2025  
**Review Cycle**: Quarterly
