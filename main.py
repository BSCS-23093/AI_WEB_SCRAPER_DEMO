import streamlit as st
from scrap_page import scrape_webpage, extract_body, cleanze_body, split_dom_content
from llm_rag import parse_with_gemini
from dotenv import load_dotenv
import os

st.title('AI WebScraper')
url = st.text_input('Enter URL')
if st.button('Scrape'):
    st.write('Scraping...')
    result = scrape_webpage(url)
    body = extract_body(result)
    cleaned_body = cleanze_body(body)
    st.session_state.dom_content = cleaned_body
    with st.expander('View DOM Content'):
        st.text_area('DOM Content', cleaned_body, height=300)
    st.write('Done')

if "dom_content" in st.session_state:
    user_prompt = st.text_area("Tell me what do you want to parse?")
    if st.button("Parse"):
        if user_prompt:
            st.write("Parsing...")
            chunks = split_dom_content(st.session_state.dom_content)
            result = parse_with_gemini(chunks,user_prompt)
            st.write(result)