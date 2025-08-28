from app import db
from flask_login import UserMixin
from datetime import datetime
from sqlalchemy import func

class Admin(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Category(db.Model):
    __tablename__ = 'category'
    id = db.Column(db.Integer, primary_key=True)
    name_en = db.Column(db.String(100), nullable=False)
    name_id = db.Column(db.String(100), nullable=False)
    description_en = db.Column(db.Text)
    description_id = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationship
    products = db.relationship('Product', back_populates='category', lazy=True)

class Product(db.Model):
    __tablename__ = 'product'
    id = db.Column(db.Integer, primary_key=True)
    name_en = db.Column(db.String(200), nullable=False)
    name_id = db.Column(db.String(200), nullable=False)
    description_en = db.Column(db.Text)
    description_id = db.Column(db.Text)
    price_usd = db.Column(db.Numeric(10, 2), nullable=False)
    price_idr = db.Column(db.Numeric(15, 2), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=False)
    stock_quantity = db.Column(db.Integer, default=0)
    min_order_quantity = db.Column(db.Integer, default=1)
    unit = db.Column(db.String(50), default='kg')
    image_url = db.Column(db.String(500))
    is_available = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationship
    category = db.relationship('Category', back_populates='products')

class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    order_number = db.Column(db.String(50), unique=True, nullable=False)
    customer_name = db.Column(db.String(100), nullable=False)
    customer_email = db.Column(db.String(120), nullable=False)
    customer_phone = db.Column(db.String(20))
    customer_company = db.Column(db.String(100))
    customer_country = db.Column(db.String(100), nullable=False)
    shipping_address = db.Column(db.Text, nullable=False)
    total_amount = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(20), nullable=False, default='pending')
    notes = db.Column(db.Text)
    admin_notes = db.Column(db.Text)

    # Shipping tracking fields
    shipping_service = db.Column(db.String(50))
    tracking_number = db.Column(db.String(100))
    shipping_date = db.Column(db.DateTime)
    estimated_delivery = db.Column(db.DateTime)
    shipping_cost = db.Column(db.Float, default=0.0)
    is_international = db.Column(db.Boolean, default=False)
    shipping_status = db.Column(db.String(20), default='not_shipped')

    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationship with order items
    items = db.relationship('OrderItem', backref='order', lazy=True, cascade='all, delete-orphan')

class OrderItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('order.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    unit_price = db.Column(db.Float, nullable=False)
    total_price = db.Column(db.Float, nullable=False)

    # Relationship
    product = db.relationship('Product', backref='order_items')

class CompanySettings(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    company_name_en = db.Column(db.String(200), nullable=False, default='Agricultural Export Co.')
    company_name_id = db.Column(db.String(200), nullable=False, default='Perusahaan Ekspor Pertanian')
    company_description_en = db.Column(db.Text, default='Premium quality agricultural products for international markets')
    company_description_id = db.Column(db.Text, default='Produk pertanian berkualitas premium untuk pasar internasional')
    contact_email = db.Column(db.String(200), default='info@agriexport.com')
    contact_phone = db.Column(db.String(50), default='+62-21-12345678')
    contact_whatsapp = db.Column(db.String(50), default='+62-812-3456-7890')
    address_en = db.Column(db.Text, default='Jakarta, Indonesia')
    address_id = db.Column(db.Text, default='Jakarta, Indonesia')
    exchange_rate = db.Column(db.Float, default=15000.0)  # USD to IDR exchange rate
    default_currency = db.Column(db.String(3), default='USD')  # USD or IDR
    # Appearance settings
    primary_color = db.Column(db.String(7), default='#28a745')  # Green color
    secondary_color = db.Column(db.String(7), default='#6c757d')  # Gray color
    logo_url = db.Column(db.String(500), default='')
    # Copyright settings
    copyright_text = db.Column(db.String(255), default="© 2024 Website by Fajar Julyana. All rights reserved.")
    layout_type = db.Column(db.String(50), default="standard")
    # Gallery settings
    gallery_images = db.Column(db.Text, default='')
    gallery_mode = db.Column(db.String(20), default='static')  # static or carousel

    # Theme System
    selected_theme = db.Column(db.String(50), default='nature_life')  # nature_life, enjoy_nature, quality_care
    custom_primary_color = db.Column(db.String(7), default='#28a745')
    custom_secondary_color = db.Column(db.String(7), default='#6c757d')
    custom_accent_color = db.Column(db.String(7), default='#17a2b8')
    theme_mode = db.Column(db.String(20), default='preset')  # preset or custom

    def __repr__(self):
        return f'<CompanySettings {self.company_name_en}>'