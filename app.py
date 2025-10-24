# Import necessary libraries
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_ollama import OllamaLLM


import streamlit as st
import os
from dotenv import load_dotenv
import sys

 first
load_dotenv()



# Prefer either LANGCHAIN_API_KEY or lang_chain_api_key in .env; avoid assigning None
_api_key = os.getenv('lang_chain_api_key') or os.getenv('LANGCHAIN_API_KEY')
if _api_key:
    # strip possible surrounding quotes from .env value
    _api_key = _api_key.strip().strip('"').strip("'")
    os.environ['LANGCHAIN_API_KEY'] = _api_key

# Enable tracing flag (fixed typo)
os.environ['LANGCHAIN_TRACING_V2'] = 'true'

#PROMT TEMPLATE
prompt=ChatPromptTemplate.from_messages(
    [
        ('system','you are a helpful assistant. please respond to the user queries'),
        ('user','question:{question}')
    ]
)
#streamlit app
st.title('langchain demo with ollama api')
input_text=st.text_input('enter your question here')

#llm
llm = OllamaLLM(model='gpt-oss')
output_parser=StrOutputParser()


#chain
chain=prompt|llm|output_parser

if input_text:
    st.write(chain.invoke({'question':input_text}))