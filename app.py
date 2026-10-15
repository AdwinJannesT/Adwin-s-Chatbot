
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

# Application heading
st.title("🤖 Adwin's AI Chatbot")
st.caption("Powered by Google Gemini")

# Read API key
api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    st.error("Gemini API key is missing.")
    st.info(
        "Add GEMINI_API_KEY to your local .env file "
        "or Streamlit Cloud Secrets."
    )
    st.stop()

# Initialize Gemini client
client = genai.Client(api_key=api_key)

# Personality instructions
PERSONALITIES = {
    "Beginner Tutor": (
        "You are a patient beginner tutor. Explain concepts "
        "in simple language, step by step. Use practical examples "
        "and define technical terms."
    ),
    "Python Developer": (
        "You are an experienced Python developer. Help with "
        "Python programming, debugging, code quality, and best "
        "practices. Provide readable code and explain important lines."
    ),
    "Embedded Systems Assistant": (
        "You are an embedded systems engineering assistant. Help "
        "with microcontrollers, GPIO, sensors, UART, SPI, I2C, "
        "PCB design, firmware, and electronics. Explain concepts "
        "clearly and distinguish verified facts from assumptions. "
        "Highlight electrical and hardware safety when relevant."
    ),
    "GenAI Expert": (
        "You are a generative AI and machine learning assistant. "
        "Explain LLMs, prompt engineering, APIs, model integration, "
        "and AI application development with practical examples."
    )
}

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []

if "suggested_prompt" not in st.session_state:
    st.session_state.suggested_prompt = None

if "personality" not in st.session_state:
    st.session_state.personality = "Beginner Tutor"

if "temperature" not in st.session_state:
    st.session_state.temperature = 0.5

# Sidebar settings
with st.sidebar:
    st.subheader("🎭 Chatbot Personality")

    personality = st.selectbox(
        "Choose your assistant",
        options=list(PERSONALITIES.keys()),
        key="personality"
    )

    st.caption({
        "Beginner Tutor": "Simple explanations and examples.",
        "Python Developer": "Code, debugging, and best practices.",
        "Embedded Systems Assistant": "MCUs, electronics, and firmware.",
        "GenAI Expert": "Generative AI and machine learning."
    }[personality])

    st.divider()
    st.subheader("⚙️ Response Settings")

    temperature = st.slider(
        "Creativity",
        min_value=0.0,
        max_value=1.0,
        step=0.1,
        key="temperature",
        help=(
            "Lower values tend to be more predictable. "
            "Higher values allow more variation."
        )
    )

    st.divider()
    st.subheader("💬 Chat Tools")

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

    if st.button("🗑️ Clear Chat", use_container_width=True):
        st.session_state.messages = []
        st.session_state.suggested_prompt = None
        st.rerun()

# Suggested prompts for a new conversation
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

    if col4.button("🔌 Embedded Systems", use_container_width=True):
        st.session_state.suggested_prompt = (
            "Explain UART, SPI, and I2C with real-world examples."
        )
        st.rerun()

# Display conversation history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input
prompt = st.chat_input("Ask me anything...")

# Use selected suggested prompt
if st.session_state.suggested_prompt:
    prompt = st.session_state.suggested_prompt
    st.session_state.suggested_prompt = None

# Process question
if prompt:
    # Save and display user's message
    st.session_state.messages.append({
        "role": "user",
        "content": prompt
    })

    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner(f"{personality} is thinking..."):
            try:
                # Include conversation history in Gemini format
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

                # Add the selected personality instructions
                contents = [
                    {
                        "role": "user",
                        "parts": [{
                            "text": (
                                "Follow these assistant instructions "
                                "throughout this conversation:\n"
                                + PERSONALITIES[personality]
                            )
                        }]
                    }
                ] + history

                response = None

                # Retry temporary server overload errors
                for attempt in range(3):
                    try:
                        response = client.models.generate_content(
                            model="gemini-3.6-flash",
                            contents=contents,
                            config=types.GenerateContentConfig(
                                temperature=temperature
                            )
                        )
                        break

                    except errors.APIError as error:
                        if error.code == 503 and attempt < 2:
                            wait_seconds = 2 ** (attempt + 1)
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
                        "Gemini is temporarily busy. "
                        "Please wait and try again."
                    )
                elif error.code == 429:
                    st.error(
                        "Gemini request limit reached. "
                        "Check your API quota and usage limits."
                    )
                else:
                    st.error(f"Gemini API error: {error}")

            except Exception as error:
                st.error(f"Something went wrong: {error}")
