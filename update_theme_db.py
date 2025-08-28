
from app import app, db
from models import CompanySettings
from sqlalchemy import text

def update_theme_system():
    """Update CompanySettings table with theme system columns"""
    with app.app_context():
        try:
            # Check if columns exist, if not add them
            inspector = db.inspect(db.engine)
            columns = [col['name'] for col in inspector.get_columns('company_settings')]
            
            if 'selected_theme' not in columns:
                with db.engine.connect() as conn:
                    conn.execute(text('ALTER TABLE company_settings ADD COLUMN selected_theme VARCHAR(50) DEFAULT "nature_life"'))
                    conn.commit()
                print("Added selected_theme column")
            
            if 'custom_primary_color' not in columns:
                with db.engine.connect() as conn:
                    conn.execute(text('ALTER TABLE company_settings ADD COLUMN custom_primary_color VARCHAR(7) DEFAULT "#28a745"'))
                    conn.commit()
                print("Added custom_primary_color column")
                
            if 'custom_secondary_color' not in columns:
                with db.engine.connect() as conn:
                    conn.execute(text('ALTER TABLE company_settings ADD COLUMN custom_secondary_color VARCHAR(7) DEFAULT "#6c757d"'))
                    conn.commit()
                print("Added custom_secondary_color column")
            
            if 'custom_accent_color' not in columns:
                with db.engine.connect() as conn:
                    conn.execute(text('ALTER TABLE company_settings ADD COLUMN custom_accent_color VARCHAR(7) DEFAULT "#17a2b8"'))
                    conn.commit()
                print("Added custom_accent_color column")
            
            if 'theme_mode' not in columns:
                with db.engine.connect() as conn:
                    conn.execute(text('ALTER TABLE company_settings ADD COLUMN theme_mode VARCHAR(20) DEFAULT "preset"'))
                    conn.commit()
                print("Added theme_mode column")
            
            # Create default settings if none exist
            settings = CompanySettings.query.first()
            if not settings:
                settings = CompanySettings()
                db.session.add(settings)
                db.session.commit()
                print("Created default company settings")
            else:
                # Update existing settings with default theme
                if not settings.selected_theme:
                    settings.selected_theme = 'nature_life'
                if not settings.theme_mode:
                    settings.theme_mode = 'preset'
                db.session.commit()
                print("Updated existing settings with default theme")
            
            print("Theme system database updated successfully!")
            
        except Exception as e:
            print(f"Error updating database: {e}")

if __name__ == '__main__':
    update_theme_system()
