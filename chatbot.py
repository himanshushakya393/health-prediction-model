import streamlit as st
import pickle
import pandas as pd
from predict import predict_with_confidence
from langchain.llms import Ollama

# 🔥 Load AI Model
llm = Ollama(model="phi3", temperature=0.2, num_predict=120)

# 🔹 Load data
columns = pickle.load(open("model/columns.pkl", "rb"))
desc = pd.read_csv("data/symptom_Description.csv")
prec = pd.read_csv("data/symptom_precaution.csv")

# 🔹 Helper functions
def get_description(disease):
    return desc[desc["Disease"] == disease]["Description"].values[0]

def get_precautions(disease):
    return prec[prec["Disease"] == disease].values[0][1:]

# 🔹 Symptom mapping (IMPROVED)
symptom_map = {
    "fever": "fever",
    "high temperature": "fever",
    "headache": "headache",
    "cough": "cough",
    "cold": "cold",
    "body pain": "muscle_pain",
    "body ache": "muscle_pain",
    "pain in body": "muscle_pain",
    "weakness": "fatigue",
    "tired": "fatigue",
    "fatigue": "fatigue",
    "vomiting": "vomiting",
    "nausea": "nausea",
    "stomach pain": "stomach_pain",
    "diarrhea": "diarrhea"
}

# 🔹 Detect symptoms
def match_symptoms(text):
    detected = []

    for word, sym in symptom_map.items():
        if word in text:
            detected.append(sym)

    for symptom in columns:
        symptom_clean = symptom.replace("_", " ").lower()
        if symptom_clean in text:
            detected.append(symptom)

    return list(set(detected))


# =========================
# 🔥 UI
# =========================

st.title("💬 AI Medical Chatbot")

if "messages" not in st.session_state:
    st.session_state.messages = []

if "user_symptoms" not in st.session_state:
    st.session_state.user_symptoms = []

# 🔹 Show history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# 🔹 Input
user_input = st.chat_input("Describe your symptoms...")

if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})

    with st.chat_message("user"):
        st.write(user_input)

    text = user_input.lower()

    detected = match_symptoms(text)

    # 🔥 Add only NEW symptoms (avoid repetition bug)
    for sym in detected:
        if sym not in st.session_state.user_symptoms:
            st.session_state.user_symptoms.append(sym)

    symptoms = st.session_state.user_symptoms

    # 🔍 Debug (optional)
    st.caption(f"Detected: {', '.join(symptoms)}")

    # =========================
    # 🤖 RESPONSE LOGIC
    # =========================

    # 🔹 No symptoms detected
    if len(symptoms) == 0:
        bot_reply = llm.invoke(f"Give simple medical advice for: {user_input}")

    # 🔹 If user says "that's it" → force prediction
    elif "that's it" in text or "thats it" in text:
        disease, confidence, top = predict_with_confidence(symptoms)

    # 🔹 If symptoms less than 2 → ask more
    if len(symptoms) < 2:
        bot_reply = f"""
👨‍⚕️ I'm analyzing your condition.

👉 Current symptoms: {', '.join(symptoms)}

Please tell me 1–2 more symptoms for better accuracy.
"""
    else:
        disease, confidence, top = predict_with_confidence(symptoms)

        # 🔴 LOW CONFIDENCE
        if confidence < 40:
            bot_reply = f"""
👨‍⚕️ I am not fully confident yet.

📊 Confidence: {confidence}%

👉 Your symptoms:
{', '.join(symptoms)}

💡 Possible conditions:
"""
            for d, c in top:
                bot_reply += f"\n• {d} ({c}%)"

            bot_reply += """

👉 Try adding more symptoms.

⚠️ Consult a doctor if needed.
"""

        # 🟢 GOOD CONFIDENCE
        else:
            description = get_description(disease)
            precautions = get_precautions(disease)

            ai_explanation = llm.invoke(f"""
Explain in simple terms:
Disease: {disease}
Symptoms: {symptoms}
""")

            bot_reply = f"""
👨‍⚕️ Based on your symptoms:

🦠 Possible Condition: *{disease}*  
📊 Confidence: {confidence}%

🔍 Other possibilities:
"""
            for d, c in top:
                bot_reply += f"\n• {d} ({c}%)"

            bot_reply += f"""

📖 Description:
{description}

🧠 AI Insight:
{ai_explanation}

🛡️ Precautions:
"""

            for p in precautions:
                bot_reply += f"\n• {p}"

            bot_reply += """

💡 Stay hydrated and take rest.

⚠️ Consult a doctor if symptoms worsen.
"""

    # 🔹 Save reply
    st.session_state.messages.append({"role": "assistant", "content": bot_reply})

    with st.chat_message("assistant"):
        st.write(bot_reply)


# 🔹 Reset
if st.button("🔄 Reset Chat"):
    st.session_state.messages = []
    st.session_state.user_symptoms = []