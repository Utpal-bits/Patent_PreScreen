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

# -------------------------- Styles --------------------------
st.markdown("""
<style>
html, body, [class*="st-"], p, span, label, h1, h2, h3, h4, h5, h6 {
    color: black !important;
}
body, .stApp {
  background: linear-gradient(120deg, #fdfbfb, #ebedee);
  background-size: 400% 400%;
  animation: gradientShift 18s ease infinite;
}
@keyframes gradientShift {
  0% {background-position: 0% 50%;}
  50% {background-position: 100% 50%;}
  100% {background-position: 0% 50%;}
}
.app-card {
  background: rgba(255,255,255,0.85);
  backdrop-filter: blur(6px);
  border-radius: 22px;
  padding: 26px 22px;
  border: 1px solid rgba(0,0,0,0.05);
  box-shadow: 0 10px 30px rgba(0,0,0,0.07);
}
.section-chip {
  display:inline-block;
  padding:8px 14px;
  border-radius:999px;
  font-weight:700;
  font-size:0.9rem;
  color:black;
  background:linear-gradient(135deg,#d5f4ff,#f3e8ff);
  border:1px solid rgba(0,0,0,0.06);
}
.qcard {
  border-radius: 15px;
  padding: 20px;
  margin-bottom: 16px;
  font-size: 1.15rem;
  font-weight: 600;
  color: black !important;
  border: 1px solid rgba(0,0,0,0.06);
  box-shadow: 0 6px 18px rgba(0,0,0,0.05);
}
.q1 { background-color: #FFD1C1; } 
.q2 { background-color: #D1C4FF; } 
.q3 { background-color: #B2F0E9; } 
.q4 { background-color: #FFE0B2; } 
.q5 { background-color: #E6CCFF; } 
.q6 { background-color: #C1E1C1; } 
.q7 { background-color: #FFCCE5; }

.insight {
  background:#f0f9ff;
  border:1px solid #bae6fd;
  color:#0c4a6e;
  padding:10px 12px;
  border-radius:12px;
  font-size:0.95rem;
  margin:6px 0;
}
div[role="radiogroup"] label {
  color: #000 !important;
}
</style>
""", unsafe_allow_html=True)

# -------------------------- Session State --------------------------
if "page" not in st.session_state:
    st.session_state.page = "general"
if "general_answers" not in st.session_state:
    st.session_state.general_answers = []
if "domain" not in st.session_state:
    st.session_state.domain = None
if "domain_answers" not in st.session_state:
    st.session_state.domain_answers = []

# -------------------------- PDF Generation Logic --------------------------
def create_pdf(score, domain, gen_answers, dom_answers):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(200, 10, txt="Patent Eligibility Report", ln=True, align='C')
    
    pdf.set_font("Arial", size=12)
    pdf.ln(10)
    pdf.cell(200, 10, txt=f"Overall Probability Score: {score}%", ln=True)
    pdf.cell(200, 10, txt=f"Selected Domain: {domain}", ln=True)
    
    pdf.ln(5)
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(200, 10, txt="Section 1: General Criteria", ln=True)
    pdf.set_font("Arial", size=10)
    for i, ans in enumerate(gen_answers):
        pdf.multi_cell(0, 8, txt=f"Q{i+1}: {ans}")

    pdf.ln(5)
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(200, 10, txt=f"Section 2: {domain} Specifics", ln=True)
    pdf.set_font("Arial", size=10)
    for i, ans in enumerate(dom_answers):
        pdf.multi_cell(0, 8, txt=f"Q{i+1}: {ans}")
        
    return pdf.output(dest='S').encode('latin-1')

# -------------------------- Helpers --------------------------
def score_block(answers, yes="Yes", neutral=("Maybe / Not Sure", "Not sure")):
    yes_count = sum(1 for a in answers if a == yes)
    neutral_count = sum(1 for a in answers if a in neutral)
    total = len(answers)
    raw = yes_count + 0.5 * neutral_count
    pct = round(raw / total * 100, 1) if total else 0.0
    return pct

def step_progress(current_step:int):
    steps = ["General", "Preliminary", "Domain", "Final Result"]
    cols = st.columns(len(steps))
    for i, label in enumerate(steps, start=1):
        with cols[i-1]:
            if i < current_step: st.markdown(f"✅ **{label}**")
            elif i == current_step: st.markdown(f"🟣 **{label}**")
            else: st.markdown(f"▫️ {label}")

