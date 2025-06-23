"""
Migration script to add station_id column to maintenance_configurations table.
"""
import psycopg2
import yaml
import os

def run_migration():
    """Run the migration to add station_id column to maintenance_configurations table."""
    # Load config from YAML file
    config_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../../../config.yml'))
    with open(config_path, 'r') as config_file:
        config = yaml.safe_load(config_file)
    
    # Get the database URL from config
    db_url = config.get('db', {}).get('url', 'postgresql://postgres:postgres@localhost:5432/prod')
    
    # Connect to the database using the URL
    conn = psycopg2.connect(db_url)
    
    # Create a cursor
    cur = conn.cursor()
    
    try:
        # Check if the column already exists
        cur.execute("""
            SELECT column_name 
            FROM information_schema.columns 
            WHERE table_name = 'maintenance_configurations' AND column_name = 'station_id';
        """)
        
        if cur.fetchone() is None:
            # Add the station_id column as a foreign key if it doesn't exist
            cur.execute("""
                ALTER TABLE maintenance_configurations
                ADD COLUMN station_id INTEGER
                REFERENCES stations(id) ON DELETE SET NULL;
            """)
            
            # Create an index for better query performance
            cur.execute("""
                CREATE INDEX IF NOT EXISTS ix_maintenance_configurations_station_id 
                ON maintenance_configurations(station_id);
            """)
            
            print("Added station_id column and index to maintenance_configurations table")
        else:
            print("station_id column already exists in maintenance_configurations table")
        
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
