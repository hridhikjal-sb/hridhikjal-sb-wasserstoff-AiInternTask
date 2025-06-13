import streamlit as st
import os
from dotenv import load_dotenv
from langchain_core.messages import HumanMessage, AIMessage
import atexit
import shutil
from loader import load_documents, scrape_and_save
from vectorstore import build_vectorstore
from rag_chain import build_rag_chain
from utils import clear_folder, delete_text_files

# Load environment variables
load_dotenv()
os.environ["GOOGLE_API_KEY"] = os.getenv("GOOGLE_API_KEY")
print("GOOGLE_API_KEY found:", os.getenv("GOOGLE_API_KEY") is not None)

# Prepare document folder
FOLDER_PATH = "docs"
os.makedirs(FOLDER_PATH, exist_ok=True)
clear_folder(FOLDER_PATH)
atexit.register(delete_text_files, FOLDER_PATH)

st.set_page_config(page_title="RAG Chatbot", page_icon="🤖")
st.title("RAG Chatbot with LangChain & Gemini")

file_type = st.radio("Choose input type:", ["document", "url"])

if "last_file_type" not in st.session_state:
    st.session_state.last_file_type = file_type

if file_type != st.session_state.last_file_type:
    clear_folder(FOLDER_PATH)
    if os.path.exists('.chroma_db'):
        shutil.rmtree('.chroma_db', ignore_errors=True)
    for key in ["docs", "chat_history", "vectorstore", "retriever", "rag_chain"]:
        st.session_state.pop(key, None)
    st.session_state.last_file_type = file_type

if file_type == "document":
    uploaded_files = st.file_uploader("Upload documents (.pdf, .docx, .txt)", type=["pdf", "docx", "txt"], accept_multiple_files=True)
    if uploaded_files:
        for file in uploaded_files:
            with open(os.path.join(FOLDER_PATH, file.name), "wb") as f:
                f.write(file.read())
        st.session_state.docs = load_documents(FOLDER_PATH)
        st.success(f"Loaded {len(st.session_state.docs)} documents.")

elif file_type == "url":
    urls_input = st.text_area("Enter URLs (comma separated):")
    if st.button("Scrape URLs") and urls_input:
        urls = [url.strip() for url in urls_input.split(",") if url.strip()]
        scrape_and_save(urls, FOLDER_PATH)
        st.session_state.docs = load_documents(FOLDER_PATH)
        st.success(f"Scraped and loaded {len(st.session_state.docs)} documents.")

if "docs" in st.session_state:
    vectorstore, retriever = build_vectorstore(st.session_state.docs)
    rag_chain = build_rag_chain(retriever)
    st.session_state.rag_chain = rag_chain

    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    user_question = st.text_input("Ask your question:")
    if st.button("Submit") and user_question:
        result = rag_chain.invoke({"input": user_question, "chat_history": st.session_state.chat_history})
        st.session_state.chat_history.extend([
            HumanMessage(content=user_question),
            AIMessage(content=result['answer'])
        ])
        st.markdown(f"**You:** {user_question}")
        st.markdown(f"**Assistant:** {result['answer']}")
else:
    st.warning("No documents found. Did you scrape URLs or upload files?")