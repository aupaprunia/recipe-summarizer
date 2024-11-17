import streamlit as st

from summarizer import get_result

def display_result(url):
    result = get_result(url)
    st.markdown(result)

prompt = st.chat_input("Enter Youtube URL for a recipe")
if prompt:
    with st.chat_message("user"):
        st.write(prompt)
    display_result(prompt)