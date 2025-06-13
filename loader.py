from langchain_community.document_loaders import PyPDFLoader, Docx2txtLoader
from langchain.document_loaders import TextLoader
from typing import List
from langchain_core.documents import Document
import os
import requests
from bs4 import BeautifulSoup
from langchain_google_genai import GoogleGenerativeAI, GoogleGenerativeAIEmbeddings


def load_documents(folder_path: str) -> List[Document]:
    documents = []
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        if filename.endswith('.pdf'):
            loader = PyPDFLoader(file_path)
        elif filename.endswith('.docx'):
            loader = Docx2txtLoader(file_path)
        elif filename.endswith('.txt'):
            loader = TextLoader(file_path, encoding='utf-8')
        else:
            continue
        documents.extend(loader.load())
    return documents


def scrape_and_save(urls: List[str], save_folder: str):
    for i, url in enumerate(urls):
        try:
            response = requests.get(url)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')
            text = soup.get_text(separator='\n', strip=True)
            filename = os.path.join(save_folder, f"page_{i+1}.txt")
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(text)
        except Exception as e:
            print(f"Error scraping {url}: {e}")
