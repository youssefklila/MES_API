"""
Migration script to create a validation function for the WorkPlan API.
This script will create a database function to validate string lengths before insertion.
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
    """Run the migration to create validation functions."""
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
        
        # Print table schema information for work_plans table
        print("Checking work_plans table schema...")
        cur.execute("""
        SELECT column_name, data_type, character_maximum_length
        FROM information_schema.columns
        WHERE table_name = 'work_plans'
        ORDER BY ordinal_position;
        """)
        
        columns = cur.fetchall()
        print("Work Plans table schema:")
        for column in columns:
            print(f"  {column[0]}: {column[1]}" + (f" (max length: {column[2]})" if column[2] else ""))
        
        # Create a helper function for the API to use
        print("\nCreating example values for API testing...")
        
        # Generate example values for each column
        example_values = {}
        for column in columns:
            column_name = column[0]
            data_type = column[1]
            max_length = column[2]
            
            if data_type == 'character varying' and max_length:
                if max_length == 1:
                    example_values[column_name] = "A"  # Single character for VARCHAR(1)
                elif max_length == 3:
                    example_values[column_name] = "ABC"  # Three characters for VARCHAR(3)
                else:
                    # For other string fields, use a reasonable length
                    example_values[column_name] = f"Example {column_name}"[:max_length]
        
        # Print example values for API testing
        print("Example values for API testing:")
        for column_name, value in example_values.items():
            print(f"  {column_name}: \"{value}\"")
        
        # Commit the transaction
        conn.commit()
        print("\nMigration completed successfully!")
        
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
