#!/usr/bin/env python3
"""
Database initialization script for Banana Leaf Export website
This script creates sample categories and products for demonstration
"""

import os
import sys
from app import app, db
from models import Category, Product, CompanySettings, Admin
from werkzeug.security import generate_password_hash

def init_database():
    """Initialize the database with sample data"""
    
    with app.app_context():
        print("Creating database tables...")
        db.create_all()
        
        # Create default admin if not exists
        create_default_admin()
        
        # Create company settings if not exists
        create_company_settings()
        
        # Create sample categories if not exist
        create_sample_categories()
        
        # Create sample products if not exist
        create_sample_products()
        
        print("Database initialization completed successfully!")

def create_default_admin():
    """Create default admin user"""
    admin = Admin.query.first()
    if not admin:
        admin = Admin(
            username='admin',
            email='admin@bananaexport.com',
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
            company_name_en='Banana Leaf Export Co.',
            company_name_id='Perusahaan Ekspor Daun Pisang',
            company_description_en='Premium quality banana leaves for international markets. We specialize in exporting fresh, organic banana leaves sourced directly from Indonesian plantations.',
            company_description_id='Daun pisang berkualitas premium untuk pasar internasional. Kami mengkhususkan diri dalam mengekspor daun pisang segar organik yang bersumber langsung dari perkebunan Indonesia.',
            contact_email='info@bananaexport.com',
            contact_phone='+62-21-12345678',
            contact_whatsapp='+62-812-3456-7890',
            address_en='Jl. Export Plaza No. 123, Jakarta 12345, Indonesia',
            address_id='Jl. Export Plaza No. 123, Jakarta 12345, Indonesia'
        )
        db.session.add(settings)
        db.session.commit()
        print("✓ Company settings created")
    else:
        print("✓ Company settings already exist")

def create_sample_categories():
    """Create sample product categories"""
    categories_data = [
        {
            'name_en': 'Fresh Banana Leaves',
            'name_id': 'Daun Pisang Segar',
            'description_en': 'Fresh, green banana leaves perfect for food packaging, traditional cooking, and ceremonial purposes.',
            'description_id': 'Daun pisang segar dan hijau yang sempurna untuk kemasan makanan, masakan tradisional, dan keperluan upacara.'
        },
        {
            'name_en': 'Dried Banana Leaves',
            'name_id': 'Daun Pisang Kering',
            'description_en': 'Naturally dried banana leaves with extended shelf life, ideal for long-distance shipping.',
            'description_id': 'Daun pisang yang dikeringkan secara alami dengan daya tahan yang lebih lama, ideal untuk pengiriman jarak jauh.'
        },
        {
            'name_en': 'Processed Banana Leaves',
            'name_id': 'Daun Pisang Olahan',
            'description_en': 'Pre-treated banana leaves ready for commercial use in restaurants and food industries.',
            'description_id': 'Daun pisang yang telah diproses dan siap digunakan secara komersial di restoran dan industri makanan.'
        },
        {
            'name_en': 'Organic Banana Leaves',
            'name_id': 'Daun Pisang Organik',
            'description_en': 'Certified organic banana leaves grown without pesticides or chemical fertilizers.',
            'description_id': 'Daun pisang organik bersertifikat yang ditanam tanpa pestisida atau pupuk kimia.'
        }
    ]
    
    for category_data in categories_data:
        existing = Category.query.filter_by(name_en=category_data['name_en']).first()
        if not existing:
            category = Category(**category_data)
            db.session.add(category)
    
    db.session.commit()
    print(f"✓ Sample categories created ({len(categories_data)} categories)")

