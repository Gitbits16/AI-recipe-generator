import streamlit as st
import requests
import time

API_BASE = "http://127.0.0.1:5000"

# Authentication guard
if not st.session_state.get("token"):
    st.switch_page("Home.py")

st.set_page_config(page_title="Explore", page_icon="🍳", layout="wide", initial_sidebar_state="expanded")

# Initialize theme
if 'theme' not in st.session_state:
    st.session_state.theme = 'dark'

def get_headers():
    """Get authorization headers"""
    return {
        "Authorization": f"Bearer {st.session_state.token}",
        "Content-Type": "application/json"
    }

def toggle_theme():
    """Toggle between light and dark theme"""
    st.session_state.theme = 'light' if st.session_state.theme == 'dark' else 'dark'

# Modern CSS with glassmorphism and animations
theme_colors = {
    'dark': {
        'bg': '#0E1117',
        'card_bg': 'rgba(255, 255, 255, 0.05)',
        'card_border': 'rgba(255, 255, 255, 0.1)',
        'text': '#FFFFFF',
        'text_secondary': '#B0B0B0',
        'gradient_1': 'rgba(102, 126, 234, 0.1)',
        'gradient_2': 'rgba(118, 75, 162, 0.1)',
        'accent': '#667eea',
        'shadow': 'rgba(0, 0, 0, 0.3)'
    },
    'light': {
        'bg': '#FFFFFF',
        'card_bg': 'rgba(255, 255, 255, 0.7)',
        'card_border': 'rgba(0, 0, 0, 0.1)',
        'text': '#1E1E1E',
        'text_secondary': '#666666',
        'gradient_1': 'rgba(102, 126, 234, 0.15)',
        'gradient_2': 'rgba(118, 75, 162, 0.15)',
        'accent': '#5A67D8',
        'shadow': 'rgba(0, 0, 0, 0.1)'
    }
}

colors = theme_colors[st.session_state.theme]

st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&display=swap');

* {{
    font-family: 'Inter', sans-serif;
}}

/* Animations */
@keyframes fadeIn {{
    from {{ opacity: 0; transform: translateY(20px); }}
    to {{ opacity: 1; transform: translateY(0); }}
}}

@keyframes slideIn {{
    from {{ transform: translateX(-100%); opacity: 0; }}
    to {{ transform: translateX(0); opacity: 1; }}
}}

@keyframes pulse {{
    0%, 100% {{ transform: scale(1); }}
    50% {{ transform: scale(1.05); }}
}}

@keyframes shimmer {{
    0% {{ background-position: -1000px 0; }}
    100% {{ background-position: 1000px 0; }}
}}

/* Main container */
.main {{
    background: {colors['bg']};
    color: {colors['text']};
    animation: fadeIn 0.6s ease-out;
}}

/* Glass card effect */
.recipe-card {{
    background: linear-gradient(135deg, {colors['gradient_1']} 0%, {colors['gradient_2']} 100%);
    backdrop-filter: blur(20px) saturate(180%);
    -webkit-backdrop-filter: blur(20px) saturate(180%);
    border: 1px solid {colors['card_border']};
    border-radius: 24px;
    padding: 2rem;
    margin-bottom: 2rem;
    box-shadow: 0 8px 32px 0 {colors['shadow']};
    transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
    animation: fadeIn 0.8s ease-out;
    position: relative;
    overflow: hidden;
    color: {colors['text']};
}}

.recipe-card::before {{
    content: '';
    position: absolute;
    top: 0;
    left: -100%;
    width: 100%;
    height: 100%;
    background: linear-gradient(90deg, transparent, rgba(255,255,255,0.1), transparent);
    transition: left 0.5s;
}}

.recipe-card:hover::before {{
    left: 100%;
}}

.recipe-card:hover {{
    transform: translateY(-8px) scale(1.02);
    box-shadow: 0 16px 48px 0 {colors['shadow']};
    border-color: {colors['accent']};
}}

/* Recipe title */
.recipe-title {{
    font-size: 1.8rem;
    font-weight: 700;
    background: linear-gradient(135deg, {colors['accent']}, #764ba2);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    margin-bottom: 1.5rem;
    animation: slideIn 0.6s ease-out;
}}

/* Input container */
.input-container {{
    background: {colors['card_bg']};
    backdrop-filter: blur(10px);
    border: 1px solid {colors['card_border']};
    border-radius: 16px;
    padding: 2rem;
    margin-bottom: 2rem;
    box-shadow: 0 4px 16px 0 {colors['shadow']};
    animation: fadeIn 0.5s ease-out;
}}

/* Buttons with gradient */
.stButton button {{
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
    border: none;
    border-radius: 12px;
    padding: 0.75rem 2rem;
    font-weight: 600;
    font-size: 1.05rem;
    transition: all 0.3s ease;
    box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);
    cursor: pointer;
}}

