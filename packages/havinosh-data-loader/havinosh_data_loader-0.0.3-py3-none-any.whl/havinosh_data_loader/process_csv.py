import pandas as pd
import os
import sys
from havinosh_data_loader.db_utils import Database
from havinosh_data_loader.logger import logger
from havinosh_data_loader.exception import LoaderException

class CSVProcessor:
    """Class for processing and inserting CSV files into PostgreSQL"""

    def __init__(self, db_instance, csv_folder="csv_files"):
        """
        Initialize CSVProcessor with database instance and folder path.

        :param db_instance: An instance of the Database class
        :param csv_folder: Folder path containing CSV files
        """
        self.db = db_instance
        self.csv_folder = csv_folder

    def process_csv(self):
        """Read and insert CSV files into PostgreSQL dynamically"""
        try:
            csv_files = [f for f in os.listdir(self.csv_folder) if f.endswith(".csv")]

            if not csv_files:
                logger.warning("⚠️ No CSV files found in the directory.")
                return

            for file in csv_files:
                try:
                    file_path = os.path.join(self.csv_folder, file)
                    table_name = os.path.splitext(file)[0].lower()  # Use filename as table name
                    
                    df = pd.read_csv(file_path)
                    
                    if df.empty:
                        logger.warning(f"⚠️ Skipping empty file: {file}")
                        continue  # Skip empty CSV files

                    # Normalize column names (lowercase, replace spaces with underscores)
                    df.columns = df.columns.str.lower().str.replace(" ", "_")

                    logger.info(f"📂 Processing file: {file}")

                    # Create table and insert data
                    self.db.create_table(table_name, df)
                    self.db.insert_data(table_name, df)

                    logger.info(f"✅ Successfully ingested {file} into table '{table_name}'")

                except pd.errors.EmptyDataError:
                    logger.error(f"❌ Skipping {file}: Empty or unreadable CSV file.")
                except Exception as e:
                    logger.error(f"❌ Error processing {file}: {e}", exc_info=True)

        except Exception as e:
            raise LoaderException(f"❌ Unexpected error in CSV processing: {e}", sys)

        finally:
            self.db.close()  # Ensure database connection is closed after processing
