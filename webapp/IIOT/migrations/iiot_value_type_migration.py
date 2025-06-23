"""Fast migration for IIOT sensor data: drop sensor_id and convert value to JSONB."""
import os
import sys
import logging
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))
from webapp.database import Database

def run_migration():
    try:
        db_url = 'postgresql://postgres:postgres@192.168.1.140:5432/postgres'
        db = Database(db_url)
        engine = db._engine
        with engine.connect() as conn:
            with conn.begin():
                # Drop sensor_id column if it exists
                try:
                    conn.execute(text("ALTER TABLE iiot_sensor_data DROP COLUMN IF EXISTS sensor_id"))
                    logger.info("Dropped sensor_id column if it existed.")
                except SQLAlchemyError as e:
                    logger.error(f"Could not drop sensor_id: {e}")
                # Convert value column to JSONB
                try:
                    conn.execute(text("ALTER TABLE iiot_sensor_data ALTER COLUMN value TYPE JSONB USING value::jsonb"))
                    logger.info("Converted value column to JSONB.")
                except SQLAlchemyError as e:
                    logger.error(f"Could not convert value to JSONB: {e}")
        logger.info("Fast migration completed successfully!")
    except Exception as e:
        logger.error(f"Migration failed: {e}")
        raise

if __name__ == "__main__":
    run_migration()
