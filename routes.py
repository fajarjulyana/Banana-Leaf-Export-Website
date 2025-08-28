from flask import render_template, request, redirect, url_for, session, flash, jsonify
from app import app, db
from models import Product, Category, Order, OrderItem, CompanySettings
import uuid
from datetime import datetime
import locale

def detect_user_location():
    """Detect user location from request headers and IP"""
    # Check Accept-Language header
    accept_language = request.headers.get('Accept-Language', '')
    if 'id' in accept_language.lower() or 'indonesia' in accept_language.lower():
        return 'id', 'IDR'
    
    # Check User-Agent for Indonesian keywords
    user_agent = request.headers.get('User-Agent', '').lower()
    if any(keyword in user_agent for keyword in ['indonesia', 'jakarta', 'id-']):
        return 'id', 'IDR'
    
    # Default to English/USD for international users
    return 'en', 'USD'

def format_currency(amount, currency='USD', lang='en'):
    """Format currency based on language and currency type"""
    if currency == 'IDR':
        return f"Rp {amount:,.0f}"
    else:
        return f"${amount:,.2f}"

def get_product_price(product, currency='USD'):
    """Get product price in specified currency"""
    if currency == 'IDR':
        return product.price_idr
    else:
        return product.price_usd

@app.route('/')
def index():
    # Auto-detect language and currency if not set
    if not request.args.get('lang') and not session.get('lang'):
        detected_lang, detected_currency = detect_user_location()
        session['lang'] = detected_lang
        session['currency'] = detected_currency
    
    # Get language and currency preference
    lang = request.args.get('lang', session.get('lang', 'en'))
    currency = request.args.get('currency', session.get('currency', 'USD'))
    session['lang'] = lang
    session['currency'] = currency
    
    # Get company settings
    settings = CompanySettings.query.first()
    if not settings:
        settings = CompanySettings()
        db.session.add(settings)
        db.session.commit()
    
    # Get categories with products
    categories = Category.query.all()
    featured_products = Product.query.filter_by(is_available=True).limit(6).all()
    
    return render_template('index.html', 
                         categories=categories, 
                         featured_products=featured_products,
                         settings=settings,
                         lang=lang,
                         currency=currency,
                         format_currency=format_currency,
                         get_product_price=get_product_price)

@app.route('/products')
def products():
    # Auto-detect language and currency if not set
    if not request.args.get('lang') and not session.get('lang'):
        detected_lang, detected_currency = detect_user_location()
        session['lang'] = detected_lang
        session['currency'] = detected_currency
    
    lang = request.args.get('lang', session.get('lang', 'en'))
    currency = request.args.get('currency', session.get('currency', 'USD'))
    session['lang'] = lang
    session['currency'] = currency
    
    category_id = request.args.get('category')
    search = request.args.get('search', '')
    
    query = Product.query.filter_by(is_available=True)
    
    if category_id:
        query = query.filter_by(category_id=category_id)
    
    if search:
        if lang == 'id':
            query = query.filter(Product.name_id.contains(search))
        else:
            query = query.filter(Product.name_en.contains(search))
    
    products = query.all()
    categories = Category.query.all()
    selected_category = Category.query.get(category_id) if category_id else None
    
    return render_template('products.html', 
                         products=products, 
                         categories=categories,
                         selected_category=selected_category,
                         search=search,
                         lang=lang,
                         currency=currency,
                         format_currency=format_currency,
                         get_product_price=get_product_price)

@app.route('/product/<int:product_id>')
def product_detail(product_id):
    # Auto-detect language and currency if not set
    if not request.args.get('lang') and not session.get('lang'):
        detected_lang, detected_currency = detect_user_location()
        session['lang'] = detected_lang
        session['currency'] = detected_currency
    
    lang = request.args.get('lang', session.get('lang', 'en'))
    currency = request.args.get('currency', session.get('currency', 'USD'))
    session['lang'] = lang
    session['currency'] = currency
    
    product = Product.query.get_or_404(product_id)
    related_products = Product.query.filter_by(
        category_id=product.category_id,
        is_available=True
    ).filter(Product.id != product_id).limit(4).all()
    
    return render_template('product_detail.html', 
                         product=product, 
                         related_products=related_products,
                         lang=lang,
                         currency=currency,
                         format_currency=format_currency,
                         get_product_price=get_product_price)

@app.route('/add_to_cart', methods=['POST'])
def add_to_cart():
    product_id = int(request.form['product_id'])
    quantity = int(request.form['quantity'])
    
    # Initialize cart if not exists
    if 'cart' not in session:
        session['cart'] = {}
    
    cart = session['cart']
    product_id_str = str(product_id)
    
    if product_id_str in cart:
        cart[product_id_str] += quantity
    else:
        cart[product_id_str] = quantity
    
    session['cart'] = cart
    flash('Product added to cart successfully!', 'success')
    
    return redirect(request.referrer or url_for('products'))

