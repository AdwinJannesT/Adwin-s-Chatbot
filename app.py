
import os
import time
import streamlit as st
from google import genai
from google.genai import types, errors
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Page configuration
st.set_page_config(
    page_title="Adwin's AI Chatbot",
    page_icon="🤖",
    layout="centered"
)

# App heading
st.title("🤖 Adwin's AI Chatbot")
st.caption("Powered by Google Gemini")

# Read API key
api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    st.error("Gemini API key is missing.")
    st.info(
        "Add GEMINI_API_KEY to your .env file "
        "or Streamlit Cloud Secrets."
    )
    st.stop()

# Initialize Gemini client
client = genai.Client(api_key=api_key)

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []

if "suggested_prompt" not in st.session_state:
    st.session_state.suggested_prompt = None

# Sidebar
with st.sidebar:
    st.subheader("⚙️ Response Settings")

    temperature = st.slider(
        "Creativity",
        min_value=0.0,
        max_value=1.0,
        value=0.5,
        step=0.1,
        help=(
            "Lower values give more predictable responses. "
            "Higher values allow more variation."
        )
    )

    st.caption(f"Current creativity: {temperature:.1f}")

    st.divider()
    st.subheader("💬 Chat Tools")

    # Download conversation
    if st.session_state.messages:
        chat_text = "\n\n".join(
            f"{'You' if msg['role'] == 'user' else 'Adwin AI'}:\n"
            f"{msg['content']}"
            for msg in st.session_state.messages
        )

        st.download_button(
            label="📥 Download Chat",
            data=chat_text,
            file_name="adwin_chat_history.txt",
            mime="text/plain",
            use_container_width=True
        )

    # Clear conversation
    if st.button("🗑️ Clear Chat", use_container_width=True):
        st.session_state.messages = []
        st.session_state.suggested_prompt = None
        st.rerun()

# Suggested prompts
if not st.session_state.messages:
    st.subheader("💡 Try asking")

    col1, col2 = st.columns(2)

    if col1.button("🐍 Python Basics", use_container_width=True):
        st.session_state.suggested_prompt = (
            "Explain Python basics with a simple example."
        )
        st.rerun()

    if col2.button("🤖 Generative AI", use_container_width=True):
        st.session_state.suggested_prompt = (
            "Explain Generative AI in simple words."
        )
        st.rerun()

    col3, col4 = st.columns(2)

    if col3.button("💻 Python Program", use_container_width=True):
        st.session_state.suggested_prompt = (
            "Write a Python program to add two numbers."
        )
        st.rerun()

    if col4.button("🧠 Machine Learning", use_container_width=True):
        st.session_state.suggested_prompt = (
            "Explain Machine Learning with a real-world example."
        )
        st.rerun()

# Display previous messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input
prompt = st.chat_input("Ask me anything...")

# Use a suggested prompt if selected
if st.session_state.suggested_prompt:
    prompt = st.session_state.suggested_prompt
    st.session_state.suggested_prompt = None

# Process the question
if prompt:
    # Save and display user message
    st.session_state.messages.append({
        "role": "user",
        "content": prompt
    })

    with st.chat_message("user"):
        st.markdown(prompt)

    # Generate response
    with st.chat_message("assistant"):
        with st.spinner("Adwin AI is thinking..."):
            try:
                # Convert messages to Gemini format
                history = [
                    {
                        "role": (
                            "user"
                            if msg["role"] == "user"
                            else "model"
                        ),
                        "parts": [{"text": msg["content"]}]
                    }
                    for msg in st.session_state.messages
                ]

                response = None

                # Retry temporary 503 errors
                for attempt in range(3):
                    try:
                        response = client.models.generate_content(
                            model="gemini-3.6-flash",
                            contents=history,
                            config=types.GenerateContentConfig(
                                temperature=temperature
                            )
                        )
                        break

                    except errors.APIError as error:
                        if error.code == 503 and attempt < 2:
                            wait_seconds = 2 ** (attempt + 1)

                            st.warning(
                                "Gemini is busy. "
                                f"Retrying in {wait_seconds} seconds..."
                            )

                            time.sleep(wait_seconds)
                        else:
                            raise

                if response is None:
                    raise RuntimeError(
                        "Gemini did not return a response."
                    )

                answer = (
                    response.text
                    or "No response received from Gemini."
                )

                st.markdown(answer)

                # Save assistant response
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": answer
                })

            except errors.APIError as error:
                if error.code == 503:
                    st.warning(
                        "Gemini is temporarily experiencing high demand. "
                        "Please wait and try again."
                    )
                elif error.code == 429:
                    st.error(
                        "Gemini request limit reached. "
                        "Check your API quota and billing settings."
                    )
                else:
                    st.error(f"Gemini API error: {error}")

            except Exception as error:
                st.error(f"Something went wrong: {error}")
