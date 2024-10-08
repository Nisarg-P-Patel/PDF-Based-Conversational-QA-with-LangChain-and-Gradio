# -*- coding: utf-8 -*-
"""PDF Based QA Chatbot.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1UmsZG-EqRb0BrKgn8iSoEt-Q-qG3tISG
"""

!pip install transformers langchain langchain_community gradio torch sentence-transformers faiss-cpu pypdf

from huggingface_hub import login
from google.colab import userdata

login(token=userdata.get('HF_KEY'))

import gradio as gr
from transformers import pipeline, AutoModelForCausalLM, AutoTokenizer
from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationBufferMemory
from langchain_community.vectorstores import FAISS
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain.llms import HuggingFacePipeline
import tempfile
import os
import tqdm

# Load the LLM
def load_llm():
    model_name = "microsoft/Phi-3.5-mini-instruct"
    tokenizer = AutoTokenizer.from_pretrained(model_name)

    model = AutoModelForCausalLM.from_pretrained(model_name, device_map="auto")

    hf_pipeline = pipeline("text-generation", model=model, tokenizer=tokenizer, max_length=512, max_new_tokens=100, pad_token_id=tokenizer.pad_token_id)
    llm = HuggingFacePipeline(pipeline=hf_pipeline)  # Wrap it in LangChain's HuggingFacePipeline
    return llm

# Initialize the LLM
llm_pipeline = load_llm()

# Create the Conversational Chain with memory
def create_conversational_chain(llm, vector_store):
    memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
    chain = ConversationalRetrievalChain.from_llm(
        llm=llm,
        chain_type='stuff',
        retriever=vector_store.as_retriever(search_kwargs={"k": 2}),
        memory=memory
    )
    return chain

# Create a Vector Store from uploaded PDF files
def create_vector_store(pdf_files):
    text = []

    for pdf_file in pdf_files:
        # Handle the file correctly using its path attribute
        pdf_path = pdf_file.name  # Get the path of the uploaded file

        # Load the content of the PDF
        loader = PyPDFLoader(pdf_path)
        text.extend(loader.load())

        # Optional: Remove the file if necessary
        # os.remove(pdf_path)  # Uncomment if you wish to remove the uploaded file after processing

    # Split the document into chunks
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=4000, chunk_overlap=10)
    text_chunks = text_splitter.split_documents(text)

    # Create embeddings using a pre-trained model
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2", model_kwargs={'device': 'cpu'})
    vector_store = FAISS.from_documents(text_chunks, embedding=embeddings)

    return vector_store

# Handle the upload and chat logic
vector_store = None
conversational_chain = None

def upload_pdf(pdf_files):
    global vector_store, conversational_chain
    vector_store = create_vector_store(pdf_files)
    if vector_store:
        conversational_chain = create_conversational_chain(llm_pipeline, vector_store)
        return "PDFs successfully processed. You can now ask questions!"
    else:
        return "Failed to process PDFs. Please try again."

def ask_question(question):
    if conversational_chain and vector_store:
        result = conversational_chain.invoke({"question": question, "chat_history": []})
        # print(result.keys())
        # print(result)
        return result["answer"]
    else:
        return "Please upload PDFs first."

# Creating the Gradio interface
with gr.Blocks() as demo:
    gr.Markdown("## PDF-Based Q&A Chatbot")

    with gr.Row():
        pdf_input = gr.File(label="Upload PDF Files", file_count="multiple", type="filepath")
        upload_button = gr.Button("Process PDFs")
        status_output = gr.Textbox(label="Status", interactive=False)

    with gr.Row():
        question_input = gr.Textbox(label="Ask a Question")
        ask_button = gr.Button("Ask")
        answer_output = gr.Textbox(label="Answer", interactive=True)

    # Event handlers
    upload_button.click(upload_pdf, inputs=[pdf_input], outputs=[status_output])
    ask_button.click(ask_question, inputs=[question_input], outputs=[answer_output])

# Launch the GUI in Colab
demo.launch(debug=True)

