
from app import app, db
from models import CompanySettings
from sqlalchemy import text

def update_company_settings_table():
    """Update CompanySettings table with new appearance columns"""
    with app.app_context():
        try:
            # Check if columns exist, if not add them
            inspector = db.inspect(db.engine)
            columns = [col['name'] for col in inspector.get_columns('company_settings')]
            
            if 'primary_color' not in columns:
                with db.engine.connect() as conn:
                    conn.execute(text('ALTER TABLE company_settings ADD COLUMN primary_color VARCHAR(7) DEFAULT "#28a745"'))
                    conn.commit()
                print("Added primary_color column")
            
            if 'secondary_color' not in columns:
                with db.engine.connect() as conn:
                    conn.execute(text('ALTER TABLE company_settings ADD COLUMN secondary_color VARCHAR(7) DEFAULT "#6c757d"'))
                    conn.commit()
                print("Added secondary_color column")
                
            if 'logo_url' not in columns:
                with db.engine.connect() as conn:
                    conn.execute(text('ALTER TABLE company_settings ADD COLUMN logo_url VARCHAR(500) DEFAULT ""'))
                    conn.commit()
                print("Added logo_url column")
            
            # Create default settings if none exist
            settings = CompanySettings.query.first()
            if not settings:
                settings = CompanySettings()
                db.session.add(settings)
                db.session.commit()
                print("Created default company settings")
            
            print("Database updated successfully!")
            
        except Exception as e:
            print(f"Error updating database: {e}")

if __name__ == '__main__':
    update_company_settings_table()
