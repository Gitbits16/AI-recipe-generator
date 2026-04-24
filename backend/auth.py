import bcrypt
import jwt
import re
from datetime import datetime, timedelta
from db import get_db_connection
from config import Config

def validate_email(email):
    """Validate email format"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def validate_password(password):
    """Validate password strength"""
    if len(password) < 8:
        return False, "Password must be at least 8 characters"
    if not re.search(r'[A-Z]', password):
        return False, "Password must contain at least one uppercase letter"
    if not re.search(r'[a-z]', password):
        return False, "Password must contain at least one lowercase letter"
    if not re.search(r'\d', password):
        return False, "Password must contain at least one number"
    return True, "Valid"

def hash_password(password):
    """Hash password using bcrypt"""
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt(Config.BCRYPT_ROUNDS)).decode('utf-8')

def verify_password(password, hashed):
    """Verify password against hash"""
    return bcrypt.checkpw(password.encode('utf-8'), hashed.encode('utf-8'))

def generate_token(email):
    """Generate JWT token"""
    payload = {
        'email': email,
        'exp': datetime.utcnow() + timedelta(hours=Config.JWT_EXPIRATION_HOURS),
        'iat': datetime.utcnow()
    }
    return jwt.encode(payload, Config.JWT_SECRET_KEY, algorithm=Config.JWT_ALGORITHM)

def verify_token(token):
    """Verify JWT token and return email"""
    try:
        payload = jwt.decode(token, Config.JWT_SECRET_KEY, algorithms=[Config.JWT_ALGORITHM])
        return payload['email']
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None

def register_user(email, password, allergy=""):
    """Register new user with validation"""
    # Validate email
    if not validate_email(email):
        return False, "Invalid email format"
    
    # Validate password
    is_valid, message = validate_password(password)
    if not is_valid:
        return False, message
    
    # Hash password
    hashed_password = hash_password(password)
    
    db = get_db_connection()
    cursor = db.cursor()
    try:
        cursor.execute(
            "INSERT INTO users (email, password, allergy) VALUES (%s, %s, %s)",
            (email, hashed_password, allergy)
        )
        db.commit()
        return True, "Registration successful"
    except Exception as e:
        if "Duplicate entry" in str(e):
            return False, "Email already registered"
        return False, "Registration failed"
    finally:
        cursor.close()
        db.close()

def validate_user(email, password):
    """Validate user credentials and return user data with token"""
    db = get_db_connection()
    cursor = db.cursor(dictionary=True)
    
    try:
        cursor.execute(
            "SELECT email, password, allergy FROM users WHERE email=%s",
            (email,)
        )
        user = cursor.fetchone()
        
        if user and verify_password(password, user['password']):
            token = generate_token(email)
            return {
                'email': user['email'],
                'allergy': user['allergy'],
                'token': token
            }
        return None
    finally:
        cursor.close()
        db.close()

def update_allergy(email, allergy):
    """Update user allergy information"""
    db = get_db_connection()
    cursor = db.cursor()
    try:
        cursor.execute(
            "UPDATE users SET allergy=%s WHERE email=%s",
            (allergy, email)
        )
        db.commit()
        return True
    except:
        return False
    finally:
        cursor.close()
        db.close()

def update_password(email, new_password):
    """Update user password with validation"""
    # Validate new password
    is_valid, message = validate_password(new_password)
    if not is_valid:
        return False, message
    
    hashed_password = hash_password(new_password)
    
    db = get_db_connection()
    cursor = db.cursor()
    try:
        cursor.execute(
            "UPDATE users SET password=%s WHERE email=%s",
            (hashed_password, email)
        )
        db.commit()
        return True, "Password updated successfully"
    except:
        return False, "Password update failed"
    finally:
        cursor.close()
        db.close()