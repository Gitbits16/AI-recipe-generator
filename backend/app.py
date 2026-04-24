from flask import Flask, request, jsonify
from flask_cors import CORS
from functools import wraps
from datetime import datetime
from config import Config
from auth import register_user, validate_user, update_password, update_allergy, verify_token
from ai_engine import generate_recipe
from db import get_db_connection, init_database
import traceback

# Validate configuration
Config.validate()

app = Flask(__name__)
CORS(app)

# Initialize database
init_database()

def token_required(f):
    """Decorator to require JWT authentication"""
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')
        
        print(f"🔑 Token received: {token[:20] if token else 'None'}...")
        
        if not token:
            print("❌ No token provided")
            return jsonify({"error": "Token is missing"}), 401
        
        try:
            # Remove 'Bearer ' prefix if present
            if token.startswith('Bearer '):
                token = token[7:]
            
            email = verify_token(token)
            print(f"📧 Email from token: {email}")
            
            if not email:
                print("❌ Token verification failed")
                return jsonify({"error": "Invalid or expired token"}), 401
            
            # Add email to request context
            request.user_email = email
            print(f"✅ User authenticated: {email}")
        except Exception as e:
            print(f"❌ Token error: {str(e)}")
            return jsonify({"error": "Invalid token"}), 401
        
        return f(*args, **kwargs)
    
    return decorated

@app.route("/register", methods=["POST"])
def register():
    """Register new user"""
    try:
        data = request.json
        print(f"📝 Register attempt: {data.get('email')}")
        
        if not data or not data.get("email") or not data.get("password"):
            return jsonify({"error": "Email and password required"}), 400
        
        success, message = register_user(
            data["email"], 
            data["password"], 
            data.get("allergy", "")
        )
        
        if success:
            print(f"✅ User registered: {data.get('email')}")
            return jsonify({"message": message}), 201
        
        print(f"❌ Registration failed: {message}")
        return jsonify({"error": message}), 400
        
    except Exception as e:
        print(f"❌ Register error: {str(e)}")
        traceback.print_exc()
        return jsonify({"error": "Registration failed"}), 500

@app.route("/login", methods=["POST"])
def login():
    """Authenticate user"""
    try:
        data = request.json
        print(f"🔐 Login attempt: {data.get('email')}")
        
        if not data or not data.get("email") or not data.get("password"):
            return jsonify({"error": "Email and password required"}), 400
        
        user = validate_user(data["email"], data["password"])
        
        if user:
            print(f"✅ Login successful: {data.get('email')}")
            return jsonify({
                "message": "Login successful",
                "token": user["token"],
                "email": user["email"],
                "allergy": user["allergy"]
            }), 200
        
        print(f"❌ Invalid credentials for: {data.get('email')}")
        return jsonify({"error": "Invalid credentials"}), 401
        
    except Exception as e:
        print(f"❌ Login error: {str(e)}")
        traceback.print_exc()
        return jsonify({"error": "Login failed"}), 500

@app.route("/generate-recipe", methods=["POST"])
@token_required
def generate_recipe_api():
    """Generate AI recipes"""
    print("\n" + "="*50)
    print("🍳 GENERATE RECIPE REQUEST")
    print("="*50)
    
    try:
        data = request.json
        print(f"📦 Request data: {data}")
        print(f"👤 User email: {request.user_email}")
        
        if not data or not data.get("ingredients"):
            print("❌ No ingredients provided")
            return jsonify({"error": "Ingredients required"}), 400
        
        # Get user's allergy info from database
        print(f"🔍 Looking up user in database: {request.user_email}")
        db = get_db_connection()
        cursor = db.cursor(dictionary=True)
        
        try:
            cursor.execute("SELECT allergy FROM users WHERE email=%s", (request.user_email,))
            user = cursor.fetchone()
            print(f"📊 Database query result: {user}")
            
            if not user:
                print(f"❌ User not found in database: {request.user_email}")
                cursor.close()
                db.close()
                return jsonify({"error": "User not found in database"}), 404
            
            allergy = user.get('allergy', '') or ''
            print(f"🚫 User allergies: {allergy if allergy else 'None'}")
            
        except Exception as e:
            print(f"❌ Database query error: {str(e)}")
            traceback.print_exc()
            cursor.close()
            db.close()
            return jsonify({"error": f"Database error: {str(e)}"}), 500
        
        cursor.close()
        db.close()
        
        # Generate recipe
        print(f"🤖 Generating recipe with ingredients: {data['ingredients']}")
        print(f"🚫 Avoiding allergies: {allergy if allergy else 'None'}")
        
        recipe = generate_recipe(data["ingredients"], allergy)
        
        print(f"📝 Recipe generated: {len(recipe)} characters")
        
        if recipe.startswith("ERROR:"):
            print(f"❌ AI generation error: {recipe}")
            return jsonify({"error": recipe}), 500
        
        # Save to history
        print("💾 Saving to history...")
        db = get_db_connection()
        cursor = db.cursor()
        
        try:
            cursor.execute(
                "INSERT INTO history (email, ingredients, generated_recipe) VALUES (%s, %s, %s)",
                (request.user_email, data["ingredients"], recipe)
            )
            db.commit()
            print("✅ Saved to history")
        except Exception as e:
            print(f"⚠️ Error saving to history: {str(e)}")
            traceback.print_exc()
        finally:
            cursor.close()
            db.close()
        
        print("✅ Recipe generation complete!")
        print("="*50 + "\n")
        return jsonify({"recipe": recipe}), 200
        
    except Exception as e:
        print(f"❌ CRITICAL ERROR in generate_recipe_api: {str(e)}")
        traceback.print_exc()
        print("="*50 + "\n")
        return jsonify({"error": f"Server error: {str(e)}"}), 500

