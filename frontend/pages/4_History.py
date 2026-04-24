import streamlit as st
import requests
import time

API_BASE = "http://127.0.0.1:5000"

# Authentication guard
if not st.session_state.get("token"):
    st.switch_page("Home.py")

st.set_page_config(page_title="History", page_icon="📜", layout="wide")

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

# Modern CSS
st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&display=swap');

* {{
    font-family: 'Inter', sans-serif;
}}

@keyframes fadeInUp {{
    from {{
        opacity: 0;
        transform: translateY(30px);
    }}
    to {{
        opacity: 1;
        transform: translateY(0);
    }}
}}

@keyframes slideIn {{
    from {{ transform: translateX(-100%); }}
    to {{ transform: translateX(0); }}
}}

.main {{
    background: {colors['bg']};
    color: {colors['text']};
}}

.history-card {{
    background: linear-gradient(135deg, rgba(66, 153, 225, 0.1) 0%, rgba(49, 130, 206, 0.1) 100%);
    backdrop-filter: blur(20px) saturate(180%);
    -webkit-backdrop-filter: blur(20px) saturate(180%);
    border: 1px solid {colors['card_border']};
    border-radius: 24px;
    padding: 1.5rem;
    margin-bottom: 1.5rem;
    box-shadow: 0 8px 32px 0 {colors['shadow']};
    transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
    animation: fadeInUp 0.6s ease-out;
    position: relative;
    overflow: hidden;
    color: {colors['text']};
}}

.history-card:hover {{
    transform: translateX(8px) scale(1.01);
    box-shadow: 0 12px 48px 0 {colors['shadow']};
    border-color: #4299e1;
}}

.history-card::before {{
    content: '';
    position: absolute;
    top: 0;
    left: -100%;
    width: 100%;
    height: 100%;
    background: linear-gradient(90deg, transparent, rgba(66, 153, 225, 0.1), transparent);
    transition: left 0.5s;
}}

.history-card:hover::before {{
    left: 100%;
}}

.history-meta {{
    display: flex;
    align-items: center;
    gap: 1.5rem;
    flex-wrap: wrap;
    color: #4299e1;
    font-weight: 600;
    margin-bottom: 1rem;
    padding: 0.75rem;
    background: rgba(66, 153, 225, 0.1);
    border-radius: 12px;
    backdrop-filter: blur(10px);
}}

.meta-item {{
    display: flex;
    align-items: center;
    gap: 0.5rem;
    font-size: 0.95rem;
}}

.recipe-preview {{
    background: {colors['card_bg']};
    border-radius: 12px;
    padding: 1rem;
    margin-top: 1rem;
    border: 1px solid {colors['card_border']};
    max-height: 200px;
    overflow: hidden;
    position: relative;
    color: {colors['text']};
}}

.recipe-preview::after {{
    content: '';
    position: absolute;
    bottom: 0;
    left: 0;
    right: 0;
    height: 60px;
    background: linear-gradient(to bottom, transparent, {colors['card_bg']});
}}

