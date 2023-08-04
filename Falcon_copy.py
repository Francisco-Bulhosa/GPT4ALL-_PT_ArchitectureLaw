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
import pandas as pd
from transformers import AutoTokenizer


#Path to wheights (file path to model)
LLM_path = 'C:/Users/franc/Documents/Data_Science/LLM/LLM_Models/ggml-model-gpt4all-falcon-q4_0'

# Instance of the LLM
llm = GPT4All(model = LLM_path, verbose=True)

# Pre process the Data from the csv's




# Read the CSV file
file_path = 'C:/Users/franc/Documents/GitHub/LangchainDocuments/pdf_extractions/rgeu.csv'
df = pd.read_csv(file_path)



tokenizer = AutoTokenizer.from_pretrained("bert-base-uncased")


# Tokenize the "text" column of your dataframe
tokenized_df = tokenizer.batch_encode_plus(
    text_list,
    padding="max_length",
    truncation=True,
    max_length=4096,
    return_tensors="pt",
)

# Initialize the HuggingFaceEmbeddings model
model_name = "sentence-transformers/all-MiniLM-L6-v2"
model_kwargs = {'device': 'cpu'}
encode_kwargs = {'normalize_embeddings': False}
hf = HuggingFaceEmbeddings(
    model_name=model_name,
    model_kwargs=model_kwargs,
    encode_kwargs=encode_kwargs
)

# Extract the "Text" column of your DataFrame to a list
text_list = df["Text"].tolist()

# Compute the embeddings for the texts using the embed_documents method
embeddings = hf.embed_documents(texts=text_list)



# Extract the "Text" column (old method)
### texts = df['Text'].tolist()



# Create embeddings
### embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

# Store embeddings on chroma
db = Chroma.from_texts(
    texts=text_list, 
    embeddings, 
    persist_directory="db2")


qa = RetrievalQA.from_chain_type(
    llm=llm,
    chain_type="stuff",
    retriever=db.as_retriever(search_kwargs={"k": 3}),
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