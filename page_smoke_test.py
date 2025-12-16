import requests
import sys

BASE = 'http://127.0.0.1:5000'
PAGES = [
    '/',
    '/index.html',
    '/about.html',
    '/admin-dashboard.html',
    '/cart.html',
    '/checkout.html',
    '/login.html',
    '/menu.html',
    '/order-history.html',
    '/register.html',
    '/success.html',
    '/track.html'
]

failed = []

print('Testing pages on', BASE)
for p in PAGES:
    url = BASE + p
    try:
        r = requests.get(url, timeout=10)
        status = r.status_code
        length = len(r.text or '')
        has_title = '<title' in (r.text or '').lower()
        ok = (status == 200 and length > 0)
        print(f"{p:20} -> {status} {'OK' if ok else 'FAIL'} (len={length}) title={'yes' if has_title else 'no'})")
        if not ok:
            failed.append((p, status, length))
    except Exception as e:
        print(f"{p:20} -> ERROR: {e}")
        failed.append((p, 'error', str(e)))

print('\nSUMMARY:')
if not failed:
    print('All pages passed (HTTP 200 with content).')
    sys.exit(0)
else:
    print(f"Failed pages: {len(failed)}")
    for f in failed:
        print(f)
    sys.exit(2)
