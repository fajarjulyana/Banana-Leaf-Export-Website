
from app import app, db
from models import Settings

with app.app_context():
    # Check if layout_type column exists, if not add it
    try:
        settings = Settings.query.first()
        if settings:
            print(f"Current layout_type: {getattr(settings, 'layout_type', 'Field not found')}")
        else:
            print("No settings found")
    except Exception as e:
        print(f"Column might not exist: {e}")
        
        # Add the column
        try:
            db.engine.execute('ALTER TABLE settings ADD COLUMN layout_type VARCHAR(50) DEFAULT "standard"')
            db.session.commit()
            print("✓ Added layout_type column to settings table")
        except Exception as alter_error:
            print(f"Error adding column: {alter_error}")