.stButton button:hover {{
    transform: translateY(-2px);
    box-shadow: 0 6px 20px rgba(102, 126, 234, 0.6);
    animation: pulse 0.6s ease-in-out;
}}

.stButton button:active {{
    transform: translateY(0);
}}

/* Save button specific styling */
.save-btn {{
    background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%) !important;
    box-shadow: 0 4px 15px rgba(245, 87, 108, 0.4) !important;
}}

.save-btn:hover {{
    box-shadow: 0 6px 20px rgba(245, 87, 108, 0.6) !important;
}}

/* Info box */
.info-box {{
    background: {colors['card_bg']};
    backdrop-filter: blur(10px);
    border: 1px solid {colors['card_border']};
    border-radius: 12px;
    padding: 1rem;
    color: {colors['text']};
    box-shadow: 0 4px 12px {colors['shadow']};
}}

/* Theme toggle button */
.theme-toggle {{
    position: fixed;
    top: 80px;
    right: 20px;
    z-index: 999;
    background: {colors['card_bg']};
    backdrop-filter: blur(10px);
    border: 1px solid {colors['card_border']};
    border-radius: 50%;
    width: 50px;
    height: 50px;
    display: flex;
    align-items: center;
    justify-content: center;
    cursor: pointer;
    box-shadow: 0 4px 12px {colors['shadow']};
    transition: all 0.3s ease;
}}

.theme-toggle:hover {{
    transform: rotate(180deg) scale(1.1);
}}

/* Success animation */
.success-popup {{
    position: fixed;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%) scale(0);
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
    padding: 2rem 3rem;
    border-radius: 20px;
    box-shadow: 0 10px 40px rgba(0, 0, 0, 0.3);
    z-index: 1000;
    animation: popIn 0.4s ease-out forwards;
}}

@keyframes popIn {{
    0% {{ transform: translate(-50%, -50%) scale(0); }}
    50% {{ transform: translate(-50%, -50%) scale(1.1); }}
    100% {{ transform: translate(-50%, -50%) scale(1); }}
}}

/* Loading animation */
.loading {{
    display: inline-block;
    width: 20px;
    height: 20px;
    border: 3px solid rgba(255,255,255,.3);
    border-radius: 50%;
    border-top-color: #fff;
    animation: spin 1s ease-in-out infinite;
}}

@keyframes spin {{
    to {{ transform: rotate(360deg); }}
}}

/* Recipe content styling */
.recipe-content {{
    background: {colors['card_bg']};
    border-radius: 12px;
    padding: 1.5rem;
    margin: 1rem 0;
    color: {colors['text']};
    line-height: 1.8;
    box-shadow: inset 0 2px 8px {colors['shadow']};
}}

/* Hover glow effect */
.glow {{
    box-shadow: 0 0 20px {colors['accent']}, 0 0 40px {colors['accent']};
}}

/* Scrollbar styling */
::-webkit-scrollbar {{
    width: 10px;
}}

::-webkit-scrollbar-track {{
    background: {colors['bg']};
}}

::-webkit-scrollbar-thumb {{
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    border-radius: 10px;
}}

