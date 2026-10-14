import os
import psycopg2
from dotenv import load_dotenv

# 1. Load variables from .env into operating system environment
load_dotenv()

# 2. Read the credentials safely
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_NAME = os.getenv("DB_NAME", "bus_tracker_db")
DB_USER = os.getenv("DB_USER", "postgres")
DB_PASSWORD = os.getenv("DB_PASSWORD")

print("🔍 Attempting to connect to PostgreSQL with:")
print(f"   Host: {DB_HOST}:{DB_PORT}")
print(f"   Database: {DB_NAME}")
print(f"   User: {DB_USER}")
print(f"   Password: {'*' * len(DB_PASSWORD) if DB_PASSWORD else 'None provided!'}")

try:
    # 3. Establish the TCP connection
    connection = psycopg2.connect(
        host=DB_HOST,
        port=DB_PORT,
        database=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD
    )

    # 4. Create a cursor and execute a test query
    cursor = connection.cursor()
    cursor.execute("SELECT version();")
    db_version = cursor.fetchone()

    print("\n✅ CONNECTION SUCCESSFUL!")
    print(f"   PostgreSQL Version: {db_version[0]}")

    # 5. Clean up and close
    cursor.close()
    connection.close()
    print("🔒 Connection closed cleanly.")

except psycopg2.OperationalError as e:
    print("\n❌ DATABASE CONNECTION FAILED:")
    print(f"   Error Details: {e}")

except Exception as e:
    print(f"\n❌ UNEXPECTED ERROR: {e}")