import sys
import os
from sqlalchemy import text

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
            session.execute(text('ALTER TABLE work_steps ALTER COLUMN setup_flag TYPE VARCHAR(20);'))
            session.execute(text('ALTER TABLE work_steps ALTER COLUMN confirmation TYPE VARCHAR(20);'))
            session.execute(text('ALTER TABLE work_steps ALTER COLUMN sequentiell TYPE VARCHAR(20);'))
            session.execute(text('ALTER TABLE work_steps ALTER COLUMN workstep_type TYPE VARCHAR(20);'))
            session.execute(text('ALTER TABLE work_steps ALTER COLUMN traceflag TYPE VARCHAR(20);'))
            session.commit()
            print("Successfully altered character field lengths in work_steps table.")
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
            session.execute(text('ALTER TABLE work_steps ALTER COLUMN setup_flag TYPE VARCHAR(1);'))
            session.execute(text('ALTER TABLE work_steps ALTER COLUMN confirmation TYPE VARCHAR(1);'))
            session.execute(text('ALTER TABLE work_steps ALTER COLUMN sequentiell TYPE VARCHAR(1);'))
            session.execute(text('ALTER TABLE work_steps ALTER COLUMN workstep_type TYPE VARCHAR(1);'))
            session.execute(text('ALTER TABLE work_steps ALTER COLUMN traceflag TYPE VARCHAR(1);'))
            session.commit()
            print("Successfully reverted character field lengths in work_steps table.")
        except Exception as e:
            session.rollback()
            print(f"An error occurred: {e}")
            raise

if __name__ == "__main__":
    upgrade()
