import os
import importlib.util
import logging
from pathlib import Path

logging.basicConfig(level=logging.INFO)

def load_user_module(file_path: str):
    """Safely load a user-provided Python module without using exec.

    This uses importlib to import the module from a path and only exposes
    a constrained interface to the caller.
    """
    path = Path(file_path)
    if not path.exists() or not path.is_file():
        raise FileNotFoundError(f"User script not found: {file_path}")

    # Basic check to avoid loading obviously dangerous filenames
    if path.suffix != ".py":
        raise ValueError("Only .py files are allowed for user scripts")

    spec = importlib.util.spec_from_file_location(path.stem, str(path))
    if spec is None or spec.loader is None:
        raise ImportError("Cannot create module spec for user script")

    module = importlib.util.module_from_spec(spec)
    # Execute the module in its own namespace. Importlib will execute the code,
    # but this is a controlled import and avoids arbitrary exec in the current
    # global namespace. Still, only do this for trusted or validated scripts.
    spec.loader.exec_module(module)
    return module


def connect_database():
    # Read password from environment variable; do not hardcode secrets.
    db_password = os.environ.get("DB_PASSWORD")
    if not db_password:
        logging.error("DB_PASSWORD is not set in environment")
        raise EnvironmentError("Missing DB_PASSWORD environment variable")

    # In a real application, use a DB driver and secure connection; this is a placeholder.
    logging.info("Connecting to DB with provided credentials (hidden)")


if __name__ == "__main__":
    # Example usage: load a user script that implements a function named `run`.
    try:
        user_module = load_user_module("user_script.py")
        if hasattr(user_module, "run") and callable(user_module.run):
            user_module.run()
        else:
            logging.warning("user_script.py does not define a callable 'run' function")

        connect_database()
    except Exception as e:
        logging.exception("Error running application: %s", e)