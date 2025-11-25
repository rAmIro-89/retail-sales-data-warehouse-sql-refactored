"""
Retail Sales Data Warehouse Example Usage

This script demonstrates the complete workflow:
1. Database setup
2. OLTP data loading
3. Data Warehouse creation
4. ETL execution
5. Analytics queries
"""

def main():
    """Main demonstration function."""
    
    print("=" * 70)
    print("RETAIL SALES DATA WAREHOUSE - SETUP GUIDE")
    print("=" * 70)
    
    print("\n[STEP 1] Database Setup")
    print("-" * 70)
    print("Execute in SQL Server Management Studio (SSMS):")
    print("\n1. Create databases:")
    print("   sql/ddl/00_creacion_bases.sql")
    print("\n2. Create OLTP structure:")
    print("   sql/ddl/01_ddl_oltp.sql")
    print("\n3. Load sample data:")
    print("   sql/dml/02_carga_oltp.sql")
    
    print("\n[STEP 2] Data Warehouse Setup")
    print("-" * 70)
    print("\n4. Create DW structure:")
    print("   sql/ddl/03_ddl_dw.sql")
    print("\n5. Run initial ETL:")
    print("   src/etl/04_etl_dw_inicial.sql")
    
    print("\n[STEP 3] Validate Setup")
    print("-" * 70)
    print("\nRun validation queries:")
    print("   SELECT COUNT(*) FROM DW_Celulares.dbo.FactVentas")
    print("   SELECT COUNT(*) FROM DW_Celulares.dbo.DimVendedor WHERE es_actual = 1")
    print("   SELECT COUNT(*) FROM DW_Celulares.dbo.DimFecha")
    
    print("\n[STEP 4] Analytics Queries")
    print("-" * 70)
    print("\nAvailable analytics:")
    print("  • Top-selling brand:")
    print("    sql/views/01_marca_mas_vendida.sql")
    print("\n  • Temporal analysis (YoY, MoM):")
    print("    sql/views/08_analisis_temporal.sql")
    print("\n  • ABC/Pareto segmentation:")
    print("    sql/views/09_analisis_abc_pareto.sql")
    print("\n  • RFM customer analysis:")
    print("    sql/views/10_analisis_rfm.sql")
    
    print("\n[STEP 5] Python Analysis")
    print("-" * 70)
    print("\nInstall dependencies:")
    print("   pip install -r requirements.txt")
    print("\nRun Jupyter notebook:")
    print("   jupyter notebook notebooks/Notebook_Estadistica_Ventas.ipynb")
    print("\nFeatures:")
    print("  • Direct SQL Server connection with SQLAlchemy")
    print("  • Star schema construction in Pandas")
    print("  • Multi-currency validation (SQL vs Python)")
    print("  • Statistical visualizations")
    print("  • Automated validation table")
    
    print("\n[STEP 6] Incremental ETL")
    print("-" * 70)
    print("\nSimulate daily processing:")
    print("\n1. Add new sales to OLTP:")
    print("   src/utils/ALTAS_SIMPLES.sql")
    print("\n2. Run incremental ETL:")
    print("   src/etl/05_reproceso_diario.sql")
    print("\nThis will:")
    print("  • Detect new sales in OLTP")
    print("  • Insert into FactVentas")
    print("  • Update SCD Type 2 for salespeople")
    print("  • Recategorize performance (Top/Medium/Low)")
    
    print("\n[RESET OPTIONS]")
    print("-" * 70)
    print("\nFull reset (OLTP + DW):")
    print("   sql/ddl/00_reset_databases.sql")
    print("\nDW only reset (keeps OLTP):")
    print("   sql/ddl/00_reset_dw.sql")
    
    print("\n[KEY FEATURES]")
    print("-" * 70)
    print("""
✓ Star Schema: 7 dimensions + 1 fact table
✓ SCD Type 2: Historical tracking of salesperson performance
✓ Multi-Currency: ARS, USD, EUR, BRL, CNY (¥) with exchange rates
✓ Advanced Analytics: YoY, MoM, ABC/Pareto, RFM
✓ Data Quality: Automated validation scripts
✓ Cross-Platform: SQL Server + Python/Pandas validation
    """)
    
    print("\n[ANALYTICS EXAMPLES]")
    print("-" * 70)
    print("\nQuery 1: Top-selling brand with multi-currency")
    print("   Shows: Brand, Units, Revenue in 5 currencies")
    print("\nQuery 2: Year-over-Year growth analysis")
    print("   Shows: Monthly trends, YoY%, MoM%, moving averages")
    print("\nQuery 3: RFM customer segmentation")
    print("   Shows: 10 segments (Champions, Loyal, At Risk, etc.)")
    print("\nQuery 4: ABC/Pareto product classification")
    print("   Shows: Products in A (80%), B (15%), C (5%) categories")
    
    print("\n[DATA QUALITY CHECKS]")
    print("-" * 70)
    print("\nRun comprehensive validation:")
    print("   07_validacion/06_validacion_calidad.sql")
    print("\nValidates:")
    print("  ✅ Referential integrity")
    print("  ✅ Unique primary keys")
    print("  ✅ No orphaned foreign keys")
    print("  ✅ Consistent metrics (margin calculations)")
    print("  ✅ Valid SCD2 date ranges")
    print("  ✅ No nulls in critical columns")
    
    print("\n[PYTHON NOTEBOOK HIGHLIGHTS]")
    print("-" * 70)
    print("""
1. Auto-reconnect to SQL Server (handles timeouts)
2. Build star schema in-memory with Pandas
3. Visualize salesperson performance over time
4. Statistical distributions (histograms + KDE)
5. Multi-currency validation (SQL vs Pandas)
6. Unicode symbols (¥, €, R$) in all charts
7. Automated ✅/❌ comparison table
    """)
    
    print("\n" + "=" * 70)
    print("READY TO START")
    print("=" * 70)
    print("\n1. Open SQL Server Management Studio (SSMS)")
    print("2. Execute scripts in order from STEP 1")
    print("3. Validate with queries from STEP 3")
    print("4. Explore analytics from STEP 4")
    print("5. Run Python notebook from STEP 5")
    print("\n✓ Complete Data Warehouse setup in ~15 minutes!")


if __name__ == "__main__":
    main()
