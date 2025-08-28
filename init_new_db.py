from app import app, db
from models import Admin, Category, Product, CompanySettings
from werkzeug.security import generate_password_hash
from datetime import datetime

def init_database():
    """Initialize SQLite database with sample data"""
    with app.app_context():
        print("Dropping all tables...")
        db.drop_all()

        print("Creating all tables...")
        db.create_all()

        # Create default admin user
        if not Admin.query.first():
            admin = Admin(
                username='admin',
                email='admin@bananaexport.com',
                password_hash=generate_password_hash('admin123')
            )
            db.session.add(admin)
            print("✓ Default admin user created (username: admin, password: admin123)")

        # Create company settings
        if not CompanySettings.query.first():
            settings = CompanySettings(
                company_name_en='Banana Leaf Export Co.',
                company_name_id='Perusahaan Ekspor Daun Pisang',
                company_description_en='Premium quality banana leaves for international markets.',
                company_description_id='Daun pisang berkualitas premium untuk pasar internasional.',
                contact_email='info@bananaexport.com',
                contact_phone='+62-21-12345678',
                contact_whatsapp='+62-812-3456-7890',
                address_en='Jakarta, Indonesia',
                address_id='Jakarta, Indonesia',
                exchange_rate=15300.0
            )
            db.session.add(settings)
            print("✓ Company settings created")

        # Create sample categories
        categories_data = [
            {
                'name_en': 'Fresh Banana Leaves',
                'name_id': 'Daun Pisang Segar',
                'description_en': 'Fresh, green banana leaves perfect for food packaging.',
                'description_id': 'Daun pisang segar dan hijau yang sempurna untuk kemasan makanan.'
            },
            {
                'name_en': 'Dried Banana Leaves',
                'name_id': 'Daun Pisang Kering',
                'description_en': 'Naturally dried banana leaves with extended shelf life.',
                'description_id': 'Daun pisang yang dikeringkan secara alami dengan daya tahan yang lebih lama.'
            }
        ]

        for category_data in categories_data:
            existing = Category.query.filter_by(name_en=category_data['name_en']).first()
            if not existing:
                category = Category(**category_data)
                db.session.add(category)

        db.session.commit()
        print("✓ Sample categories created")

        # Create sample products
        fresh_category = Category.query.filter_by(name_en='Fresh Banana Leaves').first()

        if fresh_category:
            products_data = [
                {
                    'name_en': 'Premium Fresh Banana Leaves',
                    'name_id': 'Daun Pisang Segar Premium',
                    'description_en': 'Extra large, fresh banana leaves harvested daily. Perfect for traditional Asian cuisine.',
                    'description_id': 'Daun pisang segar extra besar yang dipanen setiap hari. Sempurna untuk masakan Asia tradisional.',
                    'price_idr': 35000,
                    'price_usd': 35000 / 15300,
                    'unit': 'kg',
                    'stock_quantity': 500,
                    'min_order_quantity': 10,
                    'category_id': fresh_category.id,
                    'is_available': True
                }
            ]

            for product_data in products_data:
                existing = Product.query.filter_by(name_en=product_data['name_en']).first()
                if not existing:
                    product = Product(**product_data)
                    db.session.add(product)

            db.session.commit()
            print("✓ Sample products created")

        print("✓ SQLite database initialization completed successfully!")

if __name__ == '__main__':
    init_database()