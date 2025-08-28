from flask import render_template, request, redirect, url_for, flash, Blueprint
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import check_password_hash, generate_password_hash
from werkzeug.utils import secure_filename
from app import app, db
from models import Admin, Product, Category, Order, OrderItem, CompanySettings
from datetime import datetime
import os
import uuid

# Admin Blueprint
admin = Blueprint('admin', __name__, url_prefix='/admin')

# Upload configuration
UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def create_upload_folder():
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)

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

def sanitize_text(text):
    """Remove or replace problematic Unicode characters"""
    if not text:
        return text
    # Remove common emoji and special Unicode characters that cause encoding issues
    import re
    # Replace common problematic characters
    text = re.sub(r'[\u2700-\u27BF]', '', text)  # Remove dingbats
    text = re.sub(r'[\u2600-\u26FF]', '', text)  # Remove miscellaneous symbols
    text = re.sub(r'[\u2000-\u206F]', ' ', text)  # Replace general punctuation with space
    # Ensure the text can be encoded as UTF-8
    try:
        text.encode('utf-8')
        return text.strip()
    except UnicodeEncodeError:
        # If still problematic, keep only ASCII characters
        return ''.join(char for char in text if ord(char) < 128).strip()

@admin.route('/products/add', methods=['GET', 'POST'])
@login_required
def add_product():
    if request.method == 'POST':
        create_upload_folder()

        # Handle image upload
        image_url = request.form.get('image_url', '')
        if 'image_file' in request.files:
            file = request.files['image_file']
            if file and file.filename != '' and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                # Add unique identifier to prevent filename conflicts
                unique_filename = f"{uuid.uuid4().hex}_{filename}"
                file_path = os.path.join(UPLOAD_FOLDER, unique_filename)
                file.save(file_path)
                image_url = f"/static/uploads/{unique_filename}"

        # Sanitize text inputs to prevent Unicode encoding errors
        try:
            # Price input is in IDR (base currency)
            price_idr = float(request.form['price'])
            price_usd = price_idr / 15300  # Convert IDR to USD for reference only

            product = Product(
                name_en=sanitize_text(request.form['name_en']),
                name_id=sanitize_text(request.form['name_id']),
                description_en=sanitize_text(request.form['description_en']),
                description_id=sanitize_text(request.form['description_id']),
                price_idr=price_idr,  # Store input price as IDR (base currency)
                price_usd=price_usd,  # Store converted USD for reference
                unit=sanitize_text(request.form['unit']),
                stock_quantity=int(request.form['stock_quantity']),
                min_order_quantity=int(request.form['min_order_quantity']),
                image_url=image_url,
                category_id=int(request.form['category_id']),
                is_available=bool(request.form.get('is_available'))
            )

            db.session.add(product)
            db.session.commit()

            flash('Product added successfully!', 'success')
            return redirect(url_for('admin.products'))
        except (ValueError, UnicodeEncodeError) as e:
            flash(f'Error adding product: Please check your input for special characters. {str(e)}', 'error')
            db.session.rollback()

    categories = Category.query.all()
    return render_template('admin/products.html', categories=categories, action='add')

