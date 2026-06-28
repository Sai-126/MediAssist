import streamlit as st
import sys
sys.path.append(".")
from agents.orchestrator import Orchestrator
from data.facilities import get_facilities
from agents.dosage_helper import generate_dosage_schedule

st.set_page_config(
    page_title="MediAssist | మీ ఆరోగ్య సహాయకుడు",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Noto+Sans+Telugu:wght@400;500;600&display=swap');

html, body, [class*="css"], .stApp {
    font-family: 'Inter', 'Noto Sans Telugu', sans-serif !important;
    background-color: #F0F4FF !important;
}
#MainMenu, footer, header { visibility: hidden; }
.block-container {
    padding: 2rem 3rem 3rem 3rem !important;
    max-width: 100% !important;
}
section[data-testid="stSidebar"] { display: none; }

/* ── HEADER ── */
.ma-header {
    text-align: center;
    padding: 3.5rem 4rem 3rem;
    background: #FFFFFF;
    border: 1px solid #C7D2FE;
    border-radius: 20px;
    margin-bottom: 2rem;
}
.ma-badge {
    display: inline-flex; align-items: center; gap: 8px;
    background: #EEF2FF; border: 1px solid #C7D2FE;
    color: #4338CA; border-radius: 100px;
    padding: 6px 18px; font-size: 13px; font-weight: 600;
    letter-spacing: 0.07em; text-transform: uppercase; margin-bottom: 1.5rem;
}
.ma-title {
    font-size: 3.8rem; font-weight: 700; letter-spacing: -0.04em;
    color: #312E81; line-height: 1.05; margin: 0 0 0.4rem 0;
}
.ma-title span { color: #4F46E5; }
.ma-telugu { font-size: 1.4rem; color: #6366F1; font-family: 'Noto Sans Telugu', sans-serif; margin-bottom: 0.6rem; }
.ma-sub { font-size: 1rem; color: #6B7280; max-width: 620px; margin: 0 auto; line-height: 1.7; }

/* ── AGENT ROW ── */
.agent-row { display: flex; align-items: flex-start; gap: 1.2rem; margin-bottom: 1.5rem; }
.agent-icon-box {
    width: 58px; height: 58px; background: #EEF2FF;
    border: 1px solid #C7D2FE; border-radius: 14px;
    display: flex; align-items: center; justify-content: center;
    font-size: 1.7rem; flex-shrink: 0;
}
.agent-name { font-size: 1.35rem; font-weight: 600; color: #312E81; margin-bottom: 4px; }
.agent-te { font-size: 14px; color: #6B7280; font-family: 'Noto Sans Telugu', sans-serif; }

/* ── CARDS ── */
.resp-card {
    background: #FFFFFF; border: 1px solid #C7D2FE;
    border-radius: 16px; padding: 1.8rem 2rem; margin-top: 1.2rem;
    font-size: 16px; line-height: 1.8; color: #374151;
}
.resp-header {
    display: flex; align-items: center; gap: 10px;
    font-size: 12px; font-weight: 600; color: #6B7280;
    text-transform: uppercase; letter-spacing: 0.08em;
    margin-bottom: 1rem; padding-bottom: 1rem;
    border-bottom: 1px solid #EEF2FF;
}
.resp-dot { width: 8px; height: 8px; border-radius: 50%; background: #10B981; display: inline-block; flex-shrink: 0; }
.sched-card {
    background: #EEF2FF; border: 1px solid #C7D2FE;
    border-radius: 14px; padding: 1.2rem 1.6rem; margin-top: 1rem;
    font-size: 15px; color: #3730A3; line-height: 1.8;
}
.sched-header { font-size: 12px; font-weight: 600; color: #4F46E5; text-transform: uppercase; letter-spacing: 0.07em; margin-bottom: 0.6rem; }
.notice-banner {
    display: flex; gap: 12px; background: #FFFBEB;
    border: 1px solid #FDE68A; border-radius: 12px;
    padding: 1rem 1.4rem; font-size: 14px; color: #92400E; margin-top: 1rem; line-height: 1.6;
}
.facility-card {
    background: #EEF2FF; border: 1px solid #C7D2FE;
    border-radius: 14px; padding: 1.2rem 1.6rem; margin-top: 1rem;
    font-size: 15px; color: #3730A3; line-height: 1.9;
}
.facility-header { font-size: 12px; font-weight: 600; color: #4F46E5; text-transform: uppercase; letter-spacing: 0.07em; margin-bottom: 0.6rem; }

/* ── HELPLINE ── */
.helpline-bar {
    display: flex; background: #FFFFFF;
    border: 1px solid #C7D2FE; border-radius: 16px;
    overflow: hidden; margin-top: 2.5rem;
}
.helpline-item { flex: 1; text-align: center; padding: 1.4rem 1rem; border-right: 1px solid #E0E7FF; }
.helpline-item:last-child { border-right: none; }
.helpline-num { font-size: 1.8rem; font-weight: 700; color: #4F46E5; letter-spacing: -0.02em; }
.helpline-lbl { font-size: 13px; color: #6B7280; margin-top: 4px; line-height: 1.4; }

/* ══ STREAMLIT WIDGET OVERRIDES ══ */

/* Textarea */
.stTextArea textarea {
    background: #FFFFFF !important;
    border: 1.5px solid #C7D2FE !important;
    border-radius: 12px !important;
    font-size: 16px !important;
    color: #374151 !important;
    padding: 1rem 1.1rem !important;
    line-height: 1.6 !important;
}
.stTextArea textarea:focus {
    border-color: #4F46E5 !important;
    box-shadow: 0 0 0 3px rgba(79,70,229,0.12) !important;
}
.stTextArea textarea::placeholder { color: #A5B4FC !important; }

/* Number inputs — THE FIX: light bg, dark enough but NOT black */
.stNumberInput > div > div > input {
    background: #FFFFFF !important;
    border: 1.5px solid #C7D2FE !important;
    border-radius: 12px !important;
    font-size: 18px !important;
    font-weight: 600 !important;
    color: #4F46E5 !important;
    padding: 0.75rem 1rem !important;
    height: 54px !important;
    text-align: center !important;
}
.stNumberInput > div > div > input:focus {
    border-color: #4F46E5 !important;
    box-shadow: 0 0 0 3px rgba(79,70,229,0.12) !important;
}

/* Number +/- buttons */
.stNumberInput button {
    background: #EEF2FF !important;
    border: 1px solid #C7D2FE !important;
    border-radius: 8px !important;
    color: #4F46E5 !important;
    width: auto !important; height: auto !important;
}
.stNumberInput button svg { fill: #4F46E5 !important; color: #4F46E5 !important; }
.stNumberInput button p { color: #4F46E5 !important; }

/* Text input */
.stTextInput > div > div > input {
    background: #FFFFFF !important;
    border: 1.5px solid #C7D2FE !important;
    border-radius: 12px !important;
    font-size: 16px !important;
    color: #374151 !important;
    padding: 0.75rem 1rem !important;
    height: 52px !important;
}
.stTextInput > div > div > input::placeholder { color: #A5B4FC !important; }

/* Selectbox */
.stSelectbox > div > div {
    background: #FFFFFF !important;
    border: 1.5px solid #C7D2FE !important;
    border-radius: 12px !important;
    font-size: 16px !important;
    min-height: 52px !important;
}
[data-baseweb="select"] > div { background: #FFFFFF !important; }
[data-baseweb="select"] span { color: #374151 !important; font-size: 16px !important; }
[data-baseweb="select"] svg { color: #6366F1 !important; }
[data-baseweb="menu"] {
    background: #FFFFFF !important;
    border: 1px solid #C7D2FE !important;
    border-radius: 12px !important;
}
[data-baseweb="option"] {
    color: #374151 !important;
    background: #FFFFFF !important;
    font-size: 15px !important;
    padding: 10px 16px !important;
}
[data-baseweb="option"]:hover { background: #EEF2FF !important; color: #3730A3 !important; }

/* File uploader */
.stFileUploader > div {
    background: #F5F3FF !important;
    border: 2px dashed #C7D2FE !important;
    border-radius: 14px !important;
}
[data-testid="stFileUploaderDropzone"] { background: #F5F3FF !important; padding: 1.5rem !important; }
[data-testid="stFileUploaderDropzone"] * { color: #4B5563 !important; }
[data-testid="stFileUploaderDropzoneInstructions"] span { color: #4F46E5 !important; font-size: 15px !important; }
[data-testid="stFileUploaderDropzoneInstructions"] small { color: #9CA3AF !important; font-size: 13px !important; }

/* Buttons */
div.stButton > button {
    border-radius: 12px !important; font-weight: 600 !important;
    font-size: 16px !important; padding: 0.75rem 1.8rem !important;
    height: 52px !important; border: 1.5px solid #C7D2FE !important;
    background: #FFFFFF !important; color: #4F46E5 !important;
    transition: all 0.15s !important; width: 100% !important;
}
div.stButton > button:hover {
    background: #EEF2FF !important; border-color: #818CF8 !important;
}
div.stButton > button[kind="primary"] {
    background: #4F46E5 !important; border-color: #4F46E5 !important; color: #FFFFFF !important;
}
div.stButton > button[kind="primary"] * { color: #FFFFFF !important; }
div.stButton > button[kind="primary"]:hover { background: #4338CA !important; border-color: #4338CA !important; }

/* Widget labels */
[data-testid="stWidgetLabel"] p,
.stSelectbox label p,
.stTextArea label p,
.stNumberInput label p,
.stFileUploader label p {
    font-size: 15px !important;
    font-weight: 600 !important;
    color: #3730A3 !important;
    margin-bottom: 6px !important;
}

/* Tabs */
.stTabs [data-baseweb="tab-list"] {
    gap: 6px !important; background: transparent !important;
    border-bottom: 1.5px solid #C7D2FE !important; padding-bottom: 0 !important;
}
.stTabs [data-baseweb="tab"] {
    background: transparent !important; border-radius: 10px 10px 0 0 !important;
    padding: 14px 28px !important; font-size: 16px !important;
    font-weight: 500 !important; color: #6B7280 !important;
    border: 1.5px solid transparent !important; border-bottom: none !important;
}
.stTabs [aria-selected="true"] {
    background: #FFFFFF !important; border-color: #C7D2FE !important;
    border-bottom-color: #FFFFFF !important; color: #312E81 !important;
    font-weight: 600 !important; margin-bottom: -1.5px !important;
}
.stTabs [aria-selected="true"] p { color: #312E81 !important; font-weight: 600 !important; }
.stTabs [data-testid="stMarkdownContainer"] p { color: inherit !important; font-size: 16px !important; }
[data-baseweb="tab-highlight"] { display: none !important; }
[data-baseweb="tab-border"] { display: none !important; }

/* Metrics */
div[data-testid="stMetric"] {
    background: #FFFFFF !important; border: 1px solid #C7D2FE !important;
    border-radius: 14px !important; padding: 1.4rem 1.2rem !important;
}
div[data-testid="stMetric"] label { color: #6B7280 !important; font-size: 13px !important; font-weight: 500 !important; }
div[data-testid="stMetric"] [data-testid="stMetricValue"] {
    font-size: 2rem !important; font-weight: 700 !important; color: #4F46E5 !important;
}

/* Misc */
.stImage img { border-radius: 12px !important; border: 1px solid #C7D2FE !important; }
.stCaption p { color: #9CA3AF !important; font-size: 14px !important; }
hr { border-color: #E0E7FF !important; margin: 2rem 0 !important; }
.stSpinner * { color: #4F46E5 !important; }
.stAlert { border-radius: 12px !important; font-size: 15px !important; }
::-webkit-scrollbar { width: 6px; height: 6px; }
::-webkit-scrollbar-track { background: transparent; }
::-webkit-scrollbar-thumb { background: #C7D2FE; border-radius: 3px; }
</style>
""", unsafe_allow_html=True)

# ── HEADER ────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="ma-header">
    <div class="ma-badge">🏥 AI Health Assistant</div>
    <div class="ma-title">Medi<span>Assist</span></div>
    <div class="ma-telugu">మీ ఆరోగ్య సహాయకుడు</div>
    <div class="ma-sub">
        Helping rural patients understand prescriptions, symptoms, and government health schemes<br>
        <span style="font-family:'Noto Sans Telugu',sans-serif;color:#818CF8;">
        మందుల చీటీలు, లక్షణాలు మరియు ప్రభుత్వ పథకాల గురించి తెలుసుకోండి</span>
    </div>
</div>
""", unsafe_allow_html=True)

# ── STATS ─────────────────────────────────────────────────────────────────────
c1, c2, c3, c4 = st.columns(4)
with c1: st.metric("📄 Documents", "1,302")
with c2: st.metric("🧩 Chunks", "5,168")
with c3: st.metric("🌐 Languages / భాషలు", "2")
with c4: st.metric("🤖 Agents", "3")

st.write("")

_, lc, _ = st.columns([2, 1.5, 2])
with lc:
    language = st.selectbox(
        "Choose language / భాష ఎంచుకోండి",
        ["English", "తెలుగు (Telugu)"]
    )
lang_code = "telugu" if "తెలుగు" in language else "english"

st.write("")

@st.cache_resource
def load_orchestrator():
    return Orchestrator()
orch = load_orchestrator()

# ── TABS ──────────────────────────────────────────────────────────────────────
tab1, tab2, tab3 = st.tabs([
    "💊  Prescription Reader  |  మందుల చీటీ",
    "🩺  Symptom Checker  |  లక్షణాల తనిఖీ",
    "🏛️  Health Schemes  |  ఆరోగ్య పథకాలు"
])

# ── TAB 1: PRESCRIPTION ───────────────────────────────────────────────────────
with tab1:
    st.markdown("""
    <div class="agent-row">
        <div class="agent-icon-box">💊</div>
        <div>
            <div class="agent-name">Prescription Reader</div>
            <div class="agent-te">మీ మందుల చీటీని అర్థం చేసుకోండి — upload చేయండి లేదా టైప్ చేయండి</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    uploaded_image = st.file_uploader(
        "📷 Upload prescription image / మందుల చీటీ ఫోటో",
        type=["jpg", "jpeg", "png"]
    )
    if uploaded_image:
        col_img, _ = st.columns([1, 2])
        with col_img:
            st.image(uploaded_image,
                     caption="Uploaded prescription / అప్‌లోడ్ చేసిన మందుల చీటీ",
                     use_container_width=True)

    text_input = st.text_area(
        "✍️ Or type medicine names / లేదా మందుల పేర్లు టైప్ చేయండి",
        height=150,
        placeholder="e.g. Tab Paracetamol 500mg twice daily after food\nలేదా: పారాసెటమాల్ 500mg రోజుకు రెండుసార్లు భోజనం తర్వాత"
    )

    col_btn, _ = st.columns([1.2, 3])
    with col_btn:
        submit_rx = st.button("🔍 Explain prescription / వివరించండి",
                              type="primary", key="rx_btn")

    if submit_rx:
        if not text_input.strip() and not uploaded_image:
            st.warning("⚠️ Please enter prescription text or upload an image.")
        else:
            with st.spinner("Reading your prescription / మందుల చీటీ చదువుతున్నాము..."):
                result = orch.route(
                    "prescription",
                    query=text_input if text_input.strip() else None,
                    image_file=uploaded_image,
                    language=lang_code
                )
            st.markdown(f"""
            <div class="resp-card">
                <div class="resp-header"><span class="resp-dot"></span> AI Response / AI సమాధానం</div>
                {result}
            </div>
            """, unsafe_allow_html=True)

            if text_input.strip():
                schedule = generate_dosage_schedule(text_input)
                st.markdown(f"""
                <div class="sched-card">
                    <div class="sched-header">⏰ Dosage schedule / మందుల వేళలు</div>
                    {schedule}
                </div>
                """, unsafe_allow_html=True)

            fc1, fc2, _ = st.columns([0.6, 0.8, 4])
            with fc1: st.button("👍 Helpful", key="rx_up")
            with fc2: st.button("👎 Not helpful", key="rx_down")

# ── TAB 2: SYMPTOMS ───────────────────────────────────────────────────────────
with tab2:
    st.markdown("""
    <div class="agent-row">
        <div class="agent-icon-box">🩺</div>
        <div>
            <div class="agent-name">Symptom Checker / లక్షణాల తనిఖీ</div>
            <div class="agent-te">మీ ఆరోగ్య సమస్యలను వివరించండి — తెలుగులో లేదా English లో చెప్పవచ్చు</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    symptoms = st.text_area(
        "Describe your symptoms / మీ లక్షణాలు వివరించండి",
        height=160,
        placeholder="e.g. I have fever and headache for 2 days\nలేదా: నాకు 2 రోజులు జ్వరం మరియు తలనొప్పి ఉంది"
    )

    st.markdown("""
    <div class="notice-banner">
        ⚠️&nbsp; This is for information only. Always consult a qualified doctor.<br>
        ఇది సమాచారం కోసం మాత్రమే. వైద్యుడిని సంప్రదించండి.
    </div>
    """, unsafe_allow_html=True)

    st.write("")
    col_btn2, _ = st.columns([1.2, 3])
    with col_btn2:
        submit_sym = st.button("🔍 Check symptoms / లక్షణాలు తనిఖీ",
                               type="primary", key="sym_btn")

    if submit_sym:
        if not symptoms.strip():
            st.warning("⚠️ Please describe your symptoms / మీ లక్షణాలు వివరించండి.")
        else:
            with st.spinner("Searching medical information / సమాచారం వెతుకుతున్నాము..."):
                result = orch.route("symptoms", query=symptoms, language=lang_code)
            st.markdown(f"""
            <div class="resp-card">
                <div class="resp-header"><span class="resp-dot"></span> AI Response / AI సమాధానం</div>
                {result}
            </div>
            """, unsafe_allow_html=True)
            fc1, fc2, _ = st.columns([0.6, 0.8, 4])
            with fc1: st.button("👍 Helpful", key="sym_up")
            with fc2: st.button("👎 Not helpful", key="sym_down")

# ── TAB 3: SCHEMES ────────────────────────────────────────────────────────────
with tab3:
    st.markdown("""
    <div class="agent-row">
        <div class="agent-icon-box">🏛️</div>
        <div>
            <div class="agent-name">Health Scheme Eligibility / ఆరోగ్య పథకం అర్హత</div>
            <div class="agent-te">ఆరోగ్యశ్రీ, PM-JAY, NHM పథకాలకు మీరు అర్హులా అని తెలుసుకోండి</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)
    with col1:
        district = st.selectbox("📍 District / జిల్లా", [
            "Vijayawada", "Visakhapatnam", "Guntur", "Hyderabad",
            "Warangal", "Karimnagar", "Nizamabad", "Khammam",
            "Tirupati", "Kurnool", "Nellore", "Rajahmundry",
            "Eluru", "Bhimavaram", "Surampalem"
        ])
        income = st.number_input("💰 Annual income (₹) / వార్షిక ఆదాయం",
                                 value=0, step=10000, min_value=0)
    with col2:
        age = st.number_input("🎂 Age / వయస్సు",
                              value=30, min_value=0, max_value=120)
        family_size = st.number_input("👨‍👩‍👧‍👦 Family size / కుటుంబ సభ్యులు",
                                      value=4, min_value=1)
    with col3:
        category = st.selectbox("📋 Category / వర్గం", ["SC", "ST", "BC", "General"])
        ration = st.selectbox("🗂️ Ration card / రేషన్ కార్డు",
                              ["None / లేదు", "White", "Pink (BPL)", "Yellow (AAY)"])

    st.write("")
    col_btn3, _ = st.columns([1.5, 3])
    with col_btn3:
        submit_sch = st.button("🔍 Check eligibility / అర్హత తనిఖీ చేయండి",
                               type="primary", key="sch_btn")

    if submit_sch:
        with st.spinner("Checking scheme eligibility / పథకాల అర్హత తనిఖీ..."):
            result = orch.route(
                "scheme",
                profile={
                    "district": district,
                    "income": income,
                    "age": age,
                    "family_size": family_size,
                    "category": category,
                    "ration_card": ration
                },
                language=lang_code
            )
        st.markdown(f"""
        <div class="resp-card">
            <div class="resp-header"><span class="resp-dot"></span> Eligible Schemes / అర్హమైన పథకాలు</div>
            {result}
        </div>
        """, unsafe_allow_html=True)

        facilities = get_facilities(district)
        facility_lines = "<br>".join([f"📍 {f}" for f in facilities])
        st.markdown(f"""
        <div class="facility-card">
            <div class="facility-header">🏥 Nearby facilities / సమీప ఆసుపత్రులు</div>
            {facility_lines}
        </div>
        """, unsafe_allow_html=True)

        fc1, fc2, _ = st.columns([0.6, 0.8, 4])
        with fc1: st.button("👍 Helpful", key="sch_up")
        with fc2: st.button("👎 Not helpful", key="sch_down")

# ── HELPLINE BAR ──────────────────────────────────────────────────────────────
st.markdown("""
<div class="helpline-bar">
    <div class="helpline-item">
        <div class="helpline-num">104</div>
        <div class="helpline-lbl">Aarogyasri / NHM<br>ఆరోగ్యశ్రీ</div>
    </div>
    <div class="helpline-item">
        <div class="helpline-num">108</div>
        <div class="helpline-lbl">Emergency Ambulance<br>అత్యవసర అంబులెన్స్</div>
    </div>
    <div class="helpline-item">
        <div class="helpline-num">102</div>
        <div class="helpline-lbl">Pregnancy &amp; Mother-Child<br>గర్భిణీ సేవలు</div>
    </div>
    <div class="helpline-item">
        <div class="helpline-num">14555</div>
        <div class="helpline-lbl">PM-JAY Helpline<br>ఆయుష్మాన్ భారత్</div>
    </div>
</div>
""", unsafe_allow_html=True)

# ── FOOTER ────────────────────────────────────────────────────────────────────
st.markdown("---")
st.markdown("""
<div style="text-align:center;padding:0.5rem 0 1rem;font-size:14px;color:#6B7280;line-height:1.8;">
    🏥 <b style="color:#312E81;">MediAssist</b>
    <span style="color:#6366F1;"> మీ ఆరోగ్య సహాయకుడు</span>
    &nbsp;·&nbsp; Built for rural healthcare access · AP &amp; Telangana<br>
    <span style="font-size:12px;color:#9CA3AF;">
    ⚠️ This tool provides information only. Always consult a qualified doctor / వైద్యుడిని సంప్రదించండి.
    </span>
</div>
""", unsafe_allow_html=True)