.expand-btn {{
    margin-top: 1rem;
    padding: 0.5rem 1.5rem;
    background: linear-gradient(135deg, #4299e1 0%, #3182ce 100%);
    color: white;
    border: none;
    border-radius: 8px;
    cursor: pointer;
    transition: all 0.3s ease;
    font-weight: 600;
}}

.expand-btn:hover {{
    transform: translateY(-2px);
    box-shadow: 0 4px 12px rgba(66, 153, 225, 0.4);
}}

.stButton button {{
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
    border: none;
    border-radius: 12px;
    padding: 0.75rem 2rem;
    font-weight: 600;
    transition: all 0.3s ease;
}}

.stButton button:hover {{
    transform: translateY(-2px);
    box-shadow: 0 6px 20px rgba(102, 126, 234, 0.6);
}}

.stats-container {{
    background: {colors['card_bg']};
    backdrop-filter: blur(10px);
    border: 1px solid {colors['card_border']};
    border-radius: 16px;
    padding: 1.5rem;
    margin-bottom: 2rem;
    animation: fadeInUp 0.4s ease-out;
}}

.stat-item {{
    text-align: center;
    padding: 1rem;
}}

.stat-number {{
    font-size: 2rem;
    font-weight: 700;
    background: linear-gradient(135deg, {colors['accent']}, #764ba2);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}}

.stat-label {{
    color: {colors['text_secondary']};
    font-size: 0.9rem;
    margin-top: 0.5rem;
}}
</style>
""", unsafe_allow_html=True)

# Header
col1, col2, col3 = st.columns([1, 6, 1])

with col1:
    if st.button("🏠 Home"):
        st.switch_page("pages/0_Profile.py")

with col2:
    st.title("📜 Recipe Generation History")
    st.markdown("View all your past recipe generation requests")

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
    with st.spinner("Loading history..."):
        res = requests.get(
            f"{API_BASE}/history",
            headers=get_headers(),
            timeout=10
        )
    
    if res.status_code == 200:
        history = res.json()
        
        if not history:
            st.info("📭 No history yet. Generate some recipes to see them here!")
            st.markdown("---")
            if st.button("🔍 Explore Recipes", use_container_width=True):
                st.switch_page("pages/1_Explore.py")
        else:
            # Stats section
            st.markdown(f"""
            <div class="stats-container">
                <div style="display: flex; justify-content: space-around;">
                    <div class="stat-item">
                        <div class="stat-number">{len(history)}</div>
                        <div class="stat-label">Total Generations</div>
                    </div>
                    <div class="stat-item">
                        <div class="stat-number">{len(set(item.get('ingredients', '') for item in history))}</div>
                        <div class="stat-label">Unique Ingredient Sets</div>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            # Display history
            for idx, item in enumerate(history):
                with st.container():
                    st.markdown(f"""
                    <div class="history-card">
                        <div class="history-meta">
                            <div class="meta-item">
                                <span>🕐</span>
                                <span>{item.get('created_at', 'Unknown')}</span>
                            </div>
                            <div class="meta-item">
                                <span>🥗</span>
                                <span>{item.get('ingredients', 'N/A')[:50]}...</span>
                            </div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # Expandable recipe content
                    with st.expander("👁️ View Generated Recipes", expanded=False):
                        recipe_content = item.get('generated_recipe', 'No recipe content')
                        st.markdown(f"""
                        <div style="background: {colors['card_bg']}; padding: 1.5rem; border-radius: 12px; color: {colors['text']};">
                            <pre style="white-space: pre-wrap; font-family: 'Inter', sans-serif; line-height: 1.8; margin: 0;">
{recipe_content}
                            </pre>
                        </div>
                        """, unsafe_allow_html=True)
                        
                        col_a, col_b = st.columns(2)
                        
                        with col_a:
                            if st.button("⭐ Save to Favorites", key=f"save_hist_{idx}"):
                                try:
                                    save_res = requests.post(
                                        f"{API_BASE}/favorite",
                                        headers=get_headers(),
                                        json={"recipe": recipe_content},
                                        timeout=10
                                    )
                                    
                                    if save_res.status_code == 200:
                                        st.success("✅ Saved to favorites!")
                                        time.sleep(1)
                                    else:
                                        st.error("❌ Failed to save")
                                except Exception as e:
                                    st.error(f"Error: {str(e)}")
                        
                        with col_b:
                            if st.button("📋 Copy Text", key=f"copy_hist_{idx}"):
                                st.code(recipe_content, language=None)
    
    elif res.status_code == 401:
        st.error("Session expired. Please login again.")
        st.session_state.token = None
        st.switch_page("Home.py")
    else:
        error_msg = res.json().get("error", "Failed to load history")
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
    <small>💡 Your complete recipe generation history • Save any past recipe to favorites!</small>
</div>
""", unsafe_allow_html=True)