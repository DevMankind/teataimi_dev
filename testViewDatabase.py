from flask import Flask, render_template_string, request, redirect, url_for
import mysql.connector
from datetime import datetime

app = Flask(__name__)

# Connect to MySQL database
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="teataimi"
)

@app.route('/')
def index():
    cursor = db.cursor(dictionary=True)

    tables = ['users', 'products', 'orders', 'order_items']
    data = {}

    for table in tables:
        cursor.execute(f"SELECT * FROM {table}")
        data[table] = cursor.fetchall()

    html = """
    <html>
    <head>
        <title>TeaTaiMi Management System</title>
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <style>
            :root{
                --teal: #0f6b75;
                --teal-dark: #0b5257;
                --light-blue: #e6f5f6;
                --muted: #6c757d;
                --card-bg: #f1fbfc;
            }
            body { font-family: 'Segoe UI', Arial, sans-serif; margin:0; background: #f4f7f8; color:#21313a; }
            .topbar { background: var(--teal); color: #fff; padding:18px 0; box-shadow: 0 2px 6px rgba(11,82,87,0.12); }
            .topbar .wrap { max-width:1100px;margin:0 auto;padding:0 16px; display:flex; align-items:center; justify-content:space-between }
            .brand { font-size:1.25rem; font-weight:700; letter-spacing:0.4px }
            .brand small{ display:block; font-weight:400; font-size:0.85rem; opacity:0.9 }
            .nav { display:flex; gap:8px }
            .nav a { background: rgba(255,255,255,0.08); color:#fff; padding:8px 12px; border-radius:6px; text-decoration:none; font-size:0.95rem }
            .nav a:hover{ background: rgba(255,255,255,0.14) }
            .wrap { max-width:1100px;margin:20px auto;padding:0 16px }
            .grid { display:grid; grid-template-columns: 1fr; gap:16px }
            @media(min-width:900px){ .grid { grid-template-columns: 1fr 320px } }
            .card { background: var(--card-bg); padding:18px; border-radius:8px; box-shadow: 0 1px 4px rgba(0,0,0,0.06) }
            .card h2{ margin:0 0 12px 0; color:var(--teal-dark) }
            table{ width:100%; border-collapse:collapse; margin-top:8px }
            th, td{ padding:10px 12px; border-bottom:1px solid #e9eef0; text-align:left }
            th{ background:var(--teal); color:#fff; font-weight:600; }
            tr:nth-child(even){ background: var(--light-blue) }
            .muted{ color:var(--muted); font-size:0.95rem }
            .right { text-align:right }
            .status { padding:6px 10px; border-radius:14px; font-size:0.85rem }
            .status-Pending{ background:#ffeaa7 }
            .status-In-Progress{ background:#fab1a0 }
            .status-Completed{ background:#55efc4 }
            .status-Delivered{ background:#74b9ff }
            .small { font-size:0.9rem }
            .actions button, .btn { background:var(--teal); color:#fff; border:none; padding:8px 12px; border-radius:6px; cursor:pointer }
            .actions select{ padding:6px }
        </style>
    </head>
    <body>
        <div class="topbar">
            <div class="wrap">
                <div class="brand">TeaTaiMi <small>Management Dashboard</small></div>
                <div class="nav">
                    {% for table in data.keys() %}
                        <a href="#{{ table }}">{{ table.replace('_', ' ').title() }}</a>
                    {% endfor %}
                    <a href="/customers">Customers</a>
                    <a href="/orders">Orders</a>
                    <a href="/place_order">Place Order</a>
                </div>
            </div>
        </div>

        <div class="wrap">
            <div class="grid">
                <div>
                    {% for table, rows in data.items() %}
                        <div id="{{ table }}" class="card">
                            <h2>{{ table.replace('_', ' ').title() }}</h2>
                            {% if rows %}
                                <table>
                                    <tr>
                                        {% for col in rows[0].keys() %}
                                            <th>{{ col.replace('_', ' ').title() }}</th>
                                        {% endfor %}
                                    </tr>
                                    {% for row in rows %}
                                        <tr>
                                            {% for key, val in row.items() %}
                                                <td>
                                                    {% if key == 'status' %}
                                                        <span class="status status-{{ val.replace(' ', '-') }}">{{ val }}</span>
                                                    {% elif key == 'price' or key == 'total_amount' %}
                                                        RM {{ "%.2f"|format(val|float) }}
                                                    {% elif key == 'description' and val|length > 100 %}
                                                        {{ val[:100] }}...
                                                    {% else %}
                                                        {{ val }}
                                                    {% endif %}
                                                </td>
                                            {% endfor %}
                                        </tr>
                                    {% endfor %}
                                </table>
                            {% else %}
                                <p class="muted">No data available in this table.</p>
                            {% endif %}
                        </div>
                    {% endfor %}
                </div>

                <div>
                    <div class="card">
                        <h2>Quick Actions</h2>
                        <p class="small">Place orders, view recent activity, or manage customers quickly.</p>
                        <div style="margin-top:12px;display:flex;gap:8px">
                            <a class="btn" href="/place_order">Place Order</a>
                            <a class="btn" href="/customers">Customers</a>
                        </div>
                    </div>
                    <div class="card" style="margin-top:12px">
                        <h2>Summary</h2>
                        <p class="muted">Total tables: {{ data|length }}</p>
                        <p class="muted">Last updated: {{ now() if false else '' }}</p>
                    </div>
                </div>
            </div>
        </div>
    </body>
    </html>
    """
    return render_template_string(html, data=data)

