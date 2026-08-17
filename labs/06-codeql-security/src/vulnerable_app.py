import os
import sqlite3
from flask import Flask, request

app = Flask(__name__)

@app.route("/user")
def get_user():
    # Source: Entrada del usuario
    username = request.args.get("username")
    
    # Sink 1: SQL Injection clásico (CWE-89)
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    query = f"SELECT * FROM users WHERE username = '{username}'"
    cursor.execute(query)
    
    # Sink 2: Command Injection (CWE-78)
    os.system(f"echo Query executed for: {username}")
    
    return "User query processed"

if __name__ == "__main__":
    app.run(port=5000)