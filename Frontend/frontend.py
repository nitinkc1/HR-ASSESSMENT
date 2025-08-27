import streamlit as st
import requests

# Backend API URL
API_URL = "http://127.0.0.1:8000"

# Page setup
st.set_page_config(page_title="HR Assistant Chatbot", layout="wide")

# Header
st.markdown(
    """
    <div style='text-align: center;'>
        <h1 style='color:#4F46E5;'>🤖 HR Assistant Chatbot</h1>
        <p style='color:gray;'>Ask about employees, skills, or availability</p>
    </div>
    """,
    unsafe_allow_html=True
)

# Initialize chat history
if "history" not in st.session_state:
    st.session_state["history"] = []

# Chat container
chat_container = st.container()

# Input area
with st.form("chat_form", clear_on_submit=True):
    user_query = st.text_input("", placeholder="Type your message here...")
    submitted = st.form_submit_button("Send")
    
    if submitted and user_query:
        try:
            response = requests.post(f"{API_URL}/chat", json={"query": user_query})
            if response.status_code == 200:
                bot_reply = response.json().get("response", "No response found.")
                st.session_state["history"].append(("You", user_query))
                st.session_state["history"].append(("Bot", bot_reply))
            else:
                st.error("❌ Error: Could not get response from backend.")
        except Exception as e:
            st.error(f"⚠️ Failed to connect to backend: {e}")

# Display chat history in bubbles
with chat_container:
    for sender, msg in st.session_state["history"]:
        if sender == "You":
            st.markdown(
                f"""
                <div style='text-align: right; margin: 10px;'>
                    <span style='background-color:#DCF8C6; color:black; padding:10px 15px; border-radius:15px; display:inline-block; max-width:70%;'>
                        🧑 {msg}
                    </span>
                </div>
                """,
                unsafe_allow_html=True
            )
        else:
            st.markdown(
                f"""
                <div style='text-align: left; margin: 10px;'>
                    <span style='background-color:#E8E8E8; color:black; padding:10px 15px; border-radius:15px; display:inline-block; max-width:70%;'>
                        🤖 {msg}
                    </span>
                </div>
                """,
                unsafe_allow_html=True
            )