# Customers: view and add
@app.route('/customers', methods=['GET', 'POST'])
def customers():
    cursor = db.cursor(dictionary=True)
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        phone = request.form.get('phone')
        password = request.form.get('password')
        address = request.form.get('address')
        cursor.execute("INSERT INTO users (name, email, phone, password, role, address, created_at) VALUES (%s,%s,%s,%s,'Customer',%s,NOW())", (name, email, phone, password, address))
        db.commit()
        return redirect(url_for('customers'))

    cursor.execute("SELECT * FROM users WHERE role='Customer'")
    customers = cursor.fetchall()
    html = """
    <html>
    <head>
        <title>Customers - TeaTaiMi</title>
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <style>
            /* reuse the same variables from main page for simpler styling */
            :root{ --teal:#0f6b75; --card-bg:#f1fbfc; --muted:#6c757d }
            body{ font-family:'Segoe UI', Arial, sans-serif; margin:0; background:#f4f7f8 }
            .topbar{ background:var(--teal); color:#fff; padding:14px 0 }
            .topbar .wrap{ max-width:1100px;margin:0 auto;padding:0 16px; display:flex;align-items:center;justify-content:space-between }
            .wrap{ max-width:1100px;margin:20px auto;padding:0 16px }
            .card{ background:var(--card-bg); padding:16px;border-radius:8px }
            h1{ margin:0 0 12px 0 }
            table{ width:100%; border-collapse:collapse; margin-top:12px }
            th,td{ padding:10px; border-bottom:1px solid #e9eef0; text-align:left }
            th{ background:var(--teal); color:#fff }
            .btn{ background:var(--teal); color:#fff; padding:8px 12px; border-radius:6px; text-decoration:none }
        </style>
    </head>
    <body>
        <div class="topbar"><div class="wrap"><div>TeaTaiMi</div><div><a class="btn" href="/">Home</a></div></div></div>
        <div class="wrap">
            <div class="card">
                <h1>Customers</h1>
                <form method="post" style="margin-bottom:16px">
                    <div style="display:grid;grid-template-columns:1fr 1fr;gap:10px">
                        <input name="name" placeholder="Name" required>
                        <input name="email" type="email" placeholder="Email" required>
                        <input name="phone" placeholder="Phone">
                        <input name="password" placeholder="Password" required>
                    </div>
                    <div style="margin-top:8px"><textarea name="address" placeholder="Address" style="width:100%"></textarea></div>
                    <div style="margin-top:10px"><button class="btn" type="submit">Add Customer</button></div>
                </form>

                <h2>Customer List</h2>
                <table>
                    <tr><th>ID</th><th>Name</th><th>Email</th><th>Phone</th><th>Address</th><th>Created At</th></tr>
                    {% for c in customers %}
                        <tr>
                            <td>{{ c.user_id }}</td>
                            <td>{{ c.name }}</td>
                            <td>{{ c.email }}</td>
                            <td>{{ c.phone }}</td>
                            <td>{{ c.address }}</td>
                            <td>{{ c.created_at }}</td>
                        </tr>
                    {% endfor %}
                </table>
            </div>
        </div>
    </body>
    </html>
    """
    return render_template_string(html, customers=customers)


