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

# -------------------------- Clean & High-Contrast Styles --------------------------
st.markdown("""
<style>
/* Ensure all text is strictly black for readability */
html, body, [class*="st-"], p, span, label, h1, h2, h3, h4, h5, h6 {
    color: #000000 !important;
}

/* Light, professional background */
.stApp {
    background-color: #f8f9fa;
}

/* Main Container Card */
.app-card {
    background: #ffffff;
    border-radius: 15px;
    padding: 30px;
    border: 1px solid #dee2e6;
    box-shadow: 0 4px 12px rgba(0,0,0,0.05);
    margin-bottom: 20px;
}

/* Section Header */
.section-chip {
    display: inline-block;
    padding: 5px 15px;
    border-radius: 20px;
    background-color: #e9ecef;
    font-weight: bold;
    font-size: 0.8rem;
    margin-bottom: 10px;
    border: 1px solid #ced4da;
}

/* Simple Question Box - High Visibility */
.qbox {
    padding: 15px;
    border-radius: 10px;
    margin-top: 20px;
    border-left: 6px solid #6c757d;
}

/* Soft Pastel Backgrounds for Questions */
.bg-gen { background-color: #e7f3ff; } /* Light Blue */
.bg-dom { background-color: #fff4e6; } /* Light Orange */

/* Small Hint/Insight Text */
.hint-text {
    font-size: 0.85rem;
    color: #495057 !important;
    margin-top: 5px;
    font-style: italic;
}

/* Contact Box */
.contact-box {
    background-color: #f1f3f5;
    padding: 20px;
    border-radius: 12px;
    border: 1px dashed #adb5bd;
    margin-top: 30px;
    text-align: center;
}
</style>
""", unsafe_allow_html=True)

# -------------------------- Session State --------------------------
if "page" not in st.session_state:
    st.session_state.page = "general"
if "general_answers" not in st.session_state:
    st.session_state.general_answers = []
if "domain" not in st.session_state:
    st.session_state.domain = "Others"
if "domain_answers" not in st.session_state:
    st.session_state.domain_answers = []

# -------------------------- PDF Engine --------------------------
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
    pdf.ln(5)
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(200, 10, txt=f"{domain} Specifics:", ln=True)
    for i, a in enumerate(dom_ans):
        pdf.multi_cell(0, 8, txt=f"Q{i+1}: {a}")
    return pdf.output(dest='S').encode('latin-1')

def get_score(answers):
    yes = sum(1 for a in answers if a == "Yes")
    maybe = sum(1 for a in answers if a in ["Maybe / Not Sure", "Not sure"])
    return round(((yes + maybe*0.5) / len(answers)) * 100, 1)

def step_bar(current):
    labels = ["General", "Review", "Domain", "Result"]
    cols = st.columns(4)
    for i, l in enumerate(labels, 1):
        if i == current: cols[i-1].markdown(f"**🔵 {l}**")
        else: cols[i-1].markdown(f"{l}")

# -------------------------- Page: General --------------------------
def page_general():
    step_bar(1)
    st.markdown('<div class="app-card">', unsafe_allow_html=True)
    st.markdown('<span class="section-chip">Step 1: Core Analysis</span>', unsafe_allow_html=True)
    st.write("### 💡 General Patent Requirements")
    
    qs = [
        "Is this a physical process, machine, or compound (not just a concept)?",
        "Has the invention remained confidential (not sold or published)?",
        "Does it solve a specific technical problem?",
        "Is there a clear real-world use for this invention?",
        "Is the solution 'non-obvious' to an expert in the field?",
        "Can you provide enough detail for someone to reproduce it?",
        "Is it more than a discovery of a natural law or math formula?"
    ]
    
    answers = []
    for i, q in enumerate(qs, 1):
        st.markdown(f'<div class="qbox bg-gen"><b>{i}. {q}</b></div>', unsafe_allow_html=True)
        ans = st.radio("Choose one:", ["Yes", "No", "Maybe / Not Sure"], key=f"g_{i}", horizontal=True)
        answers.append(ans)
    
    if st.button("Continue to Preliminary Result ➡️", use_container_width=True):
        st.session_state.general_answers = answers
        st.session_state.page = "preliminary"
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

