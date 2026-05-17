import streamlit as st
import google.generativeai as genai
import pandas as pd
import os

st.set_page_config(
    page_title="Healthify Clone",
    page_icon="🩺",
    layout="centered",
    initial_sidebar_state="collapsed"
)

api = os.getenv('GOOGLE_GEMINI_API')
genai.configure(api_key=api)
model = genai.GenerativeModel('gemini-2.5-flash-lite')

# ── Custom CSS ─────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=DM+Sans:ital,wght@0,300;0,400;0,500;1,300&display=swap');

:root {
    --bg:        #080f1a;
    --bg2:       #0d1829;
    --card:      #111f35;
    --border:    #1e3352;
    --accent:    #00f5a0;
    --accent2:   #00c8ff;
    --warn:      #ff6b6b;
    --text:      #e8f4ff;
    --muted:     #6b8cae;
    --font-head: 'Syne', sans-serif;
    --font-body: 'DM Sans', sans-serif;
}

html, body, [class*="css"] {
    font-family: var(--font-body);
    background-color: var(--bg) !important;
    color: var(--text) !important;
}

#MainMenu, footer, header { visibility: hidden; }
.block-container { padding: 2rem 2.5rem 4rem !important; max-width: 860px !important; }

.hero {
    display: flex;
    flex-direction: column;
    gap: 6px;
    margin-bottom: 2rem;
    padding-bottom: 1.5rem;
    border-bottom: 1px solid var(--border);
}
.hero-eyebrow {
    font-family: var(--font-body);
    font-size: 11px;
    font-weight: 500;
    letter-spacing: 3px;
    text-transform: uppercase;
    color: var(--accent);
}
.hero-title {
    font-family: var(--font-head);
    font-size: clamp(2rem, 5vw, 3.2rem);
    font-weight: 800;
    line-height: 1.05;
    color: var(--text);
    margin: 0;
}
.hero-title span { color: var(--accent); }
.hero-sub {
    font-size: 15px;
    color: var(--muted);
    max-width: 520px;
    line-height: 1.6;
    margin-top: 4px;
}

.steps-card {
    background: var(--card);
    border: 1px solid var(--border);
    border-left: 3px solid var(--accent2);
    border-radius: 12px;
    padding: 1.2rem 1.5rem;
    margin-bottom: 2rem;
    font-size: 14px;
    color: var(--muted);
    line-height: 2;
}
.steps-card b { color: var(--text); font-weight: 500; }

.stTextInput > label {
    font-family: var(--font-head) !important;
    font-size: 13px !important;
    font-weight: 600 !important;
    letter-spacing: 1px !important;
    text-transform: uppercase !important;
    color: var(--accent2) !important;
}
.stTextInput > div > div > input {
    background: var(--card) !important;
    border: 1px solid var(--border) !important;
    border-radius: 10px !important;
    color: var(--text) !important;
    font-family: var(--font-body) !important;
    font-size: 15px !important;
    padding: 14px 16px !important;
}
.stTextInput > div > div > input:focus {
    border-color: var(--accent) !important;
    box-shadow: 0 0 0 3px rgba(0,245,160,0.08) !important;
}

[data-testid="stSidebar"] {
    background: var(--bg2) !important;
    border-right: 1px solid var(--border) !important;
}
[data-testid="stSidebar"] .block-container { padding: 1.5rem 1.2rem !important; }

.sidebar-header {
    font-family: var(--font-head);
    font-size: 18px;
    font-weight: 700;
    color: var(--text);
    letter-spacing: -0.3px;
    margin-bottom: 1.2rem;
    padding-bottom: 0.8rem;
    border-bottom: 1px solid var(--border);
}
.sidebar-header span { color: var(--accent); }

