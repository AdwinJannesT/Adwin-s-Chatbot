
import os
import time
import uuid

import streamlit as st
from dotenv import load_dotenv
from google import genai
from google.genai import types, errors

load_dotenv()

# --------------------------------------------------
# PAGE CONFIGURATION
# --------------------------------------------------

st.set_page_config(
    page_title="Adwin's AI Chatbot",
    page_icon="🤖",
    layout="centered"
)

st.title("🤖 Adwin's AI Chatbot")
st.caption("Powered by Google Gemini")

# --------------------------------------------------
# API CONFIGURATION
# --------------------------------------------------

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    st.error("Gemini API key is missing.")
    st.info(
        "Set GEMINI_API_KEY in your local .env file "
        "or Streamlit Cloud Secrets."
    )
    st.stop()

client = genai.Client(api_key=api_key)

MODEL_NAME = "gemini-3.6-flash"

# --------------------------------------------------
# CHATBOT PERSONALITIES
# --------------------------------------------------

PERSONALITIES = {
    "Beginner Tutor": (
        "You are a patient tutor. Explain concepts in simple "
        "language, step by step, with practical examples."
    ),
    "Python Developer": (
        "You are a Python developer. Help with Python code, "
        "debugging, readability, and programming best practices."
    ),
    "Embedded Systems Assistant": (
        "You are an embedded systems assistant. Explain "
        "microcontrollers, GPIO, sensors, UART, SPI, I2C, PCB "
        "design, firmware, and electronics. Mention relevant "
        "hardware safety precautions."
    ),
    "GenAI Expert": (
        "You are a generative AI assistant. Explain LLMs, "
        "prompt engineering, machine learning, Gemini APIs, "
        "and AI application development with practical examples."
    )
}

# --------------------------------------------------
# SESSION STATE
# --------------------------------------------------

if "chats" not in st.session_state:
    first_id = str(uuid.uuid4())

    st.session_state.chats = {
        first_id: {
            "title": "New Chat",
            "messages": []
        }
    }

    st.session_state.current_chat_id = first_id

if "personality" not in st.session_state:
    st.session_state.personality = "Beginner Tutor"

if "temperature" not in st.session_state:
    st.session_state.temperature = 0.5

if "pending_prompt" not in st.session_state:
    st.session_state.pending_prompt = None

# Ensure current chat exists
if st.session_state.current_chat_id not in st.session_state.chats:
    st.session_state.current_chat_id = next(
        iter(st.session_state.chats)
    )

chats = st.session_state.chats
current_id = st.session_state.current_chat_id
current_chat = chats[current_id]
messages = current_chat["messages"]

# --------------------------------------------------
# SIDEBAR: CHAT MANAGEMENT
# --------------------------------------------------

with st.sidebar:
    st.subheader("💬 Chat Management")

    if st.button("➕ New Chat", use_container_width=True):
        new_id = str(uuid.uuid4())

        st.session_state.chats[new_id] = {
            "title": "New Chat",
            "messages": []
        }

        st.session_state.current_chat_id = new_id
        st.session_state.pending_prompt = None
        st.rerun()

    chat_ids = list(chats.keys())

    selected_id = st.selectbox(
        "Your conversations",
        options=chat_ids,
        index=chat_ids.index(current_id),
        format_func=lambda chat_id: chats[chat_id]["title"],
        key="selected_chat"
    )

    if selected_id != st.session_state.current_chat_id:
        st.session_state.current_chat_id = selected_id
        st.session_state.pending_prompt = None
        st.rerun()

    # Refresh current chat after selection
    current_id = st.session_state.current_chat_id
    current_chat = st.session_state.chats[current_id]
    messages = current_chat["messages"]

    st.divider()
    st.subheader("🎭 Personality")

    personality = st.selectbox(
        "Choose your assistant",
        options=list(PERSONALITIES.keys()),
        key="personality"
    )

    st.divider()
    st.subheader("⚙️ Response Settings")

    temperature = st.slider(
        "Creativity",
        min_value=0.0,
        max_value=1.0,
        step=0.1,
        key="temperature"
    )

    st.divider()
    st.subheader("📁 Current Conversation")

    if messages:
        export_text = "\n\n".join(
            f"{'You' if msg['role'] == 'user' else 'Adwin AI'}:\n"
            f"{msg['content']}"
            for msg in messages
        )

        st.download_button(
            "📥 Download This Chat",
            data=export_text,
            file_name="adwin_chat_history.txt",
            mime="text/plain",
            use_container_width=True
        )

        if st.button(
            "🧹 Clear This Chat",
            use_container_width=True
        ):
            current_chat["messages"] = []
            current_chat["title"] = "New Chat"
            st.session_state.pending_prompt = None
            st.rerun()
    else:
        st.caption("Your conversation is empty.")

    if len(chats) > 1:
        if st.button(
            "🗑️ Delete This Chat",
            use_container_width=True
        ):
            del st.session_state.chats[current_id]

            remaining_ids = list(st.session_state.chats.keys())
            st.session_state.current_chat_id = remaining_ids[0]
            st.session_state.pending_prompt = None
            st.rerun()

