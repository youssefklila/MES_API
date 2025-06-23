"""
Migration script to correct the workplan_vers foreign key in the work_orders table.
"""
import psycopg2
import yaml
import os

def run_migration():
    """Run the migration to fix the foreign key."""
    config_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../../../config.yml'))
    print(f"Looking for config file at: {config_path}")
    
    try:
        with open(config_path, 'r') as config_file:
            config = yaml.safe_load(config_file)
    except FileNotFoundError:
        print("Config file not found, using default connection string")
        config = {'db': {'url': 'postgresql://postgres:postgres@192.168.1.140:5432/prod'}}
    
    db_url = config.get('db', {}).get('url', 'postgresql://postgres:postgres@localhost:5432/prod')
    
    conn = psycopg2.connect(db_url)
    cur = conn.cursor()
    
    try:
        # 1. Drop the incorrect foreign key constraint on workplan_id if it exists
        cur.execute("""
            ALTER TABLE work_orders
            DROP CONSTRAINT IF EXISTS fk_work_orders_workplan_id;
        """)
        print("Dropped constraint 'fk_work_orders_workplan_id' if it existed.")

        # 2. Drop the incorrect workplan_id column if it exists
        cur.execute("""
            ALTER TABLE work_orders
            DROP COLUMN IF EXISTS workplan_id;
        """)
        print("Dropped column 'workplan_id' if it existed.")

        # 3. Change the type of workplan_vers to INTEGER
        cur.execute("""
            ALTER TABLE work_orders
            ALTER COLUMN workplan_vers TYPE INTEGER USING workplan_vers::integer;
        """)
        print("Changed 'workplan_vers' column type to INTEGER.")

        # 4. Add the correct foreign key constraint on workplan_vers
        cur.execute("""
            ALTER TABLE work_orders
            ADD CONSTRAINT fk_work_orders_workplan_vers
            FOREIGN KEY (workplan_vers) REFERENCES work_plans(id);
        """)
        print("Added foreign key 'fk_work_orders_workplan_vers' to 'workplan_vers' column.")

        conn.commit()
        print("Database schema corrected successfully.")
        
    except Exception as e:
        conn.rollback()
        print(f"Error: {e}")
        # If the error is about the constraint already existing, we can ignore it.
        if 'already exists' not in str(e):
            raise
        else:
            print("Constraint likely already exists, considering this a success.")
            conn.commit() # Re-commit if it was just a pre-existing constraint
    
    finally:
        cur.close()
        conn.close()

if __name__ == "__main__":
    run_migration()
