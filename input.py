import os
import sys
import subprocess
import logging
from pathlib import Path

logging.basicConfig(level=logging.INFO)

def get_db_password():
    # Load DB password from environment variable. If not present, raise an error.
    password = os.environ.get("DB_PASSWORD")
    if not password:
        raise RuntimeError("DB_PASSWORD is not set in environment")
    return password

def run_user_script(script_name, scripts_dir="scripts", timeout=5):
    """Run an allowed user script located under `scripts_dir` safely in a subprocess.

    Only scripts within the `scripts_dir` directory are allowed. The function runs the
    script in a new process with default environment and a timeout. It captures output
    and communicates errors rather than executing the code inline.
    """
    scripts_dir = Path(scripts_dir).resolve()
    script_path = (scripts_dir / script_name).resolve()

    # Ensure the script is actually in the scripts directory (prevent traversal)
    if not str(script_path).startswith(str(scripts_dir) + os.sep):
        raise ValueError("Script path is outside allowed scripts directory")

    if script_path.suffix != ".py":
        raise ValueError("Only .py scripts are allowed")

    if not script_path.exists():
        raise FileNotFoundError(f"Script {script_path} not found")

    # Run the script in a subprocess to avoid executing arbitrary code inside this process
    try:
        logging.info("Running user script: %s", script_path)
        result = subprocess.run([sys.executable, str(script_path)], capture_output=True, text=True, timeout=timeout, check=True)
        logging.info("Script stdout:\n%s", result.stdout)
        if result.stderr:
            logging.warning("Script stderr:\n%s", result.stderr)
        return result.returncode
    except subprocess.CalledProcessError as e:
        logging.error("User script failed with return code %s", e.returncode)
        logging.error(e.stderr)
        raise
    except subprocess.TimeoutExpired:
        logging.error("User script timed out")
        raise

def connect_database():
    # Get password securely without logging it.
    password = get_db_password()
    # For the purpose of this demo, we only print a non-sensitive confirmation.
    logging.info("Connecting to DB using configured password (redacted)")
    # Here you would create a DB connection, e.g. use a database driver with password.
    return True


if __name__ == "__main__":
    # Example usage; this will raise if the environment isn't prepared.
    try:
        run_user_script("user_script.py")
    except Exception as e:
        logging.error("Failed to run user script: %s", e)

    try:
        connect_database()
    except Exception as e:
        logging.error("Failed to connect to DB: %s", e)