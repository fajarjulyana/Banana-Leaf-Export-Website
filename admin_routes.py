from flask import render_template, request, redirect, url_for, flash, Blueprint
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import check_password_hash, generate_password_hash
from app import app, db
from models import Admin, Product, Category, Order, OrderItem, CompanySettings
from datetime import datetime

# Admin Blueprint
admin = Blueprint('admin', __name__, url_prefix='/admin')

@admin.route('/')
def index():
    return redirect(url_for('admin.dashboard'))

@admin.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('admin.dashboard'))
    
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        admin_user = Admin.query.filter_by(username=username).first()
        
        if admin_user and check_password_hash(admin_user.password_hash, password):
            login_user(admin_user)
            flash('Login successful!', 'success')
            return redirect(url_for('admin.dashboard'))
        else:
            flash('Invalid username or password', 'error')
    
    return render_template('admin/login.html')

@admin.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out', 'info')
    return redirect(url_for('index'))

@admin.route('/dashboard')
@login_required
def dashboard():
    # Statistics
    total_products = Product.query.count()
    total_orders = Order.query.count()
    pending_orders = Order.query.filter_by(status='pending').count()
    total_revenue = db.session.query(db.func.sum(Order.total_amount)).filter_by(status='confirmed').scalar() or 0
    
    # Recent orders
    recent_orders = Order.query.order_by(Order.created_at.desc()).limit(5).all()
    
    return render_template('admin/dashboard.html',
                         total_products=total_products,
                         total_orders=total_orders,
                         pending_orders=pending_orders,
                         total_revenue=total_revenue,
                         recent_orders=recent_orders)

@admin.route('/products')
@login_required
def products():
    page = request.args.get('page', 1, type=int)
    search = request.args.get('search', '')
    category_id = request.args.get('category')
    
    query = Product.query
    
    if search:
        query = query.filter(Product.name_en.contains(search) | Product.name_id.contains(search))
    
    if category_id:
        query = query.filter_by(category_id=category_id)
    
    products = query.order_by(Product.created_at.desc()).paginate(
        page=page, per_page=10, error_out=False
    )
    
    categories = Category.query.all()
    
    return render_template('admin/products.html', 
                         products=products, 
                         categories=categories,
                         search=search,
                         selected_category=category_id)

@admin.route('/products/add', methods=['GET', 'POST'])
@login_required
def add_product():
    if request.method == 'POST':
        product = Product(
            name_en=request.form['name_en'],
            name_id=request.form['name_id'],
            description_en=request.form['description_en'],
            description_id=request.form['description_id'],
            price=float(request.form['price']),
            unit=request.form['unit'],
            stock_quantity=int(request.form['stock_quantity']),
            min_order_quantity=int(request.form['min_order_quantity']),
            image_url=request.form.get('image_url', ''),
            category_id=int(request.form['category_id']),
            is_available=bool(request.form.get('is_available'))
        )
        
        db.session.add(product)
        db.session.commit()
        
        flash('Product added successfully!', 'success')
        return redirect(url_for('admin.products'))
    
    categories = Category.query.all()
    return render_template('admin/products.html', categories=categories, action='add')

@admin.route('/products/edit/<int:product_id>', methods=['GET', 'POST'])
@login_required
def edit_product(product_id):
    product = Product.query.get_or_404(product_id)
    
    if request.method == 'POST':
        product.name_en = request.form['name_en']
        product.name_id = request.form['name_id']
        product.description_en = request.form['description_en']
        product.description_id = request.form['description_id']
        product.price = float(request.form['price'])
        product.unit = request.form['unit']
        product.stock_quantity = int(request.form['stock_quantity'])
        product.min_order_quantity = int(request.form['min_order_quantity'])
        product.image_url = request.form.get('image_url', '')
        product.category_id = int(request.form['category_id'])
        product.is_available = bool(request.form.get('is_available'))
        product.updated_at = datetime.utcnow()
        
        db.session.commit()
        
        flash('Product updated successfully!', 'success')
        return redirect(url_for('admin.products'))
    
    categories = Category.query.all()
    return render_template('admin/products.html', 
                         categories=categories, 
                         product=product, 
                         action='edit')

@admin.route('/products/delete/<int:product_id>')
@login_required
def delete_product(product_id):
    product = Product.query.get_or_404(product_id)
    db.session.delete(product)
    db.session.commit()
    
    flash('Product deleted successfully!', 'success')
    return redirect(url_for('admin.products'))

