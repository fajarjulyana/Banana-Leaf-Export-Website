import os
from sqlalchemy import text
from app import app, db
from models import CompanySettings   # pakai CompanySettings, bukan Settings

def upgrade_database():
    with app.app_context():
        # Check if the database file exists before attempting to connect
        db_file_path = os.path.abspath('instance/banana_export.db')
        if not os.path.exists(db_file_path):
            print(f"Database file does not exist: {db_file_path}")
            return

        try:
            db.session.execute(
                text(
                    'ALTER TABLE company_settings ADD COLUMN gallery_mode TEXT'
                ))
            db.session.commit()
            print("Column 'gallery_mode' added successfully.")
        except Exception as e:
            print(f"Error occurred: {e}")
            db.session.rollback()


if __name__ == "__main__":
    upgrade_database()
