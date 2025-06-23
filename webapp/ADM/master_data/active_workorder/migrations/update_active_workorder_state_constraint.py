"""
Migration script to update the state constraint in the active_workorders table.
"""
import psycopg2
import yaml
import os

def run_migration():
    """Run the migration to update the state constraint in the active_workorders table."""
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
        # Check if the table exists
        cur.execute("""
            SELECT EXISTS (
                SELECT FROM information_schema.tables 
                WHERE table_name = 'active_workorders'
            );
        """)
        
        table_exists = cur.fetchone()[0]
        
        if table_exists:
            # Drop the existing constraint
            cur.execute("""
                ALTER TABLE active_workorders 
                DROP CONSTRAINT IF EXISTS check_state_value;
            """)
            
            # Add the new constraint
            cur.execute("""
                ALTER TABLE active_workorders 
                ADD CONSTRAINT check_state_value CHECK (state IN (0, 1, 2, 3, 4, 5));
            """)
            
            print("Updated state constraint in active_workorders table to allow values 0-5")
        else:
            print("active_workorders table does not exist")
        
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
