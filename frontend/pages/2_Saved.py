import streamlit as st
import requests

API_BASE = "http://127.0.0.1:5000"

# Authentication guard
if not st.session_state.get("token"):
    st.switch_page("Home.py")

st.set_page_config(page_title="Saved Recipes", page_icon="⭐", layout="wide")

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

# Theme colors
theme_colors = {
    'dark': {
        'bg': '#0E1117',
        'card_bg': 'rgba(255, 255, 255, 0.05)',
        'card_border': 'rgba(255, 255, 255, 0.1)',
        'text': '#FFFFFF',
        'text_secondary': '#B0B0B0',
        'accent': '#667eea',
        'shadow': 'rgba(0, 0, 0, 0.3)'
    },
    'light': {
        'bg': '#FFFFFF',
        'card_bg': 'rgba(255, 255, 255, 0.7)',
        'card_border': 'rgba(0, 0, 0, 0.1)',
        'text': '#1E1E1E',
        'text_secondary': '#666666',
        'accent': '#5A67D8',
        'shadow': 'rgba(0, 0, 0, 0.1)'
    }
}

colors = theme_colors[st.session_state.theme]

# Modern CSS with glassmorphism
st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&display=swap');

* {{
    font-family: 'Inter', sans-serif;
}}

@keyframes fadeIn {{
    from {{ opacity: 0; transform: translateY(20px); }}
    to {{ opacity: 1; transform: translateY(0); }}
}}

@keyframes shimmer {{
    0% {{ background-position: -100% 0; }}
    100% {{ background-position: 200% 0; }}
}}

@keyframes float {{
    0%, 100% {{ transform: translateY(0); }}
    50% {{ transform: translateY(-10px); }}
}}

.main {{
    background: {colors['bg']};
    color: {colors['text']};
}}

.favorite-card {{
    background: linear-gradient(135deg, rgba(255, 215, 0, 0.1) 0%, rgba(255, 165, 0, 0.1) 100%);
    backdrop-filter: blur(20px) saturate(180%);
    -webkit-backdrop-filter: blur(20px) saturate(180%);
    border: 1px solid rgba(255, 215, 0, 0.3);
    border-radius: 24px;
    padding: 2rem;
    margin-bottom: 2rem;
    box-shadow: 0 8px 32px 0 rgba(255, 215, 0, 0.15);
    transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
    animation: fadeIn 0.6s ease-out;
    position: relative;
    overflow: hidden;
    color: {colors['text']};
}}

.favorite-card::before {{
    content: '';
    position: absolute;
    top: 0;
    left: -100%;
    width: 100%;
    height: 100%;
    background: linear-gradient(90deg, transparent, rgba(255, 215, 0, 0.2), transparent);
    transition: left 0.7s;
}}

.favorite-card:hover::before {{
    left: 100%;
}}

.favorite-card:hover {{
    transform: translateY(-10px) scale(1.02);
    box-shadow: 0 16px 48px 0 rgba(255, 215, 0, 0.3);
    border-color: rgba(255, 215, 0, 0.6);
}}

.timestamp {{
    display: inline-block;
    background: rgba(255, 215, 0, 0.2);
    padding: 0.5rem 1rem;
    border-radius: 20px;
    color: #ffa500;
    font-size: 0.9rem;
    font-weight: 600;
    margin-bottom: 1rem;
    backdrop-filter: blur(10px);
}}

.star-icon {{
    display: inline-block;
    animation: float 3s ease-in-out infinite;
    font-size: 2rem;
    margin-right: 0.5rem;
}}

.recipe-content {{
    background: {colors['card_bg']};
    border-radius: 12px;
    padding: 1.5rem;
    margin-top: 1rem;
    color: {colors['text']};
    line-height: 1.8;
    border: 1px solid {colors['card_border']};
}}

.stButton button {{
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
    border: none;
    border-radius: 12px;
    padding: 0.75rem 1.5rem;
    font-weight: 600;
    transition: all 0.3s ease;
    box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);
}}

.stButton button:hover {{
    transform: translateY(-2px);
    box-shadow: 0 6px 20px rgba(102, 126, 234, 0.6);
}}

