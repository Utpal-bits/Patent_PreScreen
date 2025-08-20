import time
import streamlit as st
st.markdown(
    """
    <style>
    /* Make all question text black */
    .question-text, h1, h2, h3, h4, h5, h6, label, .stMarkdown p {
        color: black !important;
    }

    /* Make radio button/checkbox labels black */
    .stRadio label, .stCheckbox label, .stSelectbox label {
        color: black !important;
    }

    /* Ensure text inside forms is also black */
    .stTextInput label, .stTextArea label, .stNumberInput label {
        color: black !important;
    }
    </style>
    """,
    unsafe_allow_html=True
)


# -------------------------- App Setup --------------------------
st.set_page_config(
    page_title="Patent Eligibility Checker",
    page_icon="💡",
    layout="centered"
)

# -------------------------- Styles (single, valid block) --------------------------
st.markdown("""
<style>
/* Animated gradient background */
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

/* App container card */
.app-card {
  background: rgba(255,255,255,0.85);
  backdrop-filter: blur(6px);
  border-radius: 22px;
  padding: 26px 22px;
  border: 1px solid rgba(0,0,0,0.05);
  box-shadow: 0 10px 30px rgba(0,0,0,0.07);
}

/* Section title chip */
.section-chip {
  display:inline-block;
  padding:8px 14px;
  border-radius:999px;
  font-weight:700;
  font-size:0.9rem;
  color:black !important;   /* enforce black */
  background:linear-gradient(135deg,#d5f4ff,#f3e8ff);
  border:1px solid rgba(0,0,0,0.06);
}

/* Question card (black text) */
.qcard {
  border-radius: 15px;
  padding: 20px;
  margin-bottom: 16px;
  font-size: 1.15rem;
  font-weight: 600;
  color: black !important; /* enforce black */
  border: 1px solid rgba(0,0,0,0.06);
  box-shadow: 0 6px 18px rgba(0,0,0,0.05);
  transition: transform .15s ease, box-shadow .15s ease;
}
.qcard:hover {
  transform: translateY(-2px);
  box-shadow: 0 10px 22px rgba(0,0,0,0.08);
}

/* Ensure all question text inside qcard is black */
.qcard p {
  color: black !important;
}

/* Pastel backgrounds for variety (readable with black text) */
.q1 { background-color: #FFD1C1; }
.q2 { background-color: #D1C4FF; }
.q3 { background-color: #B2F0E9; }
.q4 { background-color: #FFE0B2; }
.q5 { background-color: #E6CCFF; }
.q6 { background-color: #C1E1C1; }
.q7 { background-color: #FFCCE5; }

/* Pulse anim for headers */
@keyframes softPulse {
  0% {transform: scale(1);}
  50% {transform: scale(1.01);}
  100% {transform: scale(1);}
}
.pulse { animation: softPulse 3.8s ease-in-out infinite; }

/* Big CTA button */
div.stButton>button {
  border-radius: 14px !important;
  padding: 12px 18px !important;
  font-weight: 800 !important;
  font-size: 1.05rem !important;
  box-shadow: 0 8px 18px rgba(0,0,0,0.08) !important;
}

/* Progress badge */
.badge {
  display:inline-block;
  padding:4px 10px;
  border-radius:999px;
  background:#eef2ff;
  color:#3730a3;
  font-weight:700;
  font-size:0.85rem;
  border:1px solid #e5e7eb;
}

/* Insight pill */
.insight {
  background:#f0f9ff;
  border:1px solid #bae6fd;
  color:#0c4a6e;
  padding:10px 12px;
  border-radius:12px;
  font-size:0.95rem;
  margin:6px 0;
}

/* Tiny tip */
.tip {
  font-size:0.9rem;
  color:#111;
  background:#f8fafc;
  border:1px dashed #cbd5e1;
  padding:10px 12px;
  border-radius:12px;
}

/* Force radio labels to black for consistency */
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
if "final_score" not in st.session_state:
    st.session_state.final_score = 0

# -------------------------- Helpers --------------------------
def score_block(answers, yes="Yes", neutral=("Maybe / Not Sure", "I haven’t checked yet", "Not sure")):
    yes_count = sum(1 for a in answers if a == yes)
    neutral_count = sum(1 for a in answers if a in neutral)
    total = len(answers)
    raw = yes_count + 0.5 * neutral_count
    pct = round(raw / total * 100, 1) if total else 0.0
    return pct, yes_count, neutral_count, total

def step_progress(current_step:int):
    steps = ["General", "Domain", "Answers", "Result"]
    cols = st.columns(len(steps))
    for i, label in enumerate(steps, start=1):
        with cols[i-1]:
            if i < current_step:
                st.markdown(f"✅ **{label}**")
            elif i == current_step:
                st.markdown(f"🟣 **{label}**")
            else:
                st.markdown(f"▫️ {label}")

# -------------------------- General Questions --------------------------
def page_general():
    step_progress(1)
    st.markdown('<div class="app-card">', unsafe_allow_html=True)

    st.markdown('<span class="section-chip pulse">Step 1 · Quick Check</span>', unsafe_allow_html=True)
    st.markdown("## 💡 Patent Eligibility — Quick Check (7 questions)")
    st.write("Answer in simple terms. *Neutral options count half.*")

    questions = [
        "Have you checked if a similar idea already exists (Google, papers, products)?",
        "Is your idea solving a real problem or making something easier/faster/better?",
        "Can you explain your idea in simple words (like telling a friend)?",
        "Does your idea have a clear and useful application (daily life, business, or industry)?",
        "Does your idea include something new, not just a mix of old things?",
        "Would it be hard for a skilled person to do the same without your new way?",
        "Have you tested or built a model/prototype of your idea?"
    ]
    options = ["Yes", "No", "Maybe / Not Sure", "I haven’t checked yet"]

    answers = []
    for i, q in enumerate(questions, start=1):
        st.markdown(f'<div class="qcard q{i}">{q}</div>', unsafe_allow_html=True)
        ans = st.radio(" ", options, key=f"gen_{i}", horizontal=True, help="Pick the best fit")
        answers.append(ans)
        st.markdown('<div class="tip">Tip: If unsure, choose “Maybe / Not Sure”.</div>', unsafe_allow_html=True)

    st.divider()
    if st.button("➡️ Continue to Domain"):
        st.session_state.general_answers = answers
        st.session_state.page = "choose_domain"
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

# -------------------------- Domain Choice --------------------------
def page_domain_choice():
    step_progress(2)
    st.markdown('<div class="app-card">', unsafe_allow_html=True)
    st.markdown('<span class="section-chip pulse">Step 2 · Pick Domain</span>', unsafe_allow_html=True)
    st.markdown("## 🌐 What best fits your invention?")

    domain = st.radio(
        "Choose your background/area of interest:",
        ["Biology", "Chemistry", "Mechanical", "Computer Science", "Others"],
        horizontal=False
    )
    st.info("We’ll ask 5 simple questions tailored to your choice.")

    cols = st.columns(2)
    if cols[0].button("⬅️ Back"):
        st.session_state.page = "general"
        st.rerun()
    if cols[1].button("Next ➡️"):
        st.session_state.domain = domain
        st.session_state.page = "domain_questions"
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

# -------------------------- Domain Q Bank + Insights --------------------------
DOMAIN_QS = {
    "Biology": [
        ("Is your invention a new organism, strain, or biological material?",
         "If it's just found in nature, it’s not patentable. If it's modified/engineered or used in a new way, it can be."),
        ("Is it different from what exists naturally (not just discovered)?",
         "Natural discoveries alone aren’t patentable; engineered differences help."),
        ("Does it have a clear use (medical, agricultural, industrial)?",
         "Clear, practical use supports patentability."),
        ("Can it be reproduced consistently in a lab or controlled setting?",
         "Reproducibility is key — others should be able to follow your method."),
        ("Do you have experimental data or validation (tests/results)?",
         "Data makes your case stronger; consider basic experiments.")
    ],
    "Chemistry": [
        ("Is your compound/material new or a modified version of a known one?",
         "New or significantly modified substances can be patentable."),
        ("Does it show a new/strong property (stability, strength, reactivity)?",
         "A real, measurable improvement helps a lot."),
        ("Is it useful in industry, medicine, or daily life?",
         "Industrial applicability is required."),
        ("Can it be manufactured or synthesized in a reliable way?",
         "Repeatable production supports utility."),
        ("Do you have supporting lab data (tests, characterization)?",
         "Data like spectra or performance tests strengthens novelty/utility.")
    ],
    "Mechanical": [
        ("Does your invention add a new function or clear improvement over devices today?",
         "New function/performance is a strong sign."),
        ("Is it more than just combining old parts that work the same way?",
         "Simple combinations are usually not patentable."),
        ("Would a typical engineer find your solution non-obvious?",
         "If it’s surprising or counter-intuitive, that helps."),
        ("Does it have a real-world application in products or processes?",
         "Clear application strengthens your case."),
        ("Do you have a prototype or detailed design?",
         "Prototypes/designs help prove it works and is buildable.")
    ],
    "Computer Science": [
        ("Does your software/algorithm solve a technical problem (not just business logic)?",
         "Pure business methods/abstract math are generally not patentable."),
        ("Is it new or clearly different from known solutions?",
         "Show how it differs from common approaches."),
        ("Does it improve hardware/system performance (speed, security, memory)?",
         "Technical improvements tied to systems are stronger."),
        ("Is it tied to specific hardware or a technical architecture?",
         "Linking to hardware/technical effect helps in many jurisdictions."),
        ("Does it have a practical application with measurable benefit?",
         "Demonstrable utility boosts eligibility.")
    ],
    "Others": [
        ("Is your idea new and not an obvious tweak of existing things?",
         "You need novelty and non-obviousness."),
        ("Does it provide a clear technical advantage or solve a real problem?",
         "Practical, technical benefits matter."),
        ("Can it be used in industry or daily life?",
         "Industrial applicability is required."),
        ("Can others reproduce it by following your method?",
         "Enablement/reproducibility is important."),
        ("Do you have some proof, prototype, or data?",
         "Evidence makes your case far stronger.")
    ],
}

def domain_specific_flags(domain, answers):
    """Return tailored messages triggered by weak spots."""
    msgs = []
    a = answers  # list of 5 answers
    y = lambda i: a[i].startswith("Yes")
    n = lambda i: a[i].startswith("No")
    u = lambda i: a[i] in ("Not sure",)

    if domain == "Biology":
        if n(1):  # Q2: not different from nature
            msgs.append("🔎 It looks *natural*. **Natural things aren’t patentable** unless modified or used in a new technical way.")
        if n(3):  # reproducibility
            msgs.append("🧪 Try to make it **repeatable** in a lab and record steps/data.")
        if n(4):
            msgs.append("📊 Add **test data** (even small experiments) to support your claims.")
    elif domain == "Chemistry":
        if n(0):
            msgs.append("🧪 If it’s not new/modified, it’s hard to patent. Consider a **new form/process/use**.")
        if n(1):
            msgs.append("📈 Show a **measurable property improvement** (e.g., stronger, more stable).")
        if n(3):
            msgs.append("🏭 Propose a **repeatable synthesis or manufacturing route**.")
    elif domain == "Mechanical":
        if n(1):
            msgs.append("⚙️ A **mere combination of known parts** is usually not patentable. Show synergy/new function.")
        if n(4):
            msgs.append("🧰 A **prototype or detailed CAD** will help demonstrate practicality.")
    elif domain == "Computer Science":
        if n(0):
            msgs.append("🧠 If it’s mainly **business logic or a formula**, it’s weak. Emphasize the **technical problem**.")
        if n(2) and n(3):
            msgs.append("🖥️ Tie your idea to **system/hardware improvements** or a **technical effect**.")
    else:
        if n(0) or n(1):
            msgs.append("🔧 Highlight **what’s new** and the **technical advantage** clearly.")
        if n(3):
            msgs.append("🧪 Ensure others can **reproduce** it with your steps/data.")

    if any(u(i) for i in range(len(a))):
        msgs.append("🧭 Where you chose **Not sure**, consider a quick check or small test to gain confidence.")
    return msgs

# -------------------------- Domain Questions Page --------------------------
def page_domain_questions():
    step_progress(3)
    st.markdown('<div class="app-card">', unsafe_allow_html=True)
    st.markdown(f'<span class="section-chip pulse">Step 3 · {st.session_state.domain}</span>', unsafe_allow_html=True)
    st.markdown(f"## ✍️ {st.session_state.domain} — 5 quick questions")

    options = ["Yes", "No", "Not sure"]
    answers = []
    qs = DOMAIN_QS[st.session_state.domain]

    for idx, (q, hint) in enumerate(qs, start=1):
        st.markdown(f'<div class="qcard q{(idx % 7) or 7}">{q}</div>', unsafe_allow_html=True)
        ans = st.radio(" ", options, horizontal=True, key=f"dom_{idx}")
        answers.append(ans)
        st.markdown(f'<div class="insight">Why we ask: {hint}</div>', unsafe_allow_html=True)

    st.divider()
    pb = st.progress(0)
    cols = st.columns(2)
    if cols[0].button("⬅️ Back"):
        st.session_state.page = "choose_domain"
        st.rerun()
    if cols[1].button("Show Result ✅"):
        for i in range(0, 101, 15):
            pb.progress(i)
            time.sleep(0.02)
        st.session_state.domain_answers = answers
        st.session_state.page = "result"
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

# -------------------------- Results Page --------------------------
def page_result():
    step_progress(4)
    st.markdown('<div class="app-card">', unsafe_allow_html=True)
    st.markdown('<span class="section-chip pulse">Final · Result</span>', unsafe_allow_html=True)
    st.markdown("## 🎯 Your Patentability Snapshot")

    gen_pct, gen_yes, gen_neutral, gen_total = score_block(st.session_state.general_answers)
    dom_pct, dom_yes, dom_neutral, dom_total = score_block(st.session_state.domain_answers)

    # Weighted average: 60% general, 40% domain
    final = round(gen_pct*0.6 + dom_pct*0.4, 1)
    st.session_state.final_score = final

    st.write("### 📊 Scores")
    c1, c2, c3 = st.columns(3)
    c1.metric("General", f"{gen_pct}%")
    c2.metric(f"{st.session_state.domain}", f"{dom_pct}%")
    c3.metric("Overall", f"{final}%")

    st.progress(int(final))

    if final >= 75:
        st.success("🚀 Strong potential! Your answers suggest your idea **may be patentable**. Keep going!")
        st.balloons()
    elif final >= 50:
        st.warning("✨ Promising, but needs more clarity or evidence. You’re **on the right track**.")
    else:
        st.error("🔧 Not ready yet. Several key points need work before pursuing a patent.")

    OVERALL_GUIDE = {
        "Biology": "Naturally occurring things aren’t patentable by themselves. **Modified or engineered biology with a clear use** can be.",
        "Chemistry": "New/modified substances or **processes with better properties** can be patentable, especially with data.",
        "Mechanical": "Show **new function** or a **real improvement**, not just a combo of known parts.",
        "Computer Science": "Pure software/abstract ideas are weak. **Technical effect or system improvement** helps a lot.",
        "Others": "Focus on **novelty, usefulness, non-obviousness**, and **reproducibility**."
    }
    st.info(OVERALL_GUIDE[st.session_state.domain])

    flags = domain_specific_flags(st.session_state.domain, st.session_state.domain_answers)
    if flags:
        with st.expander("🔍 Personalized suggestions based on your answers"):
            for m in flags:
                st.markdown(f"- {m}")

    st.markdown("---")
    st.markdown("### ✅ What you can do next")
    st.markdown("""
- Do a **quick prior art search** (Google, Google Patents, big publishers).
- Write a **one-page summary**: problem, your solution, what’s new, how it works, benefits.
- Collect **evidence**: small tests, screenshots, data tables, CAD, or a short demo video.
- If you plan to file, consider talking to a **registered patent professional**.
""")

    cols = st.columns(2)
    if cols[0].button("🔁 Start Over"):
        for k in list(st.session_state.keys()):
            del st.session_state[k]
        st.rerun()
    if cols[1].button("🧭 Answer Again (Domain)"):
        st.session_state.page = "domain_questions"
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

# -------------------------- Router --------------------------
if st.session_state.page == "general":
    page_general()
elif st.session_state.page == "choose_domain":
    page_domain_choice()
elif st.session_state.page == "domain_questions":
    page_domain_questions()
elif st.session_state.page == "result":
    page_result()



