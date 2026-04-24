import streamlit as st
import requests

API_BASE = "http://127.0.0.1:5000"

# Authentication guard
if not st.session_state.get("token"):
    st.switch_page("Home.py")

st.set_page_config(page_title="Profile", page_icon="👤", layout="wide")

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

@keyframes fadeIn {{
    from {{ opacity: 0; transform: translateY(20px); }}
    to {{ opacity: 1; transform: translateY(0); }}
}}

@keyframes slideIn {{
    from {{ transform: translateX(-50px); opacity: 0; }}
    to {{ transform: translateX(0); opacity: 1; }}
}}

.main {{
    background: {colors['bg']};
    color: {colors['text']};
}}

.profile-header {{
    background: linear-gradient(135deg, {colors['accent']} 0%, #764ba2 100%);
    padding: 3rem 2rem;
    border-radius: 24px;
    text-align: center;
    margin-bottom: 2rem;
    animation: fadeIn 0.6s ease-out;
    box-shadow: 0 10px 40px rgba(102, 126, 234, 0.3);
}}

.profile-avatar {{
    width: 100px;
    height: 100px;
    border-radius: 50%;
    background: white;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 3rem;
    margin: 0 auto 1rem;
    box-shadow: 0 8px 24px rgba(0, 0, 0, 0.2);
}}

.section-card {{
    background: {colors['card_bg']};
    backdrop-filter: blur(20px) saturate(180%);
    -webkit-backdrop-filter: blur(20px) saturate(180%);
    border: 1px solid {colors['card_border']};
    border-radius: 20px;
    padding: 2rem;
    margin-bottom: 2rem;
    box-shadow: 0 8px 32px 0 {colors['shadow']};
    animation: slideIn 0.8s ease-out;
    transition: all 0.3s ease;
    color: {colors['text']};
}}

.section-card:hover {{
    transform: translateY(-5px);
    box-shadow: 0 12px 40px 0 {colors['shadow']};
}}

.section-title {{
    font-size: 1.5rem;
    font-weight: 700;
    margin-bottom: 1.5rem;
    color: {colors['accent']};
    display: flex;
    align-items: center;
    gap: 0.75rem;
}}

.stButton button {{
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
    border: none;
    border-radius: 12px;
    padding: 0.75rem 2rem;
    font-weight: 600;
    transition: all 0.3s ease;
    box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);
}}

.stButton button:hover {{
    transform: translateY(-2px);
    box-shadow: 0 6px 20px rgba(102, 126, 234, 0.6);
}}

.quick-action {{
    background: linear-gradient(135deg, rgba(102, 126, 234, 0.1) 0%, rgba(118, 75, 162, 0.1) 100%);
    padding: 1.5rem;
    border-radius: 16px;
    text-align: center;
    cursor: pointer;
    transition: all 0.3s ease;
    border: 1px solid {colors['card_border']};
    color: {colors['text']};
}}

.quick-action:hover {{
    transform: translateY(-5px);
    box-shadow: 0 8px 24px rgba(102, 126, 234, 0.3);
    border-color: {colors['accent']};
}}

.quick-action-icon {{
    font-size: 2.5rem;
    margin-bottom: 0.5rem;
}}

