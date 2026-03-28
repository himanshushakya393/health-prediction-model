import streamlit as st
import pickle
import pandas as pd
from predict import predict_with_confidence
from langchain.llms import Ollama

# 🔥 Load LLM
llm = Ollama(model="phi3", temperature=0.2, num_predict=150)

# 🔹 Page Config
st.set_page_config(page_title="Smart Healthcare System", page_icon="🏥")

# 🔹 Sidebar
menu = st.sidebar.selectbox("Select Module", [
    "Disease Prediction",
    "Chatbot",
    "Appointment",
    "Dashboard",
    "Report Analysis"
])

# 🔹 Load Data
columns = pickle.load(open("model/columns.pkl", "rb"))
desc = pd.read_csv("data/symptom_Description.csv")
prec = pd.read_csv("data/symptom_precaution.csv")

def get_description(disease):
    return desc[desc["Disease"] == disease]["Description"].values[0]

def get_precautions(disease):
    return prec[prec["Disease"] == disease].values[0][1:]

# =========================
# 🧬 DISEASE PREDICTION
# =========================
if menu == "Disease Prediction":

    st.title("🏥 Disease Prediction System")

    symptoms = st.multiselect("Select Symptoms", columns)

    if st.button("Predict Disease"):
        if len(symptoms) == 0:
            st.warning("⚠️ Please select symptoms")
        else:
            disease, confidence, top = predict_with_confidence(symptoms)

            st.success(f"🦠 Possible Disease: {disease}")
            st.info(f"📊 Confidence: {confidence}%")

            st.subheader("🔍 Top Possibilities")
            for d, c in top:
                st.write(f"• {d} ({c}%)")

            st.subheader("📖 Description")
            st.write(get_description(disease))

            st.subheader("🛡️ Precautions")
            for p in get_precautions(disease):
                st.write(f"• {p}")

# =========================
# 🤖 CHATBOT
# =========================
elif menu == "Chatbot":

    st.title("💬 AI Medical Chatbot")

    if "messages" not in st.session_state:
        st.session_state.messages = []

    if "symptoms" not in st.session_state:
        st.session_state.symptoms = []

    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.write(msg["content"])

    user_input = st.chat_input("Describe symptoms...")

    if user_input:
        st.session_state.messages.append({"role": "user", "content": user_input})
        text = user_input.lower()

        # simple symptom detection
        if "fever" in text:
            st.session_state.symptoms.append("fever")
        if "headache" in text:
            st.session_state.symptoms.append("headache")
        if "cough" in text:
            st.session_state.symptoms.append("cough")

        symptoms = list(set(st.session_state.symptoms))

        if len(symptoms) < 3:
            bot_reply = "👨‍⚕️ Please provide more symptoms."
        else:
            disease, confidence, top = predict_with_confidence(symptoms)

            if confidence < 40:
                bot_reply = "⚠️ Not enough data. Please add more symptoms."
            else:
                ai = llm.invoke(f"Explain {disease} simply.")

                bot_reply = f"""
🦠 Possible Condition: {disease}  
📊 Confidence: {confidence}%

🧠 {ai}
"""

        st.session_state.messages.append({"role": "assistant", "content": bot_reply})

        with st.chat_message("assistant"):
            st.write(bot_reply)

    if st.button("Reset Chat"):
        st.session_state.messages = []
        st.session_state.symptoms = []

# =========================
# 📅 APPOINTMENT
# =========================
elif menu == "Appointment":
    import appointment
    appointment.show()

# =========================
# 📊 DASHBOARD
# =========================
elif menu == "Dashboard":
    import dashboard
    dashboard.show()

# =========================
# 📄 REPORT
# =========================
elif menu == "Report Analysis":
    import report_analysis
    report_analysis.show()

