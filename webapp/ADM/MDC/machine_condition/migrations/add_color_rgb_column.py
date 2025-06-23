"""
Migration script to add color_rgb column to machine_conditions table.
"""
import psycopg2
import yaml
import os

def run_migration():
    """Run the migration to add color_rgb column to machine_conditions table."""
    # Load config from YAML file
    config_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../../../config.yml'))
    with open(config_path, 'r') as config_file:
        config = yaml.safe_load(config_file)
    
    # Get the database URL from config
    db_url = config.get('db', {}).get('url', 'postgresql://postgres:postgres@localhost:5432/postgres')
    
    # Connect to the database using the URL
    conn = psycopg2.connect(db_url)
    
    # Create a cursor
    cur = conn.cursor()
    
    try:
        # Check if the column already exists
        cur.execute("""
            SELECT column_name 
            FROM information_schema.columns 
            WHERE table_name = 'machine_conditions' AND column_name = 'color_rgb';
        """)
        
        if cur.fetchone() is None:
            # Add the color_rgb column if it doesn't exist
            cur.execute("""
                ALTER TABLE machine_conditions
                ADD COLUMN color_rgb VARCHAR(20);
            """)
            print("Added color_rgb column to machine_conditions table")
        else:
            print("color_rgb column already exists in machine_conditions table")
        
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
