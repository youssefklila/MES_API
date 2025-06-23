"""
Migration script to rename the workplan_id column to workplan_vers in the work_orders table.
"""
import psycopg2
import yaml
import os

def run_migration():
    """Run the migration to rename the column."""
    # Load config from YAML file
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
        # Check if the column 'workplan_id' exists and 'workplan_vers' does not
        cur.execute("""
            SELECT EXISTS (
                SELECT 1 FROM information_schema.columns
                WHERE table_name = 'work_orders' AND column_name = 'workplan_id'
            );
        """)
        old_column_exists = cur.fetchone()[0]

        cur.execute("""
            SELECT EXISTS (
                SELECT 1 FROM information_schema.columns
                WHERE table_name = 'work_orders' AND column_name = 'workplan_vers'
            );
        """)
        new_column_exists = cur.fetchone()[0]

        if old_column_exists and not new_column_exists:
            cur.execute("ALTER TABLE work_orders RENAME COLUMN workplan_id TO workplan_vers;")
            print("Renamed column 'workplan_id' to 'workplan_vers' in 'work_orders' table.")
        elif new_column_exists:
             print("Column 'workplan_vers' already exists.")
        else:
            print("Column 'workplan_id' not found, no action taken.")

        conn.commit()
        
    except Exception as e:
        conn.rollback()
        print(f"Error: {e}")
        raise
    
    finally:
        cur.close()
        conn.close()

if __name__ == "__main__":
    run_migration()
