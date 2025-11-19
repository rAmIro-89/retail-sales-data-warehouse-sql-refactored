"""
Load Module - ETL Pipeline
Handles loading transformed data into the target data warehouse
"""

import pandas as pd
from typing import Dict, Any, List
from sqlalchemy import create_engine
from src.utils.db_connection import DatabaseConnection


class DataLoader:
    """
    Class responsible for loading data into the data warehouse
    """
    
    def __init__(self, connection_params: Dict[str, Any]):
        """
        Initialize the DataLoader
        
        Args:
            connection_params: Database connection parameters
        """
        self.connection_params = connection_params
        self.db_connection = DatabaseConnection(connection_params)
        self.load_log = []
    
    def load_to_database(self, df: pd.DataFrame, table_name: str, 
                        if_exists: str = 'append', chunksize: int = 1000) -> bool:
        """
        Load DataFrame to database table
        
        Args:
            df: DataFrame to load
            table_name: Target table name
            if_exists: How to behave if table exists ('fail', 'replace', 'append')
            chunksize: Number of rows to insert at a time
            
        Returns:
            True if successful, False otherwise
        """
        try:
            print(f"Loading {len(df)} rows to table: {table_name}")
            
            # Create SQLAlchemy engine
            engine = self.db_connection.get_engine()
            
            # Load data in chunks
            df.to_sql(
                name=table_name,
                con=engine,
                if_exists=if_exists,
                index=False,
                chunksize=chunksize
            )
            
            print(f"Successfully loaded {len(df)} rows to {table_name}")
            
            self.load_log.append({
                'table': table_name,
                'rows_loaded': len(df),
                'status': 'success'
            })
            
            return True
            
        except Exception as e:
            print(f"Error loading data to {table_name}: {str(e)}")
            self.load_log.append({
                'table': table_name,
                'rows_loaded': 0,
                'status': 'failed',
                'error': str(e)
            })
            return False
    
    def load_dimension(self, df: pd.DataFrame, dimension_name: str, 
                      scd_type: int = 1) -> bool:
        """
        Load data to a dimension table with SCD (Slowly Changing Dimension) handling
        
        Args:
            df: DataFrame containing dimension data
            dimension_name: Name of the dimension table
            scd_type: Type of SCD (1 or 2)
            
        Returns:
            True if successful
        """
        table_name = f"dim_{dimension_name}"
        
        if scd_type == 1:
            # Type 1: Overwrite existing data
            return self.load_to_database(df, table_name, if_exists='replace')
        
        elif scd_type == 2:
            # Type 2: Keep historical data (requires additional logic)
            # Add versioning columns
            df['valid_from'] = pd.Timestamp.now()
            df['valid_to'] = pd.Timestamp('2999-12-31')
            df['is_current'] = True
            
            return self.load_to_database(df, table_name, if_exists='append')
        
        return False
    
    def load_fact(self, df: pd.DataFrame, fact_name: str) -> bool:
        """
        Load data to a fact table
        
        Args:
            df: DataFrame containing fact data
            fact_name: Name of the fact table
            
        Returns:
            True if successful
        """
        table_name = f"fact_{fact_name}"
        
        # Fact tables typically use append mode
        return self.load_to_database(df, table_name, if_exists='append')
    
    def bulk_load(self, data_dict: Dict[str, pd.DataFrame], table_prefix: str = "") -> Dict[str, bool]:
        """
        Load multiple DataFrames to different tables
        
        Args:
            data_dict: Dictionary mapping table names to DataFrames
            table_prefix: Optional prefix for table names
            
        Returns:
            Dictionary mapping table names to load status
        """
        results = {}
        
        for table_name, df in data_dict.items():
            full_table_name = f"{table_prefix}{table_name}" if table_prefix else table_name
            results[table_name] = self.load_to_database(df, full_table_name)
        
        return results
    
    def execute_post_load_sql(self, sql_statements: List[str]) -> bool:
        """
        Execute SQL statements after loading (e.g., indexes, constraints)
        
        Args:
            sql_statements: List of SQL statements to execute
            
        Returns:
            True if all successful
        """
        try:
            for sql in sql_statements:
                self.db_connection.execute_sql(sql)
            
            print(f"Executed {len(sql_statements)} post-load SQL statements")
            return True
            
        except Exception as e:
            print(f"Error executing post-load SQL: {str(e)}")
            return False
    
    def get_load_log(self) -> List[Dict[str, Any]]:
        """
        Get the log of all load operations
        
        Returns:
            List of load operations
        """
        return self.load_log
    
    def close(self):
        """Close database connection"""
        if self.db_connection:
            self.db_connection.close()


if __name__ == "__main__":
    # Example usage
    print("Load module loaded successfully")
