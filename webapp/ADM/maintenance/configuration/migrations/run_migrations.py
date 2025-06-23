"""
Script to run all migrations for the maintenance configuration module.
"""
from webapp.ADM.maintenance.configuration.migrations.add_port_column import run_migration as add_port_column
from webapp.ADM.maintenance.configuration.migrations.add_station_id_column import run_migration as add_station_id_column

def run_all_migrations():
    """Run all migrations for the maintenance configuration module."""
    print("Running maintenance configuration migrations...")
    
    # Run the migration to add port column
    add_port_column()
    
    # Run the migration to add station_id column
    add_station_id_column()
    
    print("All maintenance configuration migrations completed successfully.")

if __name__ == "__main__":
    run_all_migrations()
