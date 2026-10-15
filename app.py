
import os
import streamlit as st
from google import genai
from dotenv import load_dotenv

load_dotenv()

st.set_page_config(
    page_title="Adwin AI Chatbot",
    page_icon="🤖"
)

st.title("🤖 Adwin's AI Chatbot")
st.caption("Powered by Google Gemini")

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    st.error("Gemini API key is missing.")
    st.stop()

client = genai.Client(api_key=api_key)

if "messages" not in st.session_state:
    st.session_state.messages = []

# Sidebar tools
with st.sidebar:
    st.subheader("Chat Tools")

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
        st.rerun()

# Display conversation history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

prompt = st.chat_input("Ask me anything...")

if prompt:
    st.session_state.messages.append({
        "role": "user",
        "content": prompt
    })

    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                history = [
                    {
                        "role": "user" if msg["role"] == "user"
                        else "model",
                        "parts": [{"text": msg["content"]}]
                    }
                    for msg in st.session_state.messages
                ]

                response = client.models.generate_content(
                    model="gemini-3.6-flash",
                    contents=history
                )

                answer = response.text or "No response received."
                st.markdown(answer)

                st.session_state.messages.append({
                    "role": "assistant",
                    "content": answer
                })

            except Exception as error:
                st.error(f"Error: {error}")
