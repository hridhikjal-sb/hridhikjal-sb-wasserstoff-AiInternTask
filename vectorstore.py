from langchain_chroma import Chroma
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_google_genai import GoogleGenerativeAI, GoogleGenerativeAIEmbeddings


embedding_function = GoogleGenerativeAIEmbeddings(model="models/embedding-001")

def build_vectorstore(docs, persist_dir='.chroma_db'):
    splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    splits = splitter.split_documents(docs)
    vectorstore = Chroma.from_documents(
        collection_name="my_collection",
        documents=splits,
        embedding=embedding_function,
        persist_directory=persist_dir
    )
    return vectorstore, vectorstore.as_retriever(search_kwargs={"k": 2})
