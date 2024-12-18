from flask import Flask, render_template, request, redirect, url_for, session
import os
import stripe

app = Flask(__name__)
app.secret_key = os.urandom(24)  # Required for session handling

# Example product data (you can add more)
products = [
    {'id': 1, 'name': 'Product 1', 'price': 100, 'image': 'product1.jpg'},
    {'id': 2, 'name': 'Product 2', 'price': 200, 'image': 'product2.jpg'},
    {'id': 3, 'name': 'Product 3', 'price': 300, 'image': 'product3.jpg'},
    {'id': 4, 'name': 'Product 4', 'price': 400, 'image': 'product4.webp'},
    {'id': 5, 'name': 'Product 5', 'price': 500, 'image': 'product5.webp'}
]

# Route for welcome page (where the user can enter their email and phone number)
@app.route('/', methods=['GET', 'POST'])
def welcome():
    if request.method == 'POST':
        # Get the email and phone number from the form
        email = request.form['email']
        phone = request.form['phone']
        
        # You can process the data here (e.g., save to a database or send an email)
        print(f"Received email: {email}, phone: {phone}")
        
        # Redirect to the homepage after form submission
        return redirect(url_for('index'))  # Redirecting to the homepage (you can customize this)

    return render_template('welcome.html')

# Route for homepage with product catalog
@app.route('/home')
def index():
    return render_template('index.html', products=products)

@app.route('/product/<int:product_id>')
def product_details(product_id):
    product = next((prod for prod in products if prod['id'] == product_id), None)
    if product:
        return render_template('product_details.html', product=product)
    return redirect(url_for('index'))

@app.route('/add_to_cart/<int:product_id>', methods=['GET'])
def add_to_cart(product_id):
    product = next((prod for prod in products if prod['id'] == product_id), None)
    if product:
        # If cart doesn't exist in session, create it
        if 'cart' not in session:
            session['cart'] = []
        
        # Add the product to the cart (only add once per product)
        cart = session['cart']
        if product not in cart:
            cart.append(product)
        
        session.modified = True
    
    return redirect(url_for('cart'))

@app.route('/cart')
def cart():
    return render_template('cart.html', cart=session.get('cart', []))

@app.route('/checkout')
def checkout():
    cart = session.get('cart', [])
    if not cart:
        # Redirect to cart page if the cart is empty
        return redirect(url_for('cart'))
    
    # Calculate total price
    def total_price(cart):
        return sum(item['price'] for item in cart)

    # Pass the total_price function to the template
    return render_template('checkout.html', cart=cart, total_price=total_price(cart))



# Route for Stripe payment
@app.route('/stripe_payment', methods=['POST'])
def stripe_payment():
    cart = session.get('cart', [])
    if not cart:
        return redirect(url_for('cart'))

    # Convert cart items into Stripe line items
    line_items = []
    for item in cart:
        line_items.append({
            'price_data': {
                'currency': 'usd',
                'product_data': {
                    'name': item['name'],
                },
                'unit_amount': item['price'] * 100,  # Stripe uses cents for prices
            },
            'quantity': 1,
        })

@app.route('/payment', methods=['GET', 'POST'])
def payment():
    if request.method == 'POST':
        # Handle the payment process here
        print("Payment process initiated.")
        return render_template('payment.html', message="Thank you for proceeding with the payment!")
    
    # For GET requests, simply render the payment page
    return render_template('payment.html')


if __name__ == "__main__":
    app.run(debug=True)
   
















