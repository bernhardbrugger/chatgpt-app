import streamlit as st
import os
import openai


openai.organization = os.getenv("org-HgO75LNERg28F4GqsY4AbfzW")
openai.api_key = os.getenv("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")


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
