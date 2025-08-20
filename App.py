import streamlit as st

# -------------------- Page Config --------------------
st.set_page_config(page_title="Patent Eligibility Checker", page_icon="💡", layout="wide")

# -------------------- Custom CSS --------------------
st.markdown("""
<style>
body {
    background: linear-gradient(to right, #ff9966, #ffcc66);
    font-family: 'Segoe UI', sans-serif;
    color: black;
}
h2, h3 {
    color: black;
    text-shadow: 1px 1px 3px rgba(255,255,255,0.8);
}
.question-box {
    background: rgba(255,255,255,0.9);
    padding: 18px;
    border-radius: 15px;
    margin-bottom: 15px;
    box-shadow: 2px 4px 12px rgba(0,0,0,0.15);
}
.stRadio > label {
    font-weight: bold !important;
    color: black !important;
}
.stButton > button {
    background: #ff8800;
    color: white;
    border-radius: 12px;
    font-weight: bold;
    padding: 8px 20px;
    transition: all 0.3s ease-in-out;
}
.stButton > button:hover {
    transform: scale(1.05);
    background: #ffaa00;
}
</style>
""", unsafe_allow_html=True)

# -------------------- Title --------------------
st.markdown("<h2 style='text-align:center;'>💡 Patent Eligibility Checker</h2>", unsafe_allow_html=True)

# -------------------- Core Questions --------------------
core_questions = [
    "Is your idea something new?",
    "Is it different from what already exists?",
    "Can it be used in real life?",
    "Is it more than just a simple theory or law of nature?",
    "Have you checked if similar ideas already exist?",
    "Do you have details that make your idea stand out?",
    "Would experts agree that this is not an obvious solution?"
]

# -------------------- Domain-Specific --------------------
domain_questions = {
    "Does your idea involve healthcare, biotech, or pharma?":
        "⚠️ Healthcare and biotech inventions often face stricter ethical and regulatory reviews.",
    "Does it deal with software or algorithms?":
        "⚠️ Software patents can be harder to get — many jurisdictions reject 'abstract ideas' without technical application.",
    "Is it linked to government-regulated areas (like energy, defense)?":
        "⚠️ Defense and energy-related inventions may require special approvals or face export restrictions."
}

answers = {}
score = 0
maybe_tips = []
domain_warnings = []

# Collapsible Core
st.subheader("📝 Core Questions")
for i, q in enumerate(core_questions):
    with st.expander(f"Q{i+1}: {q}", expanded=False):
        ans = st.radio("Your answer:", ["Yes ✅", "No ❌", "Maybe 🤔"], key=f"core_{i}")
        answers[q] = ans
        if ans == "Yes ✅":
            score += 1
        elif ans == "Maybe 🤔":
            maybe_tips.append(f"👉 For Q{i+1}, you may need to do more research or consult an expert.")

# Collapsible Domain
st.subheader("🌐 Domain-Specific Questions")
for j, (dq, warning) in enumerate(domain_questions.items()):
    with st.expander(f"D{j+1}: {dq}", expanded=False):
        ans = st.radio("Your answer:", ["Yes ✅", "No ❌", "Maybe 🤔"], key=f"dom_{j}")
        answers[dq] = ans
        if ans == "Yes ✅":
            score += 1
            domain_warnings.append(warning)
        elif ans == "Maybe 🤔":
            maybe_tips.append(f"👉 For Domain Q{j+1}, you may need to check specific legal restrictions.")

# -------------------- Results --------------------
st.subheader("📊 Your Results")

total_q = len(core_questions) + len(domain_questions)
st.write(f"✅ Score: **{score} / {total_q}**")

if maybe_tips:
    st.warning("⚠️ Suggestions for 'Maybe':")
    for tip in maybe_tips:
        st.write(tip)

if domain_warnings:
    st.error("⚠️ Domain-Specific Considerations:")
    for dw in domain_warnings:
        st.write(dw)

if score >= total_q - 1:
    st.success("🎉 Strong potential! Filing for a patent may be a good idea.")
    st.balloons()
elif total_q//2 <= score < total_q - 1:
    st.info("⚖️ Moderate potential. Some parts need more work.")
else:
    st.error("❌ Weak potential. Needs significant improvement.")
