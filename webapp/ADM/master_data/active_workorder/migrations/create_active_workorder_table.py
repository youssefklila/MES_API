"""
Migration script to create the active_workorders table in the database.
"""
import psycopg2
import yaml
import os

def run_migration():
    """Run the migration to create the active_workorders table."""
    # Load config from YAML file
    config_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../../../config.yml'))
    print(f"Looking for config file at: {config_path}")
    
    try:
        with open(config_path, 'r') as config_file:
            config = yaml.safe_load(config_file)
    except FileNotFoundError:
        # Fallback to hardcoded connection string if config file not found
        print("Config file not found, using default connection string")
        config = {'db': {'url': 'postgresql://postgres:postgres@192.168.1.140:5432/postgres'}}
    
    # Get the database URL from config
    db_url = config.get('db', {}).get('url', 'postgresql://postgres:postgres@localhost:5432/postgres')
    
    # Connect to the database using the URL
    conn = psycopg2.connect(db_url)
    
    # Create a cursor
    cur = conn.cursor()
    
    try:
        # Check if the table already exists
        cur.execute("""
            SELECT EXISTS (
                SELECT FROM information_schema.tables 
                WHERE table_name = 'active_workorders'
            );
        """)
        
        table_exists = cur.fetchone()[0]
        
        if not table_exists:
            # Create the active_workorders table
            cur.execute("""
                CREATE TABLE active_workorders (
                    id SERIAL PRIMARY KEY,
                    workorder_id INTEGER NOT NULL,
                    station_id INTEGER NOT NULL,
                    state INTEGER NOT NULL,
                    CONSTRAINT check_state_value CHECK (state IN (0, 1)),
                    CONSTRAINT fk_workorder FOREIGN KEY (workorder_id) REFERENCES work_orders(id) ON DELETE CASCADE,
                    CONSTRAINT fk_station FOREIGN KEY (station_id) REFERENCES stations(id) ON DELETE CASCADE
                );
            """)
            
            # Create an index on workorder_id and station_id for faster lookups
            cur.execute("""
                CREATE INDEX idx_active_workorders_workorder_id ON active_workorders (workorder_id);
            """)
            
            cur.execute("""
                CREATE INDEX idx_active_workorders_station_id ON active_workorders (station_id);
            """)
            
            print("Created active_workorders table and indexes")
        else:
            print("active_workorders table already exists")
        
        # Commit the transaction
        conn.commit()
        
    except Exception as e:
        # Roll back the transaction in case of error
        conn.rollback()
        print(f"Error: {e}")
        raise
    
    finally:
        # Close the cursor and connection
        cur.close()
        conn.close()

if __name__ == "__main__":
    run_migration()
