"""
Diagnostic script to check FlavorForge backend issues
Run this to identify problems before starting the app
"""

import sys
import os

print("="*60)
print("🔍 FlavorForge Diagnostic Tool")
print("="*60 + "\n")

# Check 1: Python version
print("1️⃣ Checking Python version...")
if sys.version_info < (3, 8):
    print("   ❌ Python 3.8+ required")
    print(f"   Current: {sys.version}")
    sys.exit(1)
else:
    print(f"   ✅ Python {sys.version_info.major}.{sys.version_info.minor}")

# Check 2: Environment file
print("\n2️⃣ Checking .env file...")
env_path = os.path.join(os.path.dirname(__file__), '..', '.env')
if not os.path.exists(env_path):
    print("   ❌ .env file not found!")
    print("   Create .env in project root with required variables")
    sys.exit(1)
else:
    print("   ✅ .env file exists")

# Check 3: Load environment variables
print("\n3️⃣ Checking environment variables...")
try:
    from dotenv import load_dotenv
    load_dotenv(env_path)
    
    required_vars = [
        "OPENROUTER_API_KEY",
        "DB_PASSWORD",
        "JWT_SECRET_KEY"
    ]
    
    missing = []
    for var in required_vars:
        if not os.getenv(var):
            missing.append(var)
    
    if missing:
        print(f"   ❌ Missing variables: {', '.join(missing)}")
        sys.exit(1)
    else:
        print("   ✅ All required variables present")
        print(f"   - OPENROUTER_API_KEY: {os.getenv('OPENROUTER_API_KEY')[:20]}...")
        print(f"   - DB_PASSWORD: ***")
        print(f"   - JWT_SECRET_KEY: {os.getenv('JWT_SECRET_KEY')[:20]}...")
        
except Exception as e:
    print(f"   ❌ Error loading .env: {e}")
    sys.exit(1)

# Check 4: Required packages
print("\n4️⃣ Checking required packages...")
required_packages = {
    'flask': 'Flask',
    'flask_cors': 'flask-cors',
    'bcrypt': 'bcrypt',
    'jwt': 'PyJWT',
    'mysql.connector': 'mysql-connector-python',
    'requests': 'requests',
    'dotenv': 'python-dotenv'
}

missing_packages = []
for package, pip_name in required_packages.items():
    try:
        __import__(package)
        print(f"   ✅ {pip_name}")
    except ImportError:
        print(f"   ❌ {pip_name} not installed")
        missing_packages.append(pip_name)

if missing_packages:
    print(f"\n   Install missing packages:")
    print(f"   pip install {' '.join(missing_packages)}")
    sys.exit(1)

# Check 5: MySQL connection
print("\n5️⃣ Checking MySQL connection...")
try:
    import mysql.connector
    
    db_config = {
        'host': os.getenv('DB_HOST', 'localhost'),
        'user': os.getenv('DB_USER', 'root'),
        'password': os.getenv('DB_PASSWORD'),
    }
    
    conn = mysql.connector.connect(**db_config)
    print(f"   ✅ MySQL server connected")
    
    # Check database
    cursor = conn.cursor()
    cursor.execute(f"SHOW DATABASES LIKE '{os.getenv('DB_NAME', 'recipe_ai')}'")
    result = cursor.fetchone()
    
    if result:
        print(f"   ✅ Database '{os.getenv('DB_NAME', 'recipe_ai')}' exists")
    else:
        print(f"   ⚠️  Database '{os.getenv('DB_NAME', 'recipe_ai')}' not found")
        print(f"   Creating database...")
        cursor.execute(f"CREATE DATABASE {os.getenv('DB_NAME', 'recipe_ai')}")
        print(f"   ✅ Database created")
    
    cursor.close()
    conn.close()
    
except mysql.connector.Error as e:
    print(f"   ❌ MySQL error: {e}")
    print("\n   Possible solutions:")
    print("   1. Make sure MySQL server is running")
    print("   2. Check DB_PASSWORD in .env file")
    print("   3. Verify DB_USER has correct permissions")
    sys.exit(1)

# Check 6: Database tables
print("\n6️⃣ Checking database tables...")
try:
    import mysql.connector
    
    db_config = {
        'host': os.getenv('DB_HOST', 'localhost'),
        'user': os.getenv('DB_USER', 'root'),
        'password': os.getenv('DB_PASSWORD'),
        'database': os.getenv('DB_NAME', 'recipe_ai')
    }
    
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()
    
    required_tables = ['users', 'favorites', 'history']
    cursor.execute("SHOW TABLES")
    existing_tables = [table[0] for table in cursor.fetchall()]
    
    for table in required_tables:
        if table in existing_tables:
            print(f"   ✅ Table '{table}' exists")
        else:
            print(f"   ⚠️  Table '{table}' missing (will be created on startup)")
    
    cursor.close()
    conn.close()
    
except Exception as e:
    print(f"   ⚠️  Could not check tables: {e}")
    print("   Tables will be created on first run")

# Check 7: OpenRouter API
print("\n7️⃣ Checking OpenRouter API...")
try:
    import requests
    
    headers = {
        "Authorization": f"Bearer {os.getenv('OPENROUTER_API_KEY')}",
        "Content-Type": "application/json"
    }
    
    # Test with a simple request
    response = requests.get(
        "https://openrouter.ai/api/v1/models",
        headers=headers,
        timeout=5
    )
    
    if response.status_code == 200:
        print("   ✅ OpenRouter API key valid")
    else:
        print(f"   ❌ OpenRouter API error: {response.status_code}")
        print("   Check your OPENROUTER_API_KEY in .env")
        
except requests.exceptions.Timeout:
    print("   ⚠️  OpenRouter request timed out")
    print("   Check your internet connection")
except Exception as e:
    print(f"   ⚠️  Could not verify API: {e}")

# Final summary
print("\n" + "="*60)
print("✅ DIAGNOSTIC COMPLETE")
print("="*60)
print("\nIf all checks passed, you can start the backend:")
print("  python app.py")
print("\nIf you see errors above, fix them before starting.")
print("="*60 + "\n")