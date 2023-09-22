from dotenv import load_dotenv
from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings import  HuggingFaceEmbeddings
from langchain.llms import HuggingFaceHub
from langchain.document_loaders import PyPDFLoader
from langchain.vectorstores import FAISS
from langchain.chains import ConversationalRetrievalChain
from sonic.settings import BASE_DIR
from .models import Question
import os

load_dotenv()


def chat_response(file, query, id):
    loader = PyPDFLoader(os.path.join(
                    BASE_DIR, "media", str(file)
                ))
    data = loader.load()
    text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    docs = text_splitter.split_documents(data)
    print(len(docs))
    embeddings = HuggingFaceEmbeddings(model_name='sentence-transformers/all-MiniLM-L6-v2')
    db = FAISS.from_texts(
        [t.page_content for t in docs],
        embedding=embeddings,

    )
    llm = HuggingFaceHub(repo_id="google/flan-t5-xxl", model_kwargs={"temperature": 0.7, "max_length": 1024})
    qa_chain = ConversationalRetrievalChain.from_llm(
        llm=llm,
        retriever=db.as_retriever(search_kwargs={'k': 6}),
        return_source_documents=True,
        verbose=False
    )

    chat_history = []
    result = qa_chain({'question': query, 'chat_history': chat_history})
    print(result['answer'])
    question = Question(question=query, pdf_file_id=id)
    question.save()
    return result['answer']