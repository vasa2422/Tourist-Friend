import streamlit as st
import google.generativeai as genai
import google.api_core.exceptions
import base64
import time
from datetime import datetime

# =========================================================
# CONFIGURATION: YOUR API KEY
# =========================================================
API_KEY ="AIzaSyD1BYgaBrHzZUu3KR0B3WgR2_NZFxEdji4"
# =========================================================

# --- PAGE CONFIG ---
st.set_page_config(page_title="Travel Friend", layout="wide", page_icon="✈️")

# --- ASSET HANDLERS ---
def get_base64(file_path):
    try:
        with open(file_path, "rb") as f:
            data = f.read()
        return base64.b64encode(data).decode()
    except:
        return None

def apply_ui_design():
    # Background logic
    bg_local = get_base64("background.jpg")
    bg_url = f"data:image/png;base64,{bg_local}" if bg_local else "https://images.unsplash.com/photo-1488646953014-85cb44e25828?q=80&w=2000"
    
    logo_base64 = get_base64("logo.png")
    
    st.markdown(f"""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;600;800&display=swap');
        
        /* Full Travel Collage Background */
        .stApp {{
            background-image: linear-gradient(rgba(0,0,0,0.4), rgba(0,0,0,0.4)), url("{bg_url}");
            background-size: cover;
            background-position: center;
            background-attachment: fixed;
        }}

        /* Midnight Blue Font (#102C57) - High Visibility */
        html, body, [class*="st-"] {{
            font-family: 'Poppins', sans-serif;
            color: #102C57 !important; 
        }}

        /* Navigation Bar */
        .nav-bar {{
            background: rgba(255, 255, 255, 0.95);
            padding: 10px 40px;
            display: flex; justify-content: space-between; align-items: center;
            border-radius: 15px; max-width: 1100px; margin: 10px auto;
            box-shadow: 0 4px 12px rgba(0,0,0,0.2);
            backdrop-filter: blur(5px);
        }}

        /* Main Glassmorphism Card */
        .main-card {{
            background: rgba(255, 255, 255, 0.9);
            max-width: 1100px; margin: 0 auto; display: flex; 
            border-radius: 24px; overflow: hidden; 
            border: 1px solid rgba(255,255,255,0.5);
            backdrop-filter: blur(10px);
            box-shadow: 0 15px 35px rgba(0,0,0,0.3);
        }}

        .output-box, .suggestion-box {{
            background: #ffffff; border: 2px solid #13637a;
            border-radius: 15px; padding: 25px; margin-top: 20px;
            color: #102C57; box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        }}

        .guide-card {{
            background: #f0f7f9; border-left: 8px solid #ff6b35;
            padding: 20px; border-radius: 12px; margin-top: 20px;
            color: #102C57;
        }}

        .stButton>button {{
            background-color: #ff6b35 !important; color: white !important;
            width: 100%; border-radius: 12px !important; height: 50px;
            font-weight: 800; border: none;
        }}

        label, b, h2, h3 {{ color: #102C57 !important; font-weight: 800 !important; }}
        iframe {{ border-radius: 15px; border: 2px solid #13637a; }}
    </style>
    """, unsafe_allow_html=True)
    return logo_base64

# --- INITIALIZE UI ---
logo_data = apply_ui_design()

# --- NAVBAR ---
logo_html = f'<img src="data:image/png;base64,{logo_data}" style="height:50px;">' if logo_data else "✈️"
st.markdown(f"""
<div class="nav-bar">
    <div style="display:flex; align-items:center; gap:15px;">
        {logo_html}
        <b style="font-size:22px; letter-spacing: 1px;">TRAVEL FRIEND</b>
    </div>
    <div style="background:#fff5f2; padding:5px 15px; border-radius:20px; color:#ff6b35 !important; font-weight:bold; font-size:14px; border:1px solid #ff6b35;">
        📞 +1-234-567-890
    </div>
</div>
""", unsafe_allow_html=True)

# --- AI ENGINE ---
@st.cache_data(show_spinner=False)
def get_travel_plan(prompt, api_key):
    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-2.5-flash')
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        if "429" in str(e): return "RATE_LIMIT"
        return f"ERROR: {str(e)}"

