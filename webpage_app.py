import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate, SystemMessagePromptTemplate, HumanMessagePromptTemplate
import streamlit as st

load_dotenv()
os.environ['GOOGLE_API_KEY'] = os.getenv('gemini_key')

st.title('Automatic Webpage Creation')

model = ChatGoogleGenerativeAI(
    model='gemini-2.5-flash'
)

description = st.text_area('Describe the type of webpage you want to create')
content = st.text_area('Post the content for webpage creation')

if st.button('Generate'):

    system_template = """
You are a Senior Frontend Developer.

Generate a COMPLETE SINGLE FILE HTML webpage.

Requirements:
- Everything must be inside ONE HTML file
- Include CSS inside <style>
- Include JavaScript inside <script>
- Clean modern UI
- Mobile responsive

Special Feature:
Create a Dynamic Quiz Assessment Webpage that includes:

1. Exactly 5 Multiple Choice Questions
2. Each question must have 4 options
3. Show score after submission
4. Show correct answers
5. Generate downloadable PDF report of results
6. Use JavaScript for quiz logic
7. Use html2pdf.js CDN for PDF generation

Return ONLY HTML code.
"""

    human_template = "Build a {description} using following content: {content}"

    system_message = SystemMessagePromptTemplate.from_template(system_template)
    human_message = HumanMessagePromptTemplate.from_template(human_template)

    web_dev_template = ChatPromptTemplate.from_messages([system_message, human_message])
    prompt = web_dev_template.invoke({
        'description': description,
        'content': content
    })

    response = model.invoke(prompt)

    html_code = response.content

    with open("index.html", "w", encoding="utf-8") as f:
        f.write(html_code)

    st.download_button(
        label="Download HTML Page",
        data=open("index.html", "rb"),
        file_name="index.html",
        mime="text/html"
    )

    st.success("Website Generated Successfully!")
