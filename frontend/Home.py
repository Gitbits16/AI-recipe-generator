import streamlit as st
import requests

# --------------------------------------------------
# PAGE CONFIG (ONLY ONCE — VERY IMPORTANT)
# --------------------------------------------------
st.set_page_config(
    page_title="FlavorForge",
    layout="wide",
    initial_sidebar_state="expanded"
)

API_BASE = "http://127.0.0.1:5000"

# --------------------------------------------------
# SESSION STATE INIT
# --------------------------------------------------
if "token" not in st.session_state:
    st.session_state.token = None
if "email" not in st.session_state:
    st.session_state.email = None
if "allergy" not in st.session_state:
    st.session_state.allergy = ""
if "theme" not in st.session_state:
    st.session_state.theme = "light"

# Redirect if logged in
if st.session_state.token:
    st.switch_page("pages/0_Profile.py")

# --------------------------------------------------
# THEME COLORS
# --------------------------------------------------
colors = {
    "bg": "#F8FAFF",
    "card": "rgba(255,255,255,0.7)",
    "text": "#1E1E1E",
    "accent": "#6C63FF"
}

# --------------------------------------------------
# GLOBAL STYLES (CLEAN + NON-CONFLICTING)
# --------------------------------------------------
st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700;800&display=swap');

* {{
    font-family: 'Inter', sans-serif;
}}

.stApp {{
    background: linear-gradient(135deg, #FFF7E6 0%, #ECEBFF 50%, #F8FAFF 100%);
}}

.block-container {{
    padding-top: 3rem;
    padding-bottom: 3rem;
}}
            
    
.brand-title {{
    font-size: 56px;
    font-weight: 800;
    letter-spacing: 1.4px;
    text-align: center;
    background: linear-gradient(135deg, #6C63FF, #8E85FF);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}}

.brand-divider {{
    width: 90px;
    height: 4px;
    margin: 16px auto;
    background: linear-gradient(90deg, #6C63FF, #FFB703);
    border-radius: 8px;
}}

.brand-tagline {{
    max-width: 700px;
    margin: auto;
    text-align: center;
    font-size: 18px;
    color: #555;
    line-height: 1.6;
}}

.glass-card {{
    background: {colors["card"]};
    backdrop-filter: blur(14px);
    border-radius: 24px;
    padding: 2.5rem;
    box-shadow: 0 20px 40px rgba(0,0,0,0.08);
}}

.stButton > button {{
    background: linear-gradient(135deg, #6C63FF, #8E85FF);
    color: white;
    border-radius: 30px;
    padding: 0.8rem 1.8rem;
    font-weight: 600;
    border: none;
    transition: all 0.3s ease;
}}

.stButton > button:hover {{
    transform: scale(1.05);
    box-shadow: 0 12px 25px rgba(108,99,255,0.35);
}}

.profile-avatar {{
    width: 72px;
    height: 72px;
    border-radius: 50%;
    background: linear-gradient(135deg, #6C63FF, #8E85FF);
    display: flex;
    align-items: center;
    justify-content: center;
    color: white;
    font-size: 28px;
    font-weight: 700;
    margin: auto;
}}

.profile-email {{
    text-align: center;
    font-size: 15px;
    margin-top: 8px;
    color: #555;
}}

.profile-section {{
    margin-top: 1.8rem;
}}

.section-title {{
    font-weight: 600;
    font-size: 16px;
    margin-bottom: 0.4rem;
    color: #444;
}}

.theme-pill {{
    display: inline-block;
    padding: 6px 16px;
    border-radius: 20px;
    background: rgba(108,99,255,0.12);
    color: #6C63FF;
    font-size: 13px;
    font-weight: 600;
    margin-top: 6px;
}}

.divider {{
    height: 1px;
    background: rgba(0,0,0,0.08);
    margin: 1.5rem 0;
}}



section[data-testid="stSidebar"] {{
    background: linear-gradient(180deg, #6C63FF, #7F77FF);
    color: white;
}}

section[data-testid="stSidebar"] * {{
    color: white;
}}
</style>
""", unsafe_allow_html=True)



if st.session_state.theme == "dark":
    st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(135deg, #0E1117, #1A1D29);
        color: white;
    }
    .glass-card {
        background: rgba(255,255,255,0.08);
    }
    </style>
    """, unsafe_allow_html=True)


# --------------------------------------------------
# BRAND / HERO SECTION (NO ICON)
# --------------------------------------------------
st.markdown("""
<div style="padding-top:40px; padding-bottom:50px;">
    <div class="brand-title">FlavorForge</div>
    <div class="brand-divider"></div>
    <div class="brand-tagline">
        A personalized AI recipe generator that transforms your ingredients,
        dietary preferences, and health goals into thoughtfully crafted meals.
    </div>
</div>
""", unsafe_allow_html=True)

# --------------------------------------------------
# SIDEBAR INPUTS
# --------------------------------------------------
with st.sidebar:
    st.header("📝 Your Inputs")

    ingredients = st.text_area(
        "Ingredients (comma-separated)",
        placeholder="chicken, rice, spinach, garlic, tomatoes",
        height=120
    )

    preferences = st.multiselect(
        "Dietary Preferences",
        ["Vegetarian", "Vegan", "Low-carb", "High-protein", "Gluten-free", "None"],
        default=["None"]
    )

    cuisine = st.selectbox(
        "Cuisine",
        ["Any", "Indian", "Italian", "Mexican", "Chinese"]
    )

    goal = st.selectbox(
        "Nutrition Goal",
        ["Balanced", "Healthy", "Quick", "Low-waste"]
    )

# --------------------------------------------------
# LOGIN / REGISTER SECTION
# --------------------------------------------------
tab1, tab2 = st.tabs(["🔑 Login", "✨ Register"])


with tab1:
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)

    email = st.text_input("Email")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        try:
            res = requests.post(
                f"{API_BASE}/login",
                json={"email": email, "password": password},
                timeout=10
            )
            if res.status_code == 200:
                data = res.json()
                st.session_state.token = data["token"]
                st.session_state.email = data["email"]
                st.session_state.allergy = data.get("allergy", "")
                st.success("Login successful")
                st.rerun()
            else:
                st.error(res.json().get("error", "Invalid credentials"))
        except Exception:
            st.error("Backend server not running")

    st.markdown('</div>', unsafe_allow_html=True)

with tab2:
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)

    new_email = st.text_input("Email", key="reg_email")
    new_password = st.text_input("Password", type="password", key="reg_pass")
    confirm = st.text_input("Confirm Password", type="password")
    allergy = st.text_input("Allergies (optional)")

    if st.button("Create Account"):
        if new_password != confirm:
            st.error("Passwords do not match")
        else:
            try:
                res = requests.post(
                    f"{API_BASE}/register",
                    json={
                        "email": new_email,
                        "password": new_password,
                        "allergy": allergy
                    },
                    timeout=10
                )
                if res.status_code == 201:
                    st.success("Account created. Please login.")
                else:
                    st.error(res.json().get("error", "Registration failed"))
            except Exception:
                st.error("Backend server not running")

    st.markdown('</div>', unsafe_allow_html=True)

# --------------------------------------------------
# FOOTER
# --------------------------------------------------
st.markdown("""
<div style="text-align:center; margin-top:60px; color:#777;">
    <small>FlavorForge © 2025 • Crafted with AI & Care</small>
</div>
""", unsafe_allow_html=True)
