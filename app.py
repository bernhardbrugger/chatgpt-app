import streamlit as st
import os
import openai

# Credentials
openai.organization = "org-HgO75LNERg28F4GqsY4AbfzW"
openai.api_key = os.environ.get('OPENAI_API_KEY')

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
