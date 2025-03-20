import streamlit as st
import pandas as pd
import sqlite3
import google.generativeai as genai

# Configure Gemini API
genai.configure(api_key="YOUR API KEY")

# --- Database Setup ---
DB_FILE = "restaurant_orders.db"

# --- Create Orders Table ---
def create_orders_table():
    """Creates the orders table in the database."""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS orders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            dish_name TEXT,
            price REAL,
            category TEXT,
            cuisine TEXT,
            preparation_time INTEGER,
            availability TEXT,
            ratings REAL
        )
    """)
    conn.commit()
    conn.close()

# --- Save Order to Database ---
def save_order_to_db(order_summary):
    """Saves ordered dishes to the restaurant's database."""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    for _, row in order_summary.iterrows():
        cursor.execute("""
            INSERT INTO orders (dish_name, price, category, cuisine, preparation_time, availability, ratings)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (row["dish_name"], row["price"], row["category"], row["cuisine"],
              row["preparation_time"], row["availability"], row["ratings"]))
    conn.commit()
    conn.close()

# --- Process Uploaded File ---
def process_uploaded_file(uploaded_file):
    """Processes the uploaded CSV file and extracts menu data."""
    if uploaded_file is not None and uploaded_file.name.endswith(".csv"):
        return pd.read_csv(uploaded_file)
    return None

# --- Query Gemini API ---
def query_gemini(user_query, file_data):
    """Sends user query along with the uploaded menu data to Gemini for response."""
    prompt = f"""
    You are an expert restaurant menu assistant. The following data contains detailed information about the dishes offered by the restaurant, including:
    
    - Dish Name
    - Price
    - Category
    - Cuisine
    - Preparation Time
    - Availability
    - Ratings
    
    Use this data to accurately answer any customer queries about the menu, including:
    
    - Dish recommendations based on cuisine, price, or category
    - Estimated preparation time for a dish
    - Suggestions for meal combos based on cuisine or preferences
    - Availability of vegetarian, vegan, or gluten-free options
    - Price details and ratings of specific dishes
    
    Menu Data:
    {file_data}
    
    User Query: {user_query}
    """
    model = genai.GenerativeModel("gemini-1.5-pro")
    response = model.generate_content(prompt)

    return response.text if response else "I'm unable to fetch an answer. Please try rephrasing your query."

# --- Initialize Database ---
create_orders_table()

# --- Streamlit UI ---
st.title("🍽️ Smart Restaurant Ordering System 🤖")

# --- File Upload for Menu ---
st.sidebar.subheader("📂 Upload Restaurant Menu (CSV)")
uploaded_file = st.sidebar.file_uploader("Upload CSV", type=["csv"])

file_data = None
if uploaded_file:
    file_data = process_uploaded_file(uploaded_file)
    st.sidebar.success(f"✅ {uploaded_file.name} uploaded successfully!")

# --- Restaurant Ordering System ---
if file_data is not None and isinstance(file_data, pd.DataFrame):
    # Display restaurant menu
    st.subheader("📜 Restaurant Menu (Uploaded)")
    st.dataframe(file_data)

    # --- User Query for Menu or Suggestions ---
    user_query = st.text_input("🤔 Ask about the menu or get dish suggestions:")

    if st.button("Ask Chatbot"):
        if user_query.strip():
            response = query_gemini(user_query, file_data.to_string(index=False))
            st.write("🤖 *Chatbot Response:*", response)
        else:
            st.warning("Please enter a query before clicking the button.")

    # --- Ordering Section ---
    st.subheader("🛒 Place Your Order")

    # Multi-select for choosing dishes
    if "dish_name" in file_data.columns:
        selected_dishes = st.multiselect("Select dishes to order:", file_data["dish_name"])
    else:
        st.error("❗️ Error: 'dish_name' column not found in the uploaded menu.")
        selected_dishes = []

    if selected_dishes:
        order_summary = file_data[file_data["dish_name"].isin(selected_dishes)]

        # Show order summary
        st.write("✅ **Order Summary:**")
        st.dataframe(order_summary[["dish_name", "price", "category", "cuisine", "preparation_time", "availability", "ratings"]])

        # Calculate total price and estimated time
        total_price = order_summary["price"].sum()
        total_time = order_summary["preparation_time"].sum()

        st.write(f"💰 **Total Price:** ₹{total_price}")
        st.write(f"⏰ **Estimated Preparation Time:** {total_time} minutes")

        # Confirm order and save to database
        if st.button("Confirm Order"):
            save_order_to_db(order_summary)
            st.success("🎉 Order placed successfully! Your order has been saved in the database. 🍲")
else:
    st.info("Please upload a valid restaurant menu CSV to proceed.")
