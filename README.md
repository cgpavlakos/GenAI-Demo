# 🦙📚 LlamaIndex - RAG Chat 

Demo RAG App for Oracle Cloud Generative AI. No longer being developed. 

## Overview of the App

- Takes user queries via Streamlit's `st.chat_input` and displays both user queries and model responses with `st.chat_message`
- Uses LlamaIndex to load and index data and create a chat engine that will retrieve context from that data to respond to each user query

## Live Demo App

No longer live. Please see https://github.com/cgpavlakos/genai_agent/ for an improved version. 


## Try out the demo

Instructions here
1. Make sure you have port 8502 open on security list
2. Launch a VM with ubuntu base image
3. SSH into it (ubuntu@ipaddress) and run setup.sh
4. Your app is running on http://ipaddress:8502
5. Replace contents of ~/src/GenAI-Demo-main/data with whatever other documents you want to have for this demo
6. Use run.sh to run the demo again after you have already created it


## Instructions for other SEs: 

1. Create VM using Canonical Ubuntu 22.04 platform image
2. attach `rag-demo-setup.sh` as cloud-init script - talk to Chris if you need this
3. ssh in and check setup log with `tail -f llama_setup.log`
4. when its done, your application will be running on `ipaddress:8502`

to customize: replace the PDFs in ~/src/GenAI-Demo-main/docs

If you get `ValidationError: 1 validation error for OCIGenAIEmbeddings __root__ Could not authenticate with OCI client` then there is an issue with the oci credentials, easy to fix:

1. `sudo reboot`
2. `cd ~/src/GenAI-Demo-main`
3. `sudo chmod +x run.sh`
4. `./run.sh`
