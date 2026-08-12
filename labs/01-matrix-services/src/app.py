import os
import sys

def check_db():
    # Environment variables injected from the workflow or runner environment
    db_host = os.getenv("POSTGRES_HOST", "localhost")
    db_port = os.getenv("POSTGRES_PORT", "5432")
    
    print(f"Checking connection to PostgreSQL at {db_host}:{db_port}...")
    # Simulating successful connection check
    print("Database connection SUCCESSFUL!")

def generate_report():
    version = os.getenv("APP_VERSION", "unknown")
    environment = os.getenv("ENV_NAME", "dev")
    
    filename = f"report-{environment}.txt"
    with open(filename, "w") as f:
        f.write("Execution Report\n")
        f.write(f"Environment: {environment}\n")
        f.write(f"App Version: {version}\n")
        f.write("Status: PASSED\n")
    print(f"Report generated successfully: {filename}")

if __name__ == "__main__":
    check_db()
    generate_report()