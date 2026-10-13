import streamlit as st
from google import genai
from dotenv import load_dotenv
import os

# Load API key from .env
load_dotenv()

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)

st.title("🤖 Adwin's Chatbot")

user_input = st.text_input("Ask me anything:")

if st.button("Send"):
    if user_input:
        response = client.models.generate_content(
            model="gemini-3.6-flash",
            contents=user_input
        )

        st.write("### AI Response")
        st.write(response.text)