.empty-state {{
    text-align: center;
    padding: 4rem 2rem;
    background: {colors['card_bg']};
    backdrop-filter: blur(10px);
    border: 1px solid {colors['card_border']};
    border-radius: 24px;
    animation: fadeIn 0.8s ease-out;
}}

.empty-icon {{
    font-size: 5rem;
    margin-bottom: 1rem;
    animation: float 3s ease-in-out infinite;
}}
</style>
""", unsafe_allow_html=True)

# Header
col1, col2, col3 = st.columns([1, 6, 1])

with col1:
    if st.button("🏠 Home"):
        st.switch_page("pages/0_Profile.py")

with col2:
    st.title("⭐ Favorite Recipes")
    st.markdown("Your collection of saved recipes")

with col3:
    theme_icon = "🌙" if st.session_state.theme == 'light' else "☀️"
    if st.button(theme_icon, help="Toggle theme"):
        toggle_theme()
        st.rerun()

st.markdown("---")

# Refresh button
col1, col2 = st.columns([5, 1])
with col2:
    if st.button("🔄 Refresh", use_container_width=True):
        st.rerun()

try:
    with st.spinner("Loading your favorites..."):
        res = requests.get(
            f"{API_BASE}/favorites",
            headers=get_headers(),
            timeout=10
        )
    
    if res.status_code == 200:
        favorites = res.json()
        
        if not favorites:
            st.markdown(f"""
            <div class="empty-state">
                <div class="empty-icon">📭</div>
                <h2 style="color: {colors['text']}; margin-bottom: 1rem;">No Favorites Yet</h2>
                <p style="color: {colors['text_secondary']}; font-size: 1.1rem; margin-bottom: 2rem;">
                    Start exploring and save your favorite recipes!
                </p>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown("<br>", unsafe_allow_html=True)
            
            col1, col2, col3 = st.columns([1, 2, 1])
            with col2:
                if st.button("🔍 Explore Recipes", use_container_width=True):
                    st.switch_page("pages/1_Explore.py")
        else:
            st.success(f"✨ You have {len(favorites)} saved recipe(s)")
            st.markdown("---")
            
            # Display favorites in a grid
            for idx, fav in enumerate(favorites):
                with st.container():
                    st.markdown(f"""
                    <div class="favorite-card">
                        <div>
                            <span class="star-icon">⭐</span>
                            <span class="timestamp">Saved on: {fav.get('created_at', 'Unknown')}</span>
                        </div>
                        <div class="recipe-content">
                            <pre style="white-space: pre-wrap; font-family: 'Inter', sans-serif; margin: 0; color: {colors['text']};">
{fav.get('recipe', 'No recipe content')}
                            </pre>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # Action buttons
                    col_a, col_b, col_c = st.columns([1, 1, 4])
                    
                    with col_a:
                        if st.button("📋 Copy", key=f"copy_{idx}", use_container_width=True):
                            st.code(fav.get('recipe', ''), language=None)
                    
                    with col_b:
                        if st.button("🔗 Share", key=f"share_{idx}", use_container_width=True):
                            st.info("💡 Copy the recipe text to share with friends!")
                    
                    st.markdown("<br>", unsafe_allow_html=True)
    
    elif res.status_code == 401:
        st.error("Session expired. Please login again.")
        st.session_state.token = None
        st.switch_page("Home.py")
    else:
        error_msg = res.json().get("error", "Failed to load favorites")
        st.error(f"❌ {error_msg}")

except requests.exceptions.Timeout:
    st.error("⏱️ Request timed out. Please try again.")
except requests.exceptions.ConnectionError:
    st.error("🔌 Cannot connect to server. Ensure backend is running: cd backend && python app.py")
except Exception as e:
    st.error(f"❌ An error occurred: {str(e)}")

st.markdown("---")
st.markdown(f"""
<div style="text-align: center; color: {colors['text_secondary']}; padding: 1rem;">
    <small>💡 Tip: Copy recipes to save them externally or share with friends!</small>
</div>
""", unsafe_allow_html=True)