# --- MAIN PAGE CONTENT ---
with st.container():
    st.markdown('<div class="main-card">', unsafe_allow_html=True)
    col_left, col_right = st.columns([1, 1.8])

    with col_left:
        # Boy Illustration & Branding
        if logo_data:
            st.image(f"data:image/png;base64,{logo_data}", width=110)
        st.markdown(f"""
        <div style="background:rgba(238,246,251,0.3); padding:20px 40px; height:100%;">
            <img src="https://img.freepik.com/free-vector/traveling-concept-illustration_114360-3167.jpg" style="width:100%; border-radius:15px;">
            <h2 style="margin-top:20px;">Dream | Explore | Discover</h2>
            <p style="font-size:15px; opacity:0.9;">Plan your journey with Travel Friend. Enter your details and let AI find your path.</p>
        </div>
        """, unsafe_allow_html=True)

    with col_right:
        st.markdown('<div style="padding:40px;">', unsafe_allow_html=True)
        st.write("### Enter your tour details:")
        
        dest = st.text_input("Destination", placeholder="e.g. Switzerland")
        
        row1_c1, row1_c2 = st.columns(2)
        with row1_c1: t_date = st.text_input("Start Date", placeholder="Jan 20, 2026")
        with row1_c2: p_time = st.text_input("Pickup Time", placeholder="09:30 AM")
            
        row2_c1, row2_c2 = st.columns(2)
        with row2_c1: days = st.number_input("How many days?", min_value=1, value=3)
        with row2_c2: budget = st.selectbox("Your Budget", ["Economy", "Mid-Range", "Luxury"])

        if st.button("✈️ GENERATE MY TRAVEL PLAN"):
            if not dest:
                st.error("Please specify a destination!")
            else:
                prompt = (f"Act as a travel coordinator for {dest}. Duration: {days} days. "
                          f"Budget: {budget}. Pickup: {p_time}. Start Date: {t_date}. "
                          f"1. Provide a daily travel summary [PLAN]. "
                          f"2. Assign a local guide name and phone number for {dest} [GUIDE]. "
                          f"3. List 4 best tourist places for a {budget} traveler [PLACES]. "
                          f"Use [PLAN], [GUIDE], [PLACES] tags.")
                
                with st.spinner("Travel Friend is crafting your plan..."):
                    result = get_travel_plan(prompt, API_KEY)
                    
                    if result == "RATE_LIMIT":
                        st.error("🛑 System busy. Please wait 60 seconds.")
                    else:
                        try:
                            st.session_state.p_out = result.split("[PLAN]")[1].split("[GUIDE]")[0].strip()
                            st.session_state.g_out = result.split("[GUIDE]")[1].split("[PLACES]")[0].strip()
                            st.session_state.s_out = result.split("[PLACES]")[1].strip()
                            st.session_state.map_loc = dest
                        except:
                            st.session_state.p_out = result

        # --- OUTPUT AREA ---
        if 'p_out' in st.session_state:
            st.markdown(f'<div class="output-box"><b>📅 Your {days}-Day Itinerary:</b><br>{st.session_state.p_out}</div>', unsafe_allow_html=True)
            
            # Map View
            st.write("### 🗺️ Live Destination Map")
            map_url = f"https://www.google.com/maps?q={st.session_state.map_loc}&output=embed"
            st.markdown(f'<iframe width="100%" height="350" src="{map_url}"></iframe>', unsafe_allow_html=True)

            # Suggestions
            st.write(f"### ✨ Top Suggestions for {dest}")
            st.markdown(f'<div class="suggestion-box">{st.session_state.s_out}</div>', unsafe_allow_html=True)

            # Local Guide (At the end)
            st.markdown(f"""
            <div class="guide-card">
                <h3 style="margin:0; color:#ff6b35 !important;">👨‍✈️ Local Guide Assigned</h3>
                <p style="margin:10px 0 0 0; font-size:16px; font-weight:bold;">{st.session_state.g_out}</p>
            </div>
            """, unsafe_allow_html=True)
            
            if st.button("Confirm & Start Travel"): st.balloons()
        
        st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# --- FOOTER ---

st.markdown("<p style='text-align:center; color:white; font-weight:bold; margin-top:20px; text-shadow: 2px 2px 5px black;'>Travel Friend © 2026</p>", unsafe_allow_html=True)