@admin.route('/products/edit/<int:product_id>', methods=['GET', 'POST'])
@login_required
def edit_product(product_id):
    product = Product.query.get_or_404(product_id)

    if request.method == 'POST':
        create_upload_folder()

        # Handle image upload
        image_url = request.form.get('image_url', product.image_url)
        if 'image_file' in request.files:
            file = request.files['image_file']
            if file and file.filename != '' and allowed_file(file.filename):
                # Delete old image if it exists and is not a URL
                if product.image_url and product.image_url.startswith('/static/uploads/'):
                    old_file_path = product.image_url[1:]  # Remove leading slash
                    if os.path.exists(old_file_path):
                        os.remove(old_file_path)

                filename = secure_filename(file.filename)
                unique_filename = f"{uuid.uuid4().hex}_{filename}"
                file_path = os.path.join(UPLOAD_FOLDER, unique_filename)
                file.save(file_path)
                image_url = f"/static/uploads/{unique_filename}"

        try:
            # Price input is in IDR (base currency)
            price_idr = float(request.form['price'])
            price_usd = price_idr / 15300  # Convert IDR to USD for reference only

            product.name_en = sanitize_text(request.form['name_en'])
            product.name_id = sanitize_text(request.form['name_id'])
            product.description_en = sanitize_text(request.form['description_en'])
            product.description_id = sanitize_text(request.form['description_id'])
            product.price_idr = price_idr  # Store input price as IDR (base currency)
            product.price_usd = price_usd  # Store converted USD for reference
            product.unit = sanitize_text(request.form['unit'])
            product.stock_quantity = int(request.form['stock_quantity'])
            product.min_order_quantity = int(request.form['min_order_quantity'])
            product.image_url = image_url
            product.category_id = int(request.form['category_id'])
            product.is_available = bool(request.form.get('is_available'))
            product.updated_at = datetime.utcnow()

            db.session.commit()
        except (ValueError, UnicodeEncodeError) as e:
            flash(f'Error updating product: Please check your input for special characters. {str(e)}', 'error')
            db.session.rollback()
            return redirect(url_for('admin.edit_product', product_id=product_id))

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

@admin.route('/categories')
@login_required
def categories():
    page = request.args.get('page', 1, type=int)
    search = request.args.get('search', '')

    query = Category.query

    if search:
        query = query.filter(Category.name_en.contains(search) | Category.name_id.contains(search))

    categories = query.order_by(Category.created_at.desc()).paginate(
        page=page, per_page=10, error_out=False
    )

    return render_template('admin/categories.html', categories=categories, search=search)

@admin.route('/categories/add', methods=['GET', 'POST'])
@login_required
def add_category():
    if request.method == 'POST':
        try:
            category = Category(
                name_en=sanitize_text(request.form['name_en']),
                name_id=sanitize_text(request.form['name_id']),
                description_en=sanitize_text(request.form.get('description_en', '')),
                description_id=sanitize_text(request.form.get('description_id', ''))
            )

            db.session.add(category)
            db.session.commit()

            flash('Category added successfully!', 'success')
            return redirect(url_for('admin.categories'))
        except (ValueError, UnicodeEncodeError) as e:
            flash(f'Error adding category: Please check your input for special characters. {str(e)}', 'error')
            db.session.rollback()

    return render_template('admin/categories.html', action='add')

@admin.route('/categories/edit/<int:category_id>', methods=['GET', 'POST'])
@login_required
def edit_category(category_id):
    category = Category.query.get_or_404(category_id)

    if request.method == 'POST':
        try:
            category.name_en = sanitize_text(request.form['name_en'])
            category.name_id = sanitize_text(request.form['name_id'])
            category.description_en = sanitize_text(request.form.get('description_en', ''))
            category.description_id = sanitize_text(request.form.get('description_id', ''))

            db.session.commit()

            flash('Category updated successfully!', 'success')
            return redirect(url_for('admin.categories'))
        except (ValueError, UnicodeEncodeError) as e:
            flash(f'Error updating category: Please check your input for special characters. {str(e)}', 'error')
            db.session.rollback()
            return redirect(url_for('admin.edit_category', category_id=category_id))

    return render_template('admin/categories.html', category=category, action='edit')

@admin.route('/categories/delete/<int:category_id>')
@login_required
def delete_category(category_id):
    category = Category.query.get_or_404(category_id)

    # Check if category has products
    if category.products:
        flash('Cannot delete category with existing products!', 'error')
        return redirect(url_for('admin.categories'))

    db.session.delete(category)
    db.session.commit()

    flash('Category deleted successfully!', 'success')
    return redirect(url_for('admin.categories'))

