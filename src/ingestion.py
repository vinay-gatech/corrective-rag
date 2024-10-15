from dotenv import load_dotenv
from langchain_chroma import Chroma
from langchain_community.document_loaders import WebBaseLoader
from langchain_openai import OpenAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from openai import embeddings

# set as true if documents are not yet stored else false
STORE_DOCUMENTS = False

load_dotenv()

urls    = ['https://lilianweng.github.io/posts/2023-06-23-agent/',
           'https://lilianweng.github.io/posts/2023-03-15-prompt-engineering/',
            'https://lilianweng.github.io/posts/2023-10-25-adv-attack-llm/'
           ]

# Load content from webpages
docs    = [WebBaseLoader(url).load() for url in urls]
docs_list   = [item for sublist in docs for item in sublist]

text_splitter   = RecursiveCharacterTextSplitter.from_tiktoken_encoder(
    chunk_size=250, chunk_overlap=0
)

doc_splits  = text_splitter.split_documents(docs_list)
print(doc_splits)

# Store chunks as embeddings to Chroma (in local directory)
# Chroma.sqlite3
def store_documents_in_chroma():
    vectorstore = Chroma.from_documents(
        documents=doc_splits,
        collection_name="rag-chroma",
        embedding=OpenAIEmbeddings(),
        persist_directory="chroma"
    )


# Retrieve documents from Chroma
retriever   = Chroma(
    collection_name="rag-chroma",
    persist_directory="chroma",
    embedding_function=OpenAIEmbeddings()
).as_retriever()

if __name__ == '__main__':
    if STORE_DOCUMENTS:
        store_documents_in_chroma()
    print("--Done--")

