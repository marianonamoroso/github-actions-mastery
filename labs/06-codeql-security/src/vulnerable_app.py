import sqlite3
import os

def get_user_data(user_id):
    # ❌ VULNERABILIDAD INTENCIONAL (SQL Injection) para el scan de CodeQL
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    query = f"SELECT * FROM users WHERE id = '{user_id}'"
    cursor.execute(query)
    return cursor.fetchall()

def execute_system_command(command):
    # ❌ VULNERABILIDAD INTENCIONAL (Command Injection)
    os.system(f"echo Executing: {command}")

if __name__ == "__main__":
    print("Vulnerable application test harness ready.")