/* ---------------------------------------------------
   TEATAIMI AUTHENTICATION - Backend API Edition
   Connects to Flask REST API instead of localStorage
   
   API Endpoints:
   - POST /api/register
   - POST /api/login
   - POST /api/logout
   - GET /api/current-user
   - GET /api/products
   - GET /api/track/<order_id>
   - POST /api/place-order
   - GET /api/my-orders
--------------------------------------------------- */

/* Get current logged-in user from session */
async function getCurrentUser() {
  try {
    const response = await fetch('/api/current-user', { method: 'GET' });
    if (response.ok) {
      return await response.json();
    }
  } catch (e) {
    console.error('Error fetching current user:', e);
  }
  return null;
}


/* ---------------------------------------------------
   REGISTER USER
--------------------------------------------------- */
async function registerUser(event) {
  event.preventDefault();

  let name = document.getElementById("reg-name")?.value.trim();
  let email = document.getElementById("reg-email").value.trim();
  let password = document.getElementById("reg-password").value.trim();
  let phone = document.getElementById("reg-phone")?.value.trim() || "";
  let address = document.getElementById("reg-address")?.value.trim() || "";

  if (!name || !email || !password) {
    alert("Please fill in all required fields");
    return;
  }

  try {
    const response = await fetch('/api/register', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ name, email, password, phone, address })
    });

    const data = await response.json();

    if (response.ok) {
      alert("Registration successful! Please login.");
      window.location.href = "login.html";
    } else {
      alert(data.error || "Registration failed");
    }
  } catch (e) {
    console.error('Registration error:', e);
    alert("Registration error: " + e.message);
  }
}


/* ---------------------------------------------------
   LOGIN USER
--------------------------------------------------- */
async function loginUser(event) {
  event.preventDefault();

  let email = document.getElementById("login-email").value.trim();
  let password = document.getElementById("login-password").value.trim();

  if (!email || !password) {
    alert("Please enter email and password");
    return;
  }

  try {
    const response = await fetch('/api/login', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ email, password })
    });

    const data = await response.json();

    if (response.ok) {
      // Store user info in localStorage for frontend (non-critical, can be fetched from /api/current-user)
      localStorage.setItem("loggedInUser", JSON.stringify(data.user));
      alert("Logged in successfully!");
      // Redirect based on role
      if (data.user.role === 'Admin' || data.user.role === 'Seller') {
        window.location.href = "admin-dashboard.html";
      } else {
        window.location.href = "index.html";
      }
    } else {
      alert(data.error || "Login failed");
    }
  } catch (e) {
    console.error('Login error:', e);
    alert("Login error: " + e.message);
  }
}


/* ---------------------------------------------------
   LOGOUT
--------------------------------------------------- */
async function logoutUser() {
  try {
    const response = await fetch('/api/logout', { method: 'POST' });
    if (response.ok) {
      localStorage.removeItem("loggedInUser");
      window.location.href = "index.html";
    }
  } catch (e) {
    console.error('Logout error:', e);
  }
}


/* ---------------------------------------------------
   NAVBAR UPDATE - check session and update buttons
--------------------------------------------------- */
async function updateNavbar() {
  const user = await getCurrentUser();

  let loginBtn = document.getElementById("nav-login");
  let registerBtn = document.getElementById("nav-register");
  let cartIcon = document.getElementById("nav-cart");
  let logoutBtn = document.getElementById("nav-logout");
  let ordersBtn = document.getElementById("nav-orders");

  if (user) {
    // LOGGED IN
    if (loginBtn) loginBtn.style.display = "none";
    if (registerBtn) registerBtn.style.display = "none";
    if (logoutBtn) logoutBtn.style.display = "inline-block";
    
    // Show My Orders for customers
    if (ordersBtn && (user.role === 'Customer' || user.role === 'customer')) {
      ordersBtn.style.display = "inline-block";
    }
    
    // Show cart for customers (no cart for admin)
    if (cartIcon && (user.role !== 'Admin' && user.role !== 'Seller')) {
      cartIcon.style.display = "inline-block";
    }
  } else {
    // NOT LOGGED IN
    if (loginBtn) loginBtn.style.display = "inline-block";
    if (registerBtn) registerBtn.style.display = "inline-block";
    if (logoutBtn) logoutBtn.style.display = "none";
    if (cartIcon) cartIcon.style.display = "none";
    if (ordersBtn) ordersBtn.style.display = "none";
  }
}
document.addEventListener("DOMContentLoaded", updateNavbar);


