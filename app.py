import streamlit as st
import os
import openai
from dotenv import load_dotenv
from fpdf import FPDF
import base64
from io import BytesIO
from reportlab.lib.pagesizes import letter, A4
from reportlab.pdfgen import canvas
import textwrap
import re
import emoji

# Load environment variables from the .env file
load_dotenv()

# Credentials
openai.organization = "org-HgO75LNERg28F4GqsY4AbfzW"
openai.api_key = os.getenv('OPENAI_API_KEY')

# Streamlit app layout
st.title("Chat with GPT-4")

# Use 'st.text_area' for a larger input field
user_message = st.text_area("Enter your message:", height=100)

EMOJI_PATTERN = re.compile(
    "[\U0001F1E0-\U0001F1FF"  # flags (iOS)
    "\U0001F300-\U0001F5FF"  # symbols & pictographs
    "\U0001F600-\U0001F64F"  # emoticons
    "\U0001F680-\U0001F6FF"  # transport & map symbols
    "\U0001F700-\U0001F77F"  # alchemical symbols
    "\U0001F780-\U0001F7FF"  # Geometric Shapes Extended
    "\U0001F800-\U0001F8FF"  # Supplemental Arrows-C
    "\U0001F900-\U0001F9FF"  # Supplemental Symbols and Pictographs
    "\U0001FA00-\U0001FA6F"  # Chess Symbols
    "\U0001FA70-\U0001FAFF"  # Symbols and Pictographs Extended-A
    "\U00002702-\U000027B0"  # Dingbats
    "]+"
)

# Register the Noto Emoji font
noto_emoji_font = "NotoEmoji-Regular.ttf"
face = describe.openFont(noto_emoji_font)
pdfmetrics.registerFont(TTFont(face.familyname, noto_emoji_font))


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

    text_object = pdf.beginText(10, 800)  # 10mm from the left, 800mm from the top
    text_object.setFillColor("black")

    wrapper = textwrap.TextWrapper(width=100)  # Adjust the width as needed
    lines = text.split("\n")
    for line in lines:
        wrapped_line = wrapper.fill(line)

        segments = emoji.emojize(wrapped_line)
        for segment in segments:
            if re.match(EMOJI_PATTERN, segment):
                pdf.setFont(face.familyname, 12)
            else:
                pdf.setFont("Helvetica", 12)
            text_object.textOut(segment)
        text_object.textLine()

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