# -------------------------- Page: Preliminary --------------------------
def page_preliminary():
    step_bar(2)
    st.markdown('<div class="app-card">', unsafe_allow_html=True)
    score = get_score(st.session_state.general_answers)
    st.write("### 📊 Preliminary Score")
    st.metric("General Requirements", f"{score}%")
    st.progress(int(score))
    
    if st.button("Next: Domain Specific Questions ➡️", use_container_width=True):
        st.session_state.page = "choose_domain"
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

# -------------------------- Page: Choose Domain --------------------------
def page_choose_domain():
    step_bar(3)
    st.markdown('<div class="app-card">', unsafe_allow_html=True)
    st.write("### 🌐 Select Field")
    dom = st.selectbox("Which field does your invention belong to?", ["Computer Science", "Mechanical", "Biology", "Chemistry", "Others"])
    if st.button("Proceed to Quiz ➡️", use_container_width=True):
        st.session_state.domain = dom
        st.session_state.page = "domain_qs"
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

# -------------------------- Page: Domain Questions --------------------------
DOMAIN_DATA = {
    "Computer Science": [("Does it improve system speed or security?", "Technical effect."), ("Is it more than just business logic?", "Subject matter.")],
    "Mechanical": [("Is it a new functional arrangement?", "Novelty."), ("Does it solve a physical energy problem?", "Utility.")],
    "Biology": [("Is it modified from nature?", "Eligibility."), ("Is the process reproducible?", "Enablement.")],
    "Chemistry": [("Does it show a new chemical property?", "Novelty."), ("Is there lab data available?", "Evidence.")],
    "Others": [("Is it a new tool or method?", "Novelty."), ("Is it useful in industry?", "Utility.")]
}

def page_domain_qs():
    step_bar(3)
    st.markdown('<div class="app-card">', unsafe_allow_html=True)
    st.markdown(f"### ✍️ {st.session_state.domain} Assessment")
    
    qs = DOMAIN_DATA.get(st.session_state.domain, DOMAIN_DATA["Others"])
    answers = []
    for i, (q, hint) in enumerate(qs, 1):
        st.markdown(f'<div class="qbox bg-dom"><b>{i}. {q}</b></div>', unsafe_allow_html=True)
        st.markdown(f'<p class="hint-text">Why this matters: {hint}</p>', unsafe_allow_html=True)
        ans = st.radio("Choose one:", ["Yes", "No", "Not sure"], key=f"d_{i}", horizontal=True)
        answers.append(ans)
        
    if st.button("Show Final Result ✅", use_container_width=True):
        st.session_state.domain_answers = answers
        st.session_state.page = "result"
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

# -------------------------- Page: Result --------------------------
def page_result():
    step_bar(4)
    st.markdown('<div class="app-card">', unsafe_allow_html=True)
    st.balloons()
    
    gen_score = get_score(st.session_state.general_answers)
    dom_score = get_score(st.session_state.domain_answers)
    final_score = round((gen_score * 0.6) + (dom_score * 0.4), 1)
    
    st.markdown("## 🎉 Congratulations!")
    st.write("You have successfully completed the assessment.")
    
    st.divider()
    col1, col2, col3 = st.columns(3)
    col1.metric("Basic Score", f"{gen_score}%")
    col2.metric("Domain Score", f"{dom_score}%")
    col3.metric("Total Match", f"{final_score}%")
    st.progress(int(final_score))
    
    st.divider()
    pdf_bytes = create_pdf(final_score, st.session_state.domain, st.session_state.general_answers, st.session_state.domain_answers)
    st.download_button("📥 Download PDF Report", data=pdf_bytes, file_name="Patent_Report.pdf", mime="application/pdf", use_container_width=True)
    
    # Simple Contact Section
    st.markdown(f"""
    <div class="contact-box">
        <h4>🤔 Still not sure?</h4>
        <p>If you have queries regarding your <b>{final_score}%</b> match or need expert advice, we are here to help.</p>
        <a href="mailto:contact@yourfirm.com" style="text-decoration:none;">
            <div style="background-color:#000; color:#fff; padding:10px; border-radius:5px; font-weight:bold;">
                Get in Touch with an Expert
            </div>
        </a>
    </div>
    """, unsafe_allow_html=True)
    
    if st.button("🔁 Start New Assessment", use_container_width=True):
        for k in list(st.session_state.keys()): del st.session_state[k]
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

# Router
if st.session_state.page == "general": page_general()
elif st.session_state.page == "preliminary": page_preliminary()
elif st.session_state.page == "choose_domain": page_choose_domain()
elif st.session_state.page == "domain_qs": page_domain_qs()
elif st.session_state.page == "result": page_result()
