"""
Migration script to create monitoring_reports table.
"""
import psycopg2
import yaml
import os

def run_migration():
    """Run the migration to create monitoring_reports table."""
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
                WHERE table_name = 'monitoring_reports'
            );
        """)
        
        if not cur.fetchone()[0]:
            # Create the monitoring_reports table if it doesn't exist
            cur.execute("""
                CREATE TABLE monitoring_reports (
                    id SERIAL PRIMARY KEY,
                    report_text TEXT NOT NULL,
                    status VARCHAR(20) NOT NULL DEFAULT 'pending',
                    submitted_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
                );
                
                -- Create an enum type for report status
                DO $$ 
                BEGIN
                    IF NOT EXISTS (SELECT 1 FROM pg_type WHERE typname = 'reportstatus') THEN
                        CREATE TYPE reportstatus AS ENUM ('DONE', 'PENDING', 'FAILED');
                    END IF;
                END $$;
                
                -- Add constraint to ensure status is one of the allowed values
                ALTER TABLE monitoring_reports 
                ADD CONSTRAINT valid_status 
                CHECK (status IN ('done', 'pending', 'failed'));
            """)
            print("Created monitoring_reports table")
        else:
            print("monitoring_reports table already exists")
        
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
