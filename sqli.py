import sqlite3

def insecure_query(user_input):
    """
    This function is intentionally vulnerable to SQL injection.
    Never concatenate user input directly into an SQL query like this.
    """
    # Connect to (or create) a test database. In real applications, you'd specify a real DB file or server.
    conn = sqlite3.connect("example.db")
    cursor = conn.cursor()

    # The following line is vulnerable because it directly concatenates untrusted user input into the query.
    query = "SELECT * FROM users WHERE username = '" + user_input + "';"
    
    print("[DEBUG] Executing query:", query)
    
    # Execute the query
    cursor.execute(query)
    rows = cursor.fetchall()
    
    for row in rows:
        print(row)
    
    conn.close()


if __name__ == "__main__":
    # This user input could contain malicious SQL commands that break out of the string and inject new queries.
    user_input = input("Enter username: ")
    insecure_query(user_input)