# Orders: view and update status
@app.route('/orders', methods=['GET'])
def orders():
    cursor = db.cursor(dictionary=True)
    cursor.execute("""
        SELECT o.*, u.name as customer_name
        FROM orders o
        LEFT JOIN users u ON o.user_id = u.user_id
        ORDER BY o.order_date DESC
    """)
    orders = cursor.fetchall()

    # fetch items for each order
    for o in orders:
        cursor.execute("SELECT oi.*, p.product_name FROM order_items oi LEFT JOIN products p ON oi.product_id = p.product_id WHERE oi.order_id=%s", (o['order_id'],))
        o['items'] = cursor.fetchall()

    html = """
        <html>
        <head>
            <title>Orders - TeaTaiMi</title>
            <meta name="viewport" content="width=device-width, initial-scale=1">
            <style>
                :root{ --teal:#0f6b75; --card-bg:#f1fbfc; --muted:#6c757d; --light-blue:#e6f5f6 }
                body{ font-family:'Segoe UI', Arial, sans-serif; margin:0; background:#f4f7f8 }
                .topbar{ background:var(--teal); color:#fff; padding:14px 0 }
                .topbar .wrap{ max-width:1100px;margin:0 auto;padding:0 16px; display:flex;align-items:center;justify-content:space-between }
                .wrap{ max-width:1100px;margin:20px auto;padding:0 16px }
                .card{ background:var(--card-bg); padding:18px;border-radius:8px }
                table{ width:100%; border-collapse:collapse; margin-top:12px }
                th,td{ padding:10px; border-bottom:1px solid #e9eef0; text-align:left }
                th{ background:var(--teal); color:#fff }
                tr:nth-child(even){ background:var(--light-blue) }
                .status{ padding:6px 10px; border-radius:14px; font-size:0.9rem }
                .status-Pending{ background:#ffeaa7 }
                .status-In-Progress{ background:#fab1a0 }
                .status-Completed{ background:#55efc4 }
                .status-Delivered{ background:#74b9ff }
                .btn{ background:var(--teal); color:#fff; padding:8px 12px; border-radius:6px; border:none; cursor:pointer }
                .actions select{ padding:6px }
            </style>
        </head>
        <body>
            <div class="topbar"><div class="wrap"><div>TeaTaiMi</div><div><a class="btn" href="/">Home</a></div></div></div>
            <div class="wrap">
                <div class="card">
                    <h1>Orders</h1>
                    <table>
                        <tr><th>Order ID</th><th>Customer</th><th>Order Date</th><th>Delivery Date</th><th>Status</th><th>Total</th><th>Items</th><th>Update</th></tr>
                        {% for o in orders %}
                            <tr>
                                <td>{{ o.order_id }}</td>
                                <td>{{ o.customer_name }}</td>
                                <td>{{ o.order_date }}</td>
                                <td>{{ o.delivery_date }}</td>
                                <td><span class="status status-{{ o.status.replace(' ', '-') }}">{{ o.status }}</span></td>
                                <td>RM {{ "%.2f"|format(o.total_amount|float) }}</td>
                                <td>
                                    <ul style="margin:0;padding-left:16px">
                                        {% for it in o.items %}
                                            <li>{{ it.product_name }} x{{ it.quantity }} (RM {{ "%.2f"|format(it.price|float) }})</li>
                                        {% endfor %}
                                    </ul>
                                </td>
                                <td class="actions">
                                    <form method="post" action="/update_order/{{ o.order_id }}">
                                        <select name="status">
                                            <option {% if o.status=='Pending' %}selected{% endif %}>Pending</option>
                                            <option {% if o.status=='In Progress' %}selected{% endif %}>In Progress</option>
                                            <option {% if o.status=='Completed' %}selected{% endif %}>Completed</option>
                                            <option {% if o.status=='Delivered' %}selected{% endif %}>Delivered</option>
                                        </select>
                                        <button class="btn" type="submit">Update</button>
                                    </form>
                                </td>
                            </tr>
                        {% endfor %}
                    </table>
                </div>
            </div>
        </body>
        </html>
        """
    return render_template_string(html, orders=orders)

