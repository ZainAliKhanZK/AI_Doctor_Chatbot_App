import os
import streamlit as st
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

api_key = os.getenv("HF")

client = OpenAI(
    base_url="https://router.huggingface.co/v1",
    api_key=api_key,
)

st.title("Your Personal AI Doctor 🤖🩺")

user_input = st.text_input("Tell me about your health:")

if st.button("Send"):
    with st.spinner("Ummmm...⏳"):
        completion = client.chat.completions.create(
            model="moonshotai/Kimi-K2-Instruct-0905",
            messages=[
                {
                "role": "system",
                "content": (
                    "You are a helpful and friendly medical assistant."
                    "Do not include any medical advice that could be harmful."
                    "Do not answer any questions that are not related to health."
                    "Say sorry if user asks for adult advise."
                    "Keep the responses well structured and clear." 
                )
                },

                {
                "role": "user", 
                "content": user_input
                }
            ],
        )

    st.write(completion.choices[0].message.content)