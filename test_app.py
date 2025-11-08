import unittest
from testViewDatabase import app
import mysql.connector

class TestTeaTaimiApp(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        self.client = app.test_client()
        
        # Test database connection
        self.db = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="teataimi"
        )

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