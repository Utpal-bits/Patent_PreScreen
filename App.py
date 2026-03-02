import time
import streamlit as st
from fpdf import FPDF
import io

# -------------------------- App Setup --------------------------
st.set_page_config(
    page_title="Patent Eligibility Checker",
    page_icon="💡",
    layout="centered"
)

# -------------------------- High-Visibility CSS --------------------------
st.markdown("""
<style>
/* 1. Force Black Text Everywhere */
html, body, [class*="st-"], p, span, label, h1, h2, h3, h4, h5, h6 {
    color: #000000 !important;
}

/* 2. Fix the Selectbox/Dropdown visibility */
div[data-baseweb="select"] > div {
    background-color: #ffffff !important;
    border: 1px solid #000000 !important;
}

/* 3. Fix the Button visibility */
button[kind="primary"], button[kind="secondary"], div.stButton > button {
    background-color: #ffffff !important;
    color: #000000 !important;
    border: 2px solid #000000 !important;
    font-weight: bold !important;
}

/* 4. Fix Radio Button Labels */
div[role="radiogroup"] label {
    color: #000000 !important;
    font-weight: 500;
}

/* 5. Clean White Backgrounds for Question Boxes */
.qbox {
    padding: 15px;
    border-radius: 8px;
    margin-top: 15px;
    border: 1px solid #ced4da;
}
.bg-gen { background-color: #f0f7ff; }
.bg-dom { background-color: #fff9db; }

.app-card {
    background: #ffffff;
    border: 1px solid #dee2e6;
    padding: 25px;
    border-radius: 10px;
}
</style>
""", unsafe_allow_html=True)

# -------------------------- Session State --------------------------
if "page" not in st.session_state:
    st.session_state.page = "general"
if "general_answers" not in st.session_state:
    st.session_state.general_answers = []
if "domain" not in st.session_state:
    st.session_state.domain = "Computer Science"
if "domain_answers" not in st.session_state:
    st.session_state.domain_answers = []

# -------------------------- Helpers --------------------------
def create_pdf(score, domain, gen_ans, dom_ans):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(200, 10, txt="Patent Eligibility Report", ln=True, align='C')
    pdf.ln(10)
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt=f"Final Score: {score}%", ln=True)
    pdf.cell(200, 10, txt=f"Category: {domain}", ln=True)
    pdf.ln(10)
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(200, 10, txt="General Requirements:", ln=True)
    pdf.set_font("Arial", size=10)
    for i, a in enumerate(gen_ans):
        pdf.multi_cell(0, 8, txt=f"Q{i+1}: {a}")
    return pdf.output(dest='S').encode('latin-1')

def get_score(answers):
    yes = sum(1 for a in answers if a == "Yes")
    maybe = sum(1 for a in answers if a in ["Maybe / Not Sure", "Not sure"])
    return round(((yes + maybe*0.5) / len(answers)) * 100, 1)

# -------------------------- Pages --------------------------
def page_general():
    st.markdown('<div class="app-card">', unsafe_allow_html=True)
    st.write("### 💡 Step 1: General Requirements")
    qs = [
        "Is this a physical process, machine, or compound?",
        "Has the invention remained confidential (not sold yet)?",
        "Does it solve a specific technical problem?",
        "Is there a clear real-world use?",
        "Is it 'non-obvious' to an expert?",
        "Can you provide enough detail for reproduction?",
        "Is it more than just a discovery of a natural law?"
    ]
    answers = []
    for i, q in enumerate(qs, 1):
        st.markdown(f'<div class="qbox bg-gen"><b>{i}. {q}</b></div>', unsafe_allow_html=True)
        ans = st.radio("Choose:", ["Yes", "No", "Maybe / Not Sure"], key=f"g_{i}", horizontal=True)
        answers.append(ans)
    
    if st.button("Proceed to Review ➡️", use_container_width=True):
        st.session_state.general_answers = answers
        st.session_state.page = "preliminary"
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

def page_preliminary():
    st.markdown('<div class="app-card">', unsafe_allow_html=True)
    score = get_score(st.session_state.general_answers)
    st.write("### 📊 Preliminary Score")
    st.metric("General Requirements", f"{score}%")
    if st.button("Next: Choose Domain ➡️", use_container_width=True):
        st.session_state.page = "choose_domain"
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

def page_choose_domain():
    st.markdown('<div class="app-card">', unsafe_allow_html=True)
    st.write("### 🌐 Select Your Field")
    dom = st.selectbox("Which field does your invention belong to?", ["Computer Science", "Mechanical", "Biology", "Chemistry", "Others"])
    if st.button("Proceed to Quiz ➡️", use_container_width=True):
        st.session_state.domain = dom
        st.session_state.page = "domain_qs"
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

def page_domain_qs():
    st.markdown('<div class="app-card">', unsafe_allow_html=True)
    st.write(f"### ✍️ {st.session_state.domain} Questions")
    # Using simplified fallback domain questions
    answers = []
    for i in range(1, 3):
        st.markdown(f'<div class="qbox bg-dom"><b>Domain Question {i}</b></div>', unsafe_allow_html=True)
        ans = st.radio("Select:", ["Yes", "No", "Not sure"], key=f"d_{i}", horizontal=True)
        answers.append(ans)
    if st.button("Get Final Result ✅", use_container_width=True):
        st.session_state.domain_answers = answers
        st.session_state.page = "result"
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

def page_result():
    st.markdown('<div class="app-card">', unsafe_allow_html=True)
    st.balloons()
    gs = get_score(st.session_state.general_answers)
    ds = get_score(st.session_state.domain_answers)
    final = round((gs * 0.6) + (ds * 0.4), 1)
    
    st.markdown("## 🎉 Congratulations!")
    st.metric("Final Score", f"{final}%")
    
    pdf_bytes = create_pdf(final, st.session_state.domain, st.session_state.general_answers, st.session_state.domain_answers)
    st.download_button("📥 Download PDF", data=pdf_bytes, file_name="Report.pdf", mime="application/pdf", use_container_width=True)
    
    st.markdown("""
    <div style="background-color:#f8f9fa; padding:15px; border-radius:10px; border:1px solid #000; margin-top:20px; text-align:center;">
        <b>Still not sure?</b> Feel free to contact our expert team for guidance.
    </div>
    """, unsafe_allow_html=True)
    
    if st.button("Restart Assessment", use_container_width=True):
        for k in list(st.session_state.keys()): del st.session_state[k]
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

# Router
if st.session_state.page == "general": page_general()
elif st.session_state.page == "preliminary": page_preliminary()
elif st.session_state.page == "choose_domain": page_choose_domain()
elif st.session_state.page == "domain_qs": page_domain_qs()
elif st.session_state.page == "result": page_result()