@admin.route('/settings', methods=['GET', 'POST'])
@login_required
def settings():
    settings = CompanySettings.query.first()
    if not settings:
        settings = CompanySettings()
        db.session.add(settings)
        db.session.commit()

    if request.method == 'POST':
        create_upload_folder()

        # Handle logo upload
        logo_url = settings.logo_url or ''
        if 'logo_file' in request.files:
            file = request.files['logo_file']
            if file and file.filename != '' and allowed_file(file.filename):
                # Delete old logo if it exists and is not a URL
                if settings.logo_url and settings.logo_url.startswith('/static/uploads/'):
                    old_file_path = settings.logo_url[1:]  # Remove leading slash
                    if os.path.exists(old_file_path):
                        os.remove(old_file_path)

                filename = secure_filename(file.filename)
                unique_filename = f"logo_{uuid.uuid4().hex}_{filename}"
                file_path = os.path.join(UPLOAD_FOLDER, unique_filename)
                file.save(file_path)
                logo_url = f"/static/uploads/{unique_filename}"

        # Handle gallery images upload
        gallery_images = settings.gallery_images or ''
        existing_gallery = gallery_images.split(',') if gallery_images else []
        
        if 'gallery_files' in request.files:
            files = request.files.getlist('gallery_files')
            new_gallery_images = []
            
            for file in files:
                if file and file.filename != '' and allowed_file(file.filename):
                    filename = secure_filename(file.filename)
                    unique_filename = f"gallery_{uuid.uuid4().hex}_{filename}"
                    file_path = os.path.join(UPLOAD_FOLDER, unique_filename)
                    file.save(file_path)
                    new_gallery_images.append(f"/static/uploads/{unique_filename}")
            
            # Combine existing and new images
            all_gallery_images = [img.strip() for img in existing_gallery if img.strip()] + new_gallery_images
            gallery_images = ','.join(all_gallery_images)

        settings.company_name_en = request.form['company_name_en']
        settings.company_name_id = request.form['company_name_id']
        settings.company_description_en = request.form['company_description_en']
        settings.company_description_id = request.form['company_description_id']
        settings.contact_email = request.form['contact_email']
        settings.contact_phone = request.form['contact_phone']
        settings.contact_whatsapp = request.form['contact_whatsapp']
        settings.address_en = request.form['address_en']
        settings.address_id = request.form['address_id']
        # Appearance settings
        settings.primary_color = request.form['primary_color']
        settings.secondary_color = request.form['secondary_color']
        settings.logo_url = logo_url
        # Copyright settings
        settings.copyright_text = request.form.get('copyright_text', settings.copyright_text)
        settings.layout_type = request.form.get('layout_type', 'standard')
        # Gallery settings
        settings.gallery_images = gallery_images

        db.session.commit()

        flash('Settings updated successfully!', 'success')
        return redirect(url_for('admin.settings'))

    return render_template('admin/settings.html', settings=settings)

@admin.route('/settings/remove-gallery-image', methods=['POST'])
@login_required
def remove_gallery_image():
    settings = CompanySettings.query.first()
    if not settings:
        flash('Settings not found', 'error')
        return redirect(url_for('admin.settings'))
    
    image_url = request.form.get('image_url')
    if not image_url:
        flash('Invalid image URL', 'error')
        return redirect(url_for('admin.settings'))
    
    # Remove image from gallery list
    gallery_images = settings.gallery_images or ''
    gallery_list = [img.strip() for img in gallery_images.split(',') if img.strip()]
    
    if image_url in gallery_list:
        gallery_list.remove(image_url)
        settings.gallery_images = ','.join(gallery_list)
        
        # Delete physical file if it exists
        if image_url.startswith('/static/uploads/'):
            file_path = image_url[1:]  # Remove leading slash
            if os.path.exists(file_path):
                os.remove(file_path)
        
        db.session.commit()
        flash('Gallery image removed successfully!', 'success')
    else:
        flash('Image not found in gallery', 'error')
    
    return redirect(url_for('admin.settings'))

# Register admin blueprint
app.register_blueprint(admin)