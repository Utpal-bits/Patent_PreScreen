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
h2, h3, h4 {
    color: black;
    text-shadow: 1px 1px 3px rgba(255,255,255,0.8);
}
.question-box {
    background: rgba(255,255,255,0.85);
    padding: 18px;
    border-radius: 15px;
    margin-bottom: 12px;
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
    transition: all 0.3s ease-in-out;
}
.stButton > button:hover {
    transform: scale(1.05);
    background: #ffaa00;
}
</style>
""", unsafe_allow_html=True)

# -------------------- Title --------------------
st.markdown("<h2 style='text-align:center; animation: fadeIn 2s;'>💡 Patent Eligibility Self-Assessment</h2>", unsafe_allow_html=True)

# -------------------- Questions --------------------
questions = [
    "Is your invention novel (not publicly known)?",
    "Does it involve an inventive step (not obvious)?",
    "Can it be applied in industry?",
    "Does it fall under non-excluded subject matter (not laws of nature/abstract ideas)?",
    "Have you conducted a prior art search?",
    "Do you have technical details that distinguish your invention?",
    "Would experts in the field consider this solution non-trivial?"
]

answers = {}
score = 0
maybe_tips = []

with st.spinner("Loading assessment..."):
    for i, q in enumerate(questions[:7]):  # First 7 essential questions
        with st.expander(f"Q{i+1}: {q}", expanded=False):
            ans = st.radio("Select an option:", ["Yes ✅", "No ❌", "Maybe 🤔"], key=f"q{i}")
            answers[q] = ans
            if ans == "Yes ✅":
                score += 1
            elif ans == "Maybe 🤔":
                maybe_tips.append(f"👉 For Q{i+1}, it’s better to conduct a deeper patent search or consult an expert.")

# -------------------- Optional Domain Questions --------------------
with st.expander("🔍 Domain-Specific (Optional)"):
    st.write("Answer if you want deeper insights:")
    dom_q = st.radio("Does your invention belong to a regulated domain (e.g., biotech, pharma)?", ["Yes ✅", "No ❌", "Maybe 🤔"])
    answers["Domain Specific"] = dom_q

# -------------------- Results --------------------
st.subheader("📊 Your Assessment Results:")

st.write(f"✅ Score: **{score} / {len(questions)}**")

if maybe_tips:
    st.warning("⚠️ Suggestions for 'Maybe' answers:")
    for tip in maybe_tips:
        st.write(tip)

if score >= 6:
    st.success("🎉 Strong Patent Potential! You should seriously consider filing.")
    st.balloons()
elif 3 <= score < 6:
    st.info("⚖️ Moderate Patent Potential. Some areas need strengthening.")
else:
    st.error("❌ Weak Patent Potential. Needs significant improvement.")
