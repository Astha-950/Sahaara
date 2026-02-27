import streamlit as st
import requests

BACKEND_URL = "http://localhost:8000/ask"

# st.set_page_config must be FIRST
st.set_page_config(page_title="AI Mental Health Therapist", layout="wide")

if "user" not in st.session_state:
    st.session_state.user = None

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Show login/register if not logged in
if st.session_state.user is None:
    st.title("🧠 SafeSpace – AI Mental Health Therapist")
    tab1, tab2 = st.tabs(["Login", "Register"])

    with tab1:
        email = st.text_input("Email")
        password = st.text_input("Password", type="password", key="login_password")
        if st.button("Login", key="login_btn"):
            res = requests.post("http://localhost:8000/login",
                                json={"email": email, "password": password})
            data = res.json()
            if data["status"] == "success":
                st.session_state.user = {"name": data["name"], "phone": data["phone"]}
                st.rerun()
            else:
                st.error("Invalid credentials")

    with tab2:
        name = st.text_input("Name", key="register_name")
        email = st.text_input("Email", key="register_email")
        password = st.text_input("Password", type="password", key="register_password")
        phone = st.text_input("Phone Number (with country code e.g. +91...)", key="register_phone")
        if st.button("Register", key="register_btn"):
            res = requests.post("http://localhost:8000/register",
                                json={"name": name, "email": email,
                                      "password": password, "phone": phone})
            data = res.json()
            if data["status"] == "registered":
                st.success("Registered! Please login.")
            else:
                st.error("Email already exists.")

# Show chat only after login
else:
     
    st.title(f"Welcome {st.session_state.user['name']} 👋")
    
    # Show chat history
    for msg in st.session_state.chat_history:
        with st.chat_message(msg["role"]):
            st.write(msg["content"])

    user_input = st.chat_input("What's on your mind today?")
    if user_input:
        st.session_state.chat_history.append({"role": "user", "content": user_input})

        response = requests.post(BACKEND_URL, json={
            "message": user_input,
            "phone": st.session_state.user["phone"] , # send user phone
            "location": st.session_state.user_location
        })

        reply = response.json().get("response", "Sorry, something went wrong.")
        st.session_state.chat_history.append({"role": "assistant", "content": reply})
        st.rerun()