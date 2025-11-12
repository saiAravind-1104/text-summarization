import os
from dotenv import load_dotenv
import streamlit as st
import validators 
from langchain_core.prompts import PromptTemplate
from langchain.chains.summarize import load_summarize_chain
from langchain_groq import ChatGroq
from langchain_community.document_loaders import UnstructuredURLLoader,YoutubeLoader
from langchain.docstore.document import Document


st.set_page_config(page_title="Text Summarization", page_icon="🔍")
st.title("Text Summarization 🔍📄")

# Sidebar
with st.sidebar:
    st.session_state.key = st.text_input(
        placeholder="Please enter your Groq API key", 
        label="Groq API key", 
        type="password"
    )

url = st.text_input(placeholder="Please enter your URL here", label="URL Link",label_visibility="collapsed")
button = st.button(label="Summarize")

# Prompt
template = '''
Summarize this text and give a 200-word response:

{text}
'''

prompt = PromptTemplate(template=template, input_variables=["text"])



if button:
    if not st.session_state.key or not url:
        st.error("Please enter Groq key and URL")
    elif not validators.url(url):
        st.error("Please provide a valid URL")
    else:
        llm = ChatGroq(
            api_key=st.session_state.key,
            model_name="llama-3.1-8b-instant"
        )

        with st.spinner("Processing..."):

            # YouTube Case
            if "youtube.com" in url or "youtu.be" in url:
                loader=YoutubeLoader(urladd_video_info=True)
                docs = loader.load()

            # Normal URL Case
            else:
                loader = UnstructuredURLLoader(urls=[url], ssl_verify=False)
                docs = loader.load()

            if not docs:
                st.error("Unable to extract content from the URL.")
            else:
                chain = load_summarize_chain(
                    llm=llm,
                    chain_type="stuff",
                    prompt=prompt
                )

                response = chain.run(docs)

                st.success("Summary generated:")
                st.write(response)
