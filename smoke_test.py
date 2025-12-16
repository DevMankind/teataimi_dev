import requests
import datetime
import sys

BASE = 'http://127.0.0.1:5000'
ADMIN_EMAIL = 'admin@teataimi.com'
ADMIN_PASS = 'admin123'

s = requests.Session()

try:
    print('Logging in...')
    r = s.post(f'{BASE}/api/login', json={'email': ADMIN_EMAIL, 'password': ADMIN_PASS}, timeout=10)
    print('Login status:', r.status_code)
    try:
        print('Login response:', r.json())
    except Exception:
        print('Login response text:', r.text)
    if not r.ok:
        print('Login failed, aborting')
        sys.exit(2)

    print('\nFetching products...')
    r = s.get(f'{BASE}/api/products', timeout=10)
    print('Products status:', r.status_code)
    products = []
    try:
        products = r.json()
    except Exception as e:
        print('Failed to parse products JSON:', e)
    if not products:
        print('No products available, aborting')
        sys.exit(3)

    product = products[0]
    pid = product.get('product_id') or product.get('id') or product.get('productId')
    print('Using product:', pid, product.get('product_name') if 'product_name' in product else product)

    items = [{'product_id': pid, 'quantity': 1}]
    payload = {
        'items': items,
        'delivery_date': datetime.date.today().isoformat(),
        'delivery_method': 'Pickup'
    }

    print('\nPlacing order...')
    r = s.post(f'{BASE}/api/place-order', json=payload, timeout=15)
    print('Place-order status:', r.status_code)
    try:
        print('Place-order response:', r.json())
    except Exception:
        print('Place-order response text:', r.text)
    if r.ok:
        print('SMOKE TEST: SUCCESS')
        sys.exit(0)
    else:
        print('SMOKE TEST: FAILED')
        sys.exit(4)

except requests.exceptions.RequestException as e:
    print('Network/Request error:', e)
    sys.exit(1)
