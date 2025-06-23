"""
Migration script to update the measurement_data table:
1. Drop columns: SEQUENCE_NUMBER, MEASURE_STEP_NUMBER, UNIT
2. Make BOOKING_ID nullable
"""
import psycopg2
import yaml
from pathlib import Path

def load_config():
    """Load database configuration from config.yml."""
    config_path = Path(__file__).parent.parent.parent.parent.parent.parent / "config.yml"
    with open(config_path, "r") as f:
        config = yaml.safe_load(f)
    return config

def run_migration():
    """Run the migration to update the measurement_data table."""
    config = load_config()
    
    # Get the database URL from config
    db_url = config.get("db", {}).get("url", "postgresql://postgres:postgres@localhost:5432/postgres")
    
    # Connect to the database using the URL
    conn = psycopg2.connect(db_url)
    
    # Create a cursor
    cur = conn.cursor()
    
    try:
        # Start a transaction
        conn.autocommit = False
        
        print("Starting migration for measurement_data table...")
        
        # Drop SEQUENCE_NUMBER column if it exists
        cur.execute("""
        SELECT column_name 
        FROM information_schema.columns 
        WHERE table_name = 'measurement_data' AND column_name = 'SEQUENCE_NUMBER';
        """)
        if cur.fetchone():
            print("Dropping column 'SEQUENCE_NUMBER'...")
            cur.execute("""
            ALTER TABLE measurement_data 
            DROP COLUMN "SEQUENCE_NUMBER";
            """)
        
        # Drop MEASURE_STEP_NUMBER column if it exists
        cur.execute("""
        SELECT column_name 
        FROM information_schema.columns 
        WHERE table_name = 'measurement_data' AND column_name = 'MEASURE_STEP_NUMBER';
        """)
        if cur.fetchone():
            print("Dropping column 'MEASURE_STEP_NUMBER'...")
            cur.execute("""
            ALTER TABLE measurement_data 
            DROP COLUMN "MEASURE_STEP_NUMBER";
            """)
        
        # Drop UNIT column if it exists
        cur.execute("""
        SELECT column_name 
        FROM information_schema.columns 
        WHERE table_name = 'measurement_data' AND column_name = 'UNIT';
        """)
        if cur.fetchone():
            print("Dropping column 'UNIT'...")
            cur.execute("""
            ALTER TABLE measurement_data 
            DROP COLUMN "UNIT";
            """)
        
        # Make BOOKING_ID nullable if it's not already
        cur.execute("""
        SELECT is_nullable 
        FROM information_schema.columns 
        WHERE table_name = 'measurement_data' AND column_name = 'BOOKING_ID';
        """)
        result = cur.fetchone()
        if result and result[0] == 'NO':
            print("Making 'BOOKING_ID' nullable...")
            cur.execute("""
            ALTER TABLE measurement_data 
            ALTER COLUMN "BOOKING_ID" DROP NOT NULL;
            """)
        
        # Update the comment
        print("Updating column comment...")
        cur.execute("""
        COMMENT ON COLUMN measurement_data."BOOKING_ID" IS 'Nullable foreign key to bookings.id';
        """)
        
        # Commit the transaction
        conn.commit()
        print("Migration completed successfully!")
        
    except Exception as e:
        # Rollback in case of error
        conn.rollback()
        print(f"Error during migration: {e}")
        raise
    finally:
        # Close the cursor and connection
        cur.close()
        conn.close()

if __name__ == "__main__":
    run_migration()
