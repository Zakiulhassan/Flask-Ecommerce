
from flask import Flask, render_template, redirect, url_for, request, session
from typing import List

app = Flask(__name__)

# Sample product data
products = [
    {
        'id': 1,
        'title': 'Laptop',
        'description': 'Powerful laptop for work and entertainment',
        'image': 'laptop.jpg',
        'price': 999.99
    },
    {
        'id': 2,
        'title': 'Smartphone',
        'description': 'Latest smartphone with advanced features',
        'image': 'smartphone.jpg',
        'price': 699.99
    },
    {
        'id': 3,
        'title': 'Headphones',
        'description': 'High-quality wireless headphones for immersive audio',
        'image': 'headphones.jpg',
        'price': 149.99
    },
    {
        'id': 4,
        'title': 'Camera',
        'description': 'Professional DSLR camera for capturing stunning photos',
        'image': 'camera.jpg',
        'price': 1299.99
    },
    {
        'id': 5,
        'title': 'Fitness Tracker',
        'description': 'Track your fitness and health with this advanced tracker',
        'image': 'fitness_tracker.jpg',
        'price': 79.99
    },
    # Add more products as needed
]

@app.route('/')
def home():
    username = session.get('username')
    return render_template('home.html', products=products, username=username)

@app.route('/product/<int:id>')
def product_detail(id):
    product = next((p for p in products if p['id'] == id), None)
    if product:
        return render_template('product_detail.html', product=product)
    return 'Product not found', 404

# app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Replace with a secure secret key

# Sample user data for demonstration
users = {'user1': 'password1', 'user2': 'password2'}  

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username in users and users[username] == password:
            session['username'] = username
            return redirect(url_for('home'))
        return 'Invalid username or password'
    return render_template('login.html')


@app.route('/logout')
def logout():
    # Perform logout actions, such as clearing the session
    session.clear()
    # Redirect to the home page or another valid route
    return redirect(url_for('home'))

# Cart

@app.route('/add_to_cart/<int:id>', methods=['POST'])
def add_to_cart(id):
    if 'cart' not in session:
        session['cart'] = set()

    # Convert to set to ensure uniqueness
    cart_set = set(session['cart'])

    # Check if the user is logged in before allowing them to add to the cart
    if 'username' not in session:
        return redirect(url_for('login'))

    # Check if the product is not already in the cart
    if id not in cart_set:
        cart_set.add(id)

    # Convert back to list for easier iteration
    session['cart'] = list(cart_set)

    return redirect(url_for('home'))

@app.route('/cart')
def cart():
    if 'cart' not in session:
        session['cart'] = []

    cart_items = []
    total_price = 0

    for product_id in session['cart']:
        # Assuming you have a list of products with prices
        product = next((p for p in products if p['id'] == product_id), None)
        if product:
            cart_items.append(product)
            total_price += product.get('price', 0)  # Add the price of the product

    return render_template('cart.html', cart_items=cart_items, total_price=total_price)

@app.route('/remove_from_cart/<int:id>', methods=['POST'])
def remove_from_cart(id):
    if 'cart' in session:
        cart_list = session['cart']

        # Remove the item from the cart
        if id in cart_list:
            cart_list.remove(id)

        session['cart'] = cart_list

    return redirect(url_for('cart'))

@app.route('/clear_cart', methods=['POST'])
def clear_cart():
    if 'cart' in session:
        session.pop('cart')

    return redirect(url_for('cart'))


if __name__ == '__main__':
    app.run(debug=True)











# from flask import Flask, render_template, request, redirect, url_for, flash

# app = Flask(__name__)
# app.secret_key = 'your_secret_key'  # Change this to a random, secure key in a production environment

# # Placeholder data for products
# products = [
#     {'id': 1, 'name': 'Product 1', 'description': 'Description for Product 1', 'price': 19.99, 'image': 'product1.jpg'},
#     {'id': 2, 'name': 'Product 2', 'description': 'Description for Product 2', 'price': 29.99, 'image': 'product2.jpg'},
#     # Add more products as needed
# ]

# # Placeholder data for the user's cart
# cart = []

# # Route to show a list of all available products
# @app.route('/')
# def index():
#     return render_template('index.html', products=products)

# # Route to show details for a single product
# @app.route('/product/<int:product_id>')
# def product(product_id):
#     product = next((p for p in products if p['id'] == product_id), None)
#     if product:
#         return render_template('product.html', product=product)
#     else:
#         return render_template('404.html'), 404

# # Route to add a product to the user's cart
# @app.route('/add_to_cart/<int:product_id>', methods=['POST'])
# def add_to_cart(product_id):
#     if 'user_id' not in session:
#         flash('You must be logged in to add items to your cart.', 'warning')
#         return redirect(url_for('index'))

#     product = next((p for p in products if p['id'] == product_id), None)
#     if product:
#         cart.append(product)
#         flash(f'{product["name"]} added to your cart!', 'success')
#     else:
#         flash('Product not found.', 'danger')

#     return redirect(url_for('index'))

# # Route to show the user's cart and total
# @app.route('/cart')
# def view_cart():
#     return render_template('cart.html', cart=cart)

# # Route to remove all items from the user's cart
# @app.route('/clear_cart', methods=['POST'])
# def clear_cart():
#     cart.clear()
#     flash('Your cart has been cleared.', 'info')
#     return redirect(url_for('view_cart'))

# # Route to remove a specific product from the user's cart
# @app.route('/remove_from_cart/<int:product_id>', methods=['POST'])
# def remove_from_cart(product_id):
#     product = next((p for p in cart if p['id'] == product_id), None)
#     if product:
#         cart.remove(product)
#         flash(f'{product["name"]} removed from your cart.', 'info')
#     else:
#         flash('Product not found in your cart.', 'danger')

#     return redirect(url_for('view_cart'))

# if __name__ == '__main__':
#     app.run(debug=True)
