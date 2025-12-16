import mysql.connector
import os

DB_HOST = os.environ.get('DB_HOST', 'localhost')
DB_USER = os.environ.get('DB_USER', 'root')
DB_PASS = os.environ.get('DB_PASS', '')
DB_NAME = os.environ.get('DB_NAME', 'teataimi')

try:
    cnx = mysql.connector.connect(host=DB_HOST, user=DB_USER, password=DB_PASS, database=DB_NAME)
    cur = cnx.cursor()

    # Find pending orders
    cur.execute("SELECT order_id FROM orders WHERE status='Pending'")
    pending = [r[0] for r in cur.fetchall()]
    print('Found pending orders:', pending)

    if pending:
        # Delete order_items for these orders
        cur.execute("DELETE FROM order_items WHERE order_id IN (%s)" % ','.join(['%s']*len(pending)), tuple(pending))
        deleted_items = cur.rowcount
        print('Deleted order_items rows:', deleted_items)

        # Delete the orders themselves
        cur.execute("DELETE FROM orders WHERE order_id IN (%s)" % ','.join(['%s']*len(pending)), tuple(pending))
        deleted_orders = cur.rowcount
        print('Deleted orders rows:', deleted_orders)

        cnx.commit()
    else:
        print('No pending orders found, nothing to delete.')

    cur.close()
    cnx.close()
except Exception as e:
    print('DB error:', e)
