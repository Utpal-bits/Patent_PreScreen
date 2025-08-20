import streamlit as st

st.set_page_config(page_title="Patent Eligibility Quiz", page_icon="🧾", layout="centered")

st.title("🧾 Patent Eligibility Assessment")

# ---- Session State ----
if "page" not in st.session_state:
    st.session_state.page = 1
if "general_score" not in st.session_state:
    st.session_state.general_score = 0
if "domain" not in st.session_state:
    st.session_state.domain = None
if "domain_score" not in st.session_state:
    st.session_state.domain_score = 0


# ---- General Questions ----
def page1():
    st.header("Step 1: General Questions")
    st.write("Answer these to check if your invention meets basic patentability criteria.")

    questions = [
        "Is your invention new and not previously known?",
        "Does it have a clear practical use?",
        "Can it be reproduced by others?",
        "Is it more than just an abstract idea or theory?",
        "Does it provide a clear advantage over existing solutions?",
        "Can it be described in detail for others to understand?",
        "Is it not a law of nature, natural phenomenon, or mathematical formula?"
    ]

    answers = []
    with st.form("general_form"):
        for q in questions:
            ans = st.radio(q, ["Yes", "No"], key=q)
            answers.append(ans)
        submitted = st.form_submit_button("Next →")

    if submitted:
        st.session_state.general_score = sum([1 for a in answers if a == "Yes"])
        st.session_state.page = 2


# ---- Domain Selection ----
def page2():
    st.header("Step 2: Choose Your Domain")
    domain = st.radio(
        "Which is your background/area of interest?",
        ["Biology", "Chemistry", "Mechanical", "Computer Science", "Others"]
    )
    if st.button("Next →"):
        st.session_state.domain = domain
        st.session_state.page = 3


# ---- Domain-Specific Questions ----
def page3():
    st.header(f"Step 3: {st.session_state.domain} Questions")
    st.write("Answer these domain-specific questions.")

    domain_questions = {
        "Biology": [
            "Is your invention a new organism, strain, or biological material?",
            "Is it different from what exists naturally?",
            "Does it have a clear application (medical, agricultural, industrial)?",
            "Can it be reproduced consistently in a lab?",
            "Do you have experimental data or validation?"
        ],
        "Chemistry": [
            "Is your compound new or modified?",
            "Does it have a novel property?",
            "Is it useful in industry, medicine, or daily life?",
            "Can it be manufactured or synthesized reliably?",
            "Do you have supporting lab data?"
        ],
        "Mechanical": [
            "Does your invention provide a new function or clear improvement?",
            "Is it more than just combining old parts?",
            "Could an engineer consider it non-obvious?",
            "Does it have a practical application?",
            "Have you made a prototype or design?"
        ],
        "Computer Science": [
            "Does your software solve a technical problem?",
            "Is it new or significantly different?",
            "Is it tied to hardware or system-level improvement?",
            "Could it be reproduced easily by common coding practices?",
            "Does it have a practical application (e.g., efficiency, automation)?"
        ],
        "Others": [
            "Is your invention new and not obvious?",
            "Does it provide a clear technical advantage?",
            "Is it useful in industry or society?",
            "Can it be reproduced by others?",
            "Do you have supporting evidence or data?"
        ]
    }

    explanations = {
        "Biology": "Discoveries of natural biological materials are not patentable. But modified or engineered biological materials with specific applications may be protected.",
        "Chemistry": "Novel synthetic compounds, formulations, or chemical processes can often be patented. Common or natural chemicals cannot, unless significantly modified.",
        "Mechanical": "Mechanical inventions with clear technical improvements are usually patentable. Simple rearrangements of known devices without new functionality may not qualify.",
        "Computer Science": "Pure software ideas are not patentable. But technical software that improves hardware or solves a specific technical problem may qualify.",
        "Others": "Your invention may be patentable depending on novelty, utility, and non-obviousness."
    }

    answers = []
    with st.form("domain_form"):
        for q in domain_questions[st.session_state.domain]:
            ans = st.radio(q, ["Yes", "No"], key=q)
            answers.append(ans)
        submitted = st.form_submit_button("Show Results")

    if submitted:
        st.session_state.domain_score = sum([1 for a in answers if a == "Yes"])
        st.session_state.explanation = explanations[st.session_state.domain]
        st.session_state.page = 4


# ---- Results ----
def page4():
    st.header("✅ Your Patent Eligibility Result")

    total_score = st.session_state.general_score + st.session_state.domain_score
    total_questions = 7 + 5
    percentage = int((total_score / total_questions) * 100)

    st.subheader(f"📊 Eligibility Score: {percentage}%")
    st.write(st.session_state.explanation)

    if percentage >= 70:
        st.success("🌟 Great job! Your invention shows strong potential for patentability. Keep pushing forward!")
    elif percentage >= 40:
        st.warning("⚖️ Your invention has some patentable aspects, but improvements or clarifications may be needed.")
    else:
        st.error("🚫 Your invention may face challenges in patentability. Consider refining your idea or consulting an expert.")

    st.info("💡 Remember: This is just an initial assessment, not a legal opinion. For official advice, consult a patent professional.")


# ---- Page Navigation ----
if st.session_state.page == 1:
    page1()
elif st.session_state.page == 2:
    page2()
elif st.session_state.page == 3:
    page3()
elif st.session_state.page == 4:
    page4()
