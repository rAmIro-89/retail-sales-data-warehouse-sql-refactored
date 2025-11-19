"""
Database Connection Utility
Handles database connections and query execution
"""

import pandas as pd
from sqlalchemy import create_engine, text
from typing import Dict, Any, Optional
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


class DatabaseConnection:
    """
    Manages database connections using SQLAlchemy
    """
    
    def __init__(self, connection_params: Dict[str, Any] = None):
        """
        Initialize database connection
        
        Args:
            connection_params: Dictionary with connection parameters
                - db_type: 'postgresql', 'mysql', 'sqlite', etc.
                - host: Database host
                - port: Database port
                - database: Database name
                - username: Database user
                - password: Database password
        """
        if connection_params is None:
            # Try to load from environment variables
            connection_params = self._load_from_env()
        
        self.connection_params = connection_params
        self.engine = None
        self.connection = None
        self._connect()
    
    def _load_from_env(self) -> Dict[str, Any]:
        """
        Load connection parameters from environment variables
        
        Returns:
            Dictionary with connection parameters
        """
        return {
            'db_type': os.getenv('DB_TYPE', 'postgresql'),
            'host': os.getenv('DB_HOST', 'localhost'),
            'port': os.getenv('DB_PORT', '5432'),
            'database': os.getenv('DB_NAME', 'datawarehouse'),
            'username': os.getenv('DB_USER', 'postgres'),
            'password': os.getenv('DB_PASSWORD', '')
        }
    
    def _build_connection_string(self) -> str:
        """
        Build SQLAlchemy connection string
        
        Returns:
            Connection string
        """
        db_type = self.connection_params['db_type']
        username = self.connection_params['username']
        password = self.connection_params['password']
        host = self.connection_params['host']
        port = self.connection_params['port']
        database = self.connection_params['database']
        
        if db_type == 'sqlite':
            return f"sqlite:///{database}"
        elif db_type == 'postgresql':
            return f"postgresql://{username}:{password}@{host}:{port}/{database}"
        elif db_type == 'mysql':
            return f"mysql+pymysql://{username}:{password}@{host}:{port}/{database}"
        else:
            raise ValueError(f"Unsupported database type: {db_type}")
    
    def _connect(self):
        """Create database connection"""
        try:
            connection_string = self._build_connection_string()
            self.engine = create_engine(connection_string, echo=False)
            self.connection = self.engine.connect()
            print(f"Connected to {self.connection_params['db_type']} database")
        except Exception as e:
            print(f"Error connecting to database: {str(e)}")
            raise
    
    def execute_query(self, query: str, params: Dict[str, Any] = None) -> pd.DataFrame:
        """
        Execute a SELECT query and return results as DataFrame
        
        Args:
            query: SQL query string
            params: Optional query parameters
            
        Returns:
            DataFrame with query results
        """
        try:
            if params:
                df = pd.read_sql_query(text(query), self.connection, params=params)
            else:
                df = pd.read_sql_query(query, self.connection)
            return df
        except Exception as e:
            print(f"Error executing query: {str(e)}")
            raise
    
    def execute_sql(self, sql: str, params: Dict[str, Any] = None) -> Any:
        """
        Execute an SQL statement (INSERT, UPDATE, DELETE, etc.)
        
        Args:
            sql: SQL statement
            params: Optional parameters
            
        Returns:
            Result of the execution
        """
        try:
            if params:
                result = self.connection.execute(text(sql), params)
            else:
                result = self.connection.execute(text(sql))
            self.connection.commit()
            return result
        except Exception as e:
            self.connection.rollback()
            print(f"Error executing SQL: {str(e)}")
            raise
    
    def get_engine(self):
        """
        Get SQLAlchemy engine
        
        Returns:
            SQLAlchemy engine
        """
        return self.engine
    
    def test_connection(self) -> bool:
        """
        Test if database connection is alive
        
        Returns:
            True if connection is alive
        """
        try:
            self.connection.execute(text("SELECT 1"))
            return True
        except:
            return False
    
    def close(self):
        """Close database connection"""
        if self.connection:
            self.connection.close()
        if self.engine:
            self.engine.dispose()
        print("Database connection closed")


if __name__ == "__main__":
    # Example usage
    print("Database connection utility loaded successfully")
    
    # Test connection (will use environment variables)
    # db = DatabaseConnection()
    # print(f"Connection test: {db.test_connection()}")
    # db.close()
