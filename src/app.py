import streamlit as st
from langchain_core.messages import AIMessage, HumanMessage
from langchain.chains import create_history_aware_retriever 
from helpers import  get_vectorstore_from_url, get_context_retriever_chain, get_convo_rag_chain


# ApP Config
st.set_page_config(page_title="Chat With websites", page_icon=":round_pushpin:")
st.title("Chat with websites")

def get_response(user_query):
    # Create conversation chain
    retriever_chain= get_context_retriever_chain(st.session_state.vector_store)

    conversation_rag_chain= get_convo_rag_chain(retriever_chain)
    
    # response= get_response(user_query)
    response= conversation_rag_chain.invoke({
            "chat_history": st.session_state.chat_history,
            "input": user_query
        })
    
    return response["answer"]
# Sidebar
with st.sidebar:
    st.header("settings")
    website_url= st.text_input("Website URL")

if website_url is None or website_url == "":
    st.info("Please enter a website URL")
else:
    if "chat_history" not in st.session_state:
        st.session_state.chat_history= [
            AIMessage(content= "Hello, I am a bot, How can I help?")
    ]
        # Clear vector_store if website_url is different from the current one
    if "vector_store" in st.session_state and st.session_state.vector_store.get("url") != website_url:
        del st.session_state.vector_store
        
    
    if "vector_store" not in st.session_state:
        st.session_state.vector_store= get_vectorstore_from_url(website_url)

    st.info(f"Chatting with {website_url}")

    # User Input
    user_query= st.chat_input("Type your message")

    if user_query is not None and user_query !="":
        response= get_response(user_query)
        
        st.session_state.chat_history.append(HumanMessage(content=user_query))
        st.session_state.chat_history.append(AIMessage(content= response))
        
        
        

    # conversation
    for message in st.session_state.chat_history:
        if isinstance(message, AIMessage):
            with st.chat_message("AI"):
                st.write(message.content)
        elif isinstance(message, HumanMessage):
            with st.chat_message("Human"):
                st.write(message.content)    