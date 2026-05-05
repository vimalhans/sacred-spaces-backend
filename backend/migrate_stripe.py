import sqlite3
import os

db_path = 'worship.db'

def migrate():
    if not os.path.exists(db_path):
        print(f"Database not found at {db_path}")
        return

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    try:
        print("Adding is_premium column...")
        cursor.execute("ALTER TABLE places_of_worship ADD COLUMN is_premium BOOLEAN DEFAULT 0")
    except sqlite3.OperationalError:
        print("is_premium column already exists.")

    try:
        print("Adding stripe_customer_id column...")
        cursor.execute("ALTER TABLE places_of_worship ADD COLUMN stripe_customer_id TEXT")
    except sqlite3.OperationalError:
        print("stripe_customer_id column already exists.")

    conn.commit()
    conn.close()
    print("Migration complete!")

if __name__ == "__main__":
    migrate()
