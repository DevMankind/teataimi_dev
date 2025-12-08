/* ---------------------------------------------------
   DEFAULT ADMIN ACCOUNT
--------------------------------------------------- */
const adminAccount = {
  email: "admin@teataimi.com",
  password: "admin123",
  role: "admin"
};

if (!localStorage.getItem("admin")) {
  localStorage.setItem("admin", JSON.stringify(adminAccount));
}


/* ---------------------------------------------------
   REGISTER USER
--------------------------------------------------- */
function registerUser(event) {
  event.preventDefault();

  let email = document.getElementById("reg-email").value.trim();
  let password = document.getElementById("reg-password").value.trim();

  let users = JSON.parse(localStorage.getItem("users")) || [];

  if (users.find(u => u.email === email)) {
    alert("Email already registered!");
    return;
  }

  users.push({ email, password, role: "customer" });
  localStorage.setItem("users", JSON.stringify(users));

  alert("Registration successful! Please login.");
  window.location.href = "login.html";
}


/* ---------------------------------------------------
   LOGIN USER
--------------------------------------------------- */
function loginUser(event) {
  event.preventDefault();

  let email = document.getElementById("login-email").value.trim();
  let password = document.getElementById("login-password").value.trim();

  let admin = JSON.parse(localStorage.getItem("admin"));

  if (email === admin.email && password === admin.password) {
    localStorage.setItem("loggedInUser", JSON.stringify(admin));
    window.location.href = "admin-dashboard.html";
    return;
  }

  let users = JSON.parse(localStorage.getItem("users")) || [];
  let user = users.find(u => u.email === email && u.password === password);

  if (!user) {
    alert("Invalid login");
    return;
  }

  localStorage.setItem("loggedInUser", JSON.stringify(user));
  window.location.href = "index.html";
}


/* ---------------------------------------------------
   LOGOUT
--------------------------------------------------- */
function logoutUser() {
  localStorage.removeItem("loggedInUser");
  window.location.href = "index.html";
}


/* ---------------------------------------------------
   NAVBAR UPDATE
--------------------------------------------------- */
function updateNavbar() {
  let user = JSON.parse(localStorage.getItem("loggedInUser"));

  let loginBtn = document.getElementById("nav-login");
  let registerBtn = document.getElementById("nav-register");
  let cartIcon = document.getElementById("nav-cart");
  let logoutBtn = document.getElementById("nav-logout");
  let ordersBtn = document.getElementById("nav-orders");

  // Show My Orders only for logged-in user
  if (ordersBtn) {
    ordersBtn.style.display = user ? "inline-block" : "none";
  }

  if (user) {
    // LOGGED IN
    loginBtn.style.display = "none";
    registerBtn.style.display = "none";

    // For ADMIN — no cart
    if(user.role === "admin"){
      cartIcon.style.display = "none";
    } else{
      cartIcon.style.display = "inline-block";
    }

    logoutBtn.style.display = "inline-block";

  } else {
    // NOT logged in
    loginBtn.style.display = "inline-block";
    registerBtn.style.display = "inline-block";
    cartIcon.style.display = "none";
    logoutBtn.style.display = "none";
  }
}
document.addEventListener("DOMContentLoaded", updateNavbar);


/* ---------------------------------------------------
   USER CART KEY
--------------------------------------------------- */
function getCartKey() {
  let user = JSON.parse(localStorage.getItem("loggedInUser"));
  if (!user) return null;
  return "cart_" + user.email;
}


/* ---------------------------------------------------
   ADD TO CART
--------------------------------------------------- */
function addToCart(name, price, image) {
  let user = JSON.parse(localStorage.getItem("loggedInUser"));
  if (!user) return (window.location.href = "login.html");

  let cartKey = getCartKey();
  let cart = JSON.parse(localStorage.getItem(cartKey)) || [];

  let exists = cart.find(i => i.name === name);

  if (exists) exists.quantity += 1;
  else cart.push({ name, price, image, quantity: 1 });

  localStorage.setItem(cartKey, JSON.stringify(cart));
  updateCartIcon();
  alert("Added to cart!");
}


/* ---------------------------------------------------
   CART ICON UPDATE
--------------------------------------------------- */
function updateCartIcon() {
  let cartKey = getCartKey();
  if (!cartKey) return;

  let cart = JSON.parse(localStorage.getItem(cartKey)) || [];
  let cartIcon = document.getElementById("nav-cart");
  if (!cartIcon) return;

  let totalQty = cart.reduce((t, i) => t + i.quantity, 0);
  cartIcon.textContent = `🛒 (${totalQty})`;
}
document.addEventListener("DOMContentLoaded", updateCartIcon);


/* ---------------------------------------------------
   LOAD CART ITEMS
--------------------------------------------------- */
function loadCartItems() {
  let container = document.getElementById("cart-items");
  let totalBox = document.getElementById("cart-total");

  if (!container) return;

  let cartKey = getCartKey();
  let cart = JSON.parse(localStorage.getItem(cartKey)) || [];

  container.innerHTML = "";
  let total = 0;

  cart.forEach((item, index) => {
    let subtotal = item.price * item.quantity;
    total += subtotal;

    container.innerHTML += `
      <div class="cart-row">
        <img src="${item.image}" class="cart-img">

        <div class="cart-info">
          <h3>${item.name}</h3>
          <p>RM ${item.price.toFixed(2)}</p>
          <div class="qty-box">
            <button onclick="changeQty(${index}, -1)">−</button>
            <span>${item.quantity}</span>
            <button onclick="changeQty(${index}, 1)">+</button>
          </div>
        </div>

        <div class="cart-subtotal">RM ${subtotal.toFixed(2)}</div>

        <button class="remove-btn" onclick="removeItem(${index})">✖</button>
      </div>
    `;
  });

  totalBox.textContent = "RM " + total.toFixed(2);
}
document.addEventListener("DOMContentLoaded", loadCartItems);