/* ---------------------------------------------------
   CART FUNCTIONS (using localStorage for temp storage before checkout)
--------------------------------------------------- */
function getCart() {
  return JSON.parse(localStorage.getItem("cart")) || [];
}

function saveCart(cart) {
  localStorage.setItem("cart", JSON.stringify(cart));
}

function addToCart(productId, name, price) {
  let user = JSON.parse(localStorage.getItem("loggedInUser"));
  if (!user) {
    alert("Please login first");
    window.location.href = "login.html";
    return;
  }

  let cart = getCart();
  let item = cart.find(i => i.product_id === productId);
  
  if (item) {
    item.quantity += 1;
  } else {
    cart.push({ product_id: productId, name, price, quantity: 1 });
  }
  
  saveCart(cart);
  updateCartIcon();
  alert(`${name} added to cart!`);
}

function removeFromCart(productId) {
  let cart = getCart();
  cart = cart.filter(i => i.product_id !== productId);
  saveCart(cart);
}

function updateCartQuantity(productId, quantity) {
  let cart = getCart();
  let item = cart.find(i => i.product_id === productId);
  if (item) item.quantity = Math.max(1, quantity);
  saveCart(cart);
}

/* ---------------------------------------------------
   CART ICON UPDATE
--------------------------------------------------- */
function updateCartIcon() {
  let cart = getCart();
  let cartIcon = document.getElementById("nav-cart");
  if (!cartIcon) return;

  let totalQty = cart.reduce((t, i) => t + i.quantity, 0);
  cartIcon.textContent = totalQty > 0 ? `🛒 (${totalQty})` : '🛒';
}
document.addEventListener("DOMContentLoaded", updateCartIcon);


/* ---------------------------------------------------
   DISPLAY CART
--------------------------------------------------- */
function displayCart() {
  let cart = getCart();
  let cartDiv = document.getElementById("cart-items");
  let totalDiv = document.getElementById("cart-total");

  if (!cartDiv) return;

  if (cart.length === 0) {
    cartDiv.innerHTML = "<p>Your cart is empty</p>";
    if (totalDiv) totalDiv.innerHTML = "Total: RM 0.00";
    return;
  }

  let total = 0;
  cartDiv.innerHTML = cart.map(item => {
    let itemTotal = item.price * item.quantity;
    total += itemTotal;
    return `
      <div class="cart-item">
        <span>${item.name} x ${item.quantity}</span>
        <span>RM ${itemTotal.toFixed(2)}</span>
        <input type="number" min="1" value="${item.quantity}" 
               onchange="updateCartQuantity(${item.product_id}, this.value); displayCart()">
        <button onclick="removeFromCart(${item.product_id}); displayCart()">Remove</button>
      </div>
    `;
  }).join('');

  if (totalDiv) totalDiv.innerHTML = `Total: RM ${total.toFixed(2)}`;
}
document.addEventListener("DOMContentLoaded", displayCart);


