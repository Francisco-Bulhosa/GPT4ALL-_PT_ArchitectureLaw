

# pip install langchain==0.0.173
# pip install chromadb==0.3.23
# pip install pypdf==3.8.1
# pip install pygpt4all==1.1.0
# pip install pdf2image==1.16.3


from langchain.chains import RetrievalQA
from langchain.document_loaders import PyPDFLoader
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.llms import GPT4All
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import Chroma
from pdf2image import convert_from_path
import streamlit as st 

#Path to wheights (file path to model)
LLM_path = 'C:/Users/franc/Documents/Data_Science/LLM/LLM_Models/ggml-model-gpt4all-falcon-q4_0'

# Instance of the LLM
llm = GPT4All(model = LLM_path, verbose=True)


loader = PyPDFLoader("rgeu.pdf")

documents = loader.load_and_split()

# Document lenght after split
# len(documents)

# first page contents
print(documents[0].page_content)

# split text into chunks
text_splitter = RecursiveCharacterTextSplitter(chunk_size=1024, chunk_overlap=64)
texts = text_splitter.split_documents(documents)

# Use to see lenght of the chunks texts:
# len(texts)

# Create embeddings
embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

# Store embeddings on chroma
db = Chroma.from_documents(texts, embeddings, persist_directory="db")


qa = RetrievalQA.from_chain_type(
    llm=llm,
    chain_type="stuff",
    retriever=db.as_retriever(search_kwargs={"k": 3}),
    return_source_documents=True,
    verbose=False,
)


st.title('🏠 Enquadramento Legal')

prompt = st.text_input('Enter your prompt here!')

if prompt: 
    response = qa(prompt.strip())
    print(response["result"])
    st.write(response["result"])

    # With a streamlit expander  
    with st.expander('Document Similarity Search'):
        # Find the relevant pages
        docs_and_scores = db.similarity_search_with_score(prompt)
        # Write out the first 
        st.write(docs_and_scores[0][0].page_content) 