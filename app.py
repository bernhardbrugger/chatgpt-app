import streamlit as st
import os
import openai
from dotenv import load_dotenv

# Load environment variables from the .env file
load_dotenv()

# Credentials
openai.organization = os.getenv("__ORGANIZATION_ID")
openai.api_key = os.getenv("__API_KEY")

# Streamlit app layout
st.title("Chat with GPT-4")
user_message = st.text_input("Enter your message:")

if st.button("Send"):
    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "user", "content": user_message}
        ]
    )

    st.write(completion.choices[0].message["content"]) 
