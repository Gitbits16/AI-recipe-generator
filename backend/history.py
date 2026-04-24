from db import get_db_connection
from datetime import datetime

def save_history(email, ingredients, mood, recipe):
    """Save recipe generation to history"""
    db = get_db_connection()
    cursor = db.cursor()
    
    try:
        cursor.execute(
            """
            INSERT INTO history (email, ingredients, mood, recipe)
            VALUES (%s, %s, %s, %s)
            """,
            (email, ingredients, mood, recipe)
        )
        db.commit()
        return True
    except Exception as e:
        print(f"Error saving history: {e}")
        return False
    finally:
        cursor.close()
        db.close()

def get_user_history(email, limit=50):
    """Get user's recipe generation history"""
    db = get_db_connection()
    cursor = db.cursor(dictionary=True)
    
    try:
        cursor.execute(
            """
            SELECT id, ingredients, mood, recipe, created_at
            FROM history
            WHERE email=%s
            ORDER BY created_at DESC
            LIMIT %s
            """,
            (email, limit)
        )
        
        data = cursor.fetchall()
        
        # Format datetime for JSON serialization
        for item in data:
            if isinstance(item['created_at'], datetime):
                item['created_at'] = item['created_at'].strftime('%Y-%m-%d %H:%M:%S')
        
        return data
    except Exception as e:
        print(f"Error fetching history: {e}")
        return []
    finally:
        cursor.close()
        db.close()

def save_favorite(email, recipe):
    """Save recipe to favorites"""
    db = get_db_connection()
    cursor = db.cursor()
    
    try:
        cursor.execute(
            "INSERT INTO favorites (email, recipe) VALUES (%s, %s)",
            (email, recipe)
        )
        db.commit()
        return True
    except Exception as e:
        print(f"Error saving favorite: {e}")
        return False
    finally:
        cursor.close()
        db.close()

def get_favorites(email, limit=100):
    """Get user's favorite recipes"""
    db = get_db_connection()
    cursor = db.cursor(dictionary=True)
    
    try:
        cursor.execute(
            """
            SELECT id, recipe, created_at
            FROM favorites
            WHERE email=%s
            ORDER BY created_at DESC
            LIMIT %s
            """,
            (email, limit)
        )
        
        data = cursor.fetchall()
        
        # Format datetime for JSON serialization
        for item in data:
            if isinstance(item['created_at'], datetime):
                item['created_at'] = item['created_at'].strftime('%Y-%m-%d %H:%M:%S')
        
        return data
    except Exception as e:
        print(f"Error fetching favorites: {e}")
        return []
    finally:
        cursor.close()
        db.close()

def delete_favorite(email, favorite_id):
    """Delete a favorite recipe"""
    db = get_db_connection()
    cursor = db.cursor()
    
    try:
        cursor.execute(
            "DELETE FROM favorites WHERE id=%s AND email=%s",
            (favorite_id, email)
        )
        db.commit()
        return cursor.rowcount > 0
    except Exception as e:
        print(f"Error deleting favorite: {e}")
        return False
    finally:
        cursor.close()
        db.close()