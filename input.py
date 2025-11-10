import os
import re
import logging

logging.basicConfig(level=logging.INFO)

# Use environment variable for secrets; never hardcode credentials in source.
def get_db_password():
    return os.getenv("DB_PASSWORD")

def run_user_script(file_path):
    """
    Securely run a user-provided script only when the script is explicitly
    located in a 'safe_scripts' directory and contains only safe statements
    (prints).

    This prevents remote code execution from arbitrary files.
    """
    # Only allow scripts explicitly in a safe directory
    base = os.path.abspath(os.path.join(os.getcwd(), "safe_scripts"))
    tgt = os.path.abspath(file_path)
    if not tgt.startswith(base + os.sep):
        raise ValueError("Only scripts inside 'safe_scripts' can be executed")

    with open(tgt, "r", encoding="utf-8") as f:
        content = f.read()

    # Only allow simple print statements in safe scripts
    allowed_pattern = re.compile(r'^(\s*print\(.+\)\s*\n?)+$')
    if not allowed_pattern.match(content):
        raise ValueError("Script contains disallowed statements; only print() allowed")

    # Execute in a restricted global environment with no builtins besides print
    safe_globals = {"__builtins__": {"print": print}}
    exec(compile(content, tgt, 'exec'), safe_globals, {})

def connect_database():
    password = get_db_password()
    if not password:
        raise RuntimeError("DB_PASSWORD not set in environment")

    # Connect to DB using a driver here (omitted); never log or print the password.
    logging.info("Connecting to database using a secure connection (password hidden)")

if __name__ == "__main__":
    # Create safe folder if missing
    os.makedirs("safe_scripts", exist_ok=True)

    # Only run user scripts that have been placed in the safe_scripts folder.
    try:
        run_user_script("safe_scripts/user_script.py")
    except Exception as e:
        logging.error("Skipping user script: %s", e)

    # db password must come from environment variable
    try:
        connect_database()
    except Exception as e:
        logging.error("DB connection not configured: %s", e)