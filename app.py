import streamlit as st
from dotenv import load_dotenv
from PyPDF2 import PdfReader
from langchain.text_splitter import CharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores.chroma import Chroma
from langchain.memory import ConversationBufferMemory
from langchain.chains.conversational_retrieval.base import ConversationalRetrievalChain
from langchain.llms.huggingface_hub import HuggingFaceHub
from htmlTemplates import css, bot_template, user_template, spinner_html

def get_pdf_text(pdf_docs):
    text = ""
    for pdf in pdf_docs:
        pdf_reader = PdfReader(pdf)
        for page in pdf_reader.pages:
            text += page.extract_text()
    return text

def get_text_chunk(raw_text):
    text_splitter = CharacterTextSplitter(
        separator="\n",
        chunk_size=1000,
        chunk_overlap=200,
        length_function=len
    )
    text_chunks = text_splitter.split_text(raw_text)

    return text_chunks


def get_embeddings():
    embeddings = HuggingFaceEmbeddings(model_name='sentence-transformers/all-MiniLM-L6-v2')

    return embeddings

def create_vector_db(text_chunks, embeddings):
    vectordb = Chroma.from_texts(texts=text_chunks, embedding=embeddings, persist_directory="db")
    vectordb.persist()

    return vectordb

def create_conversation_chain(vectordb):

    llm = HuggingFaceHub(repo_id='google/flan-t5-large', model_kwargs={'temperature':0.5, 'max_length':512})

    memory = ConversationBufferMemory(memory_key='chat_history', return_messages=True)
    conversation_chain = ConversationalRetrievalChain.from_llm(
        llm=llm,
        retriever=vectordb,
        memory=memory
    )

    return conversation_chain

def handle_userinput(user_question):
    response = st.session_state.conversation({'question':user_question})
    st.session_state.chat_history=response['chat_history']

    for i, message in enumerate(st.session_state.chat_history):

        if i % 2 == 0:
            st.write(user_template.replace("{{MSG}}", message.content), unsafe_allow_html=True)
        else:
            st.write(bot_template.replace("{{MSG}}", message.content), unsafe_allow_html=True)

def main():
    load_dotenv()
    st.set_page_config(page_title="Chat with multiple PDFs", page_icon=":books:")
    st.write(css, unsafe_allow_html=True)

    if "conversation" not in st.session_state:
        st.session_state.conversation = None
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = None

    st.header("Chat with multiple PDFs :books:")
    user_question = st.text_input("Ask a question about your uploaded documents")

    if user_question:
        handle_userinput(user_question)

    with st.sidebar:
        st.subheader("Your documents")
        pdf_docs = st.file_uploader("Upload your PDFs here and click on 'Process'", accept_multiple_files=True)
        if st.button("Process"):
            # st.markdown(spinner_html, unsafe_allow_html=True)
            with st.spinner():
                # get pdf text:
                raw_text = get_pdf_text(pdf_docs)

                # get text chunks:
                text_chunks = get_text_chunk(raw_text)

                # get embeddings:
                embeddings = get_embeddings()

                # create vector database
                vectordb = create_vector_db(text_chunks, embeddings)

                # create conversation chain
                st.session_state.conversation = create_conversation_chain(vectordb.as_retriever())

if __name__ == '__main__':
    main()