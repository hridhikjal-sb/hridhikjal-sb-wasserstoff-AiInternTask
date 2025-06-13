from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains import create_history_aware_retriever, create_retrieval_chain
from langchain_google_genai import GoogleGenerativeAI
from langchain_google_genai import GoogleGenerativeAI, GoogleGenerativeAIEmbeddings

llm = GoogleGenerativeAI(model="gemini-1.5-flash")

def build_rag_chain(retriever):
    context_q_system_prompt = """
    Given a chat history and latest user question which might reference context in chat history,
    formulate a standalone question which can be understood without the chat history.
    Do not answer the question, just rephrase it if needed.
    """

    context_q_prompt = ChatPromptTemplate.from_messages([
        ("system", context_q_system_prompt),
        MessagesPlaceholder(variable_name="chat_history"),
        ("human", "{input}")
    ])

    history_aware_retriever = create_history_aware_retriever(llm, retriever, context_q_prompt)

    qa_prompt = ChatPromptTemplate.from_messages([
        ("system", "You are a helpful AI assistant. Use the following context to answer the user's question."),
        ("system", "Context: {context}"),
        MessagesPlaceholder(variable_name="chat_history"),
        ("human", "{input}")
    ])

    question_answer_chain = create_stuff_documents_chain(llm, qa_prompt)
    return create_retrieval_chain(history_aware_retriever, question_answer_chain)

