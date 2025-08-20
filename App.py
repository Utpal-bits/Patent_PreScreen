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
    maybe_count = responses.count("Maybe / Not Sure") + responses.count("I haven’t checked yet")
    
    # Each Yes = 1 point, Each Maybe = 0.5 point
    total_score = yes_count + (0.5 * maybe_count)
    percentage = round((total_score / len(questions)) * 100, 1)

    st.subheader("📊 Your Patent Check Result")
    st.write(f"🔢 **Eligibility Score: {percentage}%**")

    if percentage >= 75:
        st.success("✅ Your idea looks promising! It may be patentable. Keep going strong 🚀")
        st.info("💡 Encouragement: Great job! Your answers show you’ve thought this through. Next step could be searching prior art more carefully or drafting early notes.")
    elif 50 <= percentage < 75:
        st.warning("⚠️ Your idea has potential, but more clarity is needed before moving forward.")
        st.info("💡 Encouragement: Don’t stop here! Even many successful patents started as 'unclear' ideas. With refinement, yours could shine ✨")
    else:
        st.error("❌ Based on your answers, your idea may not yet be ready for a patent.")
        st.info("💡 Encouragement: Every great invention starts rough. Use this as a guide to improve — refine your idea, test more, and come back stronger 💪")

    st.markdown("---")
    st.markdown("✨ Want to understand better? Let’s answer more **domain-specific questions**.")
    if st.button("Go to Domain-Specific Questions ➡️"):
        st.session_state.page = "domain"
