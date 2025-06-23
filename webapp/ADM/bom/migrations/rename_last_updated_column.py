"""
Migration script to rename the lastUpdated column to last_updated in the bom_headers table.
This aligns the database schema with the SQLAlchemy model.
"""
import psycopg2
import yaml
from pathlib import Path

def load_config():
    """Load database configuration from config.yml."""
    config_path = Path(__file__).parent.parent.parent.parent.parent / "config.yml"
    with open(config_path, "r") as f:
        config = yaml.safe_load(f)
    return config

def run_migration():
    """Run the migration to rename the lastUpdated column to last_updated in the bom_headers table."""
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
        
        # Check if the lastUpdated column exists
        cur.execute("""
        SELECT column_name 
        FROM information_schema.columns 
        WHERE table_name = 'bom_headers' AND column_name = 'lastUpdated'
        """)
        
        if cur.fetchone():
            print("Renaming 'lastUpdated' column to 'last_updated' in bom_headers table...")
            
            # Rename the column
            cur.execute("""
            ALTER TABLE bom_headers 
            RENAME COLUMN "lastUpdated" TO last_updated;
            """)
            
            print("Column renamed successfully!")
        else:
            # Check if the last_updated column already exists
            cur.execute("""
            SELECT column_name 
            FROM information_schema.columns 
            WHERE table_name = 'bom_headers' AND column_name = 'last_updated'
            """)
            
            if cur.fetchone():
                print("Column 'last_updated' already exists in bom_headers table.")
            else:
                print("Neither 'lastUpdated' nor 'last_updated' column found in bom_headers table.")
                print("Adding 'last_updated' column...")
                
                # Add the last_updated column
                cur.execute("""
                ALTER TABLE bom_headers 
                ADD COLUMN last_updated TIMESTAMP WITHOUT TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP;
                """)
                
                print("Column added successfully!")
        
        # Commit the transaction
        conn.commit()
        print("Migration completed successfully!")
        
    except Exception as e:
        # Rollback in case of error
        conn.rollback()
        print(f"Migration failed: {str(e)}")
        raise
    finally:
        # Close cursor and connection
        cur.close()
        conn.close()

if __name__ == "__main__":
    run_migration()
