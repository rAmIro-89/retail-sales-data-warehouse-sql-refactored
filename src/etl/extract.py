"""
Extract Module - ETL Pipeline
Handles data extraction from various sources (CSV, databases, APIs)
"""

import pandas as pd
from typing import Dict, Any
import os
from src.utils.db_connection import DatabaseConnection


class DataExtractor:
    """
    Class responsible for extracting data from multiple sources
    """
    
    def __init__(self, config: Dict[str, Any] = None):
        """
        Initialize the DataExtractor
        
        Args:
            config: Configuration dictionary containing connection parameters
        """
        self.config = config or {}
        self.db_connection = None
        
    def extract_from_csv(self, file_path: str, **kwargs) -> pd.DataFrame:
        """
        Extract data from a CSV file
        
        Args:
            file_path: Path to the CSV file
            **kwargs: Additional arguments for pd.read_csv()
            
        Returns:
            DataFrame with extracted data
        """
        try:
            print(f"Extracting data from CSV: {file_path}")
            df = pd.read_csv(file_path, **kwargs)
            print(f"Successfully extracted {len(df)} rows")
            return df
        except Exception as e:
            print(f"Error extracting from CSV: {str(e)}")
            raise
    
    def extract_from_database(self, query: str, connection_params: Dict[str, Any]) -> pd.DataFrame:
        """
        Extract data from a database using SQL query
        
        Args:
            query: SQL query to execute
            connection_params: Database connection parameters
            
        Returns:
            DataFrame with query results
        """
        try:
            print("Extracting data from database...")
            self.db_connection = DatabaseConnection(connection_params)
            df = self.db_connection.execute_query(query)
            print(f"Successfully extracted {len(df)} rows from database")
            return df
        except Exception as e:
            print(f"Error extracting from database: {str(e)}")
            raise
        finally:
            if self.db_connection:
                self.db_connection.close()
    
    def extract_from_multiple_sources(self, sources: list) -> Dict[str, pd.DataFrame]:
        """
        Extract data from multiple sources
        
        Args:
            sources: List of dictionaries containing source information
            
        Returns:
            Dictionary mapping source names to DataFrames
        """
        results = {}
        
        for source in sources:
            source_type = source.get('type')
            source_name = source.get('name')
            
            if source_type == 'csv':
                results[source_name] = self.extract_from_csv(source['path'])
            elif source_type == 'database':
                results[source_name] = self.extract_from_database(
                    source['query'], 
                    source['connection_params']
                )
        
        return results


if __name__ == "__main__":
    # Example usage
    extractor = DataExtractor()
    
    # Example: Extract from CSV
    # df = extractor.extract_from_csv('data/raw/sales_data.csv')
    
    print("Extract module loaded successfully")