@app.route('/update_order/<int:order_id>', methods=['POST'])
def update_order(order_id):
    new_status = request.form.get('status')
    cursor = db.cursor()
    cursor.execute("UPDATE orders SET status=%s WHERE order_id=%s", (new_status, order_id))
    db.commit()
    return redirect(url_for('orders'))


# Place order: simple form to create an order (single-item) for demonstration
@app.route('/place_order', methods=['GET', 'POST'])
def place_order():
    cursor = db.cursor(dictionary=True)
    if request.method == 'POST':
        user_id = request.form.get('user_id')
        product_id = request.form.get('product_id')
        quantity = int(request.form.get('quantity') or 1)
        delivery_date = request.form.get('delivery_date') or None

        # fetch price
        cursor.execute("SELECT price FROM products WHERE product_id=%s", (product_id,))
        row = cursor.fetchone()
        if not row:
            return "Product not found", 404
        price = float(row['price'])
        total = price * quantity

        # insert order
        cursor = db.cursor()
        cursor.execute("INSERT INTO orders (user_id, delivery_date, status, total_amount) VALUES (%s,%s,'Pending',%s)", (user_id or None, delivery_date or None, total))
        db.commit()
        order_id = cursor.lastrowid

        # insert order_item
        cursor.execute("INSERT INTO order_items (order_id, product_id, quantity, price) VALUES (%s,%s,%s,%s)", (order_id, product_id, quantity, price))
        db.commit()
        return redirect(url_for('orders'))

    # GET - show form
    cursor.execute("SELECT user_id, name FROM users WHERE role='Customer'")
    customers = cursor.fetchall()
    cursor.execute("SELECT product_id, product_name, price FROM products")
    products = cursor.fetchall()

    html = """
        <html>
        <head>
            <title>Place Order - TeaTaiMi</title>
            <meta name="viewport" content="width=device-width, initial-scale=1">
            <style>
                :root{ --teal:#0f6b75; --card-bg:#f1fbfc; --muted:#6c757d }
                body{ font-family:'Segoe UI', Arial, sans-serif; margin:0; background:#f4f7f8 }
                .topbar{ background:var(--teal); color:#fff; padding:14px 0 }
                .topbar .wrap{ max-width:1100px;margin:0 auto;padding:0 16px; display:flex;align-items:center;justify-content:space-between }
                .wrap{ max-width:1100px;margin:20px auto;padding:0 16px }
                .card{ background:var(--card-bg); padding:18px;border-radius:8px }
                h1{ margin:0 0 12px 0; color:var(--teal) }
                label{ display:block; margin-top:10px; font-weight:600 }
                input, select, textarea{ width:100%; padding:8px; margin-top:6px; border:1px solid #dfeff0; border-radius:6px }
                .two{ display:grid; grid-template-columns: 1fr 1fr; gap:10px }
                .btn{ background:var(--teal); color:#fff; padding:8px 12px; border-radius:6px; border:none; cursor:pointer }
            </style>
        </head>
        <body>
            <div class="topbar"><div class="wrap"><div>TeaTaiMi</div><div><a class="btn" href="/">Home</a></div></div></div>
            <div class="wrap">
                <div class="card" style="max-width:700px;margin:0 auto">
                    <h1>Place Order</h1>
                    <form method="post">
                        <label>Customer</label>
                        <select name="user_id">
                            <option value="">(Guest)</option>
                            {% for c in customers %}
                                <option value="{{ c.user_id }}">{{ c.name }} (ID {{ c.user_id }})</option>
                            {% endfor %}
                        </select>

                        <label>Product</label>
                        <select name="product_id">
                            {% for p in products %}
                                <option value="{{ p.product_id }}">{{ p.product_name }} - RM {{ "%.2f"|format(p.price|float) }}</option>
                            {% endfor %}
                        </select>

                        <div class="two">
                            <div>
                                <label>Quantity</label>
                                <input name="quantity" type="number" value="1" min="1">
                            </div>
                            <div>
                                <label>Delivery Date</label>
                                <input name="delivery_date" type="date">
                            </div>
                        </div>

                        <div style="margin-top:16px; text-align:right">
                            <button class="btn" type="submit">Place Order</button>
                        </div>
                    </form>
                </div>
            </div>
        </body>
        </html>
    """
    return render_template_string(html, customers=customers, products=products)


if __name__ == '__main__':
    app.run(debug=True)