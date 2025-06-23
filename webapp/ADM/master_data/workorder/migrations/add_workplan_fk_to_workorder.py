"""
Migration script to add a foreign key from work_orders to work_plans.
"""
import psycopg2
import yaml
import os

def run_migration():
    """Run the migration to add the foreign key."""
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
        # Check if the column 'workplan_id' already exists in 'work_orders'
        cur.execute("""
            SELECT EXISTS (
                SELECT 1
                FROM information_schema.columns
                WHERE table_name = 'work_orders' AND column_name = 'workplan_id'
            );
        """)
        column_exists = cur.fetchone()[0]
        
        if not column_exists:
            cur.execute("ALTER TABLE work_orders ADD COLUMN workplan_id INTEGER;")
            print("Column 'workplan_id' added to 'work_orders' table.")
        else:
            print("Column 'workplan_id' already exists in 'work_orders' table.")

        # Check if the foreign key constraint already exists
        cur.execute("""
            SELECT EXISTS (
                SELECT 1
                FROM information_schema.table_constraints
                WHERE table_name = 'work_orders' AND constraint_name = 'fk_work_orders_workplan_id'
            );
        """)
        constraint_exists = cur.fetchone()[0]

        if not constraint_exists:
            cur.execute("""
                ALTER TABLE work_orders 
                ADD CONSTRAINT fk_work_orders_workplan_id 
                FOREIGN KEY (workplan_id) 
                REFERENCES work_plans(id);
            """)
            print("Foreign key 'fk_work_orders_workplan_id' on 'work_orders' table created.")
        else:
            print("Foreign key 'fk_work_orders_workplan_id' on 'work_orders' table already exists.")

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
