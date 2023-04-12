import streamlit as st
import os
import openai
from dotenv import load_dotenv

# Load environment variables from the .env file
load_dotenv()

# Credentials
openai.organization = "org-HgO75LNERg28F4GqsY4AbfzW"
openai.api_key = os.getenv('OPENAI_API_KEY')

st.title("Chat with ChatGPT")
user_message = st.text_area("Enter your message:", height=100)

if st.button("Send"):
    with st.spinner('Processing...'):  # Loading animation
        completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "user", "content": user_message}
            ]
        )

    st.write(completion.choices[0].message["content"])
