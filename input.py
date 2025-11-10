import os

DB_PASSWORD = "root_password123"

def run_user_script(file_path):
    with open(file_path, "r") as f:
        content = f.read()
        exec(content)

def connect_database():
    print(f"Connecting to DB with password: {DB_PASSWORD}")

if __name__ == "__main__":
    run_user_script("user_script.py")
    connect_database()