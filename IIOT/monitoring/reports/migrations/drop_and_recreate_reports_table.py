"""
Migration script to drop and recreate monitoring_reports table.
"""
import psycopg2
import yaml
import os

def run_migration():
    """Run the migration to drop and recreate monitoring_reports table."""
    # Load config from YAML file
    config_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../../iiot_config.yml'))
    with open(config_path, 'r') as config_file:
        config = yaml.safe_load(config_file)
    
    # Get the database URL from config
    db_url = config.get('db', {}).get('url', 'postgresql://postgres:postgres@localhost:5432/prod')
    
    # Connect to the database using the URL
    conn = psycopg2.connect(db_url)
    
    # Create a cursor
    cur = conn.cursor()
    
    try:
        # Drop the table if it exists
        cur.execute("""
            DROP TABLE IF EXISTS monitoring_reports;
            DROP TYPE IF EXISTS reportstatus;
        """)
        
        # Create the monitoring_reports table
        cur.execute("""
            CREATE TABLE monitoring_reports (
                id SERIAL PRIMARY KEY,
                report_text TEXT NOT NULL,
                status VARCHAR(20) NOT NULL DEFAULT 'PENDING',
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
            CHECK (status IN ('DONE', 'PENDING', 'FAILED'));
        """)
        
        # Commit the changes
        conn.commit()
        print("Monitoring reports table recreated successfully")
        
    except Exception as e:
        conn.rollback()
        print(f"Error during migration: {e}")
        raise
    finally:
        cur.close()
        conn.close()

if __name__ == "__main__":
    run_migration()
