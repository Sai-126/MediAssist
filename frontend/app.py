import streamlit as st

st.set_page_config(page_title="MediAssist", layout="centered")

st.title("MediAssist")
st.caption("Health assistant for rural patients — Telugu & English")

language = st.radio("Language / ???", ["English", "Telugu"], horizontal=True)

tab1, tab2, tab3 = st.tabs(["Prescription", "Symptoms", "Health Schemes"])

with tab1:
    st.subheader("Understand your prescription")
    uploaded = st.file_uploader("Upload prescription image", type=["jpg", "jpeg", "png"])
    text_input = st.text_area("Or type the prescription text")
    if st.button("Explain"):
        st.info("Agent response will appear here (connecting in Week 3)")

with tab2:
    st.subheader("Check your symptoms")
    symptoms = st.text_area("Describe your symptoms in plain language")
    if st.button("Get information"):
        st.info("Agent response will appear here (connecting in Week 3)")

with tab3:
    st.subheader("Check scheme eligibility")
    col1, col2 = st.columns(2)
    with col1:
        district = st.selectbox("District", [
            "Hyderabad", "Warangal", "Karimnagar", "Nizamabad",
            "Vijayawada", "Visakhapatnam", "Guntur", "Tirupati"
        ])
        income = st.number_input("Annual income (Rs)", value=0, step=10000)
    with col2:
        age = st.number_input("Age", value=30, min_value=0, max_value=120)
        family_size = st.number_input("Family size", value=4, min_value=1)
    if st.button("Check eligibility"):
        st.info("Agent response will appear here (connecting in Week 3)")
