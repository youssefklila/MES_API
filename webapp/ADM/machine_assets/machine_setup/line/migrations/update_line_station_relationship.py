"""
Migration script to update the line-station relationship to many-to-many.
"""
import os
import sys
import yaml
import psycopg2
from psycopg2 import sql
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

def run_migration():
    """Run the migration to update line-station relationship."""
    # Load config from YAML file
    config_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../../../../config.yml'))
    print(f"Loading config from: {config_path}")
    with open(config_path, 'r') as config_file:
        config = yaml.safe_load(config_file)
    
    # Get the database URL from config
    db_url = config.get('db', {}).get('url', 'postgresql://postgres:postgres@localhost:5432/postgres')
    
    # Connect to the database using the URL
    conn = psycopg2.connect(db_url)
    conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    
    # Create a cursor
    cur = conn.cursor()
    
    try:
        print("Starting migration: Update line-station relationship to many-to-many")
        
        # 1. Create the new association table
        print("Creating line_station_association table...")
        cur.execute("""
            CREATE TABLE IF NOT EXISTS line_station_association (
                line_id INTEGER NOT NULL,
                station_id INTEGER NOT NULL,
                created_at TIMESTAMP WITHOUT TIME ZONE NOT NULL DEFAULT NOW(),
                PRIMARY KEY (line_id, station_id),
                FOREIGN KEY (line_id) REFERENCES lines (id) ON DELETE CASCADE,
                FOREIGN KEY (station_id) REFERENCES stations (id) ON DELETE CASCADE
            );
        """)
        
        # 2. Migrate existing line-station relationships to the new table
        print("Migrating existing line-station relationships...")
        cur.execute("""
            INSERT INTO line_station_association (line_id, station_id, created_at)
            SELECT id, station_id, NOW()
            FROM lines
            WHERE station_id IS NOT NULL
            ON CONFLICT DO NOTHING;
        """)
        
        # 3. Drop the old foreign key constraint
        print("Dropping old foreign key constraints...")
        cur.execute("""
            SELECT conname FROM pg_constraint 
            WHERE conrelid = 'lines'::regclass 
            AND conname = 'lines_station_id_fkey';
        """)
        if cur.fetchone():
            cur.execute("""
                ALTER TABLE lines DROP CONSTRAINT lines_station_id_fkey;
            """)
        
        # 4. Drop the old station_id column
        print("Dropping old station_id column...")
        cur.execute("""
            SELECT column_name 
            FROM information_schema.columns 
            WHERE table_name='lines' AND column_name='station_id';
        """)
        if cur.fetchone():
            cur.execute("""
                ALTER TABLE lines DROP COLUMN station_id;
            """)
        
        conn.commit()
        print("Migration completed successfully!")
        
    except Exception as e:
        conn.rollback()
        print(f"Error during migration: {e}")
        raise
    finally:
        cur.close()
        conn.close()

if __name__ == "__main__":
    run_migration()
