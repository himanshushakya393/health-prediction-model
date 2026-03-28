import streamlit as st
import sqlite3
import pandas as pd
import matplotlib.pyplot as plt


def show():
    # 🔹 Load data
    conn = sqlite3.connect("appointments.db")
    df = pd.read_sql_query("SELECT * FROM appointments", conn)

    st.title("📊 Healthcare Dashboard")

    if df.empty:
        st.warning("No data available. Please add appointments first.")
    else:

        # =========================
        # 🔹 BASIC STATS
        # =========================
        st.subheader("📌 Key Metrics")

        total_patients = len(df)
        unique_diseases = df["disease"].nunique()

        col1, col2 = st.columns(2)
        col1.metric("Total Patients", total_patients)
        col2.metric("Unique Diseases", unique_diseases)

        st.divider()

        # =========================
        # 🔹 DISEASE DISTRIBUTION
        # =========================
        st.subheader("🦠 Disease Distribution")

        disease_counts = df["disease"].value_counts()

        fig1, ax1 = plt.subplots()
        disease_counts.plot(kind="bar", ax=ax1)
        st.pyplot(fig1)

        st.divider()

        # =========================
        # 🔹 APPOINTMENTS OVER TIME
        # =========================
        st.subheader("📅 Appointments Over Time")

        df["date"] = pd.to_datetime(df["date"])
        date_counts = df["date"].value_counts().sort_index()

        fig2, ax2 = plt.subplots()
        date_counts.plot(kind="line", ax=ax2)
        st.pyplot(fig2)

        st.divider()

        # =========================
        # 🔹 AGE DISTRIBUTION
        # =========================
        st.subheader("🎂 Age Distribution")

        fig3, ax3 = plt.subplots()
        df["age"].plot(kind="hist", bins=10, ax=ax3)
        st.pyplot(fig3)