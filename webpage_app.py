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
You are a Senior Frontend Web Developer with 10+ years experience in HTML5, CSS3, and modern JavaScript (ES6+).

Your task: Generate COMPLETE, PRODUCTION-READY frontend code based on user requirements.

Rules:
1. Generate EVERYTHING in ONE single HTML file.
2. Include CSS inside <style> tag.
3. Include JavaScript inside <script> tag.
4. The webpage must be clean, modern, responsive and interactive.
5. Use semantic HTML structure.
6. Do NOT generate separate CSS or JS files.
7. Return ONLY the HTML code.

Structure example:

<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<title>Generated Webpage</title>

<style>
/* CSS code here */
</style>

</head>

<body>

<!-- HTML content -->

<script>
// JavaScript code here
</script>

</body>
</html>
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
        label="Download HTML File",
        data=open("index.html", "rb"),
        file_name="index.html",
        mime="text/html"
    )

    st.success("Webpage Generated Successfully!")