@app.route("/history", methods=["GET"])
@token_required
def history():
    """Get user's recipe history"""
    try:
        print(f"📜 Fetching history for: {request.user_email}")
        db = get_db_connection()
        cursor = db.cursor(dictionary=True)
        
        cursor.execute(
            """
            SELECT id, ingredients, generated_recipe, created_at
            FROM history
            WHERE email=%s
            ORDER BY created_at DESC
            LIMIT 50
            """,
            (request.user_email,)
        )
        
        history_data = cursor.fetchall()
        print(f"✅ Found {len(history_data)} history items")
        
        # Format datetime
        for item in history_data:
            if isinstance(item['created_at'], datetime):
                item['created_at'] = item['created_at'].strftime('%Y-%m-%d %H:%M:%S')
        
        cursor.close()
        db.close()
        
        return jsonify(history_data), 200
    except Exception as e:
        print(f"❌ History error: {str(e)}")
        traceback.print_exc()
        return jsonify({"error": "Failed to fetch history"}), 500

@app.route("/favorite", methods=["POST"])
@token_required
def favorite():
    """Save recipe to favorites"""
    try:
        data = request.json
        print(f"⭐ Saving favorite for: {request.user_email}")
        
        if not data or not data.get("recipe"):
            return jsonify({"error": "Recipe required"}), 400
        
        db = get_db_connection()
        cursor = db.cursor()
        cursor.execute(
            "INSERT INTO favorites (email, recipe) VALUES (%s, %s)",
            (request.user_email, data["recipe"])
        )
        db.commit()
        cursor.close()
        db.close()
        
        print("✅ Favorite saved")
        return jsonify({"message": "Recipe saved to favorites"}), 200
        
    except Exception as e:
        print(f"❌ Favorite error: {str(e)}")
        traceback.print_exc()
        return jsonify({"error": "Failed to save favorite"}), 500

@app.route("/favorites", methods=["GET"])
@token_required
def favorites():
    """Get user's favorite recipes"""
    try:
        print(f"⭐ Fetching favorites for: {request.user_email}")
        db = get_db_connection()
        cursor = db.cursor(dictionary=True)
        
        cursor.execute(
            """
            SELECT id, recipe, created_at
            FROM favorites
            WHERE email=%s
            ORDER BY created_at DESC
            LIMIT 100
            """,
            (request.user_email,)
        )
        
        favorites_data = cursor.fetchall()
        print(f"✅ Found {len(favorites_data)} favorites")
        
        # Format datetime
        for item in favorites_data:
            if isinstance(item['created_at'], datetime):
                item['created_at'] = item['created_at'].strftime('%Y-%m-%d %H:%M:%S')
        
        cursor.close()
        db.close()
        
        return jsonify(favorites_data), 200
    except Exception as e:
        print(f"❌ Favorites error: {str(e)}")
        traceback.print_exc()
        return jsonify({"error": "Failed to fetch favorites"}), 500

@app.route("/update-allergy", methods=["POST"])
@token_required
def update_user_allergy():
    """Update user's allergy information"""
    try:
        data = request.json
        print(f"🚫 Updating allergy for: {request.user_email}")
        
        if "allergy" not in data:
            return jsonify({"error": "Allergy field required"}), 400
        
        if update_allergy(request.user_email, data["allergy"]):
            print("✅ Allergy updated")
            return jsonify({"message": "Allergy updated successfully"}), 200
        
        print("❌ Allergy update failed")
        return jsonify({"error": "Update failed"}), 500
        
    except Exception as e:
        print(f"❌ Update allergy error: {str(e)}")
        traceback.print_exc()
        return jsonify({"error": "Failed to update allergy"}), 500

@app.route("/update-password", methods=["POST"])
@token_required
def update_user_password():
    """Update user's password"""
    try:
        data = request.json
        print(f"🔑 Updating password for: {request.user_email}")
        
        if not data or not data.get("password"):
            return jsonify({"error": "Password required"}), 400
        
        success, message = update_password(request.user_email, data["password"])
        
        if success:
            print("✅ Password updated")
            return jsonify({"message": message}), 200
        
        print(f"❌ Password update failed: {message}")
        return jsonify({"error": message}), 400
        
    except Exception as e:
        print(f"❌ Update password error: {str(e)}")
        traceback.print_exc()
        return jsonify({"error": "Failed to update password"}), 500

@app.errorhandler(404)
def not_found(e):
    return jsonify({"error": "Endpoint not found"}), 404

@app.errorhandler(500)
def internal_error(e):
    print(f"❌ 500 Error: {str(e)}")
    traceback.print_exc()
    return jsonify({"error": "Internal server error"}), 500

if __name__ == "__main__":
    print("\n" + "="*60)
    print("🚀 Starting FlavorForge Backend...")
    print("="*60)
    print("📍 Server: http://127.0.0.1:5000")
    print("🔧 Debug mode: ON")
    print("📊 Logging: VERBOSE")
    print("="*60 + "\n")
    
    app.run(debug=True, host='127.0.0.1', port=5000)