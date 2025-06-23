"""
Script to run all migrations for the monitoring tasks module.
"""
from IIOT.monitoring.tasks.migrations.create_tasks_table import run_migration as create_tasks_table

def run_all_migrations():
    """Run all migrations for the monitoring tasks module."""
    print("Running monitoring tasks migrations...")
    
    # Run the migration to create tasks table
    create_tasks_table()
    
    print("All monitoring tasks migrations completed successfully.")

if __name__ == "__main__":
    run_all_migrations()
