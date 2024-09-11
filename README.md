# PDF-Based-Conversational-QA-with-LangChain-and-Gradio

## Overview

This project implements a PDF-based question-answering chatbot using modern Natural Language Processing (NLP) and Machine Learning techniques. The chatbot allows users to upload PDF files, processes the contents, and enables users to ask questions about the content of those PDFs.

## Features

- **Upload PDF Files**: Allows multiple PDF files to be uploaded.
- **Process PDFs**: Converts the PDF content into chunks and creates an embedding vector store for efficient retrieval.
- **Ask Questions**: Users can ask questions related to the content of the uploaded PDFs and receive answers based on the processed information.

## Technologies Used

- **Transformers**: For handling language models and pipelines.
- **LangChain**: For building conversational chains and managing memory.
- **Gradio**: For creating the user interface.
- **FAISS**: For efficient similarity search.
- **Sentence Transformers**: For generating document embeddings.
- **PyPDF**: For reading PDF files.

## Setup and Installation

1. **Install Dependencies:**

    Make sure you have Python 3.7+ installed, then run:

    ```bash
    pip install transformers langchain langchain_community gradio torch sentence-transformers faiss-cpu pypdf
    ```

2. **Authentication:**

    To use Hugging Face models, you need to authenticate. Replace `'YOUR_HF_KEY'` with your Hugging Face API key to run on google colab.

    ```python
    from huggingface_hub import login
    from google.colab import userdata

    login(token=userdata.get('HF_KEY'))
    ```

3. **Run the Notebook:**

    You can run the notebook in Google Colab or locally. If running locally, make sure to adapt the file paths and authentication steps as needed.

## Usage

1. **Upload PDF Files:**

    Use the upload button in the Gradio interface to upload one or more PDF files.

2. **Process PDFs:**

    After uploading, click "Process PDFs" to process the content. The system will prepare the data for question answering.

3. **Ask Questions:**

    Enter your question in the "Ask a Question" textbox and click "Ask" to get responses based on the content of the uploaded PDFs.

## Code

The main code is implemented in the `PDF Based QA Chatbot.ipynb` notebook. It includes:

- Loading and setting up the LLM (Language Model)
- Creating a vector store from PDF documents
- Setting up a conversational retrieval chain
- Implementing the Gradio interface for user interaction
