import streamlit as st
from dotenv import load_dotenv
from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings, HuggingFaceInstructEmbeddings
from langchain.vectorstores import FAISS
from langchain.chat_models import ChatOpenAI
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain
from langchain.llms import HuggingFaceHub
from langchain.document_loaders import PyPDFLoader
from langchain.vectorstores import Chroma
from langchain.llms import GPT4All
from langchain.chains import RetrievalQA
import os


def text_extractor(file):
    loader = PyPDFLoader(str(file))
    data = loader.load()
    text_splitter = CharacterTextSplitter(separator='\n', chunk_size=500, chunk_overlap=100)
    docs = text_splitter.split_documents(data)
    text = [t.page_content for t in docs]
    return text

def get_vectorstore(text_chunks):
    embeddings = HuggingFaceInstructEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    vectorstore = FAISS.from_texts(text_chunks, embeddings)
    print('f1done')
    return vectorstore

def get_conversation_chain(vectorstore, query):
    llm = HuggingFaceHub(repo_id="google/flan-t5-xxl", model_kwargs={"temperature":0.5, "max_length":512}, huggingfacehub_api_token='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')
    memory = ConversationBufferMemory(memory_key='chat_history', return_messages=True)
    pdf_qa = ConversationalRetrievalChain.from_llm(llm=llm,
                                                   retriever=vectorstore.as_retriever(search_kwargs={'k': 6}),
                                                   verbose=False, memory=memory)
    res = pdf_qa({"question": query})
    return res["answer"]



