import os
import sys
import logging

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))
from sqlalchemy import text
from webapp.database import Database

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def kill_locks():
    db_url = 'postgresql://postgres:postgres@192.168.1.140:5432/postgres'
    db = Database(db_url)
    engine = db._engine
    with engine.connect() as conn:
        # Find all PIDs holding locks on iiot_sensor_data
        lock_query = '''
        SELECT pg_locks.pid
        FROM pg_locks
        JOIN pg_stat_activity ON pg_locks.pid = pg_stat_activity.pid
        WHERE relation::regclass::text = 'iiot_sensor_data';
        '''
        lock_pids = conn.execute(text(lock_query)).fetchall()
        killed = 0
        for row in lock_pids:
            pid = row[0]
            # Don't kill our own session
            if pid == os.getpid():
                continue
            try:
                conn.execute(text(f"SELECT pg_terminate_backend({pid})"))
                logger.info(f"Terminated backend PID {pid}")
                killed += 1
            except Exception as e:
                logger.error(f"Could not terminate PID {pid}: {e}")
        if killed == 0:
            logger.info("No blocking sessions found or terminated.")
        else:
            logger.info(f"Terminated {killed} blocking sessions.")

if __name__ == "__main__":
    kill_locks()