def create_sample_products():
    """Create sample products"""
    # Get categories
    fresh_category = Category.query.filter_by(name_en='Fresh Banana Leaves').first()
    dried_category = Category.query.filter_by(name_en='Dried Banana Leaves').first()
    processed_category = Category.query.filter_by(name_en='Processed Banana Leaves').first()
    organic_category = Category.query.filter_by(name_en='Organic Banana Leaves').first()
    
    if not all([fresh_category, dried_category, processed_category, organic_category]):
        print("⚠ Categories not found, skipping product creation")
        return
    
    products_data = [
        {
            'name_en': 'Premium Fresh Banana Leaves',
            'name_id': 'Daun Pisang Segar Premium',
            'description_en': 'Extra large, fresh banana leaves harvested daily. Perfect for traditional Asian cuisine, food wrapping, and presentations. Size: 40-60cm length.',
            'description_id': 'Daun pisang segar extra besar yang dipanen setiap hari. Sempurna untuk masakan Asia tradisional, pembungkus makanan, dan presentasi. Ukuran: 40-60cm panjang.',
            'price': 35000,
            'unit': 'kg',
            'stock_quantity': 500,
            'min_order_quantity': 10,
            'category_id': fresh_category.id,
            'is_available': True
        },
        {
            'name_en': 'Standard Fresh Banana Leaves',
            'name_id': 'Daun Pisang Segar Standar',
            'description_en': 'High-quality fresh banana leaves suitable for commercial and home use. Size: 30-40cm length.',
            'description_id': 'Daun pisang segar berkualitas tinggi yang cocok untuk penggunaan komersial dan rumah tangga. Ukuran: 30-40cm panjang.',
            'price': 25000,
            'unit': 'kg',
            'stock_quantity': 750,
            'min_order_quantity': 20,
            'category_id': fresh_category.id,
            'is_available': True
        },
        {
            'name_en': 'Natural Dried Banana Leaves',
            'name_id': 'Daun Pisang Kering Alami',
            'description_en': 'Naturally sun-dried banana leaves with 6-month shelf life. Excellent for international shipping and storage.',
            'description_id': 'Daun pisang yang dikeringkan secara alami dengan daya tahan 6 bulan. Sangat baik untuk pengiriman internasional dan penyimpanan.',
            'price': 45000,
            'unit': 'kg',
            'stock_quantity': 300,
            'min_order_quantity': 5,
            'category_id': dried_category.id,
            'is_available': True
        },
        {
            'name_en': 'Machine Dried Banana Leaves',
            'name_id': 'Daun Pisang Kering Mesin',
            'description_en': 'Machine-dried banana leaves with consistent quality and extended shelf life. Ideal for food service industry.',
            'description_id': 'Daun pisang kering mesin dengan kualitas konsisten dan daya tahan yang diperpanjang. Ideal untuk industri layanan makanan.',
            'price': 65000,
            'unit': 'kg',
            'stock_quantity': 200,
            'min_order_quantity': 5,
            'category_id': dried_category.id,
            'is_available': True
        },
        {
            'name_en': 'Restaurant Grade Processed Leaves',
            'name_id': 'Daun Olahan Kelas Restoran',
            'description_en': 'Pre-cleaned and processed banana leaves ready for immediate commercial use. Sanitized and vacuum-packed.',
            'description_id': 'Daun pisang yang telah dibersihkan dan diproses siap untuk penggunaan komersial langsung. Disanitasi dan dikemas vakum.',
            'price': 95000,
            'unit': 'kg',
            'stock_quantity': 150,
            'min_order_quantity': 3,
            'category_id': processed_category.id,
            'is_available': True
        },
        {
            'name_en': 'Food Service Bundle Pack',
            'name_id': 'Paket Bundle Layanan Makanan',
            'description_en': 'Convenient bundle pack of processed banana leaves for restaurants and catering services. Includes 50 pieces of uniform size.',
            'description_id': 'Paket bundle praktis daun pisang olahan untuk restoran dan layanan katering. Termasuk 50 lembar dengan ukuran seragam.',
            'price': 210000,
            'unit': 'bundle',
            'stock_quantity': 100,
            'min_order_quantity': 2,
            'category_id': processed_category.id,
            'is_available': True
        },
        {
            'name_en': 'Certified Organic Fresh Leaves',
            'name_id': 'Daun Segar Organik Bersertifikat',
            'description_en': 'USDA certified organic fresh banana leaves. Grown without pesticides or chemical fertilizers. Premium quality for health-conscious consumers.',
            'description_id': 'Daun pisang segar organik bersertifikat USDA. Ditanam tanpa pestisida atau pupuk kimia. Kualitas premium untuk konsumen yang sadar kesehatan.',
            'price': 58000,
            'unit': 'kg',
            'stock_quantity': 200,
            'min_order_quantity': 5,
            'category_id': organic_category.id,
            'is_available': True
        },
        {
            'name_en': 'Organic Dried Leaves Premium',
            'name_id': 'Daun Kering Organik Premium',
            'description_en': 'Premium organic dried banana leaves with extended shelf life. Perfect for export to health-conscious international markets.',
            'description_id': 'Daun pisang kering organik premium dengan daya tahan yang diperpanjang. Sempurna untuk ekspor ke pasar internasional yang sadar kesehatan.',
            'price': 78000,
            'unit': 'kg',
            'stock_quantity': 120,
            'min_order_quantity': 3,
            'category_id': organic_category.id,
            'is_available': True
        }
    ]
    
    created_count = 0
    for product_data in products_data:
        existing = Product.query.filter_by(name_en=product_data['name_en']).first()
        if not existing:
            product = Product(**product_data)
            db.session.add(product)
            created_count += 1
    
    db.session.commit()
    print(f"✓ Sample products created ({created_count} new products)")

def reset_database():
    """Reset the entire database (WARNING: This will delete all data!)"""
    
    response = input("  WARNING: This will delete ALL data in the database! Are you sure? (yes/no): ")
    if response.lower() != 'yes':
        print("Database reset cancelled.")
        return
    
    with app.app_context():
        print("Dropping all tables...")
        db.drop_all()
        print("✓ All tables dropped")
        
        print("Creating fresh database...")
        init_database()

def main():
    """Main function to handle command line arguments"""
    
    if len(sys.argv) > 1:
        command = sys.argv[1]
        
        if command == 'reset':
            reset_database()
        elif command == 'init':
            init_database()
        elif command == 'categories':
            with app.app_context():
                create_sample_categories()
        elif command == 'products':
            with app.app_context():
                create_sample_products()
        else:
            print("Available commands:")
            print("  python init_db.py init       - Initialize database with sample data")
            print("  python init_db.py reset      - Reset entire database (WARNING: deletes all data)")
            print("  python init_db.py categories - Create sample categories only")
            print("  python init_db.py products   - Create sample products only")
    else:
        init_database()

if __name__ == '__main__':
    main()
