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

/* ── Hero ── */
.hero {
    display: flex; flex-direction: column; gap: 6px;
    margin-bottom: 2rem; padding-bottom: 1.5rem;
    border-bottom: 1px solid var(--border);
}
.hero-eyebrow {
    font-size: 11px; font-weight: 500; letter-spacing: 3px;
    text-transform: uppercase; color: var(--accent);
}
.hero-title {
    font-family: var(--font-head);
    font-size: clamp(1.8rem, 5vw, 3.2rem);
    font-weight: 800; line-height: 1.05; color: var(--text); margin: 0;
}
.hero-title span { color: var(--accent); }
.hero-sub { font-size: 15px; color: var(--muted); max-width: 520px; line-height: 1.6; margin-top: 4px; }

/* ── Profile section label ── */
.profile-label {
    font-family: var(--font-head);
    font-size: 14px; font-weight: 700;
    color: var(--text); letter-spacing: -0.3px;
    margin-bottom: 0.5rem;
}
.profile-label span { color: var(--accent); }

/* ── BMI badge ── */
.bmi-badge {
    display: flex; align-items: center; gap: 10px;
    background: linear-gradient(135deg, rgba(0,245,160,0.08), rgba(0,200,255,0.06));
    border: 1px solid rgba(0,245,160,0.25);
    border-radius: 10px; padding: 12px 14px; margin: 0.8rem 0;
}
.bmi-dot {
    width: 10px; height: 10px; border-radius: 50%;
    background: var(--accent); flex-shrink: 0;
    box-shadow: 0 0 8px var(--accent); animation: pulse 2s infinite;
}
@keyframes pulse {
    0%, 100% { opacity: 1; transform: scale(1); }
    50%       { opacity: 0.5; transform: scale(1.3); }
}
.bmi-text { font-family: var(--font-head); font-size: 15px; font-weight: 700; color: var(--accent); }
.bmi-label { font-size: 14px; color: var(--muted); margin-top: 2px; }
.bmi-muted { font-size: 13px; color: var(--muted); padding: 6px 0; }

/* ── Inputs ── */
.stTextInput > label {
    font-family: var(--font-head) !important;
    font-size: 11px !important; font-weight: 600 !important;
    letter-spacing: 1.5px !important; text-transform: uppercase !important;
    color: var(--muted) !important;
}
.stTextInput > div > div > input {
    background: var(--card) !important;
    border: 1px solid var(--border) !important;
    border-radius: 10px !important; color: var(--text) !important;
    font-family: var(--font-body) !important;
    font-size: 16px !important; padding: 12px 14px !important;
}
.stTextInput > div > div > input:focus {
    border-color: var(--accent) !important;
    box-shadow: 0 0 0 3px rgba(0,245,160,0.08) !important;
}
.stSelectbox > label {
    font-size: 11px !important; font-weight: 600 !important;
    letter-spacing: 1.5px !important; text-transform: uppercase !important;
    color: var(--muted) !important;
}
.stSelectbox > div > div {
    background: var(--card) !important;
    border: 1px solid var(--border) !important;
    border-radius: 10px !important; color: var(--text) !important;
}
.stSlider > label {
    font-size: 11px !important; font-weight: 600 !important;
    letter-spacing: 1.5px !important; text-transform: uppercase !important;
    color: var(--muted) !important;
}

/* ── Expander (profile section) ── */
.stExpander {
    background: var(--card) !important;
    border: 1px solid var(--border) !important;
    border-radius: 12px !important;
    margin-bottom: 1.5rem !important;
}
.stExpander summary {
    color: var(--accent) !important;
    font-weight: 600 !important;
    font-size: 14px !important;
}

/* ── Divider ── */
.divider {
    height: 1px; background: var(--border);
    margin: 1rem 0;
}

/* ── Question label ── */
.question-label {
    font-family: var(--font-head);
    font-size: 13px; font-weight: 600;
    letter-spacing: 1px; text-transform: uppercase;
    color: var(--accent2); margin-bottom: 0.3rem;
}

/* ── Response ── */
.response-wrap {
    background: var(--card); border: 1px solid var(--border);
    border-top: 3px solid var(--accent); border-radius: 14px;
    padding: 0.8rem 1rem; margin-top: 1.5rem;
    line-height: 1.8; font-size: 15px;
}
.response-tag {
    font-family: var(--font-head); font-size: 9px;
    font-weight: 700; letter-spacing: 2px;
    text-transform: uppercase; color: var(--accent);
    margin-bottom: 0.4rem;
}

.stAlert { border-radius: 10px !important; border-left-color: var(--warn) !important; }
hr { border-color: var(--border) !important; }

/* ── Mobile ── */
@media (max-width: 768px) {
    .block-container { padding: 1rem 1rem 3rem !important; }
    .hero { margin-bottom: 1rem; padding-bottom: 1rem; }
    .hero-sub { font-size: 13px; max-width: 100%; }
    .response-wrap { font-size: 14px; }
}
</style>
""", unsafe_allow_html=True)


# ── Hero ───────────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero">
    <div class="hero-eyebrow">AI · Health · Personalised</div>
    <h1 class="hero-title">Healthify <span>Clone</span></h1>
    <p class="hero-sub">Your personal health companion powered by Gemini AI. Ask anything — get guidance built around <em>your</em> body.</p>
</div>
""", unsafe_allow_html=True)


# ── Profile inputs (expander — works perfectly on mobile) ──────────────────
with st.expander("👤  Enter your profile", expanded=True):
    col1, col2 = st.columns(2)
    with col1:
        name   = st.text_input('Full name')
        age    = st.text_input('Age (years)')
        weight = st.text_input('Weight (kg)')
    with col2:
        gender = st.selectbox('Gender', ['Male', 'Female', 'Other'])
        height = st.text_input('Height (cm)')
        fittness = st.slider('Fitness level (0–5)', 0, 5, step=1,
                             help='0 = sedentary · 5 = peak fitness')

    # BMI inside the expander
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

            st.markdown(f"""
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
            st.markdown('<p class="bmi-muted">⚠ Enter valid numbers for weight and height.</p>', unsafe_allow_html=True)
    else:
        st.markdown('<p class="bmi-muted">Fill in weight & height to see your BMI.</p>', unsafe_allow_html=True)


# ── Question ───────────────────────────────────────────────────────────────
user_query = st.text_input('Ask your health question',
                            placeholder='e.g. Why do I feel tired after meals?')

if user_query:
    if not weight or not height or bmi is None:
        st.warning('Please fill in your weight and height in your profile above.')
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