/* ---------------------------------------------------
   PLACE ORDER
--------------------------------------------------- */
async function placeOrder(event) {
  event.preventDefault();

  let user = await getCurrentUser();
  if (!user) {
    alert("Please login first");
    return;
  }

  let cart = getCart();
  if (cart.length === 0) {
    alert("Your cart is empty");
    return;
  }

  let deliveryDate = document.getElementById("delivery-date")?.value;
  let deliveryMethod = document.getElementById("delivery-method")?.value || "Pickup";

  try {
    const response = await fetch('/api/place-order', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        items: cart.map(item => ({ product_id: item.product_id, quantity: item.quantity })),
        delivery_date: deliveryDate,
        delivery_method: deliveryMethod
      })
    });

    const data = await response.json();

    if (response.ok) {
      localStorage.removeItem("cart");
      alert(`Order placed successfully! Order ID: ${data.order_id}`);
      window.location.href = "success.html";
    } else {
      alert(data.error || "Failed to place order");
    }
  } catch (e) {
    console.error('Order error:', e);
    alert("Order error: " + e.message);
  }
}


/* ---------------------------------------------------
   LOAD ORDER HISTORY
--------------------------------------------------- */
async function loadOrderHistory() {
  try {
    const response = await fetch('/api/my-orders');
    if (!response.ok) {
      console.log('Not logged in or no orders');
      return;
    }

    const orders = await response.json();
    let historyDiv = document.getElementById("order-history");
    if (!historyDiv) return;

    if (orders.length === 0) {
      historyDiv.innerHTML = "<p>No orders yet</p>";
      return;
    }

    historyDiv.innerHTML = orders.map(o => `
      <div class="order-card">
        <h3>Order #${o.order_id}</h3>
        <p><strong>Date:</strong> ${new Date(o.order_date).toLocaleDateString()}</p>
        <p><strong>Status:</strong> <span class="status">${o.status}</span></p>
        <p><strong>Delivery:</strong> ${o.delivery_date || 'Pickup'}</p>
        <p><strong>Total:</strong> RM ${o.total_amount.toFixed(2)}</p>
      </div>
    `).join('');
  } catch (e) {
    console.error('Error loading order history:', e);
  }
}
document.addEventListener("DOMContentLoaded", loadOrderHistory);


/* ---------------------------------------------------
   TRACK ORDER
--------------------------------------------------- */
async function trackOrder(event) {
  if (event) event.preventDefault();

  let orderId = document.getElementById("track-order-id")?.value.trim();
  if (!orderId) {
    alert("Please enter an order ID");
    return;
  }

  try {
    const response = await fetch(`/api/track/${orderId}`);
    const data = await response.json();

    if (response.ok) {
      let resultDiv = document.getElementById("track-result");
      if (resultDiv) {
        resultDiv.innerHTML = `
          <h3>Order #${data.order_id}</h3>
          <p><strong>Status:</strong> ${data.status}</p>
          <p><strong>Delivery Date:</strong> ${data.delivery_date || 'Not set'}</p>
          <p><strong>Total:</strong> RM ${data.total_amount.toFixed(2)}</p>
        `;
      }
    } else {
      alert(data.error || "Order not found");
    }
  } catch (e) {
    console.error('Track error:', e);
    alert("Error tracking order: " + e.message);
  }
}


/* ---------------------------------------------------
   LOAD PRODUCTS FOR MENU
--------------------------------------------------- */
async function loadProducts() {
  try {
    const response = await fetch('/api/products');
    const products = await response.json();

    let gridDiv = document.getElementById("product-grid");
    if (!gridDiv) return;

    gridDiv.innerHTML = products.map(p => `
      <article class="product-card">
        <div class="product-img" style="background:#e0e0e0">
          <img src="images/product-${p.product_id}.jpg" alt="${p.product_name}" onerror="this.style.display='none'">
        </div>
        <h3>${p.product_name}</h3>
        <p class="price">RM ${p.price.toFixed(2)}</p>
        <p class="desc">${p.description || ''}</p>
        <button class="btn" onclick="addToCart(${p.product_id}, '${p.product_name}', ${p.price})">Add to Cart</button>
      </article>
    `).join('');
  } catch (e) {
    console.error('Error loading products:', e);
  }
}
document.addEventListener("DOMContentLoaded", loadProducts);







