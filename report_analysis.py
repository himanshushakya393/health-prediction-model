import streamlit as st
import pandas as pd

def show():
    st.title("📄 Health Report Analysis")

    st.write("Upload your medical report (CSV or Excel)")

    # 🔹 File Upload
    file = st.file_uploader("Upload Report", type=["csv", "xlsx"])

    if file is not None:
        # 🔹 Load file
        if file.name.endswith(".csv"):
            df = pd.read_csv(file)
        else:
            df = pd.read_excel(file)

        st.subheader("📊 Uploaded Data")
        st.dataframe(df)

        st.divider()

        # =========================
        # 🔥 SIMPLE ANALYSIS
        # =========================

        st.subheader("🧠 Analysis Results")

        for col in df.columns:
            if df[col].dtype != "object":

                avg = df[col].mean()

                st.write(f"🔹 {col}")
                st.write(f"Average: {avg}")

                # 🔥 Basic health rules
                if "sugar" in col.lower():
                    if avg > 140:
                        st.error("⚠️ High Blood Sugar Detected")
                    else:
                        st.success("✅ Normal Sugar Level")

                elif "bp" in col.lower() or "pressure" in col.lower():
                    if avg > 130:
                        st.error("⚠️ High Blood Pressure")
                    else:
                        st.success("✅ Normal BP")

                elif "cholesterol" in col.lower():
                    if avg > 200:
                        st.error("⚠️ High Cholesterol")
                    else:
                        st.success("✅ Normal Cholesterol")

                st.divider()

        st.info("💡 This is a basic analysis. Consult a doctor for medical advice.")