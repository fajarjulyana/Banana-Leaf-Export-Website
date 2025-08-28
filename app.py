import os
import logging
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from sqlalchemy.orm import DeclarativeBase
from werkzeug.middleware.proxy_fix import ProxyFix

# Configure logging
logging.basicConfig(level=logging.DEBUG)

class Base(DeclarativeBase):
    pass

db = SQLAlchemy(model_class=Base)

# Create the app
app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET", "banana-export-secret-key")
app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1)

# Configure the database with error handling
database_url = os.environ.get("DATABASE_URL", "sqlite:///banana_export.db")
app.config["SQLALCHEMY_DATABASE_URI"] = database_url

# Configure engine options based on database type
if database_url.startswith("postgresql"):
    app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {
        "pool_recycle": 300,
        "pool_pre_ping": True,
        "pool_timeout": 20,
        "pool_size": 5,
        "max_overflow": 10
    }
else:
    app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {
        "pool_pre_ping": True,
    }

# Initialize extensions
db.init_app(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'admin.login'

@login_manager.user_loader
def load_user(user_id):
    from models import Admin
    return Admin.query.get(int(user_id))

# Import routes
from routes import *
from admin_routes import *

# Add custom template filters
@app.template_filter('nl2br')
def nl2br_filter(text):
    """Convert newlines to HTML line breaks"""
    if text is None:
        return ''
    return text.replace('\n', '<br>\n')

def init_database():
    """Initialize database with error handling"""
    try:
        with app.app_context():
            # Import models to ensure tables are created
            import models
            
            # Test database connection first
            try:
                db.engine.execute('SELECT 1')
                print("✓ Database connection successful")
            except Exception as e:
                print(f"⚠ Database connection test failed: {e}")
                print("Falling back to SQLite...")
                app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///banana_export.db"
                db.init_app(app)
            
            # Create all tables
            db.create_all()
            print("✓ Database tables created")
            
            # Create default admin user if none exists
            from models import Admin
            from werkzeug.security import generate_password_hash
            
            if not Admin.query.first():
                admin = Admin(
                    username='admin',
                    email='admin@bananaexport.com',
                    password_hash=generate_password_hash('admin123')
                )
                db.session.add(admin)
                db.session.commit()
                print("✓ Default admin created: username=admin, password=admin123")
                
    except Exception as e:
        print(f"❌ Database initialization failed: {e}")
        print("Using minimal configuration...")

# Initialize database when module is imported
init_database()
