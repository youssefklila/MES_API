import os
import sys
import logging

# Ensure the project root is in sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))

from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError
from webapp.database import Database

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def check_and_drop_constraints():
    db_url = 'postgresql://postgres:postgres@192.168.1.140:5432/postgres'
    db = Database(db_url)
    engine = db._engine
    with engine.connect() as conn:
        # 1. Check for foreign key constraints on sensor_id
        fk_query = '''
        SELECT conname
        FROM pg_constraint
        WHERE conrelid = 'iiot_sensor_data'::regclass
          AND contype = 'f'
          AND array_position(conkey, (
            SELECT attnum FROM pg_attribute WHERE attrelid = 'iiot_sensor_data'::regclass AND attname = 'sensor_id'
          )) IS NOT NULL;
        '''
        fk_result = conn.execute(text(fk_query)).fetchall()
        if fk_result:
            logger.info(f"Found foreign key constraints on sensor_id: {[row[0] for row in fk_result]}")
            for row in fk_result:
                try:
                    conn.execute(text(f'ALTER TABLE iiot_sensor_data DROP CONSTRAINT IF EXISTS {row[0]}'))
                    logger.info(f"Dropped constraint: {row[0]}")
                except SQLAlchemyError as e:
                    logger.error(f"Could not drop constraint {row[0]}: {e}")
        else:
            logger.info("No foreign key constraints found on sensor_id.")

        # 2. Check for locks on the table
        lock_query = '''
        SELECT pg_locks.pid, locktype, mode, granted, pg_stat_activity.query, pg_stat_activity.state
        FROM pg_locks
        JOIN pg_stat_activity ON pg_locks.pid = pg_stat_activity.pid
        WHERE relation::regclass::text = 'iiot_sensor_data';
        '''
        lock_result = conn.execute(text(lock_query)).fetchall()
        if lock_result:
            logger.info("Locks found on iiot_sensor_data:")
            for row in lock_result:
                logger.info(row)
        else:
            logger.info("No locks found on iiot_sensor_data.")

if __name__ == "__main__":
    check_and_drop_constraints()