# -------------------------- Pages --------------------------
def page_general():
    step_progress(1)
    st.markdown('<div class="app-card">', unsafe_allow_html=True)
    st.markdown('<span class="section-chip">Step 1 · Core Requirements</span>', unsafe_allow_html=True)
    st.markdown("## 💡 Patent Eligibility — General Criteria")
    
    # REFINED QUESTIONS
    questions = [
        "Is your invention a process, machine, manufacture, or composition of matter (not just a pure idea)?",
        "Have you confirmed that your invention has not been publicly disclosed or sold before today?",
        "Does your invention provide a 'technical solution' to a 'technical problem'?",
        "Does the invention produce a specific, substantial, and credible real-world benefit?",
        "Is your solution 'non-obvious' to someone with average skill in your specific field?",
        "Can the invention be described in enough detail that someone else could actually build it?",
        "Does your invention avoid being a 'mere discovery' of a natural law or mathematical formula?"
    ]
    options = ["Yes", "No", "Maybe / Not Sure"]
    
    answers = []
    for i, q in enumerate(questions, start=1):
        st.markdown(f'<div class="qcard q{i}">{q}</div>', unsafe_allow_html=True)
        ans = st.radio("Selection:", options, key=f"gen_{i}", horizontal=True)
        answers.append(ans)

    if st.button("➡️ See Preliminary Result"):
        st.session_state.general_answers = answers
        st.session_state.page = "preliminary_result"
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

def page_preliminary_result():
    step_progress(2)
    st.markdown('<div class="app-card">', unsafe_allow_html=True)
    gen_pct = score_block(st.session_state.general_answers)
    st.metric("General Eligibility Score", f"{gen_pct}%")
    st.progress(int(gen_pct))
    
    if gen_pct >= 70:
        st.success("The fundamental legal requirements for a patent look solid.")
    else:
        st.warning("Your idea may face challenges regarding basic patentability (Novelty/Subject Matter).")
        
    if st.button("🔬 Refine with Domain Questions ➡️"):
        st.session_state.page = "choose_domain"
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

def page_domain_choice():
    step_progress(3)
    st.markdown('<div class="app-card">', unsafe_allow_html=True)
    domain = st.radio("Select Invention Category:", ["Biology", "Chemistry", "Mechanical", "Computer Science", "Others"])
    if st.button("Next ➡️"):
        st.session_state.domain = domain
        st.session_state.page = "domain_questions"
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

# (Note: I've truncated the DOMAIN_QS and domain_specific_flags for brevity, keep your existing logic there)
DOMAIN_QS = {
    "Biology": [("Is it modified from its natural state?", "Natural items aren't patentable."), ("Is it reproducible?", "Consistency is key."), ("Does it have industrial use?", "Utility is required."), ("Is there test data?", "Evidence matters."), ("Is it a new strain?", "Novelty.")],
    "Chemistry": [("Is the compound new?", "Novelty."), ("Better properties?", "Improvement."), ("Industrial use?", "Utility."), ("Can it be synthesized?", "Enablement."), ("Is it stable?", "Practicality.")],
    "Mechanical": [("New function?", "Improvement."), ("Not just a combo?", "Synergy."), ("Non-obvious?", "Inventive step."), ("Industrial use?", "Utility."), ("Do you have a CAD/model?", "Enablement.")],
    "Computer Science": [("Technical problem solved?", "Not just business logic."), ("New algorithm?", "Novelty."), ("Hardware improvement?", "Technical effect."), ("Practical application?", "Utility."), ("Avoids abstract math?", "Subject matter.")],
    "Others": [("Is it new?", "Novelty."), ("Is it useful?", "Utility."), ("Is it non-obvious?", "Inventive step."), ("Reproducible?", "Enablement."), ("Technical advantage?", "Requirement.")]
}

def page_domain_questions():
    step_progress(3)
    st.markdown('<div class="app-card">', unsafe_allow_html=True)
    st.markdown(f"## ✍️ {st.session_state.domain} Specifics")
    qs = DOMAIN_QS[st.session_state.domain]
    answers = []
    for idx, (q, hint) in enumerate(qs, start=1):
        st.markdown(f'<div class="qcard q{(idx % 7) or 7}">{q}</div>', unsafe_allow_html=True)
        ans = st.radio("Select:", ["Yes", "No", "Not sure"], key=f"dom_{idx}", horizontal=True)
        answers.append(ans)
    
    if st.button("Show Final Result ✅"):
        st.session_state.domain_answers = answers
        st.session_state.page = "result"
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

def page_result():
    step_progress(4)
    st.markdown('<div class="app-card">', unsafe_allow_html=True)
    gen_pct = score_block(st.session_state.general_answers)
    dom_pct = score_block(st.session_state.domain_answers)
    final_score = round(gen_pct*0.6 + dom_pct*0.4, 1)

    st.markdown("## 🎯 Final Patentability Snapshot")
    st.metric("Overall Probability", f"{final_score}%")
    
    # PDF Generation Section
    st.divider()
    st.markdown("### 📄 Export Results")
    pdf_data = create_pdf(final_score, st.session_state.domain, st.session_state.general_answers, st.session_state.domain_answers)
    st.download_button(
        label="Download Result as PDF",
        data=pdf_data,
        file_name="Patent_Report.pdf",
        mime="application/pdf"
    )
    
    if st.button("🔁 Restart"):
        for k in list(st.session_state.keys()): del st.session_state[k]
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

# Router
if st.session_state.page == "general": page_general()
elif st.session_state.page == "preliminary_result": page_preliminary_result()
elif st.session_state.page == "choose_domain": page_domain_choice()
elif st.session_state.page == "domain_questions": page_domain_questions()
elif st.session_state.page == "result": page_result()
