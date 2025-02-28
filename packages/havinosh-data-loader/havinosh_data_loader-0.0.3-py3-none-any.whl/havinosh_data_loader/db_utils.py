import psycopg2
import pandas as pd
from psycopg2 import sql, extras
from havinosh_data_loader.config import DB_CONFIG
from havinosh_data_loader.logger import logger
from havinosh_data_loader.exception import LoaderException

class Database:
    """Database class to handle PostgreSQL operations"""

    def __init__(self, db_config=None):
        """
        Initialize Database object.

        :param db_config: Dictionary with database credentials. Defaults to DB_CONFIG.
        """
        self.db_config = db_config or DB_CONFIG
        self.conn = None  # Connection instance

    def connect(self):
        """Establish a PostgreSQL connection"""
        try:
            self.conn = psycopg2.connect(**self.db_config)
            logger.info("✅ Connected to PostgreSQL database")
        except Exception as e:
            raise LoaderException(f"❌ Failed to connect to database: {e}")

    def close(self):
        """Close the database connection"""
        if self.conn:
            self.conn.close()
            logger.info("🔌 Database connection closed.")

    def create_table(self, table_name, df):
        """Dynamically create a table based on DataFrame structure with inferred types"""
        try:
            if self.conn is None:
                self.connect()
            cursor = self.conn.cursor()

            dtype_mapping = {
                "int64": "BIGINT",
                "float64": "DOUBLE PRECISION",
                "object": "TEXT",
                "datetime64[ns]": "TIMESTAMP",
                "bool": "BOOLEAN"
            }

            columns = ", ".join([f'"{col}" {dtype_mapping.get(str(df[col].dtype), "TEXT")}' for col in df.columns])
            query = sql.SQL('CREATE TABLE IF NOT EXISTS {} ({});').format(
                sql.Identifier(table_name), sql.SQL(columns)
            )

            cursor.execute(query)
            self.conn.commit()
            cursor.close()
            logger.info(f"✅ Table '{table_name}' created successfully!")
        except Exception as e:
            if self.conn:
                self.conn.rollback()
            raise LoaderException(f"❌ Error creating table: {e}")

    def insert_data(self, table_name, df):
        """Insert data into the PostgreSQL table efficiently using execute_values"""
        try:
            if self.conn is None:
                self.connect()
            cursor = self.conn.cursor()

            if df.empty:
                logger.warning(f"⚠️ No data to insert into '{table_name}'")
                return  # Avoid running an empty insert

            columns = list(df.columns)
            values = [tuple(row) for row in df.itertuples(index=False, name=None)]

            insert_query = sql.SQL('INSERT INTO {} ({}) VALUES %s').format(
                sql.Identifier(table_name),
                sql.SQL(', ').join(map(sql.Identifier, columns))
            )

            extras.execute_values(cursor, insert_query, values)
            self.conn.commit()
            cursor.close()
            logger.info(f"✅ Data inserted into '{table_name}' successfully!")
        except Exception as e:
            if self.conn:
                self.conn.rollback()
            raise LoaderException(f"❌ Error inserting data: {e}")

    def execute_query(self, query):
        """Execute a raw SQL query and return results if it's a SELECT query"""
        try:
            if self.conn is None:
                self.connect()
            cursor = self.conn.cursor()

            cursor.execute(query)

            if query.strip().upper().startswith("SELECT"):
                result = cursor.fetchall()  # Fetch results for SELECT queries
                cursor.close()
                logger.info("✅ SELECT query executed successfully!")
                return result

            self.conn.commit()
            cursor.close()
            logger.info("✅ Query executed successfully!")
        except Exception as e:
            if self.conn:
                self.conn.rollback()
            raise LoaderException(f"❌ Error executing query: {e}")
