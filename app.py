import streamlit as st
import os
import openai
from dotenv import load_dotenv
from fpdf import FPDF
import base64
from io import BytesIO

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
    buffer = BytesIO()
    pdf = canvas.Canvas(buffer, pagesize=A4)

    pdf.setFont("Helvetica", 12)
    text_object = pdf.beginText(10, 800)  # 10mm from the left, 800mm from the top
    text_object.setFillColor("black")

    lines = text.split("\n")
    for line in lines:
        text_object.textLine(line)

    pdf.drawText(text_object)
    pdf.showPage()
    pdf.save()
    
    buffer.seek(0)
    return buffer.read()

def download_button(file_data, file_name, button_text):
    b64 = base64.b64encode(file_data).decode()
    href = f'<a href="data:application/octet-stream;base64,{b64}" download="{file_name}">{button_text}</a>'
    st.markdown(href, unsafe_allow_html=True)

if response:
    # PDF Download
    pdf_data = create_pdf(response)
    download_button(pdf_data, "generated_text.pdf", "Download as PDF")
