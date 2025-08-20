import streamlit as st

# ---- Custom CSS ----
st.markdown("""
    <style>
    .question-box {
        border-radius: 15px;
        padding: 20px;
        margin-bottom: 20px;
        font-size: 1.3em;  /* Bigger text */
        font-weight: 500;
        color: white;
    }
    .q1 { background-color: #FF6F61; }   /* coral */
    .q2 { background-color: #6A5ACD; }   /* slate blue */
    .q3 { background-color: #20B2AA; }   /* teal */
    .q4 { background-color: #FFB347; }   /* orange */
    .q5 { background-color: #8A2BE2; }   /* purple */
    .q6 { background-color: #2E8B57; }   /* green */
    .q7 { background-color: #FF69B4; }   /* pink */
    </style>
""", unsafe_allow_html=True)

st.title("💡 Patent Eligibility Quick Check")

st.write("Answer a few simple questions to see if your idea *may* be eligible for a patent.")

# ---- First Page: 7 General Questions ----
questions = [
    "Have you checked if a similar idea already exists (like in Google, research papers, or products)?",
    "Is your idea solving a real problem or making something easier/faster/better?",
    "Can you explain your idea in simple words (like you are telling a friend)?",
    "Does your idea have a clear and useful application (in daily life, business, or industry)?",
    "Does your idea include something new, not just a combination of existing things?",
    "Could someone skilled in the area easily copy your idea, or does it require a new way of thinking?",
    "Have you tested or built a model/prototype of your idea?"
]

options = ["Yes", "No", "Maybe / Not Sure", "I haven’t checked yet"]

responses = []

for i, q in enumerate(questions, start=1):
    st.markdown(f'<div class="question-box q{i}">{q}</div>', unsafe_allow_html=True)
    ans = st.radio("", options, key=f"q{i}")
    responses.append(ans)

# ---- Submit Button ----
if st.button("👉 Show Result"):
    yes_count = responses.count("Yes")
    st.subheader("📊 Your Patent Check Result")
    
    if yes_count >= 5:
        st.success("✅ Your idea looks promising! It **may be eligible** for a patent. Let’s dig deeper.")
    elif 3 <= yes_count < 5:
        st.warning("⚠️ Your idea has potential, but more clarity is needed before moving toward a patent.")
    else:
        st.error("❌ Based on your answers, your idea may not be ready for a patent yet. Try refining it.")

    st.markdown("---")
    st.markdown("✨ Want to understand better? Let’s answer more **domain-specific questions**.")
    if st.button("Go to Domain-Specific Questions ➡️"):
        st.session_state.page = "domain"
