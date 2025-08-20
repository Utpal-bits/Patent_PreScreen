import streamlit as st

st.set_page_config(page_title="Patentability Survey", layout="centered")

# ---- Helper functions ----
def get_score(answer):
    """Assigns score: Yes=1, No=-1, Maybe/Not sure=0"""
    if answer == "Yes":
        return 1
    elif answer == "No":
        return -1
    else:  # "Maybe/Not sure"
        return 0

# ---- Session state to manage navigation ----
if "stage" not in st.session_state:
    st.session_state.stage = "general"

# ---- Stage 1: General Questions ----
if st.session_state.stage == "general":
    st.title("📝 Patent Eligibility Quick Check")

    st.write("Please answer these simple questions about your idea/invention. "
             "Select the option that best fits. Don’t worry if you’re not sure — choose *Maybe/Not sure*.")

    general_questions = [
        "Is your idea **new** — something that does not already exist in the market or literature?",
        "Does your idea solve a **real problem** or improve something in a practical way?",
        "Can your idea be **applied in the real world** (not just theoretical)?",
        "Is your idea more than just a **basic discovery or observation** (e.g., not just ‘sugar dissolves in water’)?",
        "Would it take some level of **effort or creativity** for another person to come up with this idea?",
        "Have you checked if something **very similar already exists** (prior art)?",
        "Could your idea be described clearly enough that someone else could **replicate it**?"
    ]

    answers = []
    for q in general_questions:
        ans = st.radio(q, ["Yes", "No", "Maybe/Not sure"], index=2, key=q)
        answers.append(ans)

    if st.button("Submit General Assessment"):
        total_score = sum(get_score(a) for a in answers)

        st.session_state.general_score = total_score
        st.session_state.stage = "result"
        st.experimental_rerun()

# ---- Stage 2: Results ----
elif st.session_state.stage == "result":
    st.title("✅ General Assessment Result")

    score = st.session_state.general_score

    if score >= 4:
        st.success("Your idea looks **potentially patentable**! 🚀")
    elif 1 <= score < 4:
        st.info("Your idea **may be patentable**, but needs more clarity. Consider deeper checks. 🔍")
    else:
        st.warning("Your idea **may not be patentable** in its current form. You might need improvements. ⚠️")

    if st.button("👉 Answer More Questions for Detailed Check"):
        st.session_state.stage = "domain_select"
        st.experimental_rerun()

# ---- Stage 3: Domain Selection ----
elif st.session_state.stage == "domain_select":
    st.title("🌐 Choose Your Area")

    domain = st.radio(
        "Which area best matches your idea or background?",
        ["Biology / Biotechnology",
         "Computer Science / Software",
         "Pharmaceuticals / Life Sciences",
         "Engineering / Mechanical / Physical Sciences",
         "Other"]
    )

    if st.button("Next"):
        st.session_state.domain = domain
        st.session_state.stage = "domain_questions"
        st.experimental_rerun()

# ---- Stage 4: Domain-Specific Questions ----
elif st.session_state.stage == "domain_questions":
    st.title("🔬 Domain-Specific Questions")

    domain = st.session_state.domain

    domain_questions = {
        "Biology / Biotechnology": [
            "Does your idea involve a **new organism, strain, or genetic modification**?",
            "Is your invention something that can be **reproduced in a lab** (not a natural discovery)?",
            "Does it provide a **clear benefit** (like faster growth, disease resistance, higher yield)?",
            "Have you tested or planned a way to **prove it works**?",
            "Is your idea different from what’s already **commonly used in labs**?"
        ],
        "Computer Science / Software": [
            "Does your software solve a **technical problem** (not just a business method)?",
            "Is there a **novel algorithm** or unique way of processing data?",
            "Does it improve **performance, efficiency, or security** significantly?",
            "Can it be described in a way that others could **implement it**?",
            "Is it more than just a **presentation of information** or simple rule-based logic?"
        ],
        "Pharmaceuticals / Life Sciences": [
            "Is your invention a **new compound, formulation, or drug combination**?",
            "Does it have a **demonstrated medical effect** (not just a hypothesis)?",
            "Is the preparation or method of use **different from existing drugs**?",
            "Have you conducted or planned **tests/experiments** to support the effect?",
            "Is it not just a **natural product** but something modified or applied in a new way?"
        ],
        "Engineering / Mechanical / Physical Sciences": [
            "Does your invention involve a **new device, material, or process**?",
            "Does it provide a **measurable improvement** (faster, cheaper, stronger, safer)?",
            "Can it be **built or prototyped** with current technology?",
            "Is it different from existing **machines, tools, or materials**?",
            "Can it be clearly described so others could **reproduce it**?"
        ],
        "Other": [
            "Does your idea solve a **real-world problem** in a new way?",
            "Is it different from **common knowledge or basic practices**?",
            "Can you explain how it could be **used or applied**?",
            "Have you thought about how to **prove or demonstrate** it?",
            "Could it be **replicated** if someone followed your description?"
        ]
    }

    q_list = domain_questions[domain]
    answers = []
    for q in q_list:
        ans = st.radio(q, ["Yes", "No", "Maybe/Not sure"], index=2, key=q)
        answers.append(ans)

    if st.button("Submit Domain Assessment"):
        total_score = sum(get_score(a) for a in answers)
        st.success(f"Your domain-specific score is: {total_score}/5")
        st.balloons()
