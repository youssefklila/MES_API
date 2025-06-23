import sys
import os
from sqlalchemy import text

# Add the project root directory to the Python path to allow for module imports
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../../../../'))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

# Import the container after setting the path
from webapp.containers import Container

def run_migration():
    """
    Applies the database migration to add a foreign key from work_steps to erp_groups.
    This script uses the application's own dependency injection container to safely
    access the database configuration and session management.
    """
    print("Initializing application container...")
    # The container loads configuration from environment variables by default in this project.
    container = Container()
    
    db = container.db()
    session_factory = db.session

    with session_factory() as session:
        try:
            print("Applying migration: Add erp_group_id foreign key to work_steps table...")

            # Use a transaction to ensure all changes are applied atomically
            with session.begin():
                # 1. Drop the old workstep_erp column if it exists
                print("Dropping old 'workstep_erp' column...")
                session.execute(text("ALTER TABLE work_steps DROP COLUMN IF EXISTS workstep_erp;"))

                # 2. Add the new erp_group_id column if it doesn't exist
                print("Adding new 'erp_group_id' column...")
                session.execute(text("ALTER TABLE work_steps ADD COLUMN IF NOT EXISTS erp_group_id INTEGER;"))

                # 3. Add the foreign key constraint if it doesn't exist
                print("Adding foreign key constraint to 'erp_group_id'...")
                session.execute(text("""
                    DO $$
                    BEGIN
                        IF NOT EXISTS (
                            SELECT 1 FROM pg_constraint
                            WHERE conname = 'fk_erp_group' AND conrelid = 'work_steps'::regclass
                        ) THEN
                            ALTER TABLE work_steps
                            ADD CONSTRAINT fk_erp_group
                            FOREIGN KEY (erp_group_id)
                            REFERENCES erp_groups (id)
                            ON DELETE SET NULL;
                        END IF;
                    END;
                    $$;
                """))

            print("Migration applied successfully.")

        except Exception as e:
            print(f"An error occurred: {e}")
            # The transaction is automatically rolled back by the 'with' statement on exception
            print("Migration failed and was rolled back.")
        finally:
            print("Session closed.")

if __name__ == "__main__":
    run_migration()

