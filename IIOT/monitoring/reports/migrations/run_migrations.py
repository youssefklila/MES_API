"""
Script to run all migrations for the monitoring reports module.
"""
from IIOT.monitoring.reports.migrations.create_reports_table import run_migration as create_reports_table

def run_all_migrations():
    """Run all migrations for the monitoring reports module."""
    print("Running monitoring reports migrations...")
    
    # Run the migration to create reports table
    create_reports_table()
    
    print("All monitoring reports migrations completed successfully.")

if __name__ == "__main__":
    run_all_migrations()
