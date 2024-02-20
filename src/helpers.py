from langchain_core.messages import AIMessage, HumanMessage
from langchain_community.document_loaders import WebBaseLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.chains import create_history_aware_retriever, create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from dotenv import load_dotenv
import streamlit as st
 
load_dotenv()





def get_context_retriever_chain(vector_store):
    llm= ChatOpenAI()
    retriever= vector_store.as_retriever()
    prompt= ChatPromptTemplate.from_messages([
        MessagesPlaceholder(variable_name= "chat_history"),
        ("user", "{input}"),
        ("user","Given the above conversation, generate a search quesry to look up in order to get information relevant to the conversation")
    ])
    retriever_chain= create_history_aware_retriever(llm, retriever, prompt)
    return retriever_chain



def get_vectorstore_from_url(url):

    #Get the text in documetn form 
    loader= WebBaseLoader(url)
    document= loader.load()

    text_splitter= RecursiveCharacterTextSplitter()
    document_chunks= text_splitter.split_documents(document)

    # Create a vectorstore
    vector_store= Chroma.from_documents(document_chunks, OpenAIEmbeddings())
    return vector_store

def get_convo_rag_chain(retriever_chain):
    print("INSIDE RAG CONVO CHAIN")
    llm= ChatOpenAI()
    prompt= ChatPromptTemplate.from_messages([
        ("system", "Answer the user's question based on the below context: \n\n{context}"),
        MessagesPlaceholder(variable_name="chat_history"),
        ("user", "{input}")
    ])
    
    stuff_documents_chain= create_stuff_documents_chain(llm, prompt)
    print("STUFFING COMPLETE")

    return create_retrieval_chain(retriever_chain, stuff_documents_chain)
         