/* ---------------------------------------------------
   CHANGE QUANTITY
--------------------------------------------------- */
function changeQty(index, amount) {
  let cartKey = getCartKey();
  let cart = JSON.parse(localStorage.getItem(cartKey)) || [];

  cart[index].quantity += amount;

  if (cart[index].quantity <= 0) cart.splice(index, 1);

  localStorage.setItem(cartKey, JSON.stringify(cart));
  loadCartItems();
  updateCartIcon();
}


/* ---------------------------------------------------
   REMOVE ITEM
--------------------------------------------------- */
function removeItem(index) {
  let cartKey = getCartKey();
  let cart = JSON.parse(localStorage.getItem(cartKey)) || [];

  cart.splice(index, 1);

  localStorage.setItem(cartKey, JSON.stringify(cart));
  loadCartItems();
  updateCartIcon();
}


/* ---------------------------------------------------
   IMPORTANT FIX: CHECKOUT BUTTON ON CART PAGE
--------------------------------------------------- */
document.addEventListener("DOMContentLoaded", () => {
  const btn = document.getElementById("checkout-btn");
  if (btn) {
    btn.addEventListener("click", () => {
      window.location.href = "checkout.html";
    });
  }
});


/* ---------------------------------------------------
   CHECKOUT PAGE ONLY
--------------------------------------------------- */
document.addEventListener("DOMContentLoaded", () => {
  let form = document.getElementById("checkout-form");
  if (form) {
    form.addEventListener("submit", checkoutOrder);
  }
});


function checkoutOrder(event) {
  event.preventDefault();

  let cartKey = getCartKey();
  let cart = JSON.parse(localStorage.getItem(cartKey)) || [];
  if (cart.length === 0) return alert("Your cart is empty!");

  let user = JSON.parse(localStorage.getItem("loggedInUser"));
  if (!user) return (window.location.href = "login.html");

  let orderNo = "T" + Math.floor(100000 + Math.random() * 900000);

  let name = document.getElementById("cust-name").value;
  let phone = document.getElementById("cust-phone").value;
  let date = document.getElementById("order-date").value;
  let time = document.getElementById("time-slot").value;
  let option = document.getElementById("delivery-option").value;
  let payment = document.getElementById("payment-method").value;

  let address =
  option === "Delivery"
    ? `${document.getElementById("cust-address1").value}, ${document.getElementById("cust-city").value}, ${document.getElementById("cust-state").value}, ${document.getElementById("cust-postcode").value}`
    : "Pickup — Southbay Plaza Condominium, Batu Maung";



  let orders = JSON.parse(localStorage.getItem("orders")) || [];
  orders.push({
    orderNo,
    user: user.email,
    items: cart,
    name,
    phone,
    date,
    time,
    option,
    address,
    payment,
    status: "Pending"
  });

  localStorage.setItem("orders", JSON.stringify(orders));
  localStorage.removeItem(cartKey);

  // Store the last order details temporarily for popup + redirect
localStorage.setItem("lastOrder", JSON.stringify({
  orderNo,
  name,
  phone,
  date,
  time,
  option,
  address,
  payment
}));

// SHOW POPUP
alert(`🎉 Order Placed Successfully!

Tracking Number: ${orderNo}

Your order is now being processed.`);
    
// REDIRECT to Order History
window.location.href = "order-history.html";

}


/* ---------------------------------------------------
   SUCCESS PAGE
--------------------------------------------------- */
function loadSuccessPage() {
  let box = document.getElementById("order-id");
  if (!box) return;

  let params = new URLSearchParams(window.location.search);
  box.textContent = params.get("order");
}
document.addEventListener("DOMContentLoaded", loadSuccessPage);


/* ---------------------------------------------------
   ADMIN - LOAD ORDERS
--------------------------------------------------- */
function loadAdminOrders() {
  let table = document.getElementById("admin-orders");
  if (!table) return;

  let orders = JSON.parse(localStorage.getItem("orders")) || [];
  table.innerHTML = "";

  orders.forEach((o, i) => {
    table.innerHTML += `
      <tr>
        <td>${o.orderNo}</td>
        <td>${o.user}</td>
        <td>${o.items.length} items</td>
        <td>${o.status}</td>
        <td>
          <select onchange="updateOrderStatus(${i}, this.value)">
            <option ${o.status === "Pending" ? "selected" : ""}>Pending</option>
            <option ${o.status === "Preparing" ? "selected" : ""}>Preparing</option>
            <option ${o.status === "Completed" ? "selected" : ""}>Completed</option>
          </select>
        </td>
      </tr>
    `;
  });
}
document.addEventListener("DOMContentLoaded", loadAdminOrders);


/* ---------------------------------------------------
   UPDATE STATUS
--------------------------------------------------- */
function updateOrderStatus(index, newStatus) {
  let orders = JSON.parse(localStorage.getItem("orders")) || [];
  orders[index].status = newStatus;
  localStorage.setItem("orders", JSON.stringify(orders));
  loadAdminOrders();
}







