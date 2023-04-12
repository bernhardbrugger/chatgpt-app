import streamlit as st
import os
import openai
from dotenv import load_dotenv
from fpdf import FPDF
import base64

# Load environment variables from the .env file
load_dotenv()

# Credentials
openai.organization = "org-HgO75LNERg28F4GqsY4AbfzW"
openai.api_key = os.getenv('OPENAI_API_KEY')

# Streamlit app layout
st.title("Chat with GPT-4")

# Use 'st.text_area' for a larger input field
user_message = st.text_area("Enter your message:", height=100)

response = None
if st.button("Send"):
    with st.spinner('Processing...'):  # Loading animation
        completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "user", "content": user_message}
            ]
        )

    response = completion.choices[0].message["content"]
    st.write(response)

def create_pdf(text: str) -> bytes:
    pdf = FPDF(orientation='P', unit='mm', format='A4')
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.multi_cell(0, 10, text)
    pdf_out = pdf.output(dest='S').encode('latin1', 'replace')  # Replace the characters that cannot be encoded
    return pdf_out

def download_button(file_data, file_name, button_text):
    b64 = base64.b64encode(file_data).decode()
    href = f'<a href="data:application/octet-stream;base64,{b64}" download="{file_name}">{button_text}</a>'
    st.markdown(href, unsafe_allow_html=True)

if response:
    # PDF Download
    pdf_data = create_pdf(response)
    download_button(pdf_data, "generated_text.pdf", "Download as PDF")
