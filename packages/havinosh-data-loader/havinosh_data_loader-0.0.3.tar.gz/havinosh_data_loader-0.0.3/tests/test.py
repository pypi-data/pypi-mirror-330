import os
from havinosh_data_loader import Config, Database, CSVProcessor
from havinosh_data_loader.logger import logger
from havinosh_data_loader.exception import LoaderException

def main():
    try:
        # Load database configuration from .env or default values
        config = Config()
        db_config = config.get_config()

        # Initialize Database instance
        db = Database(db_config)
        db.connect()  # Establish database connection

        # Initialize CSVProcessor instance
        csv_processor = CSVProcessor(db, csv_folder="csv_files")

        # Process and insert CSV files into PostgreSQL
        csv_processor.process_csv()

        # Close the database connection
        db.close()

        logger.info("✅ All CSV files processed successfully!")

    except LoaderException as e:
        logger.error(f"❌ LoaderException occurred: {e}")
    except Exception as e:
        logger.error(f"❌ Unexpected error: {e}")

if __name__ == "__main__":
    main()
