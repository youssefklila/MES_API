"""
Migration script to fix client_id validation issues in company_codes table.
This script ensures that all company_codes records have a valid client_id.
"""
import psycopg2
import yaml
from pathlib import Path

def load_config():
    """Load database configuration from config.yml."""
    config_path = Path(__file__).parent.parent.parent.parent.parent.parent.parent / "config.yml"
    with open(config_path, "r") as f:
        config = yaml.safe_load(f)
    return config

def run_migration():
    """Run the migration to fix client_id validation issues."""
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
        
        # 1. Check if there are any company_codes with NULL client_id
        cur.execute("SELECT COUNT(*) FROM company_codes WHERE client_id IS NULL")
        null_count = cur.fetchone()[0]
        print(f"Found {null_count} company_codes with NULL client_id")
        
        if null_count > 0:
            # 2. Get the first client_id from the clients table
            cur.execute("SELECT id FROM clients LIMIT 1")
            result = cur.fetchone()
            
            if result:
                default_client_id = result[0]
                print(f"Using default client_id: {default_client_id}")
                
                # 3. Update company_codes with NULL client_id to use the default client_id
                cur.execute(f"UPDATE company_codes SET client_id = {default_client_id} WHERE client_id IS NULL")
                print(f"Updated {cur.rowcount} company_codes with default client_id")
            else:
                print("No clients found in the database. Cannot fix company_codes.")
                return
        
        # 4. Check if the schema needs to be modified to make client_id NOT NULL
        cur.execute("""
        SELECT is_nullable 
        FROM information_schema.columns 
        WHERE table_name = 'company_codes' AND column_name = 'client_id'
        """)
        is_nullable = cur.fetchone()[0]
        
        if is_nullable == 'YES':
            print("Modifying company_codes schema to make client_id NOT NULL")
            cur.execute("ALTER TABLE company_codes ALTER COLUMN client_id SET NOT NULL")
        
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
