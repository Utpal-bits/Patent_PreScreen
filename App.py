import streamlit as st

# -------------------------- Page Setup --------------------------
st.set_page_config(
    page_title="Patent Eligibility Quiz",
    page_icon="🧾",
    layout="centered"
)

# -------------------------- Custom CSS --------------------------
st.markdown("""
    <style>
    /* --- General Styling --- */
    h1, h2, h3, h4, h5, h6 {
        font-size: 200% !important;
        color: #2c3e50;
        font-weight: 600;
    }
    .stRadio label {
        font-size: 140% !important;
        color: #154360;
    }
    .stButton>button {
        font-size: 140% !important;
        border-radius: 10px;
        padding: 12px 24px;
        background: linear-gradient(135deg, #2E86C1, #5DADE2);
        color: white;
        font-weight: bold;
        transition: 0.3s ease-in-out;
    }
    .stButton>button:hover {
        background: linear-gradient(135deg, #1F618D, #2874A6);
        transform: scale(1.05);
    }

    /* --- Question Box --- */
    .question-box {
        background: #f4f6f7;
        padding: 20px;
        border-radius: 12px;
        margin-bottom: 20px;
        border-left: 6px solid #5DADE2;
        animation: fadeIn 1s ease-in-out;
    }
    .question-box:nth-child(odd) {
        background: #EBF5FB;
        border-left: 6px solid #3498DB;
    }
    .question-box:nth-child(even) {
        background: #E8F8F5;
        border-left: 6px solid #1ABC9C;
    }

    /* --- Results Animation --- */
    .success, .warning, .error {
        font-size: 150% !important;
        animation: fadeIn 1.5s ease-in-out;
    }

    /* --- Fade In --- */
    @keyframes fadeIn {
        from {opacity: 0; transform: translateY(15px);}
        to {opacity: 1; transform: translateY(0);}
    }

    /* --- Progress Tracker --- */
    .progress-container {
        display: flex;
        justify-content: space-between;
        margin: 20px 0;
        padding: 0 15px;
    }
    .step {
        flex: 1;
        text-align: center;
        position: relative;
        font-weight: bold;
        color: #7f8c8d;
    }
    .step.active {
        color: #2E86C1;
    }
    .step::before {
        content: '';
        display: block;
        margin: 0 auto 8px auto;
        width: 28px;
        height: 28px;
        border-radius: 50%;
        background: #bdc3c7;
    }
    .step.active::before {
        background: #2E86C1;
    }
    .step::after {
        content: '';
        position: absolute;
        top: 12px;
        left: 50%;
        width: 100%;
        height: 4px;
        background: #bdc3c7;
        z-index: -1;
    }
    .step:last-child::after {
        display: none;
    }
    .active + .step::after {
        background: #2E86C1;
    }
    </style>
""", unsafe_allow_html=True)

# -------------------------- Title --------------------------
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

# ---- Progress Tracker ----
def progress_tracker(current_step):
    steps = ["Step 1", "Step 2", "Step 3", "Step 4"]
    tracker_html = '<div class="progress-container">'
    for i, step in enumerate(steps, 1):
        if i == current_step:
            tracker_html += f'<div class="step active">{step}</div>'
        else:
            tracker_html += f'<div class="step">{step}</div>'
    tracker_html += '</div>'
    st.markdown(tracker_html, unsafe_allow_html=True)

# ---- General Questions ----
def page1():
    progress_tracker(1)
    st.header("✨ Step 1: General Questions")
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
            with st.container():
                st.markdown(f"<div class='question-box'><b>{q}</b></div>", unsafe_allow_html=True)
                ans = st.radio("", ["Yes", "No"], key=q)
                answers.append(ans)
        submitted = st.form_submit_button("Next →")

    if submitted:
        st.session_state.general_score = sum([1 for a in answers if a == "Yes"])
        st.session_state.page = 2

# ---- Domain Selection ----
def page2():
    progress_tracker(2)
    st.header("🎨 Step 2: Choose Your Domain")
    domain = st.radio(
        "Which is your background/area of interest?",
        ["Biology", "Chemistry", "Mechanical", "Computer Science", "Others"]
    )
    if st.button("Next →"):
        st.session_state.domain = domain
        st.session_state.page = 3

# ---- Domain-Specific Questions ----
def page3():
    progress_tracker(3)
    st.header(f"🔬 Step 3: {st.session_state.domain} Questions")
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
        "Biology": "🧬 Discoveries of natural biological materials are not patentable. But modified or engineered biological materials with specific applications may be protected.",
        "Chemistry": "⚗️ Novel synthetic compounds, formulations, or chemical processes can often be patented. Common or natural chemicals cannot, unless significantly modified.",
        "Mechanical": "⚙️ Mechanical inventions with clear technical improvements are usually patentable. Simple rearrangements of known devices without new functionality may not qualify.",
        "Computer Science": "💻 Pure software ideas are not patentable. But technical software that improves hardware or solves a specific technical problem may qualify.",
        "Others": "✨ Your invention may be patentable depending on novelty, utility, and non-obviousness."
    }

    answers = []
    with st.form("domain_form"):
        for q in domain_questions[st.session_state.domain]:
            with st.container():
                st.markdown(f"<div class='question-box'><b>{q}</b></div>", unsafe_allow_html=True)
                ans = st.radio("", ["Yes", "No"], key=q)
                answers.append(ans)
        submitted = st.form_submit_button("Show Results")

    if submitted:
        st.session_state.domain_score = sum([1 for a in answers if a == "Yes"])
        st.session_state.explanation = explanations[st.session_state.domain]
        st.session_state.page = 4

# ---- Results ----
def page4():
    progress_tracker(4)
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