[data-testid="stSidebar"] .stTextInput > label,
[data-testid="stSidebar"] .stSelectbox > label,
[data-testid="stSidebar"] .stSlider > label {
    font-size: 11px !important;
    font-weight: 600 !important;
    letter-spacing: 1.5px !important;
    text-transform: uppercase !important;
    color: var(--muted) !important;
}
[data-testid="stSidebar"] .stTextInput > div > div > input {
    background: var(--card) !important;
    border: 1px solid var(--border) !important;
    border-radius: 8px !important;
    color: var(--text) !important;
    padding: 10px 12px !important;
    font-size: 14px !important;
}
[data-testid="stSidebar"] .stSelectbox > div > div {
    background: var(--card) !important;
    border: 1px solid var(--border) !important;
    border-radius: 8px !important;
    color: var(--text) !important;
}

.bmi-badge {
    display: flex;
    align-items: center;
    gap: 10px;
    background: linear-gradient(135deg, rgba(0,245,160,0.08), rgba(0,200,255,0.06));
    border: 1px solid rgba(0,245,160,0.25);
    border-radius: 10px;
    padding: 12px 14px;
    margin-top: 0.8rem;
}
.bmi-dot {
    width: 10px; height: 10px;
    border-radius: 50%;
    background: var(--accent);
    flex-shrink: 0;
    box-shadow: 0 0 8px var(--accent);
    animation: pulse 2s infinite;
}
@keyframes pulse {
    0%, 100% { opacity: 1; transform: scale(1); }
    50%       { opacity: 0.5; transform: scale(1.3); }
}
.bmi-text { font-family: var(--font-head); font-size: 15px; font-weight: 700; color: var(--accent); }
.bmi-label { font-size: 16px; color: var(--muted); margin-top: 2px; letter-spacing: 0.5px; }
.bmi-muted { font-size: 13px; color: var(--muted); padding: 10px 0 0; }

.response-wrap {
    background: var(--card);
    border: 1px solid var(--border);
    border-top: 3px solid var(--accent);
    border-radius: 14px;
    padding: 0.7rem 1rem;
    margin-top: 1.5rem;
    line-height: 1.8;
    font-size: 15px;
}
.response-tag {
    font-family: var(--font-head);
    font-size: 9px; margin-bottom: 0.4rem;
    font-weight: 700;
    letter-spacing: 2px;
    text-transform: uppercase;
    color: var(--accent);
    
}

.stAlert { border-radius: 10px !important; border-left-color: var(--warn) !important; }
hr { border-color: var(--border) !important; }

/* ── SIDEBAR TOGGLE BUTTON ── */
[data-testid="stSidebarCollapsedControl"] {
    background: var(--accent) !important;
    border-radius: 8px !important;
    padding: 4px !important;
}
[data-testid="stSidebarCollapsedControl"] svg {
    fill: #080f1a !important;
    color: #080f1a !important;
}
button[kind="header"] {
    background: var(--accent) !important;
    border-radius: 8px !important;
}

/* ── MOBILE RESPONSIVE ── */
@media (max-width: 768px) {
    .block-container { padding: 1rem 1rem 3rem !important; }

    .hero { margin-bottom: 0.8rem; padding-bottom: 0.8rem; }
    .hero-eyebrow { font-size: 10px; letter-spacing: 2px; }
    .hero-title { font-size: 1.8rem !important; }
    .hero-sub { font-size: 13px; max-width: 100%; }

    .steps-card {
        padding: 0.9rem 1rem;
        font-size: 13px;
        line-height: 2.2;
    }

    .stTextInput > div > div > input {
        font-size: 16px !important;
        padding: 12px 14px !important;
    }

    .response-wrap { padding: 0.6rem 0.8rem; font-size: 14px; }

    .bmi-text { font-size: 14px; }
    .bmi-label { font-size: 14px; }
}

