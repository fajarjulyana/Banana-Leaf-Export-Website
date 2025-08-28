from app import app, db
from models import Admin, Category, Product, CompanySettings
from werkzeug.security import generate_password_hash
from datetime import datetime

def init_database():
    with app.app_context():
        # Drop all tables and recreate
        print("Dropping all tables...")
        db.drop_all()

        print("Creating all tables...")
        db.create_all()

        # Create default admin user
        if not Admin.query.first():
            admin = Admin(
                username='admin',
                password_hash=generate_password_hash('admin123')
            )
            db.session.add(admin)
            print("✓ Default admin user created (username: admin, password: admin123)")

        # Create categories
        categories_data = [
            {
                'name_en': 'Banana Leaves',
                'name_id': 'Daun Pisang',
                'description_en': 'Fresh banana leaves for traditional food packaging and cooking',
                'description_id': 'Daun pisang segar untuk pembungkus makanan tradisional dan memasak'
            },
            {
                'name_en': 'Cocofit',
                'name_id': 'Cocofit',
                'description_en': 'Processed coconut fiber growing medium for hydroponics',
                'description_id': 'Media tanam serat kelapa olahan untuk hidroponik'
            },
            {
                'name_en': 'Charcoal',
                'name_id': 'Arang',
                'description_en': 'Premium charcoal products for various applications',
                'description_id': 'Produk arang premium untuk berbagai aplikasi'
            },
            {
                'name_en': 'Rice Husk',
                'name_id': 'Sekam Padi',
                'description_en': 'Rice husk and derived products for agriculture',
                'description_id': 'Sekam padi dan produk turunannya untuk pertanian'
            }
        ]

        created_categories = []
        for cat_data in categories_data:
            if not Category.query.filter_by(name_en=cat_data['name_en']).first():
                category = Category(**cat_data)
                db.session.add(category)
                created_categories.append(category)

        db.session.commit()
        print(f"✓ Categories created ({len(created_categories)} new)")

        # Get categories for products
        banana_leaves = Category.query.filter_by(name_en='Banana Leaves').first()
        cocofit = Category.query.filter_by(name_en='Cocofit').first()
        charcoal = Category.query.filter_by(name_en='Charcoal').first()
        rice_husk = Category.query.filter_by(name_en='Rice Husk').first()

        # Create sample products
        products_data = [
            # Banana Leaves Products
            {
                'name_en': 'Premium Banana Leaves',
                'name_id': 'Daun Pisang Premium',
                'description_en': 'Fresh, clean banana leaves perfect for traditional food wrapping and eco-friendly packaging.',
                'description_id': 'Daun pisang segar dan bersih sempurna untuk pembungkus makanan tradisional dan kemasan ramah lingkungan.',
                'price_usd': 1.50,
                'price_idr': 22500,
                'unit': 'kg',
                'stock_quantity': 500,
                'min_order_quantity': 10,
                'category_id': banana_leaves.id,
                'is_featured': True,
            },
            {
                'name_en': 'Organic Banana Leaves',
                'name_id': 'Daun Pisang Organik',
                'description_en': 'Certified organic banana leaves grown without pesticides. Ideal for premium food packaging.',
                'description_id': 'Daun pisang organik bersertifikat yang ditanam tanpa pestisida. Ideal untuk kemasan makanan premium.',
                'price_usd': 2.00,
                'price_idr': 30000,
                'unit': 'kg',
                'stock_quantity': 300,
                'min_order_quantity': 5,
                'category_id': banana_leaves.id,
                'is_featured': True,
            },

            # Cocofit Products
            {
                'name_en': 'Cocofit Growing Medium',
                'name_id': 'Media Tanam Cocofit',
                'description_en': 'Processed coconut fiber medium perfect for hydroponic and organic farming applications.',
                'description_id': 'Media serat kelapa yang telah diproses, sempurna untuk hidroponik dan pertanian organik.',
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

            # Rice Husk Products
            {
                'name_en': 'Rice Husk Pellets',
                'name_id': 'Pelet Sekam Padi',
                'description_en': 'Compressed rice husk pellets for biomass fuel and growing medium applications.',
                'description_id': 'Pelet sekam padi yang dipadatkan untuk bahan bakar biomassa dan aplikasi media tanam.',
                'price_usd': 0.80,
                'price_idr': 12000,
                'unit': 'kg',
                'stock_quantity': 800,
                'min_order_quantity': 50,
                'category_id': rice_husk.id,
            }
        ]

        created_count = 0
        for prod_data in products_data:
            if not Product.query.filter_by(name_en=prod_data['name_en']).first():
                product = Product(**prod_data)
                db.session.add(product)
                created_count += 1

        db.session.commit()
        print(f"✓ Products created ({created_count} new)")

        # Create company settings
        if not CompanySettings.query.first():
            settings = CompanySettings(
                company_name_en='Indonesian Agricultural Export',
                company_name_id='Ekspor Pertanian Indonesia',
                company_description_en='Premium quality Indonesian agricultural products for international markets with sustainable farming practices.',
                company_description_id='Produk pertanian Indonesia berkualitas premium untuk pasar internasional dengan praktik pertanian berkelanjutan.',
                contact_email='info@agriexport-indonesia.com',
                contact_phone='+62-21-87654321',
                contact_whatsapp='+62-812-9876-5432',
                address_en='Jakarta, Indonesia - Agricultural Export Division',
                address_id='Jakarta, Indonesia - Divisi Ekspor Pertanian',
                exchange_rate=15000.0,
                default_currency='USD'
            )
            db.session.add(settings)
            db.session.commit()
            print("✓ Company settings created")

        print("\n🎉 Database initialization completed successfully!")
        print("You can now log in to the admin panel with:")
        print("Username: admin")
        print("Password: admin123")

if __name__ == '__main__':
    init_database()