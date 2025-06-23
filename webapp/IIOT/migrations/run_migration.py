"""Script to run the IIOT migrations."""
import os
import sys
import logging
from sqlalchemy import create_engine, text
from sqlalchemy.exc import SQLAlchemyError

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Add the project root directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))

# Import the database module
from webapp.database import Database

def run_migration():
    """Run the migration to add station_id column to iiot_sensor_data table."""
    try:
        # Use a hardcoded connection string for simplicity
        # You can modify this to match your database configuration
        db_url = 'postgresql://postgres:postgres@192.168.1.140:5432/postgres'
        
        # Create a database connection
        db = Database(db_url)
        engine = db._engine
        
        # Create a new connection for each operation
        with engine.connect() as conn:
            # Check if the column already exists
            try:
                conn.execute(text("SELECT station_id FROM iiot_sensor_data LIMIT 1"))
                logger.info("The station_id column already exists. No migration needed.")
                return
            except SQLAlchemyError:
                logger.info("The station_id column does not exist. Proceeding with migration.")
        
        # Create a new connection for the migration
        with engine.connect() as conn:
            # Execute the migration statements
            with conn.begin():
                # Add the station_id column
                conn.execute(text("ALTER TABLE iiot_sensor_data ADD COLUMN station_id INTEGER REFERENCES stations(id)"))
                logger.info("Added station_id column to iiot_sensor_data table")
                
                # Create an index for the station_id column
                conn.execute(text("CREATE INDEX ix_iiot_sensor_data_station_id ON iiot_sensor_data(station_id)"))
                logger.info("Created index for station_id column")
        
        logger.info("Migration completed successfully!")
        
    except Exception as e:
        logger.error(f"Error during migration: {str(e)}")
        raise

if __name__ == "__main__":
    run_migration()
