import streamlit as st
import pandas as pd
import sqlite3
import google.generativeai as genai

# Configure Gemini API
genai.configure(api_key="YOUR API KEY")

# --- Database Setup ---
DB_FILE = "clinic_appointments.db"

def create_appointments_table():
    """Creates the appointments table in the database."""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS appointments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            patient_name TEXT,
            doctor_name TEXT,
            specialization TEXT,
            appointment_date TEXT,
            appointment_time TEXT,
            consultation_fee REAL
        )
    """)
    conn.commit()
    conn.close()

def save_appointment_to_db(patient_name, doctor_name, specialization, appointment_date, appointment_time, consultation_fee):
    """Saves the booked appointment to the database."""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO appointments (patient_name, doctor_name, specialization, appointment_date, appointment_time, consultation_fee)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (patient_name, doctor_name, specialization, appointment_date, appointment_time, consultation_fee))
    conn.commit()
    conn.close()

def process_uploaded_file(uploaded_file):
    """Processes the uploaded CSV file and extracts clinic data."""
    if uploaded_file is not None and uploaded_file.name.endswith(".csv"):
        try:
            return pd.read_csv(uploaded_file)
        except Exception as e:
            st.error(f"❗ Error reading the uploaded file: {e}")
            return None
    else:
        st.error("❗ Please upload a valid CSV file.")
        return None

def query_gemini(user_query, file_data):
    """Sends user query along with the uploaded doctor data to Gemini for response."""
    prompt = f"""
    You are an expert clinic assistant. The following data contains information about doctors available at the clinic:
    
    - Doctor Name
    - Specialization
    - Available Dates
    - Available Times
    - Consultation Fee
    
    Use this data to answer patient queries regarding:
    - Available doctors on a specific date
    - Booking an appointment for a specific date/time
    - Consultation fees for different specializations
    
    Clinic Data:
    {file_data}
    
    User Query: {user_query}
    """
    model = genai.GenerativeModel("gemini-1.5-pro")
    response = model.generate_content(prompt)
    return response.text if response else "I'm unable to fetch an answer. Please try rephrasing your query."

# --- Initialize Database ---
create_appointments_table()

# --- Streamlit UI ---
st.title("🏥 Clinic Appointment Booking AI 🤖")

# --- File Upload for Doctor Availability ---
st.sidebar.subheader("📂 Upload Doctor Availability Data (CSV)")
uploaded_file = st.sidebar.file_uploader("Upload CSV", type=["csv"])

file_data = None
if uploaded_file:
    file_data = process_uploaded_file(uploaded_file)
    if file_data is not None:
        st.sidebar.success(f"✅ {uploaded_file.name} uploaded successfully!")

# --- Appointment Booking System ---
if file_data is not None and isinstance(file_data, pd.DataFrame):
    # Display available doctors
    st.subheader("👨‍⚕ Available Doctors (Uploaded Data)")
    st.dataframe(file_data)

    # --- User Query for Appointment Information ---
    user_query = st.text_input("🤔 Ask about doctor availability, fees, or appointment booking:")
    if st.button("Ask Chatbot"):
        if user_query.strip():
            response = query_gemini(user_query, file_data.to_string(index=False))
            st.write("🤖 Chatbot Response:", response)
        else:
            st.warning("Please enter a query before clicking the button.")

    # --- Booking an Appointment ---
    st.subheader("📅 Book an Appointment")
    
    if "doctor_name" in file_data.columns:
        selected_doctor = st.selectbox("Select a Doctor:", file_data["doctor_name"])
    else:
        st.error("❗ Error: 'doctor_name' column not found in the uploaded data.")
        selected_doctor = None

    if selected_doctor:
        doctor_info = file_data[file_data["doctor_name"] == selected_doctor].iloc[0]
        available_dates = doctor_info["available_dates"].split(",")
        available_times = doctor_info["available_times"].split(",")
        consultation_fee = doctor_info["consultation_fee"]
        specialization = doctor_info["specialization"]

        selected_date = st.selectbox("Choose an Appointment Date:", available_dates)
        selected_time = st.selectbox("Choose an Appointment Time:", available_times)
        patient_name = st.text_input("Enter Your Name:")

        if st.button("Confirm Appointment"):
            if patient_name.strip():
                save_appointment_to_db(patient_name, selected_doctor, specialization, selected_date, selected_time, consultation_fee)
                st.success(f"🎉 Appointment booked successfully with Dr. {selected_doctor} on {selected_date} at {selected_time}.")
            else:
                st.warning("Please enter your name before confirming the appointment.")
else:
    st.info("Please upload a valid doctor availability CSV to proceed.")
