"""
Transform Module - ETL Pipeline
Handles data transformation, cleaning, and business logic
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Any
from datetime import datetime


class DataTransformer:
    """
    Class responsible for transforming and cleaning data
    """
    
    def __init__(self):
        """Initialize the DataTransformer"""
        self.transformation_log = []
    
    def clean_data(self, df: pd.DataFrame, config: Dict[str, Any] = None) -> pd.DataFrame:
        """
        Clean data by handling missing values, duplicates, and data types
        
        Args:
            df: Input DataFrame
            config: Configuration for cleaning operations
            
        Returns:
            Cleaned DataFrame
        """
        df_clean = df.copy()
        
        print("Starting data cleaning...")
        
        # Remove duplicates
        initial_rows = len(df_clean)
        df_clean = df_clean.drop_duplicates()
        duplicates_removed = initial_rows - len(df_clean)
        
        if duplicates_removed > 0:
            print(f"Removed {duplicates_removed} duplicate rows")
        
        # Handle missing values
        missing_before = df_clean.isnull().sum().sum()
        if config and 'fill_na' in config:
            df_clean = df_clean.fillna(config['fill_na'])
        
        missing_after = df_clean.isnull().sum().sum()
        print(f"Missing values: {missing_before} -> {missing_after}")
        
        self.transformation_log.append({
            'operation': 'clean_data',
            'timestamp': datetime.now(),
            'duplicates_removed': duplicates_removed,
            'missing_values_handled': missing_before - missing_after
        })
        
        return df_clean
    
    def standardize_columns(self, df: pd.DataFrame, column_mapping: Dict[str, str] = None) -> pd.DataFrame:
        """
        Standardize column names
        
        Args:
            df: Input DataFrame
            column_mapping: Dictionary mapping old names to new names
            
        Returns:
            DataFrame with standardized columns
        """
        df_transformed = df.copy()
        
        # Convert to lowercase and replace spaces with underscores
        df_transformed.columns = df_transformed.columns.str.lower().str.replace(' ', '_')
        
        # Apply custom mapping if provided
        if column_mapping:
            df_transformed = df_transformed.rename(columns=column_mapping)
        
        print(f"Standardized {len(df_transformed.columns)} columns")
        
        return df_transformed
    
    def apply_business_rules(self, df: pd.DataFrame, rules: List[Dict[str, Any]]) -> pd.DataFrame:
        """
        Apply business rules and calculations
        
        Args:
            df: Input DataFrame
            rules: List of business rules to apply
            
        Returns:
            Transformed DataFrame
        """
        df_transformed = df.copy()
        
        for rule in rules:
            rule_type = rule.get('type')
            
            if rule_type == 'calculate':
                # Create calculated columns
                df_transformed[rule['target_column']] = df_transformed.eval(rule['formula'])
            
            elif rule_type == 'filter':
                # Apply filters
                df_transformed = df_transformed.query(rule['condition'])
            
            elif rule_type == 'categorize':
                # Create categories
                df_transformed[rule['target_column']] = pd.cut(
                    df_transformed[rule['source_column']],
                    bins=rule['bins'],
                    labels=rule['labels']
                )
        
        print(f"Applied {len(rules)} business rules")
        
        return df_transformed
    
    def create_dimension_keys(self, df: pd.DataFrame, dimension_columns: List[str], 
                             key_column: str = 'dimension_key') -> pd.DataFrame:
        """
        Create surrogate keys for dimension tables
        
        Args:
            df: Input DataFrame
            dimension_columns: Columns that define the dimension
            key_column: Name for the surrogate key column
            
        Returns:
            DataFrame with surrogate keys
        """
        df_transformed = df.copy()
        
        # Create a unique key based on dimension columns
        df_transformed[key_column] = df_transformed.groupby(dimension_columns).ngroup() + 1
        
        print(f"Created {key_column} with {df_transformed[key_column].nunique()} unique values")
        
        return df_transformed
    
    def aggregate_data(self, df: pd.DataFrame, group_by: List[str], 
                      aggregations: Dict[str, str]) -> pd.DataFrame:
        """
        Aggregate data by specified columns
        
        Args:
            df: Input DataFrame
            group_by: Columns to group by
            aggregations: Dictionary of column -> aggregation function
            
        Returns:
            Aggregated DataFrame
        """
        df_agg = df.groupby(group_by).agg(aggregations).reset_index()
        
        print(f"Aggregated {len(df)} rows into {len(df_agg)} rows")
        
        return df_agg
    
    def get_transformation_log(self) -> List[Dict[str, Any]]:
        """
        Get the log of all transformations performed
        
        Returns:
            List of transformation operations
        """
        return self.transformation_log


if __name__ == "__main__":
    # Example usage
    transformer = DataTransformer()
    
    print("Transform module loaded successfully")
