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
