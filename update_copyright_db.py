
from app import app, db
from models import CompanySettings
from sqlalchemy import text

def update_copyright_column():
    """Add copyright column to CompanySettings table"""
    with app.app_context():
        try:
            # Check if copyright_text column exists
            inspector = db.inspect(db.engine)
            columns = [col['name'] for col in inspector.get_columns('company_settings')]
            
            if 'copyright_text' not in columns:
                with db.engine.connect() as conn:
                    conn.execute(text('ALTER TABLE company_settings ADD COLUMN copyright_text VARCHAR(200) DEFAULT "© 2024 Website by Fajar Julyana. All rights reserved."'))
                    conn.commit()
                print("Added copyright_text column")
            
            # Update existing settings with default copyright if empty
            settings = CompanySettings.query.first()
            if settings and not settings.copyright_text:
                settings.copyright_text = "© 2024 Website by Fajar Julyana. All rights reserved."
                db.session.commit()
                print("Updated default copyright text")
            
            print("Copyright database update completed successfully!")
            
        except Exception as e:
            print(f"Error updating database: {e}")

if __name__ == '__main__':
    update_copyright_column()
