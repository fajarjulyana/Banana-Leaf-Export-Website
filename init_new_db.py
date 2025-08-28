#!/usr/bin/env python3
"""
New database initialization script with diverse agricultural products
Including banana leaves, cocofit, charcoal, rice husk, and more
"""

import os
import sys
from app import app, db
from models import Category, Product, CompanySettings, Admin
from werkzeug.security import generate_password_hash

def init_database():
    """Initialize the database with diverse agricultural products"""
    
    with app.app_context():
        print("Creating database tables...")
        
        # Drop and recreate all tables to ensure schema consistency
        db.drop_all()
        db.create_all()
        
        # Create default admin if not exists
        create_default_admin()
        
        # Create company settings if not exists
        create_company_settings()
        
        # Create diverse product categories
        create_agricultural_categories()
        
        # Create diverse agricultural products
        create_agricultural_products()
        
        print("Database initialization completed successfully!")

def create_default_admin():
    """Create default admin user"""
    admin = Admin.query.first()
    if not admin:
        admin = Admin(
            username='admin',
            email='admin@agriexport.com',
            password_hash=generate_password_hash('admin123')
        )
        db.session.add(admin)
        db.session.commit()
        print("✓ Default admin user created (username: admin, password: admin123)")
    else:
        print("✓ Admin user already exists")

def create_company_settings():
    """Create default company settings"""
    settings = CompanySettings.query.first()
    if not settings:
        settings = CompanySettings(
            company_name_en='Agricultural Export Indonesia',
            company_name_id='Ekspor Pertanian Indonesia',
            company_description_en='Premium quality agricultural products from Indonesia for international markets. We specialize in exporting banana leaves, cocofit products, charcoal, rice husk, and various agricultural commodities.',
            company_description_id='Produk pertanian berkualitas premium dari Indonesia untuk pasar internasional. Kami mengkhususkan diri dalam mengekspor daun pisang, produk cocofit, arang, sekam padi, dan berbagai komoditas pertanian.',
            contact_email='info@agriexport.com',
            contact_phone='+62-21-87654321',
            contact_whatsapp='+62-812-9876-5432',
            address_en='Jl. Agro Export Center No. 88, Jakarta 12340, Indonesia',
            address_id='Jl. Agro Export Center No. 88, Jakarta 12340, Indonesia',
            exchange_rate=15000.0,
            default_currency='USD'
        )
        db.session.add(settings)
        db.session.commit()
        print("✓ Company settings created")
    else:
        print("✓ Company settings already exist")

def create_agricultural_categories():
    """Create diverse agricultural product categories"""
    categories_data = [
        {
            'name_en': 'Banana Leaf Products',
            'name_id': 'Produk Daun Pisang',
            'description_en': 'Fresh and processed banana leaves for food packaging, traditional cooking, and ceremonial purposes.',
            'description_id': 'Daun pisang segar dan olahan untuk kemasan makanan, masakan tradisional, dan keperluan upacara.'
        },
        {
            'name_en': 'Coconut Fiber (Cocofit)',
            'name_id': 'Serat Kelapa (Cocofit)',
            'description_en': 'High-quality coconut coir fiber products for horticulture, construction, and industrial applications.',
            'description_id': 'Produk serat sabut kelapa berkualitas tinggi untuk hortikultura, konstruksi, dan aplikasi industri.'
        },
        {
            'name_en': 'Charcoal Products',
            'name_id': 'Produk Arang',
            'description_en': 'Premium charcoal products including coconut shell charcoal and hardwood charcoal for various uses.',
            'description_id': 'Produk arang premium termasuk arang tempurung kelapa dan arang kayu keras untuk berbagai kegunaan.'
        },
        {
            'name_en': 'Rice Husk & By-products',
            'name_id': 'Sekam Padi & Produk Sampingan',
            'description_en': 'Rice husk, rice bran, and other rice processing by-products for animal feed and industrial use.',
            'description_id': 'Sekam padi, dedak padi, dan produk sampingan pengolahan padi lainnya untuk pakan ternak dan penggunaan industri.'
        },
        {
            'name_en': 'Palm Products',
            'name_id': 'Produk Kelapa Sawit',
            'description_en': 'Palm kernel shells, palm fiber, and other palm oil processing by-products.',
            'description_id': 'Cangkang inti sawit, serat sawit, dan produk sampingan pengolahan minyak sawit lainnya.'
        },
        {
            'name_en': 'Spices & Herbs',
            'name_id': 'Rempah & Herbal',
            'description_en': 'Dried Indonesian spices and herbs for culinary and medicinal purposes.',
            'description_id': 'Rempah dan herbal Indonesia kering untuk keperluan kuliner dan obat-obatan.'
        }
    ]
    
    for category_data in categories_data:
        existing = Category.query.filter_by(name_en=category_data['name_en']).first()
        if not existing:
            category = Category(**category_data)
            db.session.add(category)
    
    db.session.commit()
    print(f"✓ Agricultural categories created ({len(categories_data)} categories)")

