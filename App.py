import streamlit as st
from io import BytesIO
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import A4
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics

# -------------------------- App Setup --------------------------
st.set_page_config(
    page_title="Patent Eligibility Checker",
    page_icon="💡",
    layout="centered"
)

# -------------------------- Session --------------------------
if "page" not in st.session_state:
    st.session_state.page = "general"
if "general_answers" not in st.session_state:
    st.session_state.general_answers = []
if "domain_answers" not in st.session_state:
    st.session_state.domain_answers = []

# -------------------------- Scoring --------------------------
def score_block(answers):
    yes_count = sum(1 for a in answers if a == "Yes")
    neutral_count = sum(1 for a in answers if a in ["Maybe / Not Sure", "I haven’t checked yet", "Not sure"])
    total = len(answers)
    raw = yes_count + 0.5 * neutral_count
    return round((raw / total) * 100, 1) if total else 0.0

# -------------------------- PDF Generator --------------------------
def generate_patent_pdf(gen_pct, dom_pct, final_pct, general_answers, domain_answers):
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4)
    elements = []
    styles = getSampleStyleSheet()

    title_style = styles["Heading1"]
    normal_style = styles["Normal"]

    elements.append(Paragraph("Patent Eligibility Assessment Report", title_style))
    elements.append(Spacer(1, 0.4 * inch))

    elements.append(Paragraph(f"General Technical Score: {gen_pct}%", normal_style))
    elements.append(Paragraph(f"Domain-Specific Score: {dom_pct}%", normal_style))
    elements.append(Paragraph(f"Final Weighted Score: {final_pct}%", normal_style))
    elements.append(Spacer(1, 0.4 * inch))

    interpretation = ""
    if final_pct >= 75:
        interpretation = "Strong potential for patentability."
    elif final_pct >= 50:
        interpretation = "Promising but requires refinement."
    else:
        interpretation = "Currently weak for patent protection."

    elements.append(Paragraph(f"Interpretation: {interpretation}", normal_style))
    elements.append(Spacer(1, 0.5 * inch))

    elements.append(Paragraph("General Answers:", styles["Heading3"]))
    elements.append(Spacer(1, 0.2 * inch))

    for i, ans in enumerate(general_answers, 1):
        elements.append(Paragraph(f"Q{i}: {ans}", normal_style))

    elements.append(Spacer(1, 0.4 * inch))
    elements.append(Paragraph("Domain Answers (Computer Science):", styles["Heading3"]))
    elements.append(Spacer(1, 0.2 * inch))

    for i, ans in enumerate(domain_answers, 1):
        elements.append(Paragraph(f"Q{i}: {ans}", normal_style))

    doc.build(elements)
    buffer.seek(0)
    return buffer

# -------------------------- General Page --------------------------
def page_general():
    st.title("💡 Patent Eligibility — Technical Check")

    questions = [
        "Have you performed a prior art search and found no identical solution?",
        "Can you clearly describe the technical mechanism that makes your idea work?",
        "Does your invention solve a specific technical problem?",
        "Does it produce measurable technical improvement?",
        "Is the inventive step more than combining known elements?",
        "Would a skilled professional consider it non-obvious?",
        "Could someone reproduce it from your written explanation?"
    ]

    options = ["Yes", "No", "Maybe / Not Sure", "I haven’t checked yet"]

    answers = []
    for i, q in enumerate(questions):
        st.subheader(q)
        ans = st.radio("Select an option:", options, key=f"gen_{i}")
        answers.append(ans)

    if st.button("See Preliminary Result ➡️"):
        st.session_state.general_answers = answers
        st.session_state.page = "prelim"
        st.rerun()

# -------------------------- Preliminary --------------------------
def page_prelim():
    pct = score_block(st.session_state.general_answers)

    st.title("📊 Preliminary Result")
    st.metric("Score", f"{pct}%")
    st.progress(int(pct))

    if st.button("Refine with Domain Questions ➡️"):
        st.session_state.page = "domain"
        st.rerun()

# -------------------------- Domain --------------------------
def page_domain():
    st.title("🔬 Domain Questions (Computer Science)")

    questions = [
        "Does your solution improve hardware/system performance?",
        "Is it tied to specific technical architecture?",
        "Is it more than business logic?",
        "Is it different from known algorithms?",
        "Do you have measurable benchmark results?"
    ]

    options = ["Yes", "No", "Not sure"]

    answers = []
    for i, q in enumerate(questions):
        st.subheader(q)
        ans = st.radio("Select an option:", options, key=f"dom_{i}")
        answers.append(ans)

    if st.button("Show Final Result ✅"):
        st.session_state.domain_answers = answers
        st.session_state.page = "result"
        st.rerun()

# -------------------------- Result --------------------------
def page_result():
    gen_pct = score_block(st.session_state.general_answers)
    dom_pct = score_block(st.session_state.domain_answers)
    final = round(gen_pct * 0.6 + dom_pct * 0.4, 1)

    st.title("🎯 Final Patentability Snapshot")
    st.metric("Overall Score", f"{final}%")
    st.progress(int(final))

    if final >= 75:
        st.success("Strong potential for patentability.")
    elif final >= 50:
        st.warning("Promising but needs refinement.")
    else:
        st.error("Currently weak for patent protection.")

    st.divider()

    # Generate PDF in memory
    pdf_buffer = generate_patent_pdf(
        gen_pct,
        dom_pct,
        final,
        st.session_state.general_answers,
        st.session_state.domain_answers
    )

    st.download_button(
        label="📄 Download Detailed PDF Report",
        data=pdf_buffer,
        file_name="Patent_Eligibility_Report.pdf",
        mime="application/pdf"
    )

    st.divider()

    col1, col2 = st.columns(2)

    with col1:
        if st.button("🔁 Start Over"):
            for k in list(st.session_state.keys()):
                del st.session_state[k]
            st.rerun()

    with col2:
        if st.button("🧭 Answer Domain Again"):
            st.session_state.page = "domain"
            st.rerun()

# -------------------------- Router --------------------------
if st.session_state.page == "general":
    page_general()
elif st.session_state.page == "prelim":
    page_prelim()
elif st.session_state.page == "domain":
    page_domain()
elif st.session_state.page == "result":
    page_result()
