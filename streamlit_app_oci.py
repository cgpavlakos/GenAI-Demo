#inspired by https://llamaindex-chat-with-docs.streamlit.app

import streamlit as st
import openai
from llama_index.llms.openai import OpenAI
try:
  from llama_index import VectorStoreIndex, ServiceContext, Document, SimpleDirectoryReader
except ImportError:
  from llama_index.core import VectorStoreIndex, ServiceContext, Document, SimpleDirectoryReader

##OCI imports
from langchain_community.llms import OCIGenAI
from langchain_community.embeddings import OCIGenAIEmbeddings
from llama_index.llms.langchain import LangChainLLM
from llama_index.core import Settings
import oci 

# todo: make llm selection configurable

#use cohere on OCI generative AI as embedding model
Settings.embed_model=OCIGenAIEmbeddings(
    model_id="cohere.embed-english-v3.0",
    service_endpoint="https://inference.generativeai.us-chicago-1.oci.oraclecloud.com",
    compartment_id=st.secrets.compartment_id
    )


# Settings.llm=OCIGenAI(
#    model_id="cohere.command",
#    service_endpoint="https://inference.generativeai.us-chicago-1.oci.oraclecloud.com",
#    compartment_id=st.secrets.compartment_id,
#    model_kwargs={"max_tokens":800,"temperature":0.7,"prompt":"You are an expert on Oracle Cloud and your job is to answer technical questions. Assume that all questions are related to the Oracle Cloud. Keep your answers technical and based on facts – do not hallucinate features."} 
# ) 



# Settings.llm=OCIGenAI(
#    model_id="cohere.command-light",
#    service_endpoint="https://inference.generativeai.us-chicago-1.oci.oraclecloud.com",
#    compartment_id=st.secrets.compartment_id,
#    model_kwargs={"max_tokens":800,"temperature":0.7,"prompt":"You are an expert on Oracle Cloud and your job is to answer technical questions. Assume that all questions are related to the Oracle Cloud. Keep your answers technical and based on facts – do not hallucinate features."} 
# ) 

#use llama on OCI generative as LLM
Settings.llm=OCIGenAI(
    model_id="meta.llama-2-70b-chat",
    service_endpoint="https://inference.generativeai.us-chicago-1.oci.oraclecloud.com",
    compartment_id=st.secrets.compartment_id,
    #### update prompt to your use case
    model_kwargs={"max_tokens":800,"temperature":0.7,"prompt":"You are an expert on Oracle Cloud and your job is to answer technical questions. Assume that all questions are related to the Oracle Cloud. Keep your answers technical and based on facts – do not hallucinate features. Do not ask follow up questions."} 
)



st.set_page_config(page_title="Chat with your docs, powered by OCI Generative AI", page_icon="🤖", layout="centered", initial_sidebar_state="collapsed", menu_items=None)
# openai.api_key = st.secrets.openai_key
st.title("Demo: Private and Secure RAG Chat")
st.subheader("Powered by OCI Generative AI and LlamaIndex")
st.info("Check out the [architecure diagram](https://objectstorage.us-chicago-1.oraclecloud.com/n/axuvcnsxqjy5/b/RAG-Demo/o/RAG_Architecture.png) and [sequence diagram](https://objectstorage.us-chicago-1.oraclecloud.com/n/axuvcnsxqjy5/b/RAG-Demo/o/RAG_Sequence_Diagram.png) to see how OCI Generative AI, Streamlit, and LlamaIndex come together for this demo of a fully secure and private RAG chatbot.", icon="📃")

if "messages" not in st.session_state.keys(): # Initialize the chat messages history
    st.session_state.messages = [
        {"role": "assistant", "content": "Ask me a question about your private documents!"}
    ]

@st.cache_resource(show_spinner=False)
def load_data():
    with st.spinner(text="Loading and indexing the private documents – hang tight! This may take 1-2 minutes."):
        reader = SimpleDirectoryReader(input_dir="./data", recursive=True)
        docs = reader.load_data()
        index = VectorStoreIndex.from_documents(docs)
        return index

index = load_data()

if "chat_engine" not in st.session_state.keys(): # Initialize the chat engine
        st.session_state.chat_engine = index.as_chat_engine(chat_mode="condense_question", verbose=True)
        #accepts condense_question, react, openai, best, condense_plus_context, condense_question
        #st.session_state.chat_engine = index.as_chat_engine(chat_mode="react", verbose=True)

if prompt := st.chat_input("Your question"): # Prompt for user input and save to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})

for message in st.session_state.messages: # Display the prior chat messages
    with st.chat_message(message["role"]):
        st.write(message["content"])

#add button to clear chat
with st.sidebar:
    #st.button("Reset Chat", type="primary", on_click=st.session_state.messages.clear, help="Clear Chat History",use_container_width=True)
    st.button("Reset Chat", type="primary", help="Clear Chat History",use_container_width=True)
    st.write("This demo site was created by chris.pavlakos@oracle.com to showcase Oracle Cloud's Generative AI offerings and how a RAG chatbot can be deployed completely within a customer's tenancy.")
    # st.write("This demo uses Oracle Generative AI service, the VM-hosted python app uses Streamlit and LlamaIndex. The document base is Oracle Cloud documentation and pricing.")
    st.write("Default configuration is llama-2-70b-chat for llm and cohere-embed-v3.0 for embedding.")
    st.write("It can also use cohere.command, cohere.command-light, OpenAI, Gemini, or any custom model. These will be selectable in the UI in a future release along with hyperparameter tuning.")

# If last message is not from assistant, generate a new response
if st.session_state.messages[-1]["role"] != "assistant":
    with st.chat_message("assistant"):
        with st.spinner("Processing..."):
            response = st.session_state.chat_engine.chat(prompt)
            st.write(response.response)
            message = {"role": "assistant",  "content": response.response}
            st.session_state.messages.append(message) # Add response to message history