def create_agricultural_products():
    """Create diverse agricultural products with dual pricing"""
    # Get categories
    banana_leaf = Category.query.filter_by(name_en='Banana Leaf Products').first()
    cocofit = Category.query.filter_by(name_en='Coconut Fiber (Cocofit)').first()
    charcoal = Category.query.filter_by(name_en='Charcoal Products').first()
    rice_husk = Category.query.filter_by(name_en='Rice Husk & By-products').first()
    palm = Category.query.filter_by(name_en='Palm Products').first()
    spices = Category.query.filter_by(name_en='Spices & Herbs').first()
    
    if not all([banana_leaf, cocofit, charcoal, rice_husk, palm, spices]):
        print("⚠ Categories not found, skipping product creation")
        return
    
    products_data = [
        # Banana Leaf Products
        {
            'name_en': 'Premium Fresh Banana Leaves',
            'name_id': 'Daun Pisang Segar Premium',
            'description_en': 'Extra large, fresh banana leaves harvested daily. Perfect for traditional Asian cuisine, food wrapping, and presentations. Size: 40-60cm length.',
            'description_id': 'Daun pisang segar extra besar yang dipanen setiap hari. Sempurna untuk masakan Asia tradisional, pembungkus makanan, dan presentasi. Ukuran: 40-60cm panjang.',
            'price_usd': 2.50,
            'price_idr': 37500,
            'unit': 'kg',
            'stock_quantity': 500,
            'min_order_quantity': 10,
            'category_id': banana_leaf.id,
        },
        {
            'name_en': 'Dried Banana Leaves',
            'name_id': 'Daun Pisang Kering',
            'description_en': 'Naturally dried banana leaves with extended shelf life. Ideal for international shipping and long-term storage.',
            'description_id': 'Daun pisang yang dikeringkan secara alami dengan daya tahan yang diperpanjang. Ideal untuk pengiriman internasional dan penyimpanan jangka panjang.',
            'price_usd': 3.20,
            'price_idr': 48000,
            'unit': 'kg',
            'stock_quantity': 300,
            'min_order_quantity': 5,
            'category_id': banana_leaf.id,
        },
        
        # Coconut Fiber Products
        {
            'name_en': 'Coconut Coir Fiber',
            'name_id': 'Serat Sabut Kelapa',
            'description_en': 'High-quality coconut coir fiber for horticulture applications. Excellent water retention and aeration properties.',
            'description_id': 'Serat sabut kelapa berkualitas tinggi untuk aplikasi hortikultura. Sifat retensi air dan aerasi yang sangat baik.',
            'price_usd': 1.80,
            'price_idr': 27000,
            'unit': 'kg',
            'stock_quantity': 800,
            'min_order_quantity': 50,
            'category_id': cocofit.id,
        },
        {
            'name_en': 'Cocofit Growing Medium',
            'name_id': 'Media Tanam Cocofit',
            'description_en': 'Processed coconut fiber growing medium, perfect for hydroponic and organic farming.',
            'description_id': 'Media tanam serat kelapa yang telah diproses, sempurna untuk hidroponik dan pertanian organik.',
            'price_usd': 2.20,
            'price_idr': 33000,
            'unit': 'kg',
            'stock_quantity': 600,
            'min_order_quantity': 25,
            'category_id': cocofit.id,
        },
        
        # Charcoal Products
        {
            'name_en': 'Coconut Shell Charcoal',
            'name_id': 'Arang Tempurung Kelapa',
            'description_en': 'Premium coconut shell charcoal with high carbon content. Ideal for BBQ, shisha, and industrial applications.',
            'description_id': 'Arang tempurung kelapa premium dengan kandungan karbon tinggi. Ideal untuk BBQ, shisha, dan aplikasi industri.',
            'price_usd': 0.95,
            'price_idr': 14250,
            'unit': 'kg',
            'stock_quantity': 1000,
            'min_order_quantity': 100,
            'category_id': charcoal.id,
        },
        {
            'name_en': 'Hardwood Charcoal',
            'name_id': 'Arang Kayu Keras',
            'description_en': 'High-quality hardwood charcoal for restaurant and industrial use. Long burning time and high heat output.',
            'description_id': 'Arang kayu keras berkualitas tinggi untuk restoran dan penggunaan industri. Waktu bakar lama dan output panas tinggi.',
            'price_usd': 1.15,
            'price_idr': 17250,
            'unit': 'kg',
            'stock_quantity': 750,
            'min_order_quantity': 50,
            'category_id': charcoal.id,
        },
        
        # Rice Husk Products
        {
            'name_en': 'Rice Husk',
            'name_id': 'Sekam Padi',
            'description_en': 'Clean rice husk for animal feed, construction material, and biofuel production.',
            'description_id': 'Sekam padi bersih untuk pakan ternak, bahan konstruksi, dan produksi biofuel.',
            'price_usd': 0.15,
            'price_idr': 2250,
            'unit': 'kg',
            'stock_quantity': 2000,
            'min_order_quantity': 500,
            'category_id': rice_husk.id,
        },
        {
            'name_en': 'Rice Bran',
            'name_id': 'Dedak Padi',
            'description_en': 'Nutritious rice bran for animal feed and food processing industry.',
            'description_id': 'Dedak padi bergizi untuk pakan ternak dan industri pengolahan makanan.',
            'price_usd': 0.25,
            'price_idr': 3750,
            'unit': 'kg',
            'stock_quantity': 1500,
            'min_order_quantity': 200,
            'category_id': rice_husk.id,
        },
        
        # Palm Products
        {
            'name_en': 'Palm Kernel Shell',
            'name_id': 'Cangkang Inti Sawit',
            'description_en': 'Palm kernel shells for biomass fuel and activated carbon production.',
            'description_id': 'Cangkang inti sawit untuk bahan bakar biomassa dan produksi karbon aktif.',
            'price_usd': 0.35,
            'price_idr': 5250,
            'unit': 'kg',
            'stock_quantity': 1200,
            'min_order_quantity': 300,
            'category_id': palm.id,
        },
        
        # Spices
        {
            'name_en': 'Dried Turmeric',
            'name_id': 'Kunyit Kering',
            'description_en': 'Premium dried turmeric from Java, high curcumin content for export quality.',
            'description_id': 'Kunyit kering premium dari Jawa, kandungan curcumin tinggi untuk kualitas ekspor.',
            'price_usd': 4.50,
            'price_idr': 67500,
            'unit': 'kg',
            'stock_quantity': 200,
            'min_order_quantity': 5,
            'category_id': spices.id,
        },
        {
            'name_en': 'Dried Ginger',
            'name_id': 'Jahe Kering',
            'description_en': 'High-quality dried ginger slices, perfect for tea, cooking, and medicinal purposes.',
            'description_id': 'Irisan jahe kering berkualitas tinggi, sempurna untuk teh, memasak, dan keperluan obat.',
            'price_usd': 3.80,
            'price_idr': 57000,
            'unit': 'kg',
            'stock_quantity': 150,
            'min_order_quantity': 5,
            'category_id': spices.id,
        },
    ]
    
    created_count = 0
    for product_data in products_data:
        existing = Product.query.filter_by(name_en=product_data['name_en']).first()
        if not existing:
            product = Product(**product_data)
            db.session.add(product)
            created_count += 1
    
    db.session.commit()
    print(f"✓ Agricultural products created ({created_count} new products)")

def main():
    """Main function"""
    init_database()

if __name__ == '__main__':
    main()