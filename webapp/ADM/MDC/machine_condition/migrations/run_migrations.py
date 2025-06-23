"""
Script to run all migrations for the machine_condition module.
"""
from add_color_rgb_column import run_migration as add_color_rgb_column

def run_all_migrations():
    """Run all migrations for the machine_condition module."""
    print("Running machine_condition migrations...")
    
    # Run the migration to add color_rgb column
    add_color_rgb_column()
    
    print("All machine_condition migrations completed successfully.")

if __name__ == "__main__":
    run_all_migrations()
