# llm
# 🤖 RAG Chatbot using LangChain, Gemini & Streamlit

This project is a Retrieval-Augmented Generation (RAG) chatbot built using LangChain, Google Gemini (via LangChain's GoogleGenerativeAI integration), and Streamlit. It supports document upload (PDF, DOCX, TXT) and web URL scraping for context-aware Q&A.

---

Features

 Upload multiple documents (`.pdf`, `.docx`, `.txt`)
 Scrape and load content from URLs
 Vector storage using Chroma DB
 Context-aware Q&A using Gemini 1.5 Flash
Modular code split into multiple files
 Simple and intuitive Streamlit interface

---

File Structure

├── app.py # Streamlit frontend
├── loader.py # Document loading and web scraping
├── vectorstore.py # Embedding and vector DB setup
├── rag_chain.py # Prompt templates and chain construction
├── utils.py # Helper utilities (cleanup, etc.)
├── .env # Environment variables (API keys)
├── docs/ # Folder for loaded/scraped documents
├── .chroma_db/ # Vector database files
└── README.md # This file

yaml
Copy
Edit


