# Import necessary libraries
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_ollama import OllamaLLM


import streamlit as st
import os
from dotenv import load_dotenv
import sys

# If the user runs this file with `python app.py` Streamlit will warn repeatedly
# because there's no ScriptRunContext. Detect that case early and exit with a
# helpful message. When run with `streamlit run app.py` the ScriptRunContext
# will be present and the app continues as normal.
try:
    # streamlit 1.12+ provides this helper
    from streamlit.runtime.scriptrunner import get_script_run_ctx
except Exception:
    # older/newer streamlit or import failure — treat as no context available
    def get_script_run_ctx():
        return None

# Load environment variables from .env file
# Load .env into environment first
load_dotenv()

# If executed directly with `python app.py`, there's no Streamlit run context
# and the app will produce many "missing ScriptRunContext" warnings. Exit
# early with instructions so the user can run the app correctly.
if __name__ == "__main__":
    try:
        ctx = get_script_run_ctx()
    except Exception:
        ctx = None
    if ctx is None:
        print("This application must be started with Streamlit. Run:\n  streamlit run app.py")
        sys.exit(0)

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