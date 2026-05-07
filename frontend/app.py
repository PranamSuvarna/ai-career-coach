import streamlit as st
import requests

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="AI Career Coach",
    page_icon="🚀",
    layout="wide"
)

# ---------------- API URLS ----------------
ANALYZE_API_URL = "http://127.0.0.1:8000/analyze/"
RESUME_API_URL = "http://127.0.0.1:8000/analyze-resume/"
CHAT_API_URL = "http://127.0.0.1:8000/chat/"

# ---------------- CUSTOM CSS ----------------
st.markdown("""
<style>
.stApp {
    background: linear-gradient(to right, #0f172a, #111827);
    color: white;
}

.card {
    background-color: #1e293b;
    padding: 20px;
    border-radius: 20px;
    margin-bottom: 20px;
    box-shadow: 0px 4px 15px rgba(0,0,0,0.3);
}

.metric {
    font-size: 24px;
    font-weight: bold;
}
</style>
""", unsafe_allow_html=True)

# ---------------- SESSION STATE ----------------
if "messages" not in st.session_state:
    st.session_state.messages = []

# ---------------- DISPLAY RESULTS FUNCTION ----------------
def display_results(data):

    st.subheader("📊 Analysis Results")

    # Career
    st.write("### 🎯 Career Prediction")
    st.success(data.get("career", "N/A"))

    # Confidence
    st.write("### 📈 Confidence")
    st.info(f"{data.get('confidence', 0)} %")

    # Skills
    st.write("### 🧠 Extracted Skills")

    skills = data.get("skills", [])

    if skills:
        st.write(", ".join(skills))
    else:
        st.warning("No skills detected")

    # Roadmap
    st.write("### 🗺️ Career Roadmap")

    roadmap = data.get("roadmap", [])

    if roadmap:
        for step in roadmap:
            st.write(f"✔️ {step}")
    else:
        st.warning("No roadmap available")

    # ---------------- AI ADVICE FIX ----------------
    adv = data.get("advice", "")

    st.subheader("💡 AI Advice")

    if isinstance(adv, dict):

        st.write("💪 Strengths:", adv.get("strengths", []))
        st.write("⚠ Weaknesses:", adv.get("weaknesses", []))
        st.write("📚 Recommendations:", adv.get("recommendations", []))

    else:
        st.write(adv)

# ---------------- HEADER ----------------
st.markdown(
    '<div class="main-title">🚀 AI Career Coach</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">AI-Powered Career Guidance & Resume Analyzer</div>',
    unsafe_allow_html=True
)

# ---------------- TABS ----------------
tab1, tab2, tab3 = st.tabs([
    "📝 Skill Analysis",
    "📄 Resume Upload",
    "🤖 AI Career Chat"
])

# =========================================================
# TAB 1 — SKILL ANALYSIS
# =========================================================
with tab1:

    st.subheader("📝 Analyze Skills")

    user_input = st.text_area(
        "Enter your skills / resume text:",
        height=220
    )

    if st.button("🔍 Analyze Skills"):

        if user_input.strip() == "":
            st.error("⚠️ Please enter some text")

        else:

            try:

                with st.spinner("Analyzing..."):

                    response = requests.post(
                        ANALYZE_API_URL,
                        json={"text": user_input},
                        timeout=30
                    )

                    if response.status_code == 200:

                        data = response.json()

                        display_results(data)

                    else:
                        st.error(f"Server Error: {response.status_code}")

            except Exception as e:
                st.error(f"❌ Connection Error: {e}")

# =========================================================
# TAB 2 — RESUME UPLOAD
# =========================================================
with tab2:

    st.subheader("📄 Upload Resume")

    uploaded_file = st.file_uploader(
        "Upload PDF Resume",
        type=["pdf"]
    )

    if uploaded_file is not None:

        if st.button("📤 Analyze Resume"):

            try:

                with st.spinner("Analyzing Resume..."):

                    files = {
                        "file": (
                            uploaded_file.name,
                            uploaded_file,
                            "application/pdf"
                        )
                    }

                    response = requests.post(
                        RESUME_API_URL,
                        files=files,
                        timeout=60
                    )

                    if response.status_code == 200:

                        data = response.json()

                        display_results(data)

                    else:
                        st.error(f"Server Error: {response.status_code}")

            except Exception as e:
                st.error(f"❌ Upload Error: {e}")

# =========================================================
# TAB 3 — AI CHATBOT
# =========================================================
with tab3:

    st.subheader("🤖 AI Career Chat")

    # Display chat messages
    for msg in st.session_state.messages:

        if msg["role"] == "user":

            st.markdown(
                f'<div class="user-msg">🧑‍💻 {msg["content"]}</div>',
                unsafe_allow_html=True
            )

        else:

            st.markdown(
                f'<div class="bot-msg">🤖 {msg["content"]}</div>',
                unsafe_allow_html=True
            )

    # Chat Input
    user_message = st.chat_input(
        "Ask anything about careers, AI, resumes..."
    )

    if user_message:

        # Add user message
        st.session_state.messages.append({
            "role": "user",
            "content": user_message
        })

        try:

            with st.spinner("AI Thinking..."):

                response = requests.post(
                    CHAT_API_URL,
                    json={
                        "message": user_message
                    },
                    timeout=30
                )

                if response.status_code == 200:

                    data = response.json()

                    ai_reply = data.get(
                        "reply",
                        "No response received"
                    )

                else:
                    ai_reply = f"Server Error: {response.status_code}"

        except Exception as e:
            ai_reply = f"Connection Error: {str(e)}"

        # Add AI reply
        st.session_state.messages.append({
            "role": "assistant",
            "content": ai_reply
        })

        st.rerun()