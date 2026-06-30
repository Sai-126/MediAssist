import streamlit as st
import sys
sys.path.append(".")
from agents.orchestrator import Orchestrator
from data.facilities import get_facilities
from agents.dosage_helper import generate_dosage_schedule

st.set_page_config(
    page_title="MediAssist | Rural Health Assistant",
    page_icon="\U0001F3E5",
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

* {
    color: #1F2937;
}

.ma-header {
    text-align: center;
    padding: 3.5rem 2rem 3rem;
    background: #FFFFFF;
    border: 1px solid #C7D2FE;
    border-radius: 20px;
    margin-bottom: 2rem;
}
.ma-badge {
    display: inline-flex; align-items: center; gap: 8px;
    background: #EEF2FF; border: 1px solid #C7D2FE;
    color: #4338CA !important; border-radius: 100px;
    padding: 6px 18px; font-size: 13px; font-weight: 600;
    letter-spacing: 0.07em; text-transform: uppercase; margin-bottom: 1.5rem;
}
.ma-title {
    font-size: 3.8rem; font-weight: 700; letter-spacing: -0.04em;
    color: #312E81 !important; line-height: 1.05; margin: 0 0 0.4rem 0;
    white-space: nowrap;
}
.ma-title span { color: #4F46E5 !important; }
.ma-telugu { font-size: 1.4rem; color: #6366F1 !important; font-family: 'Noto Sans Telugu', sans-serif; margin-bottom: 0.6rem; }
.ma-sub { font-size: 1rem; color: #6B7280 !important; max-width: 620px; margin: 0 auto; line-height: 1.7; }

@media (max-width: 768px) {
    .ma-title { font-size: 2.2rem; white-space: normal; }
    .ma-telugu { font-size: 1.1rem; }
    .ma-header { padding: 2rem 1rem; }
}

/* ---- METRICS ---- */
div[data-testid="stMetric"] {
    background: #F7F9FF !important;
    border: 1px solid #C7D2FE !important;
    border-radius: 14px !important;
    padding: 1rem !important;
}
div[data-testid="stMetricLabel"] {
    color: #4338CA !important;
}
div[data-testid="stMetricLabel"] p {
    color: #4338CA !important;
    font-weight: 600 !important;
    opacity: 1 !important;
}
div[data-testid="stMetricValue"] {
    color: #312E81 !important;
}
div[data-testid="stMetricValue"] div {
    color: #312E81 !important;
    opacity: 1 !important;
}

/* ---- LABELS (widget titles) ---- */
label, [data-testid="stWidgetLabel"] p, [data-testid="stWidgetLabel"] {
    color: #312E81 !important;
    font-weight: 600 !important;
    opacity: 1 !important;
}

/* ---- TABS ---- */
.stTabs [data-baseweb="tab-list"] {
    gap: 8px;
    background-color: transparent !important;
}
.stTabs [data-baseweb="tab"] {
    background-color: #FFFFFF !important;
    border: 1px solid #C7D2FE !important;
    border-radius: 10px;
    padding: 12px 20px;
    font-weight: 600;
}
.stTabs [data-baseweb="tab"] p {
    color: #312E81 !important;
    opacity: 1 !important;
}
.stTabs [aria-selected="true"] {
    background-color: #4F46E5 !important;
    border: 1px solid #4F46E5 !important;
}
.stTabs [aria-selected="true"] p {
    color: #FFFFFF !important;
}

/* ---- SELECTBOX (closed state) ---- */
.stSelectbox div[data-baseweb="select"] > div {
    background-color: #FFFFFF !important;
    border: 1px solid #C7D2FE !important;
}
.stSelectbox div[data-baseweb="select"] > div > div {
    color: #312E81 !important;
    opacity: 1 !important;
    font-weight: 600 !important;
}
.stSelectbox [data-baseweb="select"] span {
    color: #312E81 !important;
}

/* ---- SELECTBOX dropdown (open list) ---- */
div[data-baseweb="popover"] ul {
    background-color: #FFFFFF !important;
}
div[data-baseweb="popover"] li {
    background-color: #FFFFFF !important;
    color: #312E81 !important;
}
div[data-baseweb="popover"] li:hover {
    background-color: #EEF2FF !important;
    color: #312E81 !important;
}
div[role="listbox"] {
    background-color: #FFFFFF !important;
}
div[role="option"] {
    background-color: #FFFFFF !important;
    color: #312E81 !important;
}
div[role="option"]:hover {
    background-color: #EEF2FF !important;
}

/* ---- TEXT INPUT / TEXTAREA / NUMBER INPUT ---- */
.stTextInput input, .stTextArea textarea, .stNumberInput input {
    color: #1F2937 !important;
    background-color: #FFFFFF !important;
    border: 1px solid #C7D2FE !important;
}
.stTextInput input::placeholder, .stTextArea textarea::placeholder {
    color: #9CA3AF !important;
}
.stNumberInput button {
    background-color: #EEF2FF !important;
    color: #312E81 !important;
}

/* ---- FILE UPLOADER ---- */
[data-testid="stFileUploaderDropzone"] {
    background-color: #F9FAFF !important;
    border: 1.5px dashed #A5B4FC !important;
}
[data-testid="stFileUploaderDropzone"] * {
    color: #312E81 !important;
    opacity: 1 !important;
}
[data-testid="stFileUploaderDropzoneInstructions"] span,
[data-testid="stFileUploaderDropzoneInstructions"] small {
    color: #4B5563 !important;
}
[data-testid="stFileUploaderFile"] {
    background-color: #FFFFFF !important;
    color: #312E81 !important;
}
[data-testid="stFileUploaderFile"] * {
    color: #312E81 !important;
}

/* ---- BUTTONS ---- */
.stButton button {
    background-color: #FFFFFF !important;
    color: #312E81 !important;
    border: 1px solid #C7D2FE !important;
    font-weight: 600 !important;
}
.stButton button p {
    color: #312E81 !important;
}
.stButton button[kind="primary"] {
    background-color: #4F46E5 !important;
    border: 1px solid #4F46E5 !important;
}
.stButton button[kind="primary"] p {
    color: #FFFFFF !important;
}

/* ---- ALERTS ---- */
.stAlert {
    background-color: #FFFBEB !important;
}
.stAlert p {
    color: #92400E !important;
}

/* ---- AGENT ROW ---- */
.agent-row { display: flex; align-items: flex-start; gap: 1.2rem; margin-bottom: 1.5rem; }
.agent-icon-box {
    width: 58px; height: 58px; background: #EEF2FF;
    border: 1px solid #C7D2FE; border-radius: 14px;
    display: flex; align-items: center; justify-content: center;
    font-size: 1.7rem; flex-shrink: 0;
}
.agent-name { font-size: 1.35rem; font-weight: 600; color: #312E81 !important; margin-bottom: 4px; }
.agent-te { font-size: 14px; color: #6B7280 !important; font-family: 'Noto Sans Telugu', sans-serif; }

/* ---- RESPONSE CARDS ---- */
.resp-card {
    background: #FFFFFF; border: 1px solid #C7D2FE;
    border-radius: 16px; padding: 1.8rem 2rem; margin-top: 1.2rem;
    font-size: 16px; line-height: 1.8; color: #374151 !important;
}
.resp-card * { color: #374151 !important; }
.resp-header {
    display: flex; align-items: center; gap: 10px;
    font-size: 12px; font-weight: 600; color: #6B7280 !important;
    text-transform: uppercase; letter-spacing: 0.08em;
    margin-bottom: 1rem; padding-bottom: 1rem;
    border-bottom: 1px solid #EEF2FF;
}
.resp-dot { width: 8px; height: 8px; border-radius: 50%; background: #10B981; display: inline-block; flex-shrink: 0; }

.sched-card {
    background: #EEF2FF; border: 1px solid #C7D2FE;
    border-radius: 14px; padding: 1.2rem 1.6rem; margin-top: 1rem;
    font-size: 15px; color: #3730A3 !important; line-height: 1.8;
}
.sched-card * { color: #3730A3 !important; }
.sched-header { font-size: 12px; font-weight: 600; color: #4F46E5 !important; text-transform: uppercase; letter-spacing: 0.07em; margin-bottom: 0.6rem; }

.notice-banner {
    display: flex; gap: 12px; background: #FFFBEB;
    border: 1px solid #FDE68A; border-radius: 12px;
    padding: 1rem 1.4rem; font-size: 14px; color: #92400E !important; margin-top: 1rem; line-height: 1.6;
}
.notice-banner * { color: #92400E !important; }

.facility-card {
    background: #EEF2FF; border: 1px solid #C7D2FE;
    border-radius: 14px; padding: 1.2rem 1.6rem; margin-top: 1rem;
    font-size: 15px; color: #3730A3 !important; line-height: 1.9;
}
.facility-card * { color: #3730A3 !important; }
.facility-header { font-size: 12px; font-weight: 600; color: #4F46E5 !important; text-transform: uppercase; letter-spacing: 0.07em; margin-bottom: 0.6rem; }

/* ---- HELPLINE BAR ---- */
.helpline-bar {
    display: flex; flex-wrap: wrap; background: #FFFFFF;
    border: 1px solid #C7D2FE; border-radius: 16px;
    overflow: hidden; margin-top: 2.5rem;
}
.helpline-item { flex: 1; min-width: 140px; text-align: center; padding: 1.4rem 1rem; border-right: 1px solid #E0E7FF; }
.helpline-item:last-child { border-right: none; }
.helpline-num { font-size: 1.8rem; font-weight: 700; color: #4F46E5 !important; letter-spacing: -0.02em; }
.helpline-lbl { font-size: 13px; color: #6B7280 !important; margin-top: 4px; line-height: 1.4; }
.helpline-lbl * { color: #6B7280 !important; }

/* ---- FOOTER ---- */
.ma-footer { color: #6B7280 !important; }
.ma-footer * { color: #6B7280 !important; }
.ma-footer b { color: #312E81 !important; }
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="ma-header">
    <div class="ma-badge">\U0001F3E5 AI Health Assistant</div>
    <div class="ma-title">Medi<span>Assist</span></div>
    <div class="ma-telugu">\u0c2e\u0c40 \u0c06\u0c30\u0c4b\u0c17\u0c4d\u0c2f \u0c38\u0c39\u0c3e\u0c2f\u0c15\u0c41\u0c21\u0c41</div>
    <div class="ma-sub">
        Helping rural patients understand prescriptions, symptoms, and government health schemes<br>
        <span style="font-family:'Noto Sans Telugu',sans-serif;color:#818CF8;">
        \u0c2e\u0c02\u0c26\u0c41\u0c32 \u0c1a\u0c40\u0c1f\u0c40\u0c32\u0c41, \u0c32\u0c15\u0c4d\u0c37\u0c23\u0c3e\u0c32\u0c41 \u0c2e\u0c30\u0c3f\u0c2f\u0c41 \u0c2a\u0c4d\u0c30\u0c2e\u0c41\u0c24\u0c4d\u0c35 \u0c2a\u0c25\u0c15\u0c3e\u0c32 \u0c17\u0c41\u0c30\u0c3f\u0c02\u0c1a\u0c3f \u0c24\u0c46\u0c32\u0c41\u0c38\u0c41\u0c15\u0c4b\u0c02\u0c21\u0c3f</span>
    </div>
</div>
""", unsafe_allow_html=True)

c1, c2, c3, c4 = st.columns(4)
with c1: st.metric("\U0001F4C4 Documents", "1,302")
with c2: st.metric("\U0001F9E9 Chunks", "5,168")
with c3: st.metric("\U0001F310 Languages", "2")
with c4: st.metric("\U0001F916 Agents", "3")

st.write("")

_, lc, _ = st.columns([2, 1.5, 2])
with lc:
    language = st.selectbox(
        "Choose language / \u0c2c\u0c3e\u0c37 \u0c0e\u0c02\u0c1a\u0c41\u0c15\u0c4b\u0c02\u0c21\u0c3f",
        ["English", "\u0c24\u0c46\u0c32\u0c41\u0c17\u0c41 (Telugu)"]
    )
lang_code = "telugu" if "\u0c24\u0c46\u0c32\u0c41\u0c17\u0c41" in language else "english"

st.write("")

@st.cache_resource
def load_orchestrator():
    return Orchestrator()
orch = load_orchestrator()

tab1, tab2, tab3 = st.tabs([
    "\U0001F48A  Prescription Reader",
    "\U0001FA7A  Symptom Checker",
    "\U0001F3DB\uFE0F  Health Schemes"
])

with tab1:
    st.markdown("""
    <div class="agent-row">
        <div class="agent-icon-box">\U0001F48A</div>
        <div>
            <div class="agent-name">Prescription Reader</div>
            <div class="agent-te">Understand your prescription - upload or type</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    uploaded_image = st.file_uploader(
        "\U0001F4F7 Upload prescription image",
        type=["jpg", "jpeg", "png"]
    )
    if uploaded_image:
        col_img, _ = st.columns([1, 2])
        with col_img:
            st.image(uploaded_image, caption="Uploaded prescription", use_container_width=True)

    text_input = st.text_area(
        "\u270D\uFE0F Or type medicine names",
        height=150,
        placeholder="e.g. Tab Paracetamol 500mg twice daily after food"
    )

    col_btn, _ = st.columns([1.2, 3])
    with col_btn:
        submit_rx = st.button("\U0001F50D Explain prescription", type="primary", key="rx_btn")

    if submit_rx:
        if not text_input.strip() and not uploaded_image:
            st.warning("Please enter prescription text or upload an image.")
        else:
            with st.spinner("Reading your prescription..."):
                result = orch.route(
                    "prescription",
                    query=text_input if text_input.strip() else None,
                    image_file=uploaded_image,
                    language=lang_code
                )
            st.markdown(f'''<div class="resp-card"><div class="resp-header"><span class="resp-dot"></span> AI Response</div>{result}</div>''', unsafe_allow_html=True)

            if text_input.strip():
                schedule = generate_dosage_schedule(text_input)
                st.markdown(f'''<div class="sched-card"><div class="sched-header">Dosage schedule</div>{schedule}</div>''', unsafe_allow_html=True)

            fc1, fc2, _ = st.columns([0.6, 0.8, 4])
            with fc1: st.button("\U0001F44D Helpful", key="rx_up")
            with fc2: st.button("\U0001F44E Not helpful", key="rx_down")

with tab2:
    st.markdown("""
    <div class="agent-row">
        <div class="agent-icon-box">\U0001FA7A</div>
        <div>
            <div class="agent-name">Symptom Checker</div>
            <div class="agent-te">Describe how you are feeling</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    symptoms = st.text_area(
        "Describe your symptoms",
        height=160,
        placeholder="e.g. I have fever and headache for 2 days"
    )

    st.markdown("""
    <div class="notice-banner">
        This is for information only. Always consult a qualified doctor.
    </div>
    """, unsafe_allow_html=True)

    st.write("")
    col_btn2, _ = st.columns([1.2, 3])
    with col_btn2:
        submit_sym = st.button("\U0001F50D Check symptoms", type="primary", key="sym_btn")

    if submit_sym:
        if not symptoms.strip():
            st.warning("Please describe your symptoms.")
        else:
            with st.spinner("Searching medical information..."):
                result = orch.route("symptoms", query=symptoms, language=lang_code)
            st.markdown(f'''<div class="resp-card"><div class="resp-header"><span class="resp-dot"></span> AI Response</div>{result}</div>''', unsafe_allow_html=True)
            fc1, fc2, _ = st.columns([0.6, 0.8, 4])
            with fc1: st.button("\U0001F44D Helpful", key="sym_up")
            with fc2: st.button("\U0001F44E Not helpful", key="sym_down")

with tab3:
    st.markdown("""
    <div class="agent-row">
        <div class="agent-icon-box">\U0001F3DB\uFE0F</div>
        <div>
            <div class="agent-name">Health Scheme Eligibility</div>
            <div class="agent-te">Check Aarogyasri, PM-JAY, NHM eligibility</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)
    with col1:
        district = st.selectbox("District", [
            "Adilabad", "Bhadradri Kothagudem", "Hanumakonda", "Hyderabad",
            "Jagtial", "Jangaon", "Jayashankar Bhupalpally", "Jogulamba Gadwal",
            "Kamareddy", "Karimnagar", "Khammam", "Komaram Bheem",
            "Mahabubabad", "Mahabubnagar", "Mancherial", "Medak",
            "Medchal Malkajgiri", "Mulugu", "Nagarkurnool", "Nalgonda",
            "Narayanpet", "Nirmal", "Nizamabad", "Peddapalli",
            "Rajanna Sircilla", "Ranga Reddy", "Sangareddy", "Siddipet",
            "Suryapet", "Vikarabad", "Wanaparthy", "Warangal",
            "Yadadri Bhuvanagiri",
            "Alluri Sitharama Raju", "Anakapalli", "Anantapur", "Annamayya",
            "Bapatla", "Chittoor", "East Godavari", "Eluru",
            "Guntur", "Kakinada", "Konaseema", "Krishna",
            "Kurnool", "Nandyal", "NTR", "Palnadu",
            "Parvathipuram Manyam", "Prakasam", "Sri Potti Sriramulu Nellore",
            "Sri Sathya Sai", "Srikakulam", "Tirupati", "Visakhapatnam",
            "Vizianagaram", "West Godavari", "YSR Kadapa"
        ])
        income = st.number_input("Annual income (Rs)", value=0, step=10000, min_value=0)
    with col2:
        age = st.number_input("Age", value=30, min_value=0, max_value=120)
        family_size = st.number_input("Family size", value=4, min_value=1)
    with col3:
        category = st.selectbox("Category", ["SC", "ST", "BC", "General"])
        ration = st.selectbox("Ration card", ["None", "White", "Pink (BPL)", "Yellow (AAY)"])

    st.write("")
    col_btn3, _ = st.columns([1.5, 3])
    with col_btn3:
        submit_sch = st.button("\U0001F50D Check eligibility", type="primary", key="sch_btn")

    if submit_sch:
        with st.spinner("Checking scheme eligibility..."):
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
        st.markdown(f'''<div class="resp-card"><div class="resp-header"><span class="resp-dot"></span> Eligible Schemes</div>{result}</div>''', unsafe_allow_html=True)

        facilities = get_facilities(district)
        facility_lines = "<br>".join([f"\U0001F4CD {f}" for f in facilities])
        st.markdown(f'''<div class="facility-card"><div class="facility-header">Nearby facilities</div>{facility_lines}</div>''', unsafe_allow_html=True)

        fc1, fc2, _ = st.columns([0.6, 0.8, 4])
        with fc1: st.button("\U0001F44D Helpful", key="sch_up")
        with fc2: st.button("\U0001F44E Not helpful", key="sch_down")

st.markdown("""
<div class="helpline-bar">
    <div class="helpline-item"><div class="helpline-num">104</div><div class="helpline-lbl">Aarogyasri / NHM</div></div>
    <div class="helpline-item"><div class="helpline-num">108</div><div class="helpline-lbl">Emergency Ambulance</div></div>
    <div class="helpline-item"><div class="helpline-num">102</div><div class="helpline-lbl">Pregnancy &amp; Mother-Child</div></div>
    <div class="helpline-item"><div class="helpline-num">14555</div><div class="helpline-lbl">PM-JAY Helpline</div></div>
</div>
""", unsafe_allow_html=True)

st.markdown("---")
st.markdown("""
<div class="ma-footer" style="text-align:center;padding:0.5rem 0 1rem;font-size:14px;line-height:1.8;">
    \U0001F3E5 <b>MediAssist</b>
    &nbsp;-&nbsp; Built for rural healthcare access - AP &amp; Telangana<br>
    <span style="font-size:12px;">
    This tool provides information only. Always consult a qualified doctor.
    </span>
</div>
""", unsafe_allow_html=True)