.info-badge {{
    display: inline-block;
    background: linear-gradient(135deg, {colors['accent']} 0%, #764ba2 100%);
    color: white;
    padding: 0.5rem 1rem;
    border-radius: 20px;
    font-size: 0.9rem;
    font-weight: 600;
    margin: 0.25rem;
}}
</style>
""", unsafe_allow_html=True)

# Header
col1, col2 = st.columns([6, 1])

with col1:
    st.markdown(f"""
    <div class="profile-header">
        <div class="profile-avatar">👤</div>
        <h1 style="color: white; margin-bottom: 0.5rem;">Welcome Back!</h1>
        <p style="color: rgba(255,255,255,0.9); font-size: 1.1rem;">{st.session_state.email}</p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    theme_icon = "🌙" if st.session_state.theme == 'light' else "☀️"
    if st.button(theme_icon, help="Toggle theme"):
        toggle_theme()
        st.rerun()

# Quick Actions
st.markdown(f"""
<div style="margin-bottom: 2rem;">
    <h3 style="color: {colors['text']}; margin-bottom: 1rem;">⚡ Quick Actions</h3>
</div>
""", unsafe_allow_html=True)

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown(f"""<div class="quick-action"><div class="quick-action-icon">🔍</div><div>Explore Recipes</div></div>""", unsafe_allow_html=True)
    if st.button("Go", key="explore_btn", use_container_width=True):
        st.switch_page("pages/1_Explore.py")

with col2:
    st.markdown(f"""<div class="quick-action"><div class="quick-action-icon">⭐</div><div>Saved Recipes</div></div>""", unsafe_allow_html=True)
    if st.button("Go", key="saved_btn", use_container_width=True):
        st.switch_page("pages/2_Saved.py")

with col3:
    st.markdown(f"""<div class="quick-action"><div class="quick-action-icon">📜</div><div>History</div></div>""", unsafe_allow_html=True)
    if st.button("Go", key="history_btn", use_container_width=True):
        st.switch_page("pages/4_History.py")

with col4:
    st.markdown(f"""<div class="quick-action"><div class="quick-action-icon">👋</div><div>Logout</div></div>""", unsafe_allow_html=True)
    if st.button("Go", key="logout_btn", use_container_width=True):
        st.switch_page("pages/3_Logout.py")

st.markdown("<br>", unsafe_allow_html=True)

# Profile Information
col1, col2 = st.columns(2)

with col1:
    st.markdown(f"""
    <div class="section-card">
        <div class="section-title">🚫 Allergy Information</div>
        <p style="color: {colors['text_secondary']}; margin-bottom: 1rem;">
            Enter allergies separated by commas
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    new_allergy = st.text_input(
        "Allergies",
        st.session_state.get("allergy", ""),
        placeholder="e.g., peanuts, shellfish, dairy",
        label_visibility="collapsed"
    )
    
    if st.button("💾 Update Allergy Information", type="primary", use_container_width=True):
        try:
            with st.spinner("Updating..."):
                res = requests.post(
                    f"{API_BASE}/update-allergy",
                    headers=get_headers(),
                    json={"allergy": new_allergy},
                    timeout=10
                )
            
            if res.status_code == 200:
                st.session_state.allergy = new_allergy
                st.success("✅ Allergy information updated successfully")
            elif res.status_code == 401:
                st.error("Session expired. Please login again.")
                st.session_state.token = None
                st.switch_page("Home.py")
            else:
                error_msg = res.json().get("error", "Update failed")
                st.error(f"❌ {error_msg}")
        except Exception as e:
            st.error(f"An error occurred: {str(e)}")

with col2:
    st.markdown(f"""
    <div class="section-card">
        <div class="section-title">🔑 Change Password</div>
        <p style="color: {colors['text_secondary']}; margin-bottom: 1rem;">
            Password must be 8+ chars with uppercase, lowercase, and numbers
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    with st.form("password_form"):
        new_pass = st.text_input("New Password", type="password")
        confirm_pass = st.text_input("Confirm Password", type="password")
        submit_password = st.form_submit_button("🔐 Update Password", use_container_width=True)
        
        if submit_password:
            if not new_pass or not confirm_pass:
                st.error("❌ All fields are required")
            elif new_pass != confirm_pass:
                st.error("❌ Passwords do not match")
            elif len(new_pass) < 8:
                st.error("❌ Password must be at least 8 characters")
            else:
                try:
                    with st.spinner("Updating password..."):
                        res = requests.post(
                            f"{API_BASE}/update-password",
                            headers=get_headers(),
                            json={"password": new_pass},
                            timeout=10
                        )
                    
                    if res.status_code == 200:
                        st.success("✅ Password updated successfully")
                    elif res.status_code == 401:
                        st.error("Session expired. Please login again.")
                        st.session_state.token = None
                        st.switch_page("Home.py")
                    else:
                        error_msg = res.json().get("error", "Password update failed")
                        st.error(f"❌ {error_msg}")
                except Exception as e:
                    st.error(f"An error occurred: {str(e)}")

st.markdown("<br>", unsafe_allow_html=True)

# Account Overview
st.markdown(f"""
<div class="section-card">
    <div class="section-title">ℹ️ Account Overview</div>
    <div style="display: flex; flex-wrap: wrap; gap: 1rem; margin-top: 1rem;">
        <span class="info-badge">📧 {st.session_state.email}</span>
        <span class="info-badge">🚫 {st.session_state.allergy or 'No allergies'}</span>
        <span class="info-badge">✅ Active</span>
    </div>
</div>
""", unsafe_allow_html=True)