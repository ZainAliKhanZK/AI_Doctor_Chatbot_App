import os
import streamlit as st
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

api_key = os.getenv("HF")

st.set_page_config(
    page_title="AI Health Assistant",
    page_icon="🩺",
    layout="centered",
    initial_sidebar_state="expanded",
)

st.markdown(
    """
    <style>
    .main {
        background-color: #f7f9fb;
    }
    .app-header {
        text-align: center;
        padding: 1.2rem 0 0.5rem 0;
    }
    .app-header h1 {
        font-size: 2.1rem;
        margin-bottom: 0.2rem;
    }
    .app-header p {
        color: #6b7280;
        font-size: 0.95rem;
    }
    .disclaimer {
        background-color: #fff8e1;
        border-left: 4px solid #f5b400;
        padding: 0.8rem 1rem;
        border-radius: 6px;
        font-size: 0.85rem;
        color: #6b5b00;
        margin-bottom: 1.2rem;
    }
    .stChatMessage {
        border-radius: 12px;
    }
    footer {visibility: hidden;}
    </style>
    """,
    unsafe_allow_html=True,
)

# Header 
st.markdown(
    """
    <div class="app-header">
        <h1>🩺 Your Personal AI Health Assistant</h1>
        <p>Friendly, general health guidance — not a substitute for professional care.</p>
    </div>
    """,
    unsafe_allow_html=True,
)


# Sidebar 
with st.sidebar:
    st.header("About")
    st.write(
        "This assistant uses an AI model to answer general health-related "
        "questions in a clear, friendly way."
    )
    st.write("---")
    if st.button("🗑️ Clear conversation"):
        st.session_state.messages = []
        st.rerun()

# API key check 
if not api_key:
    st.error(
        "No API key found. Please set the `HF` environment variable in your .env file."
    )
    st.stop()

client = OpenAI(
    base_url="https://router.huggingface.co/v1",
    api_key=api_key,
)

SYSTEM_PROMPT = (
    "You are a helpful and friendly medical assistant. "
    "Do not include any medical advice that could be harmful. "
    "Do not answer any questions that are not related to health. "
    "Politely decline if the user asks for advice unrelated to health or for adult content. "
    "Keep responses well structured, clear, and easy to read, using short paragraphs "
    "or bullet points where helpful."
)

# ---------- Chat state ----------
if "messages" not in st.session_state:
    st.session_state.messages = []

# Render existing conversation
for msg in st.session_state.messages:
    with st.chat_message(msg["role"], avatar="🧑" if msg["role"] == "user" else "🩺"):
        st.markdown(msg["content"])

# ---------- Chat input ----------
user_input = st.chat_input("Tell me about your health concern...")

if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user", avatar="🧑"):
        st.markdown(user_input)

    with st.chat_message("assistant", avatar="🩺"):
        with st.spinner("Thinking through your question..."):
            try:
                completion = client.chat.completions.create(
                    model="moonshotai/Kimi-K2-Instruct-0905",
                    messages=[{"role": "system", "content": SYSTEM_PROMPT}]
                    + st.session_state.messages,
                )
                reply = completion.choices[0].message.content
            except Exception as e:
                reply = f"Sorry, something went wrong while contacting the assistant.\n\n`{e}`"

        st.markdown(reply)

    st.session_state.messages.append({"role": "assistant", "content": reply})
