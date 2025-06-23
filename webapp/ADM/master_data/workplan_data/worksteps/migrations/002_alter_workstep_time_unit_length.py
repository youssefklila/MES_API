import sys
import os
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

# Add the project root to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..', '..', '..', '..')))

from webapp.containers import Container

def upgrade():
    """Applies the migration."""
    container = Container()
    db = container.db()
    session_factory = db.session

    with session_factory() as session:
        try:
            session.execute(text(
                'ALTER TABLE work_steps ALTER COLUMN time_unit TYPE VARCHAR(20);'
            ))
            session.commit()
            print("Successfully altered time_unit column length in work_steps table.")
        except Exception as e:
            session.rollback()
            print(f"An error occurred: {e}")
            raise

def downgrade():
    """Reverts the migration."""
    container = Container()
    db = container.db()
    session_factory = db.session

    with session_factory() as session:
        try:
            session.execute(text(
                'ALTER TABLE work_steps ALTER COLUMN time_unit TYPE VARCHAR(3);'
            ))
            session.commit()
            print("Successfully reverted time_unit column length in work_steps table.")
        except Exception as e:
            session.rollback()
            print(f"An error occurred: {e}")
            raise

if __name__ == "__main__":
    # This allows running the migration script directly
    # For example: python webapp/ADM/master_data/workplan_data/worksteps/migrations/002_alter_workstep_time_unit_length.py
    upgrade()
