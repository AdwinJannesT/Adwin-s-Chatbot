# 🤖 Adwin's AI Chatbot

A Generative AI chatbot built using Python, Streamlit, and Google's Gemini API. Ask questions, receive AI-generated responses, and continue conversations through an interactive web interface.

## ✨ Features

- Interactive chatbot interface
- AI-generated responses using Google Gemini
- Conversation history during the current session
- Context-aware follow-up questions
- Clear chat functionality
- Secure API key configuration

## 🛠️ Technologies Used

- **Python** — application logic
- **Streamlit** — web interface
- **Google Gemini API** — AI response generation
- **python-dotenv** — environment variable management
- **Git and GitHub** — version control and source hosting

## 📁 Project Structure

```text
ai-chatbot/
├── app.py
├── .gitignore
├── requirements.txt
├── Readme.md
└── .env  (local only; not uploaded to GitHub)
```

## 🚀 Run Locally

### 1. Clone the repository

```bash
git clone https://github.com/AdwinJannesT/Adwin-s-Chatbot.git
```

### 2. Enter the project directory

```bash
cd Adwin-s-Chatbot
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure your Gemini API key

Create a `.env` file in the project directory:

```env
GEMINI_API_KEY=your_api_key_here
```

Replace the placeholder with your own Gemini API key. Never publish the real key.

### 5. Run the chatbot

```bash
streamlit run app.py
```

The application will open in your browser.

## 🌐 Live Demo

[[Open the deployed AI chatbot](PASTE_YOUR_STREAMLIT_APP_URL_HERE)](https://adwin-ai-chatbot.streamlit.app/)

Replace the placeholder with your actual Streamlit Community Cloud URL after deployment succeeds.

## 🔒 Security

- Keep API keys out of source code.
- Never commit `.env` to GitHub.
- Use Streamlit Secrets to configure the API key for cloud deployment.
- If an API key is exposed, revoke it and create a replacement.

## 🔮 Future Improvements

- Persistent conversation history
- PDF question answering using Retrieval-Augmented Generation (RAG)
- Improved error handling
- Additional interface customization

## 👨‍💻 Author

**Adwin Jannes T**