@admin.route('/orders')
@login_required
def orders():
    page = request.args.get('page', 1, type=int)
    status = request.args.get('status', 'all')
    
    query = Order.query
    
    if status != 'all':
        query = query.filter_by(status=status)
    
    orders = query.order_by(Order.created_at.desc()).paginate(
        page=page, per_page=10, error_out=False
    )
    
    return render_template('admin/orders.html', orders=orders, selected_status=status)

@admin.route('/orders/<int:order_id>')
@login_required
def order_detail(order_id):
    order = Order.query.get_or_404(order_id)
    return render_template('admin/orders.html', order=order, action='detail')

@admin.route('/orders/<int:order_id>/update', methods=['POST'])
@login_required
def update_order(order_id):
    order = Order.query.get_or_404(order_id)
    
    order.status = request.form['status']
    order.admin_notes = request.form.get('admin_notes', '')
    
    # Update shipping tracking information
    order.shipping_service = request.form.get('shipping_service', '')
    order.tracking_number = request.form.get('tracking_number', '')
    order.shipping_cost = float(request.form.get('shipping_cost', 0) or 0)
    order.is_international = bool(request.form.get('is_international'))
    order.shipping_status = request.form.get('shipping_status', 'not_shipped')
    
    # Set shipping date if status is shipped and no date set
    if order.status == 'shipped' and not order.shipping_date:
        order.shipping_date = datetime.utcnow()
    
    # Calculate estimated delivery based on shipping type
    if order.shipping_date and not order.estimated_delivery:
        from datetime import timedelta
        if order.is_international:
            # International: 7-14 days
            order.estimated_delivery = order.shipping_date + timedelta(days=10)
        else:
            # Domestic: 1-3 days
            order.estimated_delivery = order.shipping_date + timedelta(days=2)
    
    order.updated_at = datetime.utcnow()
    
    db.session.commit()
    
    flash('Order updated successfully!', 'success')
    return redirect(url_for('admin.orders'))

@admin.route('/shipping')
@login_required
def shipping_tracking():
    try:
        page = request.args.get('page', 1, type=int)
        status = request.args.get('status', 'all')
        shipping_type = request.args.get('type', 'all')  # all, domestic, international
        
        query = Order.query.filter(Order.status.in_(['shipped', 'delivered']))
        
        if status != 'all':
            query = query.filter_by(shipping_status=status)
        
        if shipping_type == 'domestic':
            query = query.filter_by(is_international=False)
        elif shipping_type == 'international':
            query = query.filter_by(is_international=True)
        
        orders = query.order_by(Order.shipping_date.desc().nullslast()).paginate(
            page=page, per_page=10, error_out=False
        )
        
        return render_template('admin/shipping.html', 
                             orders=orders, 
                             selected_status=status,
                             selected_type=shipping_type)
    except Exception as e:
        flash(f'Error loading shipping page: {str(e)}', 'error')
        return redirect(url_for('admin.dashboard'))

@admin.route('/orders/<int:order_id>/tracking', methods=['POST'])
@login_required
def update_tracking(order_id):
    order = Order.query.get_or_404(order_id)
    
    order.tracking_number = request.form.get('tracking_number', '')
    order.shipping_service = request.form.get('shipping_service', '')
    order.shipping_status = request.form.get('shipping_status', 'not_shipped')
    order.updated_at = datetime.utcnow()
    
    db.session.commit()
    
    flash('Tracking information updated successfully!', 'success')
    return redirect(url_for('admin.order_detail', order_id=order_id))

@admin.route('/settings', methods=['GET', 'POST'])
@login_required
def settings():
    settings = CompanySettings.query.first()
    if not settings:
        settings = CompanySettings()
        db.session.add(settings)
        db.session.commit()
    
    if request.method == 'POST':
        settings.company_name_en = request.form['company_name_en']
        settings.company_name_id = request.form['company_name_id']
        settings.company_description_en = request.form['company_description_en']
        settings.company_description_id = request.form['company_description_id']
        settings.contact_email = request.form['contact_email']
        settings.contact_phone = request.form['contact_phone']
        settings.contact_whatsapp = request.form['contact_whatsapp']
        settings.address_en = request.form['address_en']
        settings.address_id = request.form['address_id']
        settings.updated_at = datetime.utcnow()
        
        db.session.commit()
        
        flash('Settings updated successfully!', 'success')
        return redirect(url_for('admin.settings'))
    
    return render_template('admin/settings.html', settings=settings)

# Register admin blueprint
app.register_blueprint(admin)