@app.route('/cart')
def cart():
    lang = request.args.get('lang', session.get('lang', 'en'))
    currency = request.args.get('currency', session.get('currency', 'USD'))
    session['lang'] = lang
    session['currency'] = currency
    
    cart = session.get('cart', {})
    cart_items = []
    total = 0
    
    for product_id, quantity in cart.items():
        product = Product.query.get(int(product_id))
        if product and product.is_available:
            price = get_product_price(product, currency)
            item_total = price * quantity
            cart_items.append({
                'product': product,
                'quantity': quantity,
                'total': item_total
            })
            total += item_total
    
    return render_template('cart.html', 
                         cart_items=cart_items, 
                         total=total,
                         lang=lang,
                         currency=currency,
                         format_currency=format_currency,
                         get_product_price=get_product_price)

@app.route('/update_cart', methods=['POST'])
def update_cart():
    product_id = request.form['product_id']
    quantity = int(request.form['quantity'])
    
    cart = session.get('cart', {})
    
    if quantity > 0:
        cart[product_id] = quantity
    else:
        cart.pop(product_id, None)
    
    session['cart'] = cart
    return redirect(url_for('cart'))

@app.route('/remove_from_cart', methods=['POST'])
def remove_from_cart():
    product_id = request.form['product_id']
    cart = session.get('cart', {})
    cart.pop(product_id, None)
    session['cart'] = cart
    
    flash('Product removed from cart', 'info')
    return redirect(url_for('cart'))

@app.route('/login', methods=['GET', 'POST'])
def customer_login():
    lang = request.args.get('lang', session.get('lang', 'en'))
    currency = request.args.get('currency', session.get('currency', 'USD'))
    session['lang'] = lang
    session['currency'] = currency
    
    if request.method == 'POST':
        email = request.form['email']
        name = request.form['name']
        
        # Simple login - store customer info in session
        session['customer_email'] = email
        session['customer_name'] = name
        session['is_logged_in'] = True
        
        flash('Login successful!', 'success')
        return redirect(url_for('checkout'))
    
    return render_template('customer_login.html', lang=lang, currency=currency)

@app.route('/logout')
def customer_logout():
    session.pop('customer_email', None)
    session.pop('customer_name', None)
    session.pop('is_logged_in', None)
    
    flash('You have been logged out', 'info')
    return redirect(url_for('index'))

@app.route('/checkout')
def checkout():
    lang = request.args.get('lang', session.get('lang', 'en'))
    currency = request.args.get('currency', session.get('currency', 'USD'))
    session['lang'] = lang
    session['currency'] = currency
    
    # Check if user is logged in
    if not session.get('is_logged_in'):
        flash('Please login to proceed to checkout', 'warning')
        return redirect(url_for('customer_login'))
    
    cart = session.get('cart', {})
    if not cart:
        flash('Your cart is empty', 'warning')
        return redirect(url_for('products'))
    
    cart_items = []
    total = 0
    
    for product_id, quantity in cart.items():
        product = Product.query.get(int(product_id))
        if product and product.is_available:
            price = get_product_price(product, currency)
            item_total = price * quantity
            cart_items.append({
                'product': product,
                'quantity': quantity,
                'total': item_total
            })
            total += item_total
    
    return render_template('checkout.html', 
                         cart_items=cart_items, 
                         total=total,
                         lang=lang,
                         currency=currency,
                         format_currency=format_currency,
                         get_product_price=get_product_price)

@app.route('/place_order', methods=['POST'])
def place_order():
    lang = session.get('lang', 'en')
    cart = session.get('cart', {})
    
    if not cart:
        flash('Your cart is empty', 'warning')
        return redirect(url_for('products'))
    
    # Create order
    order_number = f"BLE{datetime.now().strftime('%Y%m%d')}{str(uuid.uuid4())[:8].upper()}"
    
    order = Order(
        order_number=order_number,
        customer_name=request.form['customer_name'],
        customer_email=request.form['customer_email'],
        customer_phone=request.form.get('customer_phone', ''),
        customer_company=request.form.get('customer_company', ''),
        customer_country=request.form['customer_country'],
        shipping_address=request.form['shipping_address'],
        notes=request.form.get('notes', ''),
        total_amount=0  # Will be calculated below
    )
    
    db.session.add(order)
    db.session.flush()  # Get the order ID
    
    total_amount = 0
    
    # Create order items
    currency = session.get('currency', 'USD')
    for product_id, quantity in cart.items():
        product = Product.query.get(int(product_id))
        if product and product.is_available:
            unit_price = get_product_price(product, currency)
            item_total = unit_price * quantity
            
            order_item = OrderItem(
                order_id=order.id,
                product_id=product.id,
                quantity=quantity,
                unit_price=unit_price,
                total_price=item_total
            )
            
            db.session.add(order_item)
            total_amount += item_total
    
    order.total_amount = total_amount
    db.session.commit()
    
    # Clear cart
    session['cart'] = {}
    
    flash(f'Order placed successfully! Order number: {order_number}', 'success')
    return redirect(url_for('index'))

@app.route('/set_language/<lang>')
def set_language(lang):
    session['lang'] = lang
    return redirect(request.referrer or url_for('index'))
