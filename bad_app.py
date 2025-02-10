#!/usr/bin/env python3
"""
This script is deliberately riddled with security flaws.
It demonstrates how not to handle user input, database operations,
file access, and command execution.

WARNING: Do NOT use this code in a real production environment!
"""

import os
import sqlite3
import hashlib

# 1. Hardcoded credentials (Sensitive Information Exposure)
#    Storing credentials in code is dangerous.
DB_NAME = "insecure_db.sqlite"
ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "password123"  # Hard-coded password

def init_db():
    """
    Create a sample table if it doesn't already exist.
    """
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT,
            password TEXT
        )
    """)
    conn.commit()
    conn.close()

def insecure_login(username, password):
    """
    Demonstrates multiple vulnerabilities:
    - Uses SQL string concatenation -> SQL injection possibility.
    - Stores and checks passwords in plaintext (or weakly hashed).
    """
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    # 2. SQL Injection vulnerability
    #    User input is directly concatenated into the SQL query string.
    query = f"SELECT * FROM users WHERE username='{username}' AND password='{password}'"
    print("[DEBUG] Executing query:", query)  # Debug output exposing sensitive info
    cursor.execute(query)
    
    row = cursor.fetchone()
    conn.close()

    if row:
        return True
    return False

def insecure_register(username, password):
    """
    Demonstrates additional poor practices:
    - Weak (MD5) password hashing (or none at all).
    - No checks for strong passwords or duplicates.
    """
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    # 3. Weak cryptographic function (MD5)
    #    MD5 is considered broken for many security-critical uses.
    hashed_password = hashlib.md5(password.encode()).hexdigest()
    
    # 4. Again, direct SQL concatenation -> SQL injection possibility.
    query = f"INSERT INTO users (username, password) VALUES ('{username}', '{hashed_password}')"
    print("[DEBUG] Executing insert:", query)
    cursor.execute(query)
    
    conn.commit()
    conn.close()

def insecure_shell():
    """
    Demonstrates command injection vulnerability:
    - os.system() call directly uses user input with no sanitization.
    """
    cmd = input("Enter a shell command to execute: ")
    # 5. Command Injection vulnerability
    os.system(cmd)

def main():
    """
    A simple menu-driven interface with multiple insecurities.
    """
    init_db()

    print("1. Register a new user")
    print("2. Log in")
    print("3. Run a shell command (INSECURE)")
    choice = input("Choose an option: ")

    if choice == '1':
        username = input("Enter desired username: ")
        password = input("Enter desired password: ")
        insecure_register(username, password)
        print("User registered!")
    elif choice == '2':
        username = input("Enter username: ")
        password = input("Enter password: ")
        if insecure_login(username, password):
            print("Successfully logged in!")
        else:
            print("Login failed.")
    elif choice == '3':
        insecure_shell()
    else:
        print("Invalid option.")

    # 6. Storing sensitive data in a world-readable file
    #    (Credentials are being logged in plaintext).
    with open("insecure_log.txt", "a") as f:
        f.write(f"Last action by user '{username}' with password '{password}'\n")

    # 7. Hard-coded admin check with insecure approach:
    if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
        print("Welcome, Admin! You have all the power.")
        # Example of doing something only an admin should do
        # But it's trivially bypassed if someone obtains the hard-coded password
    else:
        print("You are not the admin.")

if __name__ == "__main__":
    main()
