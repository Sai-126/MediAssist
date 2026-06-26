import streamlit as st
import sys
sys.path.append(".")
from agents.orchestrator import Orchestrator

st.set_page_config(
    page_title="MediAssist",
    layout="centered",
    initial_sidebar_state="collapsed"
)

@st.cache_resource
def load_orchestrator():
    return Orchestrator()

orch = load_orchestrator()

col1, col2 = st.columns([3, 1])
with col1:
    st.title("MediAssist")
    st.caption("Rural health assistant - Telugu and English")
with col2:
    language = st.radio("", ["English", "Telugu"], key="lang")

lang_code = "telugu" if language == "Telugu" else "english"

st.divider()

tab1, tab2, tab3 = st.tabs([
    "Prescription",
    "Symptoms",
    "Health Schemes"
])

with tab1:
    st.subheader("Understand your prescription")
    text_input = st.text_area(
        "Type medicine names and instructions",
        height=120,
        placeholder="e.g. Tab Paracetamol 500mg twice daily after food"
    )
    if st.button("Explain", type="primary", key="btn1"):
        if not text_input.strip():
            st.warning("Please enter prescription text.")
        else:
            with st.spinner("Reading prescription..."):
                result = orch.route("prescription", query=text_input, language=lang_code)
            st.markdown(result)

with tab2:
    st.subheader("Describe your symptoms")
    symptoms = st.text_area(
        "How are you feeling?",
        height=120,
        placeholder="e.g. I have fever and headache for 2 days"
    )
    st.caption("For information only. Always consult a doctor.")
    if st.button("Get information", type="primary", key="btn2"):
        if not symptoms.strip():
            st.warning("Please describe your symptoms.")
        else:
            with st.spinner("Searching medical information..."):
                result = orch.route("symptoms", query=symptoms, language=lang_code)
            st.markdown(result)

with tab3:
    st.subheader("Check health scheme eligibility")
    col1, col2 = st.columns(2)
    with col1:
        district = st.selectbox("District", [
            "Hyderabad", "Warangal", "Karimnagar", "Nizamabad",
            "Khammam", "Vijayawada", "Visakhapatnam", "Guntur",
            "Tirupati", "Kurnool", "Nellore", "Rajahmundry"
        ])
        income = st.number_input("Annual income (Rs)", value=0, step=10000)
    with col2:
        age = st.number_input("Age", value=30, min_value=0, max_value=120)
        family_size = st.number_input("Family size", value=4, min_value=1)
    category = st.selectbox("Category", ["SC", "ST", "BC", "General"])

    if st.button("Check eligibility", type="primary", key="btn3"):
        with st.spinner("Checking schemes..."):
            result = orch.route(
                "scheme",
                profile={
                    "district": district,
                    "income": income,
                    "age": age,
                    "family_size": family_size,
                    "category": category
                },
                language=lang_code
            )
        st.markdown(result)