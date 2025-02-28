"""
Havinosh Data Loader
--------------------
A Python package for dynamically loading CSV files into PostgreSQL tables.

Modules:
- config: Database configuration settings.
- db_utils: Database class for connection, table creation, and data insertion.
- process_csv: CSVProcessor class for processing and inserting CSV files.
"""

from .config import Config
from .db_utils import Database
from .process_csv import CSVProcessor  # Importing the class instead of function

__all__ = ["Config", "Database", "CSVProcessor"]

__version__ = "0.0.3"  # Increment version after changes
__author__ = "Vishal Singh Sangral"
__email__ = "support@havinosh.com"
__license__ = "MIT"
