import os
import importlib.util
from pathlib import Path

# Load database password from environment variable instead of hardcoding
DB_PASSWORD = os.getenv("DB_PASSWORD")

def run_user_script(file_path):
    """
    Safely load and execute a user script using importlib instead of exec().
    
    Args:
        file_path: Path to the script to execute
        
    Raises:
        ValueError: If file_path is invalid or unsafe
        FileNotFoundError: If the script file does not exist
    """
    # Validate file path to prevent directory traversal attacks
    file_path = Path(file_path).resolve()
    
    # Ensure the file exists
    if not file_path.exists():
        raise FileNotFoundError(f"Script file not found: {file_path}")
    
    # Ensure the file is a Python file
    if file_path.suffix != ".py":
        raise ValueError(f"Only Python files are allowed: {file_path}")
    
    # Ensure the file is within the current directory (basic sandboxing)
    try:
        file_path.relative_to(Path.cwd())
    except ValueError:
        raise ValueError(f"Script must be in the current directory: {file_path}")
    
    # Safely load the module using importlib
    spec = importlib.util.spec_from_file_location("user_module", file_path)
    if spec is None or spec.loader is None:
        raise ValueError(f"Cannot load module from: {file_path}")
    
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

def connect_database():
    """
    Connect to the database with password from environment variable.
    
    Note: Passwords should NOT be printed to logs in production.
    """
    if DB_PASSWORD is None:
        raise ValueError("DB_PASSWORD environment variable is not set")
    
    # In production, DO NOT print passwords to console
    print("Connecting to DB with credentials from environment variable")
    # Actual database connection logic would go here
    # e.g., connection = psycopg2.connect(host="...", user="...", password=DB_PASSWORD)

if __name__ == "__main__":
    # Set a default password for testing if not provided
    if os.getenv("DB_PASSWORD") is None:
        os.environ["DB_PASSWORD"] = "test_password_123"
    
    run_user_script("user_script.py")
    connect_database()
