__import__('pysqlite3')
import sys
sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')
import sqlite3

import streamlit as st
from langchain_core.messages import AIMessage, HumanMessage
from langchain.chains import create_history_aware_retriever 
from helpers import  get_vectorstore_from_url, get_context_retriever_chain, get_convo_rag_chain, get_response


# ApP Config
st.set_page_config(page_title="Chat With websites", page_icon=":round_pushpin:")
st.title("Chat with websites")


# Sidebar
with st.sidebar:
    st.header("settings")
    website_url= st.text_input("Website URL")

if website_url is None or website_url == "":
    st.info("Please enter a website URL")
else:
    st.info(f"Chatting with {website_url}")
    if "website_data" not in st.session_state or st.session_state.website_data.get("url") != website_url:
        st.session_state.website_data = {
            "url": website_url,
            "vector_store": get_vectorstore_from_url(website_url),
            "chat_history": [AIMessage(content="Hello, I am a bot, How can I help?")]
        }
        
    # User Input
    user_query= st.chat_input("Type your message")

    if user_query is not None and user_query !="":
        response = get_response(user_query, st.session_state.website_data["vector_store"], st.session_state.website_data["chat_history"])
        
        st.session_state.website_data["chat_history"].append(HumanMessage(content=user_query))
        st.session_state.website_data["chat_history"].append(AIMessage(content=response))
        
        
        

    # conversation
    for message in st.session_state.website_data["chat_history"]:
        if isinstance(message, AIMessage):
            with st.chat_message("AI"):
                st.write(message.content)
        elif isinstance(message, HumanMessage):
            with st.chat_message("Human"):
                st.write(message.content)    