"""
Migration script to create monitoring_tasks table.
"""
import psycopg2
import yaml
import os

def run_migration():
    """Run the migration to create monitoring_tasks table."""
    # Load config from YAML file
    config_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../../iiot_config.yml'))
    with open(config_path, 'r') as config_file:
        config = yaml.safe_load(config_file)
    
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
                WHERE table_name = 'monitoring_tasks'
            );
        """)
        
        if not cur.fetchone()[0]:
            # Create the monitoring_tasks table if it doesn't exist
            cur.execute("""
                CREATE TABLE monitoring_tasks (
                    id SERIAL PRIMARY KEY,
                    description TEXT NOT NULL,
                    priority VARCHAR(50) NOT NULL,
                    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
                    assigned_to INTEGER REFERENCES users(id)
                );
            """)
            print("Created monitoring_tasks table")
        else:
            print("monitoring_tasks table already exists")
        
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
