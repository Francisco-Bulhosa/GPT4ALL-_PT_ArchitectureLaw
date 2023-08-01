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

#Path to wheights (file path to model)
LLM_path = 'C:/Users/franc/Documents/Data_Science/LLM/LLM_Models/ggml-model-gpt4all-falcon-q4_0'

# Instance of the LLM
llm = GPT4All(model = LLM_path, verbose=True)

# Pre process the Data from the csv's









tokenizer = Tokenizer(num_words=100000) # You can adjust the number of words based on your data

# Tokenize the "text" column of your dataframe
tokenized_df = tokenizer.batch_encode_plus(
df["text"],
padding="max_length",
truncation=True,
max_length=512,
return_tensors="pt")

# Create the tokenized dataframe
tokenized_df = pd.DataFrame(tokenized_df.tolist())

# Use the tokenized dataframe to create the embeddings
embeddings = HuggingFaceEmbeddings.from_tensor(tokenized_df["input_ids"])
embeddings = embeddings.to(device)







# Read the CSV file
file_path = 'C:/Users/franc/Documents/GitHub/LangchainDocuments/pdf_extractions/rgeu.csv'
df = pd.read_csv(file_path)

# Extract the "Text" column (old method)
### texts = df['Text'].tolist()



# Define a custom encoding scheme that maps the "Article" column to a number
encoding_scheme = HfEncodingScheme(
   input_ids=["Article"],
   output_ids=["Text"],
   num_output_ids=1,
   padding="max_length",
   truncation=True,
   max_length=100,
   return_tensors="pt"
)

# Encode the data using the custom encoding scheme
encoded_data = encoding_scheme.encode_plus(df, return_tensors="pt")

# Create a HuggingFaceEmbeddings model with the encoded data
model = HfEmbeddings(encoded_data)

# Get the embeddings for the "Article" column
embeddings = model.get_embeddings("Article")









# Create embeddings
embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

# Store embeddings on chroma
db = Chroma.from_texts(texts, embeddings, persist_directory="db2")


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