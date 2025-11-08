import unittest
from testViewDatabase import app
import mysql.connector
import os


class TestTeaTaimiApp(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        self.client = app.test_client()
        
        # Test database connection from environment or defaults
        DB_HOST = os.environ.get('DB_HOST', 'localhost')
        DB_USER = os.environ.get('DB_USER', 'root')
        DB_PASS = os.environ.get('DB_PASS', '')
        DB_NAME = os.environ.get('DB_NAME', 'teataimi')
        self.db = mysql.connector.connect(host=DB_HOST, user=DB_USER, password=DB_PASS, database=DB_NAME)

    def test_home_page(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        
    def test_customers_page(self):
        response = self.client.get('/customers')
        self.assertEqual(response.status_code, 200)
        
    def test_orders_page(self):
        response = self.client.get('/orders')
        self.assertEqual(response.status_code, 200)
        
    def test_place_order_page(self):
        response = self.client.get('/place_order')
        self.assertEqual(response.status_code, 200)
        
    def test_database_connection(self):
        cursor = self.db.cursor()
        cursor.execute("SELECT 1")
        result = cursor.fetchone()
        self.assertEqual(result[0], 1)

if __name__ == '__main__':
    unittest.main()