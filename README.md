# OmniSearch AI - Restaurant Menu Chatbot & Clinic Appointment Generator

## 📌 Overview
**OmniSearch AI** is a Streamlit-based AI-powered chatbot application that provides two functionalities:

1. **Restaurant Menu Chatbot**: Users can upload restaurant menus in CSV format, query dish availability, get recommendations, and place orders.
2. **Clinic Appointment Generator**: Users can upload clinic schedules, check doctor availability, and book appointments using an AI-powered chatbot.

## 🚀 Features

### ✅ Restaurant Menu Chatbot
- Upload restaurant menu in CSV format
- AI-powered chatbot to answer menu-related queries
- Place and confirm orders
- Check dish availability and get preparation time
- Store order details in a database (SQLite)

### ✅ Clinic Appointment Generator
- Upload doctor availability data in CSV format
- AI-powered chatbot for scheduling appointments
- View available doctors and consultation fees
- Book and save appointments in an SQLite database
- Retrieve saved appointments

## 🛠 Installation & Setup

### 1️⃣ Clone the Repository
```sh
git clone https://github.com/your-username/restaurant-clinic-chatbot.git
cd restaurant-clinic-chatbot
```

### 2️⃣ Set Up a Virtual Environment
#### On macOS/Linux:
```sh
python3 -m venv venv
source venv/bin/activate
```
#### On Windows:
```sh
python -m venv venv
venv\Scripts\activate
```

### 3️⃣ Install Dependencies
```sh
pip install -r requirements.txt
```

## 🔑 Google Gemini API Key Setup
This chatbot uses **Google Gemini AI** to process queries. You need to configure an API key.

### How to Get a Gemini API Key:
1. Go to [Google AI Studio](https://aistudio.google.com/)
2. Sign in with your Google account
3. Generate an API key from the API Keys section
4. Copy the API key

### Add API Key to the Project:
1. Open the `app.py` file
2. Replace the API key in this line:
   ```python
   genai.configure(api_key="YOUR_GEMINI_API_KEY_HERE")
   ```
3. Save the file

## 🏃‍♂️ Running the Application
Run the application using Streamlit:
```sh
streamlit run app.py
```
This will open the web app in your browser.

---
## 🍲 Placing an Order (Restaurant Chatbot)
1. Go to the **Place Order** section.
2. Select dishes from the multi-select dropdown.
3. Confirm your order after verifying availability.
4. Order details are automatically saved to the SQLite database (`restaurant_orders.db`).

### 📽️ Working Demo
Watch the working demo video of the restaurant order process:

[![Watch the Video](Video)](https://drive.google.com/file/d/1t0bEkN4o1UPFn_f8o7upZ87wzOrLLg10/view?usp=sharing )

### 📚 Viewing Order Details in Database
To view saved orders:
```sh
sqlite3 restaurant_orders.db
```
Then run:
```sql
SELECT * FROM orders;
```

### 📝 Generating Order Confirmation
After confirming the order, the chatbot will generate an order summary. Optionally, download the confirmation receipt in PDF format.

---
## 🏥 Booking an Appointment (Clinic Chatbot)
1. Upload the **Doctor Availability CSV** file.
2. Ask questions about available doctors, fees, and time slots.
3. Select a doctor and pick a time slot.
4. Confirm the appointment (saved in `clinic_appointments.db`).

### 📚 Viewing Appointments in Database
To view saved appointments:
```sh
sqlite3 clinic_appointments.db
```
Then run:
```sql
SELECT * FROM appointments;
```

---
## 📜 License
This project is licensed under the **MIT License**.

---
## 🤝 Contributing
1. Fork the repository
2. Create a feature branch (`git checkout -b feature-branch`)
3. Commit changes (`git commit -m "Added new feature"`)
4. Push to the branch (`git push origin feature-branch`)
5. Create a Pull Request

---
## 💬 Questions?
Feel free to open an issue or reach out if you have any questions!