# --------------------------------------------------
# MAIN CHAT AREA
# --------------------------------------------------

current_id = st.session_state.current_chat_id
current_chat = st.session_state.chats[current_id]
messages = current_chat["messages"]

st.subheader(f"💬 {current_chat['title']}")

# Suggested prompts for an empty conversation
if not messages:
    st.markdown("### 💡 Try asking")

    col1, col2 = st.columns(2)

    if col1.button("🐍 Python Basics", use_container_width=True):
        st.session_state.pending_prompt = (
            "Explain Python basics with a simple example."
        )
        st.rerun()

    if col2.button("🤖 Generative AI", use_container_width=True):
        st.session_state.pending_prompt = (
            "Explain Generative AI in simple words."
        )
        st.rerun()

    col3, col4 = st.columns(2)

    if col3.button("💻 Python Program", use_container_width=True):
        st.session_state.pending_prompt = (
            "Write a Python program to add two numbers."
        )
        st.rerun()

    if col4.button("🔌 Embedded Systems", use_container_width=True):
        st.session_state.pending_prompt = (
            "Explain UART, SPI, and I2C with real-world examples."
        )
        st.rerun()

# Display previous messages
for message in messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input
prompt = st.chat_input("Ask me anything...")

if st.session_state.pending_prompt:
    prompt = st.session_state.pending_prompt
    st.session_state.pending_prompt = None

# --------------------------------------------------
# SEND MESSAGE TO GEMINI
# --------------------------------------------------

if prompt:
    # Automatically title a new chat from the first question
    if not messages:
        title = prompt.strip().replace("\n", " ")
        current_chat["title"] = (
            title[:35] + "..." if len(title) > 35 else title
        )

    messages.append({
        "role": "user",
        "content": prompt
    })

    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner(f"{personality} is thinking..."):
            try:
                # Send conversation history in Gemini format
                history = [
                    {
                        "role": (
                            "user"
                            if msg["role"] == "user"
                            else "model"
                        ),
                        "parts": [{"text": msg["content"]}]
                    }
                    for msg in messages
                ]

                response = None

                # Retry temporary service overload
                for attempt in range(3):
                    try:
                        response = client.models.generate_content(
                            model=MODEL_NAME,
                            contents=history,
                            config=types.GenerateContentConfig(
                                system_instruction=PERSONALITIES[
                                    personality
                                ],
                                temperature=temperature
                            )
                        )
                        break

                    except errors.APIError as error:
                        if error.code == 503 and attempt < 2:
                            time.sleep(2 ** (attempt + 1))
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

                messages.append({
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
                        "Check your API usage limits."
                    )
                else:
                    st.error(f"Gemini API error: {error}")

            except Exception as error:
                st.error(f"Something went wrong: {error}")
