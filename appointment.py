import streamlit as st
import sqlite3

def show():
    st.write("✅ Appointment module loaded")  # debug

    conn = sqlite3.connect("appointments.db", check_same_thread=False)
    cursor = conn.cursor()

    st.title("📅 Appointment Booking System")

    name = st.text_input("Patient Name")
    age = st.number_input("Age", min_value=1, max_value=120)
    date = st.date_input("Select Date")
    disease = st.text_input("Disease / Symptoms")

    if st.button("Book Appointment"):
        if name and disease:
            cursor.execute("""
            INSERT INTO appointments (name, age, date, disease, status)
            VALUES (?, ?, ?, ?, ?)
            """, (name, age, str(date), disease, "Pending"))

            conn.commit()
            st.success("✅ Appointment Booked Successfully")
        else:
            st.warning("⚠️ Please fill all details")

    st.divider()

    st.subheader("📋 All Appointments")

    cursor.execute("SELECT * FROM appointments")
    data = cursor.fetchall()

    for row in data:
        st.write(f"""
👤 Name: {row[1]}  
🎂 Age: {row[2]}  
📅 Date: {row[3]}  
🦠 Issue: {row[4]}  
📌 Status: {row[5]}
""")
        st.divider()