sudo iptables -I INPUT 6 -m state --state NEW -p tcp --dport 8502 -j ACCEPT
cd ~/src/llama/llamaenv/bin
source activate
cd ~/src/GenAI-Demo-main
nohup streamlit run streamlit_app_oci.py &