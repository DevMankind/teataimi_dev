#!/usr/bin/env python3
"""Create an admin account in the teataimi database"""

import mysql.connector
import os

# Get DB credentials from environment or defaults
DB_HOST = os.environ.get('DB_HOST', 'localhost')
DB_USER = os.environ.get('DB_USER', 'root')
DB_PASS = os.environ.get('DB_PASS', '')
DB_NAME = os.environ.get('DB_NAME', 'teataimi')

print(f'Connecting to {DB_HOST} as {DB_USER}...')

try:
    conn = mysql.connector.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASS,
        database=DB_NAME
    )
    cursor = conn.cursor()
    
    # Check if admin already exists
    cursor.execute('SELECT user_id FROM users WHERE email=%s', ('admin@teataimi.com',))
    existing = cursor.fetchone()
    
    if existing:
        print('✓ Admin account already exists (user_id: ' + str(existing[0]) + ')')
    else:
        # Insert admin account
        cursor.execute(
            'INSERT INTO users (name, email, phone, password, role, address, created_at) VALUES (%s,%s,%s,%s,%s,%s,NOW())',
            ('Admin User', 'admin@teataimi.com', '0000000000', 'admin123', 'Admin', 'Admin Office')
        )
        conn.commit()
        print('✓ Admin account created successfully!')
        print('  Email: admin@teataimi.com')
        print('  Password: admin123')
        print('  Role: Admin')
        print()
        print('You can now log in at http://127.0.0.1:5000/login')
    
    cursor.close()
    conn.close()
except Exception as e:
    print(f'✗ Error: {e}')
    import traceback
    traceback.print_exc()
