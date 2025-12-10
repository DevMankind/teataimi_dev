#!/usr/bin/env python3
import mysql.connector
from datetime import datetime

# Connect to MySQL
db = mysql.connector.connect(
    host='localhost',
    user='root',
    password='',
    database='teataimi'
)

cursor = db.cursor()

try:
    # Insert new admin account with correct spelling
    query = """
    INSERT INTO users (name, email, phone, password, role, address, created_at)
    VALUES (%s, %s, %s, %s, %s, %s, %s)
    """
    data = ('Admin User', 'admin@teataimi.com', '0000000000', 'admin123', 'Admin', 'Admin Office', datetime.now())
    
    cursor.execute(query, data)
    db.commit()
    
    print(f"✓ Admin account created successfully!")
    print(f"  Email: admin@teataimi.com")
    print(f"  Password: admin123")
    print(f"  Role: Admin")
    
except mysql.connector.Error as err:
    print(f"✗ Database error: {err}")
finally:
    cursor.close()
    db.close()
