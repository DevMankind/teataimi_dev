import mysql.connector
import os

DB_HOST = os.environ.get('DB_HOST', 'localhost')
DB_USER = os.environ.get('DB_USER', 'root')
DB_PASS = os.environ.get('DB_PASS', '')
DB_NAME = os.environ.get('DB_NAME', 'teataimi')
ORDER_ID = 12207

try:
    cnx = mysql.connector.connect(host=DB_HOST, user=DB_USER, password=DB_PASS, database=DB_NAME)
    cur = cnx.cursor(dictionary=True)

    cur.execute("SELECT order_id, user_id, order_date, delivery_date, status, total_amount FROM orders WHERE order_id = %s", (ORDER_ID,))
    order = cur.fetchone()
    print('ORDER ROW:')
    print(order)

    cur.execute("SELECT oi.order_item_id, oi.order_id, oi.product_id, p.product_name, oi.quantity, oi.price FROM order_items oi LEFT JOIN products p ON oi.product_id = p.product_id WHERE oi.order_id = %s", (ORDER_ID,))
    items = cur.fetchall()
    print('\nORDER ITEMS:')
    for it in items:
        print(it)

    cur.close()
    cnx.close()
except Exception as e:
    print('DB error:', e)
