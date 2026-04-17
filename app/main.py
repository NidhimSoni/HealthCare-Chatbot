# LETS IMPORT THE LIBRARIES
import os
from dotenv import load_dotenv
from pdfextractor import text_extractor
import streamlit as st
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_community.embeddings import HuggingFaceBgeEmbeddings
from pypdf import PdfReader
from langchain_text_splitters import RecursiveCharacterTextSplitter  # for chunking
import faiss
from langchain_community.vectorstores import FAISS

import warnings
warnings.filterwarnings('ignore')

load_dotenv()

# LETS NOW CONFIGURE EMBEDDING MODEL
embedding_model =  HuggingFaceBgeEmbeddings(model_name='all-MiniLM-L6-v2')

# lets create the main page

st.title(':orange[CHATBOT:] :blue[AI ASSISTED CHATBOT USING RAG ]')
tips = '''
Follow the steps to use the Application :
1) Upload Your PDFs in the sidebar
2) write a query and start the chat.
'''
st.text(tips)

llm = ChatGoogleGenerativeAI(model = 'gemini-2.5-flash',temperature = 0)
# LETS CREATE THE SIDEBAR

st.sidebar.title(':green[UPLOAD YOUR FILES]')
st.sidebar.subheader(':rainbow[Upload PDF Files only.]')
pdf_file = st.sidebar.file_uploader('UPLOAD HERE',type=['pdf'],accept_multiple_files=True)
if pdf_file:
    st.sidebar.success('FILE UPLOADED SUCCESSFULLY')

    all_text = " "
    files = pdf_file if isinstance(pdf_file,list) else [pdf_file]
    for file in files:
        all_text += text_extractor(file)
    # STEP 1 : CHUNKING
    splitter = RecursiveCharacterTextSplitter(chunk_size = 1000,chunk_overlap = 200)
    chunks = splitter.split_text(all_text)

    # STEP 2 : CREATE THE vector database
    metadatas = [{"Sources":"uploaded_file",'page': i} for i in range(len(chunks))]
    vector_store = FAISS.from_texts(chunks,embedding_model,metadatas=metadatas)
    retriever = vector_store.as_retriever(search_kwargs={'k':3})

    def generate_content(query):
        # STEP 3 : Retrieval (R)
        retrieved_docs = retriever.invoke(query)
        context = '\n'.join([d.page_content for d in retrieved_docs])

        # STEP 4 : AUGMENTING(A)
        augmented_prompt = f'''
<Role> You are a helpful assistant using RAG.
<Goal> Answer the question asked by the user. Here is the question {query} 
<Context> Here are the documents retrieved from the vector database to support the answer which you have to generate
{context}
<Purpose> Your main task is to read the document completely without missing anything important and give 
the answers to the queries asked by user.
Don't give any false information if you dont know anything don't give answer to that just say you don't know'''
        
        # STEP 5 : GENERATE (G)
        response = llm.invoke(augmented_prompt)
        sources = []
        for doc in retrieved_docs:
            sources.append(doc.metadata)
        return response.content,sources
    # CREATE CHATBOT IN ORDER TO START A CONVERASATION
    # To INITIALIZE A CHAT CREATE HISTORY IF NOT CREATED
    if 'history' not in st.session_state:
        st.session_state.history = []
    
    # WE NEED TO DISPLAY THE HISTORY
    for msg in st.session_state.history:
        if msg['role']== 'user':
            st.info(f":green[USER:] :blue[{msg['text']}]")
        else:
            st.success(f":orange[CHATBOT:] :blue[{msg['text']}]")
    
    # INPUT FROM THE USER USING STREAMLIT FEATURES
    with st.form('CHATBOT FORM',clear_on_submit=True):
        user_query = st.text_area('ASK ANYTHING: ')
        send = st.form_submit_button('ASK')

    # now WE HAVE TO START THE CONVERSATION AND APPEND THE OUTPUT AND QUERY IN HISTORY
    if user_query and send:
        with st.spinner('CHATBOT IS THINKING...'):

            st.session_state.history.append({'role':'user',
                                            'text':user_query})
            
            answer,sources =generate_content(user_query)
            source_text = '\n'.join([f"- {s.get('source','unknown')} (page{s.get('page','?')})"
                                     for s in sources])
            final_output = f"{answer}\n\n Sources : \n{source_text}"
            st.session_state.history.append({'role':'chatbot',
                                            'text':final_output})
            st.rerun()