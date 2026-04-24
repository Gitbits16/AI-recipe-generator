import mysql.connector
from mysql.connector import pooling
from config import Config

# Connection pool for better performance
connection_pool = None

def initialize_pool():
    """Initialize the connection pool"""
    global connection_pool
    try:
        connection_pool = pooling.MySQLConnectionPool(
            pool_name="recipe_pool",
            pool_size=5,
            host=Config.DB_HOST,
            user=Config.DB_USER,
            password=Config.DB_PASSWORD,
            database=Config.DB_NAME
        )
        print("✅ Database connection pool initialized")
    except mysql.connector.Error as err:
        print(f"❌ Database connection pool error: {err}")
        raise

def get_db_connection():
    """Get database connection from pool"""
    global connection_pool
    if connection_pool is None:
        initialize_pool()
    
    try:
        return connection_pool.get_connection()
    except mysql.connector.Error as err:
        print(f"❌ Database connection error: {err}")
        raise

def init_database():
    """Initialize database tables if they don't exist"""
    db = get_db_connection()
    cursor = db.cursor()
    
    try:
        # Users table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INT AUTO_INCREMENT PRIMARY KEY,
                email VARCHAR(255) UNIQUE NOT NULL,
                password VARCHAR(255) NOT NULL,
                allergy TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                INDEX idx_email (email)
            )
        """)
        
        # Favorites table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS favorites (
                id INT AUTO_INCREMENT PRIMARY KEY,
                email VARCHAR(255) NOT NULL,
                recipe TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (email) REFERENCES users(email) ON DELETE CASCADE,
                INDEX idx_email_date (email, created_at)
            )
        """)
        
        # History table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS history (
                id INT AUTO_INCREMENT PRIMARY KEY,
                email VARCHAR(255) NOT NULL,
                ingredients TEXT NOT NULL,
                generated_recipe TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (email) REFERENCES users(email) ON DELETE CASCADE,
                INDEX idx_email_date (email, created_at)
            )
        """)
        
        db.commit()
        print("✅ Database tables initialized successfully")
        
    except mysql.connector.Error as err:
        print(f"❌ Database initialization error: {err}")
        raise
    finally:
        cursor.close()
        db.close()