::-webkit-scrollbar-thumb:hover {{
    background: linear-gradient(135deg, #764ba2 0%, #667eea 100%);
}}
</style>
""", unsafe_allow_html=True)

# Header with theme toggle
col1, col2, col3 = st.columns([1, 6, 1])

with col1:
    if st.button("🏠 Home"):
        st.switch_page("pages/0_Profile.py")

with col2:
    st.title("🔍 Explore Recipes")
    st.markdown("Generate personalized AI-powered recipes based on your ingredients!")

with col3:
    theme_icon = "🌙" if st.session_state.theme == 'light' else "☀️"
    if st.button(theme_icon, help="Toggle theme"):
        toggle_theme()
        st.rerun()

st.markdown("---")

# Input section with glass effect
col1, col2 = st.columns([3, 1])

with col1:
    ingredients = st.text_area(
        "🥗 Available Ingredients",
        placeholder="e.g., chicken, tomatoes, basil, pasta, olive oil, garlic",
        height=120,
        help="Enter the ingredients you have available, separated by commas"
    )

with col2:
    st.markdown(f"""
    <div class="info-box">
        <h4 style="margin: 0 0 0.5rem 0;">🚫 Your Allergies</h4>
        <p style="margin: 0; color: {colors['text_secondary']};">{st.session_state.get('allergy', 'None')}</p>
        <small style="color: {colors['text_secondary']};">Update in Profile</small>
    </div>
    """, unsafe_allow_html=True)

# Generate button
if st.button("✨ Generate Recipes", type="primary", use_container_width=True, key="generate_btn"):
    if not ingredients or not ingredients.strip():
        st.error("❌ Please enter at least one ingredient")
    else:
        # Initialize saved recipes key in session state
        if 'saved_recipe_ids' not in st.session_state:
            st.session_state.saved_recipe_ids = set()
        
        try:
            with st.spinner("🍳 Cooking up some amazing recipes..."):
                res = requests.post(
                    f"{API_BASE}/generate-recipe",
                    headers=get_headers(),
                    json={"ingredients": ingredients},
                    timeout=60
                )
            
            if res.status_code == 200:
                recipe_text = res.json().get("recipe", "")
                
                if recipe_text.startswith("ERROR:"):
                    st.error(f"❌ {recipe_text}")
                else:
                    # Split recipes
                    recipes = recipe_text.split("RECIPE:")
                    recipes = [r.strip() for r in recipes if r.strip()]
                    
                    # Store recipes in session state
                    st.session_state.generated_recipes = recipes
                    
                    st.success(f"✅ Generated {len(recipes)} delicious recipes!")
                    st.markdown("---")
                    
                    # Display each recipe
                    for i, recipe in enumerate(recipes, 1):
                        recipe_id = f"recipe_{i}_{hash(recipe)}"
                        
                        with st.container():
                            st.markdown(f"""
                            <div class="recipe-card">
                                <div class="recipe-title">🍽️ Recipe {i}</div>
                                <div class="recipe-content">
                                    <pre style="white-space: pre-wrap; font-family: 'Inter', sans-serif; margin: 0; color: {colors['text']};">
{recipe}
                                    </pre>
                                </div>
                            </div>
                            """, unsafe_allow_html=True)
                            
                            col_a, col_b, col_c = st.columns([1, 1, 3])
                            
                            with col_a:
                                save_btn_key = f"save_{i}"
                                if st.button(f"⭐ Save", key=save_btn_key, use_container_width=True):
                                    try:
                                        save_res = requests.post(
                                            f"{API_BASE}/favorite",
                                            headers=get_headers(),
                                            json={"recipe": recipe},
                                            timeout=10
                                        )
                                        
                                        if save_res.status_code == 200:
                                            st.session_state.saved_recipe_ids.add(recipe_id)
                                            st.success("✅ Saved to favorites!")
                                            time.sleep(1)
                                            st.rerun()
                                        else:
                                            st.error("❌ Failed to save")
                                    except Exception as e:
                                        st.error(f"Error: {str(e)}")
                            
                            with col_b:
                                if st.button("📋 Copy", key=f"copy_{i}", use_container_width=True):
                                    st.code(recipe, language=None)
                            
                            st.markdown("<br>", unsafe_allow_html=True)
            
            elif res.status_code == 401:
                st.error("Session expired. Please login again.")
                st.session_state.token = None
                st.switch_page("Home.py")
            else:
                error_msg = res.json().get("error", "Failed to generate recipes")
                st.error(f"❌ {error_msg}")
                
        except requests.exceptions.Timeout:
            st.error("⏱️ Request timed out. The AI might be busy. Please try again.")
        except requests.exceptions.ConnectionError:
            st.error("🔌 Cannot connect to server. Ensure backend is running: cd backend && python app.py")
        except Exception as e:
            st.error(f"❌ An error occurred: {str(e)}")

st.markdown("---")

# Tips section with glass card
st.markdown(f"""
<div class="input-container">
    <h3 style="color: {colors['accent']}; margin-bottom: 1rem;">💡 Pro Tips for Better Recipes</h3>
    <ul style="line-height: 2; color: {colors['text_secondary']};">
        <li><strong>Be specific</strong> with ingredients (e.g., "chicken breast" vs "chicken")</li>
        <li><strong>Include quantities</strong> if you want more precise recipes</li>
        <li><strong>Update allergies</strong> in Profile - AI automatically avoids them!</li>
        <li><strong>Try different combinations</strong> to discover new favorites</li>
    </ul>
</div>
""", unsafe_allow_html=True)