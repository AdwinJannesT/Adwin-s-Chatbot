# AI Chatbot using Google Gemini

## Project Overview
A Generative AI chatbot built using Python, Streamlit, and the Google Gemini API. The application accepts user questions and generates AI-powered responses through an interactive web interface.

## Features
- Interactive chatbot interface
- AI-generated responses using Gemini
- Python-based application
- Secure API key management using environment variables

## Technologies Used
- **Python 3.14.5** — application logic
- **Streamlit** — web interface
- **Google Gemini API** — response generation
- **python-dotenv** — loads environment variables

## Project Structure
```text
ai-chatbot/
├── app.py
├── .env
├── .gitignore
├── requirements.txt
└── README.md
```

## Installation and Setup

1. Clone this repository:
   ```bash
   git clone YOUR_GITHUB_REPOSITORY_URL
   ```

2. Open the project folder:
   ```bash
   cd ai-chatbot
   ```

3. Install the dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Create a `.env` file and add your Gemini API key:
   ```env
   GEMINI_API_KEY=your_api_key_here
   ```

5. Run the application:
   ```bash
   streamlit run app.py
   ```

## Security
Never commit your `.env` file or publish your API key. The `.gitignore` file excludes the environment file from Git tracking.

## Future Improvements
- Conversation history
- PDF question answering using RAG
- Improved error handling
- Cloud deployment

## Author
Your Name
