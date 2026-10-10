"""
Standalone database repair and migration script for quorv.org.
Usage via SSH or cPanel Terminal: python fix_db.py
"""
import os
import sys
import sqlite3

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(BASE_DIR, 'db.sqlite3')

print("=== Quorv Database Health Check ===")
if os.path.exists(db_path):
    print(f"Found database at: {db_path}")
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Check core_industry table
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='core_industry';")
    if cursor.fetchone():
        cursor.execute("PRAGMA table_info(core_industry);")
        cols = [col[1] for col in cursor.fetchall()]
        print(f"Current columns in core_industry: {cols}")
        if 'image_url' not in cols:
            print("Adding missing column 'image_url' to core_industry...")
            cursor.execute("ALTER TABLE core_industry ADD COLUMN image_url varchar(500) DEFAULT '';")
            conn.commit()
            print("Successfully added image_url column!")
        else:
            print("Column 'image_url' is already present.")
    else:
        print("Table 'core_industry' not found yet.")
    conn.close()
else:
    print(f"Note: db.sqlite3 not found at {db_path} (will be created by migrate)")

# Run Django migrate
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
try:
    import django
    django.setup()
    from django.core.management import call_command
    print("Running Django migrations...")
    call_command('migrate', interactive=False)
    print("Migrations completed successfully!")
except Exception as e:
    print(f"Django migrate output: {e}")

print("=== Done ===")