/* Mobile sidebar toggle hint */
@media (max-width: 768px) {
    .mobile-hint {
        display: block;
        background: rgba(0,245,160,0.06);
        border: 1px solid rgba(0,245,160,0.2);
        border-radius: 10px;
        padding: 10px 14px;
        margin-bottom: 0.8rem;
        font-size: 13px;
        color: var(--accent);
        white-space: nowrap;
        overflow: hidden;
        text-overflow: ellipsis;
    }
}
@media (min-width: 769px) {
    .mobile-hint { display: none; }
}
</style>
""", unsafe_allow_html=True)


# ── Sidebar ────────────────────────────────────────────────────────────────
st.sidebar.markdown('<div class="sidebar-header">Your <span>Profile</span></div>', unsafe_allow_html=True)

name     = st.sidebar.text_input('Full name')
gender   = st.sidebar.selectbox('Gender', ['Male', 'Female', 'Other'])
age      = st.sidebar.text_input('Age (years)')
weight   = st.sidebar.text_input('Weight (kg)')
height   = st.sidebar.text_input('Height (cm)')
fittness = st.sidebar.slider('Fitness level', 0, 5, step=1,
                              help='0 = sedentary  ·  5 = peak fitness')

st.sidebar.markdown('<hr>', unsafe_allow_html=True)

bmi = None
bmi_cat = ''
if weight and height:
    try:
        bmi = pd.to_numeric(weight) / (pd.to_numeric(height) / 100) ** 2
        bmi_val = round(bmi, 2)
        if bmi_val < 18.5:   bmi_cat = "Underweight"
        elif bmi_val < 25.0: bmi_cat = "Normal weight"
        elif bmi_val < 30.0: bmi_cat = "Overweight"
        else:                bmi_cat = "Obese"

        st.sidebar.markdown(f"""
        <div class="bmi-badge">
            <div class="bmi-dot"></div>
            <div>
                <div class="bmi-text">{bmi_val} kg/m²</div>
                <div class="bmi-label">{bmi_cat}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    except Exception:
        bmi = None
        st.sidebar.markdown('<p class="bmi-muted">⚠ Enter valid numbers.</p>', unsafe_allow_html=True)
else:
    st.sidebar.markdown('<p class="bmi-muted">Fill in weight &amp; height to see your BMI.</p>', unsafe_allow_html=True)


# ── Main ───────────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero">
    <div class="hero-eyebrow">AI · Health · Personalised</div>
    <h1 class="hero-title">Healthify <span>Clone</span></h1>
    <p class="hero-sub">Your personal health companion powered by Gemini AI. Ask anything — get guidance built around <em>your</em> body.</p>
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div class="mobile-hint">
    ☰ Tap the top-left arrow to open your profile
</div>
<div class="steps-card">
    <b>① </b>Open sidebar &amp; fill your profile<br>
    <b>② </b>Check your live BMI<br>
    <b>③ </b>Ask your health question below
</div>
""", unsafe_allow_html=True)

user_query = st.text_input('Ask your health question', placeholder='e.g. Why do I feel tired after meals?')

if user_query:
    if not weight or not height or bmi is None:
        st.warning('Please fill in your weight and height in the sidebar first.')
    else:
        prompt = f"""Assume you are a health expert. Answer the user's question using their profile below.

User profile:
- Name: {name}
- Gender: {gender}
- Age: {age}
- Weight: {weight} kg
- Height: {height} cm
- BMI: {round(bmi, 2)} kg/m² ({bmi_cat})
- Fitness self-rating: {fittness} / 5

Response format:
* Open with a 1-2 line personalised comment on their profile.
* Explain the problem clearly based on their query.
* List possible causes.
* Suggest practical, evidence-based solutions.
* Recommend a specialist type if relevant.
* Do NOT recommend any specific medication.
* Use bullet points and tables where helpful.
* Close with a 5-7 line summary.

User's question: {user_query}"""

        with st.spinner('Analysing your profile…'):
            response = model.generate_content(prompt)

        st.markdown('<div class="response-wrap"><div class="response-tag">✦ AI Health Guidance</div>', unsafe_allow_html=True)
        st.write(response.text)
        st.markdown('</div>', unsafe_allow_html=True)
