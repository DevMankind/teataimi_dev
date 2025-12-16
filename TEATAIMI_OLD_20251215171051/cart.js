document.addEventListener('DOMContentLoaded', () => {
    displayCartItems();
    updateCartCount(); // From your auth.js logic if it exists
});

// 1. DISPLAY ITEMS
function displayCartItems() {
    const cartContainer = document.getElementById('cart-items');
    const cartTotalEl = document.getElementById('cart-total');
    const finalTotalEl = document.getElementById('cart-total-final');
    
    // Get cart from storage
    let cart = JSON.parse(localStorage.getItem('cart')) || [];
    
    // Clear current display
    cartContainer.innerHTML = '';

    // Handle Empty Cart
    if (cart.length === 0) {
        cartContainer.innerHTML = `
            <div style="text-align:center; padding: 40px;">
                <h3>Your cart is empty</h3>
                <p>Looks like you haven't added any desserts yet.</p>
                <a href="menu.html" class="btn btn-primary" style="margin-top:15px;">Go to Menu</a>
            </div>
        `;
        cartTotalEl.innerText = 'RM 0.00';
        finalTotalEl.innerText = 'RM 0.00';
        return;
    }

    let total = 0;

    // Loop through items and generate HTML
    cart.forEach((item, index) => {
        // Calculate item total
        const itemTotal = item.price * item.quantity;
        total += itemTotal;

        const cartItem = document.createElement('div');
        cartItem.classList.add('cart-item');
        // styling for the dynamic item
        cartItem.style.display = 'flex';
        cartItem.style.gap = '15px';
        cartItem.style.marginBottom = '20px';
        cartItem.style.borderBottom = '1px solid #eee';
        cartItem.style.paddingBottom = '15px';

        cartItem.innerHTML = `
            <img src="${item.image}" alt="${item.name}" style="width:80px; height:80px; object-fit:cover; border-radius:8px;">
            <div style="flex:1;">
                <h4 style="margin:0 0 5px 0;">${item.name}</h4>
                <p class="muted" style="margin:0;">RM ${item.price.toFixed(2)}</p>
            </div>
            <div style="display:flex; flex-direction:column; align-items:flex-end; gap:5px;">
                <input type="number" min="1" value="${item.quantity}" 
                    onchange="updateQuantity(${index}, this.value)"
                    style="width:50px; padding:5px;">
                <button onclick="removeFromCart(${index})" 
                    style="color:red; background:none; border:none; cursor:pointer; font-size:0.9rem;">
                    Remove
                </button>
            </div>
        `;
        cartContainer.appendChild(cartItem);
    });

    // Update Totals
    cartTotalEl.innerText = 'RM ' + total.toFixed(2);
    finalTotalEl.innerText = 'RM ' + total.toFixed(2);
}

// 2. UPDATE QUANTITY
function updateQuantity(index, newQty) {
    let cart = JSON.parse(localStorage.getItem('cart')) || [];
    
    if (newQty < 1) {
        newQty = 1;
    }
    
    cart[index].quantity = parseInt(newQty);
    localStorage.setItem('cart', JSON.stringify(cart));
    displayCartItems(); // Re-render
}

// 3. REMOVE ITEM
function removeFromCart(index) {
    let cart = JSON.parse(localStorage.getItem('cart')) || [];
    cart.splice(index, 1); // Remove item at specific index
    localStorage.setItem('cart', JSON.stringify(cart));
    displayCartItems(); // Re-render
    
    // Optional: Update cart icon count
    if(typeof updateCartCount === 'function') updateCartCount();
}

// 4. CHECKOUT BUTTON LISTENER
document.getElementById('checkout-btn').addEventListener('click', () => {
    let cart = JSON.parse(localStorage.getItem('cart')) || [];
    
    if (cart.length === 0) {
        alert("Your cart is empty!");
        return;
    }

    // Check if user is logged in (assuming auth.js sets a 'user' item)
    const user = localStorage.getItem('user'); 
    
    if (!user) {
        alert("Please login to proceed to checkout.");
        window.location.href = 'login.html';
    } else {
        // Proceed to checkout page
        window.location.href = 'checkout.html';
    }
});