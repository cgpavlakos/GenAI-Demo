# 🦙📚 LlamaIndex - Chat with the Streamlit docs

Demo RAG App for Oracle Cloud Generative AI. 

## Overview of the App

- Takes user queries via Streamlit's `st.chat_input` and displays both user queries and model responses with `st.chat_message`
- Uses LlamaIndex to load and index data and create a chat engine that will retrieve context from that data to respond to each user query

## Live Demo App

http://rag.pavlakos.me

## Get an OpenAI API key

You can get your own OpenAI API key by following the following instructions:
1. Go to https://platform.openai.com/account/api-keys.
2. Click on the `+ Create new secret key` button.
3. Next, enter an identifier name (optional) and click on the `Create secret key` button.

## Try out the demo

Instructions here
1. Make sure you have port 8502 open on security list
2. Launch a VM with ubuntu base image
3. SSH into it (ubuntu@ipaddress) and run setup.sh
4. Your app is running on http://<ipaddress>:8502
5. Replace contents of ~/src/GenAI-Demo-main/data with whatever other documents you want to have for this demo
6. Use run.sh to run the demo again after you have already created it