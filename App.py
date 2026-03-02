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

# -------------------------- Custom Styles --------------------------
st.markdown("""
<style>
/* Global text color override for visibility */
html, body, [class*="st-"], p, span, label, h1, h2, h3, h4, h5, h6 {
    color: #1a1a1a !important;
}

/* Background Animation */
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

/* Container Styling */
.app-card {
  background: rgba(255,255,255,0.92);
  backdrop-filter: blur(10px);
  border-radius: 22px;
  padding: 30px;
  border: 1px solid rgba(0,0,0,0.05);
  box-shadow: 0 10px 30px rgba(0,0,0,0.1);
}

.section-chip {
  display:inline-block;
  padding:8px 16px;
  border-radius:999px;
  font-weight:700;
  font-size:0.85rem;
  background: linear-gradient(135deg, #6366f1, #a855f7);
  color: white !important;
  margin-bottom: 15px;
}

.qcard {
  border-radius: 12px;
  padding: 18px;
  margin-bottom: 12px;
  font-size: 1.1rem;
  font-weight: 600;
  border-left: 5px solid #6366f1;
  box-shadow: 0 4px 12px rgba(0,0,0,0.05);
}

/* Question Backgrounds */
.q1 { background-color: #f0f4ff; }
.q2 { background-color: #f5f3ff; }
.q3 { background-color: #fdf2f8; }
.q4 { background-color: #fffbeb; }
.q5 { background-color: #f0fdf4; }
.q6 { background-color: #eff6ff; }
.q7 { background-color: #fef2f2; }

.insight {
  background: #f8fafc;
  border: 1px solid #e2e8f0;
  padding: 8px 12px;
  border-radius: 8px;
  font-size: 0.9rem;
  font-style: italic;
  margin-bottom: 20px;
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

# -------------------------- PDF Logic --------------------------
def create_pdf(score, domain, gen_ans, dom_ans):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(200, 10, txt="Patent Eligibility Assessment Report", ln=True, align='C')
    pdf.ln(10)
    
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(200, 10, txt=f"Overall Result: {score}% Probability", ln=True)
    pdf.cell(200, 10, txt=f"Invention Domain: {domain}", ln=True)
    pdf.ln(10)
    
    pdf.set_font("Arial", 'B', 11)
    pdf.cell(200, 10, txt="General Criteria Assessment:", ln=True)
    pdf.set_font("Arial", size=10)
    for i, a in enumerate(gen_ans):
        pdf.multi_cell(0, 8, txt=f"Requirement {i+1}: {a}")
    
    pdf.ln(5)
    pdf.set_font("Arial", 'B', 11)
    pdf.cell(200, 10, txt=f"{domain} Specific Assessment:", ln=True)
    pdf.set_font("Arial", size=10)
    for i, a in enumerate(dom_ans):
        pdf.multi_cell(0, 8, txt=f"Domain Check {i+1}: {a}")
        
    return pdf.output(dest='S').encode('latin-1')

# -------------------------- Scoring Helper --------------------------
def get_score_pct(answers):
    yes_count = sum(1 for a in answers if a == "Yes")
    maybe_count = sum(1 for a in answers if a in ["Maybe / Not Sure", "Not sure"])
    total = len(answers)
    raw = yes_count + (maybe_count * 0.5)
    return round((raw / total) * 100, 1) if total > 0 else 0

def step_progress(current):
    steps = ["General", "Prelim", "Domain", "Result"]
    cols = st.columns(4)
    for i, label in enumerate(steps, 1):
        if i < current: cols[i-1].markdown(f"✅ **{label}**")
        elif i == current: cols[i-1].markdown(f"🟣 **{label}**")
        else: cols[i-1].markdown(f"▫️ {label}")

# -------------------------- Page Functions --------------------------

def page_general():
    step_progress(1)
    st.markdown('<div class="app-card">', unsafe_allow_html=True)
    st.markdown('<span class="section-chip">Step 1: Core Requirements</span>', unsafe_allow_html=True)
    st.markdown("## 💡 Essential Patent Criteria")
    
    qs = [
        "Is this a process, machine, or composition of matter (not just a concept)?",
        "Has this invention stayed private (no public sales or posts yet)?",
        "Does your invention solve a specific technical problem?",
        "Is there a clear, real-world practical use for this invention?",
        "Would a professional in your field find this solution 'non-obvious'?",
        "Can you explain it clearly enough for someone else to build it?",
        "Is this more than just a discovery of a natural law or math formula?"
    ]
    
    answers = []
    for i, q in enumerate(qs, 1):
        st.markdown(f'<div class="qcard q{i}">{q}</div>', unsafe_allow_html=True)
        ans = st.radio("Your Answer:", ["Yes", "No", "Maybe / Not Sure"], key=f"g_{i}", horizontal=True)
        answers.append(ans)
    
    if st.button("Calculate Preliminary Score ➡️", use_container_width=True):
        st.session_state.general_answers = answers
        st.session_state.page = "preliminary"
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

def page_preliminary():
    step_progress(2)
    st.markdown('<div class="app-card">', unsafe_allow_html=True)
    score = get_score_pct(st.session_state.general_answers)
    st.metric("General Eligibility Score", f"{score}%")
    st.progress(int(score))
    
    if score >= 70:
        st.success("Strong Foundation! Your idea meets the core legal definitions of a patentable invention.")
    else:
        st.warning("Potential Hurdles: Some core requirements (like novelty or technical character) need more focus.")
        
    if st.button("Move to Domain Specific Questions ➡️", use_container_width=True):
        st.session_state.page = "choose_domain"
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

def page_choose_domain():
    step_progress(3)
    st.markdown('<div class="app-card">', unsafe_allow_html=True)
    st.markdown("## 🌐 Select your Invention Category")
    dom = st.selectbox("Which field best describes your work?", ["Computer Science", "Mechanical", "Biology", "Chemistry", "Others"])
    if st.button("Start Domain Quiz ➡️", use_container_width=True):
        st.session_state.domain = dom
        st.session_state.page = "domain_qs"
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

DOMAIN_DATA = {
    "Computer Science": [("Does it improve system speed/security?", "Technical effect."), ("Is it more than just business logic?", "Subject matter.")],
    "Mechanical": [("Is it a new functional arrangement?", "Novelty."), ("Does it solve a physical friction/energy problem?", "Utility.")],
    "Biology": [("Is it modified from nature?", "Eligibility."), ("Is the process reproducible?", "Enablement.")],
    "Chemistry": [("Does it show a new chemical property?", "Novelty."), ("Is there lab data to support it?", "Evidence.")],
    "Others": [("Is it a new tool or method?", "Novelty."), ("Is it useful in industry?", "Utility.")]
}

def page_domain_qs():
    step_progress(3)
    st.markdown('<div class="app-card">', unsafe_allow_html=True)
    st.markdown(f"## ✍️ {st.session_state.domain} Specifics")
    
    qs = DOMAIN_DATA.get(st.session_state.domain, DOMAIN_DATA["Others"])
    answers = []
    for i, (q, hint) in enumerate(qs, 1):
        st.markdown(f'<div class="qcard q{i}">{q}</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="insight">Note: {hint}</div>', unsafe_allow_html=True)
        ans = st.radio("Answer:", ["Yes", "No", "Not sure"], key=f"d_{i}", horizontal=True)
        answers.append(ans)
        
    if st.button("Analyze Final Result ✅", use_container_width=True):
        st.session_state.domain_answers = answers
        st.session_state.page = "result"
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

def page_result():
    step_progress(4)
    st.markdown('<div class="app-card">', unsafe_allow_html=True)
    st.balloons()
    
    # Calculate Final Scores
    gen_score = get_score_pct(st.session_state.general_answers)
    dom_score = get_score_pct(st.session_state.domain_answers)
    final_score = round((gen_score * 0.6) + (dom_score * 0.4), 1)
    
    st.markdown("## 🎉 Congratulations on Your Assessment!")
    st.success("You've completed the evaluation. Below is your detailed patentability snapshot.")
    
    # Score Grid
    st.markdown("### 📊 Scoring Summary")
    c1, c2, c3 = st.columns(3)
    c1.metric("Basic Criteria", f"{gen_score}%")
    c2.metric(f"{st.session_state.domain}", f"{dom_score}%")
    c3.metric("Overall Match", f"{final_score}%")
    st.progress(int(final_score))
    
    # PDF Export
    st.divider()
    st.markdown("### 📄 Save Your Report")
    pdf_bytes = create_pdf(final_score, st.session_state.domain, st.session_state.general_answers, st.session_state.domain_answers)
    st.download_button(
        label="Download Full Results (PDF)",
        data=pdf_bytes,
        file_name="Patent_Assessment.pdf",
        mime="application/pdf",
        use_container_width=True
    )
    
    # Contact Section
    st.markdown("---")
    st.markdown("""
    <div style="background-color: #f0f7ff; padding: 20px; border-radius: 15px; border: 1px solid #cfe2ff;">
        <h4 style="margin-top:0;">🤔 Still Not Sure?</h4>
        <p>Patent eligibility can be nuanced. If your score wasn't what you expected, or if you need professional guidance to file your application, feel free to reach out.</p>
        <a href="mailto:expert@example.com" style="text-decoration:none;">
            <button style="width:100%; padding:10px; background-color:#0d6efd; color:white; border:none; border-radius:8px; font-weight:bold; cursor:pointer;">
                Contact a Patent Specialist
            </button>
        </a>
    </div>
    """, unsafe_allow_html=True)
    
    if st.button("🔁 Start New Analysis", use_container_width=True):
        for k in list(st.session_state.keys()): del st.session_state[k]
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

# -------------------------- Router --------------------------
if st.session_state.page == "general": page_general()
elif st.session_state.page == "preliminary": page_preliminary()
elif st.session_state.page == "choose_domain": page_choose_domain()
elif st.session_state.page == "domain_qs": page_domain_qs()
elif st.session_state.page == "result": page_result()
