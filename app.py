import streamlit as st
from openai import OpenAI
import io
import hashlib
import datetime
from PIL import Image
import requests
from bs4 import BeautifulSoup
import tempfile
import time
import os

# ============================================
# PAGE CONFIGURATION
# ============================================

st.set_page_config(
    page_title="Angaza AI - Premium Intelligence",
    page_icon="💎",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================
# PROFESSIONAL CUSTOM CSS
# ============================================

st.markdown("""
<style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
    
    * {
        font-family: 'Inter', sans-serif;
    }
    
    /* Hide default Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Main container */
    .main-header {
        background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
        padding: 24px 32px;
        border-radius: 16px;
        margin-bottom: 24px;
        box-shadow: 0 4px 20px rgba(0,0,0,0.1);
    }
    
    .logo-text {
        font-size: 28px;
        font-weight: 700;
        color: white;
    }
    
    .logo-sub {
        font-size: 14px;
        color: rgba(255,255,255,0.8);
        margin-top: 4px;
    }
    
    .user-badge {
        background: rgba(255,255,255,0.15);
        padding: 8px 16px;
        border-radius: 40px;
        backdrop-filter: blur(10px);
    }
    
    /* Chat input styling */
    .stChatInput > div {
        border-radius: 30px !important;
        border: 2px solid #e0e0e0 !important;
        transition: all 0.3s ease;
    }
    
    .stChatInput > div:focus-within {
        border-color: #2a5298 !important;
        box-shadow: 0 0 0 3px rgba(42,82,152,0.1);
    }
    
    .stChatInput button {
        background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%) !important;
        border-radius: 50% !important;
    }
    
    /* Button styling */
    .stButton > button {
        background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
        color: white;
        font-weight: 500;
        border: none;
        border-radius: 10px;
        padding: 10px 20px;
        transition: transform 0.2s, box-shadow 0.2s;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(30,60,114,0.3);
    }
    
    /* Sidebar styling */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #f8f9fc 0%, #ffffff 100%);
        border-right: 1px solid #e0e0e0;
    }
    
    [data-testid="stSidebar"] > div:first-child {
        padding-top: 20px;
    }
    
    /* Sidebar profile card */
    .profile-card {
        text-align: center;
        padding: 24px;
        background: linear-gradient(135deg, #f0f4fc 0%, #e8eef8 100%);
        border-radius: 20px;
        margin-bottom: 24px;
    }
    
    .profile-avatar {
        font-size: 56px;
        margin-bottom: 12px;
    }
    
    .profile-name {
        font-weight: 700;
        font-size: 18px;
        color: #1e3c72;
        margin-bottom: 4px;
    }
    
    .profile-email {
        font-size: 12px;
        color: #666;
    }
    
    .profile-badge {
        display: inline-block;
        background: #2a5298;
        color: white;
        font-size: 10px;
        padding: 2px 10px;
        border-radius: 20px;
        margin-top: 8px;
    }
    
    /* Section headers in sidebar */
    .section-header {
        font-size: 14px;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 1px;
        color: #666;
        margin: 16px 0 12px 0;
    }
    
    /* Divider */
    .custom-divider {
        margin: 16px 0;
        border-top: 1px solid #e0e0e0;
    }
    
    /* File uploader styling */
    .stFileUploader > div {
        border: 2px dashed #2a5298 !important;
        border-radius: 16px !important;
        background: #f8fafd !important;
    }
    
    /* Chat message styling */
    [data-testid="stChatMessage"] {
        border-radius: 16px !important;
        margin-bottom: 16px !important;
    }
    
    [data-testid="stChatMessage"]:has(div[data-testid="stChatMessageAvatarUser"]) {
        background: linear-gradient(135deg, #f0f4fc 0%, #e8eef8 100%);
    }
    
    /* Thinking animation */
    @keyframes pulse {
        0%, 100% { opacity: 0.4; transform: scale(0.9); }
        50% { opacity: 1; transform: scale(1.1); }
    }
    
    .thinking-container {
        display: flex;
        align-items: center;
        gap: 12px;
        padding: 16px 20px;
        background: #f0f4fc;
        border-radius: 20px;
        margin: 8px 0;
    }
    
    .thinking-dot {
        width: 10px;
        height: 10px;
        background: #2a5298;
        border-radius: 50%;
        animation: pulse 1.2s infinite ease-in-out;
    }
    
    .thinking-dot:nth-child(1) { animation-delay: 0s; }
    .thinking-dot:nth-child(2) { animation-delay: 0.2s; }
    .thinking-dot:nth-child(3) { animation-delay: 0.4s; }
    
    /* Metric cards */
    [data-testid="stMetric"] {
        background: #f8fafd;
        border-radius: 12px;
        padding: 12px;
    }
    
    /* Login card */
    .login-wrapper {
        display: flex;
        justify-content: center;
        align-items: center;
        min-height: 80vh;
    }
    
    .login-card {
        background: white;
        border-radius: 24px;
        padding: 48px 40px;
        max-width: 460px;
        width: 100%;
        text-align: center;
        box-shadow: 0 20px 40px rgba(0,0,0,0.1);
        border: 1px solid rgba(0,0,0,0.05);
    }
    
    .login-icon {
        font-size: 64px;
        margin-bottom: 16px;
    }
    
    .login-title {
        font-size: 32px;
        font-weight: 700;
        background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 8px;
    }
    
    .login-subtitle {
        color: #666;
        margin-bottom: 32px;
    }
    
    /* Footer */
    .footer {
        text-align: center;
        padding: 20px;
        color: #999;
        font-size: 12px;
        border-top: 1px solid #e0e0e0;
        margin-top: 30px;
    }
    
    /* Status indicators */
    .file-active {
        background: #e8f5e9;
        padding: 8px 12px;
        border-radius: 12px;
        font-size: 12px;
        margin: 8px 0;
    }
</style>
""", unsafe_allow_html=True)

# ============================================
# USER DATABASE
# ============================================

users_db = {}

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def create_user(email, password, name):
    if email in users_db:
        return False
    users_db[email] = {
        "password": hash_password(password),
        "name": name,
        "email": email,
        "created_at": datetime.datetime.now().isoformat()
    }
    return True

def verify_user(email, password):
    if email in users_db:
        return users_db[email]["password"] == hash_password(password)
    return False

# Demo users
create_user("denis@angaza.ai", "admin123", "Denis Kirui")
create_user("demo@angaza.ai", "demo123", "Demo User")

# ============================================
# LOGIN FUNCTIONS
# ============================================

def email_login():
    email = st.session_state.get("login_email", "")
    password = st.session_state.get("login_password", "")
    
    if verify_user(email, password):
        st.session_state.logged_in = True
        st.session_state.user_email = email
        st.session_state.user_name = users_db[email]["name"]
        st.rerun()
    else:
        st.error("❌ Invalid email or password")

def email_signup():
    email = st.session_state.get("signup_email", "")
    password = st.session_state.get("signup_password", "")
    confirm = st.session_state.get("confirm_password", "")
    name = st.session_state.get("signup_name", "")
    
    if not email or not password or not name:
        st.error("Please fill all fields")
        return
    
    if password != confirm:
        st.error("Passwords do not match")
        return
    
    if create_user(email, password, name):
        st.session_state.logged_in = True
        st.session_state.user_email = email
        st.session_state.user_name = name
        st.success("✨ Account created successfully!")
        st.rerun()
    else:
        st.error("Email already exists")

def logout():
    st.session_state.logged_in = False
    st.session_state.messages = []
    st.rerun()

def google_login():
    st.session_state.logged_in = True
    st.session_state.user_email = "user@gmail.com"
    st.session_state.user_name = "Valued Customer"
    st.rerun()

# ============================================
# LOGIN SCREEN
# ============================================

def login_screen():
    st.markdown("""
    <div class="login-wrapper">
        <div class="login-card">
            <div class="login-icon">💎</div>
            <div class="login-title">Angaza AI</div>
            <div class="login-subtitle">Premium Intelligence from Kenya</div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("🔐 Continue with Google", use_container_width=True):
            google_login()
    
    st.markdown("<div style='text-align: center; margin: 20px 0; color: #999;'>or</div>", unsafe_allow_html=True)
    
    tab1, tab2 = st.tabs(["📧 Sign In", "✨ Create Account"])
    
    with tab1:
        st.text_input("Email address", key="login_email", placeholder="denis@angaza.ai")
        st.text_input("Password", type="password", key="login_password", placeholder="Enter your password")
        st.button("Sign In", on_click=email_login, use_container_width=True)
        st.caption("Demo: denis@angaza.ai / admin123")
    
    with tab2:
        st.text_input("Full name", key="signup_name", placeholder="Denis Kirui")
        st.text_input("Email", key="signup_email", placeholder="denis@angaza.ai")
        st.text_input("Password", type="password", key="signup_password", placeholder="Create a password")
        st.text_input("Confirm password", type="password", key="confirm_password", placeholder="Confirm your password")
        st.button("Create Account", on_click=email_signup, use_container_width=True)
    
    st.markdown("</div></div>", unsafe_allow_html=True)

# ============================================
# URL READER FUNCTION
# ============================================

def extract_url_content(url):
    try:
        response = requests.get(url, headers={"User-Agent": "Mozilla/5.0"}, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')
        
        for script in soup(["script", "style"]):
            script.decompose()
        
        text = soup.get_text()
        lines = (line.strip() for line in text.splitlines())
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        text = ' '.join(chunk for chunk in chunks if chunk)
        
        return text[:8000]
    except Exception as e:
        return None

# ============================================
# MAIN APP
# ============================================

def main_app():
    # Professional Header
    st.markdown(f"""
    <div class="main-header">
        <div style="display: flex; justify-content: space-between; align-items: center;">
            <div>
                <div class="logo-text">💎 Angaza AI</div>
                <div class="logo-sub">Premium Intelligence Platform</div>
            </div>
            <div class="user-badge">
                👋 {st.session_state.user_name}
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Sidebar
    with st.sidebar:
        # Profile Card
        st.markdown(f"""
        <div class="profile-card">
            <div class="profile-avatar">💎</div>
            <div class="profile-name">{st.session_state.user_name}</div>
            <div class="profile-email">{st.session_state.user_email}</div>
            <div class="profile-badge">Premium Member</div>
        </div>
        """, unsafe_allow_html=True)
        
        # Configuration Section
        st.markdown('<div class="section-header">⚙️ Configuration</div>', unsafe_allow_html=True)
        
        api_key = st.text_input("Groq API Key", type="password", placeholder="Enter your API key")
        model = st.selectbox("AI Model", ["llama-3.3-70b-versatile", "llama3-70b-8192"])
        
        # Performance Section
        st.markdown('<div class="section-header">⚡ Performance</div>', unsafe_allow_html=True)
        
        thinking_speed = st.select_slider(
            "Response Speed",
            options=["Fast", "Balanced", "Deep"],
            value="Balanced"
        )
        
        thinking_times = {"Fast": 0.3, "Balanced": 1.0, "Deep": 2.5}
        thinking_delay = thinking_times[thinking_speed]
        
        # Tools Section
        st.markdown('<div class="section-header">🛠️ Tools</div>', unsafe_allow_html=True)
        
        with st.expander("🔗 URL Reader", expanded=False):
            url = st.text_input("Enter URL", placeholder="https://example.com")
            if url and st.button("Read URL", use_container_width=True):
                with st.spinner("Reading..."):
                    content = extract_url_content(url)
                    if content:
                        st.session_state.file_content = content
                        st.session_state.file_name = f"URL: {url[:50]}"
                        st.success("✅ Content loaded")
                    else:
                        st.error("Could not read URL")
        
        with st.expander("📎 File Upload", expanded=False):
            uploaded_file = st.file_uploader("Upload", type=["txt", "pdf", "jpg", "png"], label_visibility="collapsed")
            if uploaded_file:
                if uploaded_file.type == "text/plain":
                    st.session_state.file_content = uploaded_file.read().decode("utf-8")
                    st.session_state.file_name = uploaded_file.name
                    st.success(f"✅ {uploaded_file.name}")
                elif uploaded_file.type == "application/pdf":
                    try:
                        import pdfplumber
                        all_text = ""
                        with pdfplumber.open(io.BytesIO(uploaded_file.read())) as pdf:
                            for page in pdf.pages:
                                text = page.extract_text()
                                if text:
                                    all_text += text
                        st.session_state.file_content = all_text
                        st.session_state.file_name = uploaded_file.name
                        st.success(f"✅ PDF loaded")
                    except:
                        st.error("PDF reading failed")
                elif uploaded_file.type.startswith("image/"):
                    st.session_state.image_name = uploaded_file.name
                    st.image(uploaded_file, width=100)
                    st.success(f"✅ Image loaded")
        
        # Active file indicator
        if "file_name" in st.session_state:
            st.markdown(f'<div class="file-active">📄 Active: {st.session_state.file_name[:30]}</div>', unsafe_allow_html=True)
            if st.button("🗑️ Clear File", use_container_width=True):
                for key in ["file_content", "file_name", "image_name"]:
                    if key in st.session_state:
                        del st.session_state[key]
                st.rerun()
        
        st.markdown('<div class="custom-divider"></div>', unsafe_allow_html=True)
        
        # Session Management
        col1, col2 = st.columns(2)
        with col1:
            if st.button("🗑️ Clear Chat", use_container_width=True):
                st.session_state.messages = []
                st.rerun()
        with col2:
            if st.button("🚪 Logout", use_container_width=True):
                logout()
        
        # Stats
        if "messages" in st.session_state:
            st.metric("💬 Messages", len(st.session_state.messages))
    
    # Chat Area
    if "messages" not in st.session_state:
        st.session_state.messages = []
    
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.write(msg["content"])
    
    # Chat Input
    if api_key:
        client = OpenAI(api_key=api_key, base_url="https://api.groq.com/openai/v1")
        
        prompt = st.chat_input("Ask me anything...")
        
        if prompt:
            st.session_state.messages.append({"role": "user", "content": prompt})
            with st.chat_message("user"):
                st.write(prompt)
            
            with st.chat_message("assistant"):
                thinking_placeholder = st.empty()
                
                with thinking_placeholder.container():
                    st.markdown("""
                    <div class="thinking-container">
                        <div class="thinking-dot"></div>
                        <div class="thinking-dot"></div>
                        <div class="thinking-dot"></div>
                        <span style="color: #666;">Angaza AI is analyzing...</span>
                    </div>
                    """, unsafe_allow_html=True)
                
                time.sleep(thinking_delay)
                
                try:
                    messages = []
                    
                    if "file_content" in st.session_state:
                        messages.append({
                            "role": "system",
                            "content": f"Document context: {st.session_state.file_content[:3000]}"
                        })
                    
                    for msg in st.session_state.messages:
                        messages.append({"role": msg["role"], "content": msg["content"]})
                    
                    response = client.chat.completions.create(
                        model=model,
                        messages=messages,
                        temperature=0.7,
                        max_tokens=2048
                    )
                    reply = response.choices[0].message.content
                    
                    thinking_placeholder.empty()
                    st.write(reply)
                    st.session_state.messages.append({"role": "assistant", "content": reply})
                    
                except Exception as e:
                    thinking_placeholder.empty()
                    st.error(f"Error: {e}")
    else:
        st.info("🔑 **Enter your Groq API key in the sidebar to begin**")
    
    # Footer
    st.markdown("""
    <div class="footer">
        💎 Angaza AI | Premium Intelligence Platform | © 2025 | Powered by Groq
    </div>
    """, unsafe_allow_html=True)

# ============================================
# INITIALIZE AND RUN
# ============================================

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    login_screen()
else:
    main_app()