import streamlit as st
from fpdf import FPDF
import io

# -------------------------- App Setup --------------------------
st.set_page_config(
    page_title="Patent Checker",
    layout="centered"
)

# -------------------------- The "Pure Simple" CSS --------------------------
st.markdown("""
<style>
/* 1. Reset everything to White Background & Black Text */
.stApp, div[data-testid="stAppViewContainer"] {
    background-color: #ffffff !important;
}

html, body, [class*="st-"], p, span, label, h1, h2, h3, h4, h5, h6 {
    color: #000000 !important;
}

/* 2. Style Inputs: White box with thin black border */
div[data-baseweb="select"] > div, div[data-baseweb="input"] > div {
    background-color: #ffffff !important;
    border: 1px solid #cccccc !important;
    color: #000000 !important;
}

/* 3. Style Buttons: Light grey with black text (Standard look) */
div.stButton > button {
    background-color: #f0f0f0 !important;
    color: #000000 !important;
    border: 1px solid #999999 !important;
    border-radius: 4px !important;
    width: 100%;
}

/* 4. Simple Question Container */
.question-block {
    margin-bottom: 25px;
    padding: 10px;
    border-bottom: 1px solid #eeeeee;
}
</style>
""", unsafe_allow_html=True)

# -------------------------- Session State --------------------------
if "page" not in st.session_state:
    st.session_state.page = "general"
if "general_answers" not in st.session_state:
    st.session_state.general_answers = []

# -------------------------- Functions --------------------------
def create_pdf(score, domain):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(200, 10, txt="Patent Assessment Report", ln=True, align='C')
    pdf.ln(10)
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt=f"Final Assessment Score: {score}%", ln=True)
    pdf.cell(200, 10, txt=f"Domain: {domain}", ln=True)
    return pdf.output(dest='S').encode('latin-1')

# -------------------------- Navigation --------------------------
if st.session_state.page == "general":
    st.title("💡 Step 1: General Requirements")
    
    qs = [
        "1. Is this a physical process, machine, or compound?",
        "2. Has the invention remained confidential (not sold yet)?",
        "3. Does it solve a specific technical problem?"
    ]
    
    temp_answers = []
    for q in qs:
        st.markdown(f"**{q}**")
        ans = st.radio("Choose:", ["Yes", "No", "Maybe"], key=q, horizontal=True)
        temp_answers.append(ans)
    
    if st.button("Proceed to Field Selection"):
        st.session_state.general_answers = temp_answers
        st.session_state.page = "domain"
        st.rerun()

elif st.session_state.page == "domain":
    st.title("🌐 Step 2: Select Field")
    
    field = st.selectbox(
        "Which field does your invention belong to?",
        ["Computer Science", "Mechanical", "Biology", "Chemistry", "Others"]
    )
    
    if st.button("See Final Result"):
        st.session_state.field = field
        st.session_state.page = "result"
        st.rerun()

elif st.session_state.page == "result":
    st.title("🎯 Final Assessment")
    
    # Simple score calculation based on "Yes" counts
    yes_count = st.session_state.general_answers.count("Yes")
    score = int((yes_count / 3) * 100)
    
    st.success(f"🎉 Congratulations! Your assessment is complete.")
    st.write(f"**Field:** {st.session_state.field}")
    st.write(f"**Assessment Score:** {score}%")
    
    pdf_data = create_pdf(score, st.session_state.field)
    st.download_button(
        label="Download Result as PDF",
        data=pdf_data,
        file_name="Patent_Assessment.pdf",
        mime="application/pdf"
    )
    
    st.divider()
    st.write("### 📬 Contact Us")
    st.write("Still not sure? Feel free to contact our expert team for more personalized guidance.")
    
    if st.button("Restart Assessment"):
        st.session_state.page = "general"
        st.rerun()
