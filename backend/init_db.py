import os
import psycopg2
from dotenv import load_dotenv

# 1. Load environment variables
load_dotenv()

def initialize_database():
    """
    Reads database/schema.sql and executes it against PostgreSQL
    to create all necessary tables and indexes.
    """
    # Find the schema.sql file path relative to this script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    schema_path = os.path.join(script_dir, "..", "database", "schema.sql")

    if not os.path.exists(schema_path):
        print(f"❌ Error: schema.sql file not found at {schema_path}")
        return

    print("📄 Reading schema.sql...")
    with open(schema_path, "r") as f:
        schema_sql = f.read()

    conn = None
    cur = None
    try:
        print("🔌 Connecting to PostgreSQL...")
        conn = psycopg2.connect(
            host=os.getenv("DB_HOST", "localhost"),
            port=os.getenv("DB_PORT", "5432"),
            database=os.getenv("DB_NAME", "bus_tracker_db"),
            user=os.getenv("DB_USER", "postgres"),
            password=os.getenv("DB_PASSWORD")
        )

        cur = conn.cursor()
        print("⚙️  Executing schema SQL...")
        cur.execute(schema_sql)

        # Commit DDL changes to disk!
        conn.commit()
        print("✅ SUCCESS: All database tables and indexes created successfully!")

    except Exception as e:
        print(f"❌ Failed to initialize database: {e}")
        if conn:
            conn.rollback()

    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()
        print("🔒 Connection closed.")

if __name__ == "__main__":
    initialize_database()