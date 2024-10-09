from dotenv import load_dotenv
from langchain_chroma import Chroma
from langchain_community.document_loaders import WebBaseLoader
from langchain_openai import OpenAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter

load_dotenv(dotenv_path='.env')
# List of URLs to scrape
scrape_urls = [
            'https://lilianweng.github.io/posts/2023-06-23-agent/',
            'https://lilianweng.github.io/posts/2023-03-15-prompt-engineering/',
            'https://lilianweng.github.io/posts/2023-10-25-adv-attack-llm/'
            ]

def load_documents(urls):
    docs        = [WebBaseLoader(url).load() for url in urls]
    docs_list   = [item for sublist in docs for item in sublist]
    return docs_list

def split_text(docs_list):
    text_splitter   = RecursiveCharacterTextSplitter.from_tiktoken_encoder(
        chunk_size=250, chunk_overlap=0
    )
    docs_splits = text_splitter.split_documents(docs_list)
    return docs_splits

def store_to_vectordb(split_documents):
        # Store in the locally running Chroma DB
        vectorstore = Chroma.from_documents(
            documents=split_documents,
            collection_name="rag-chroma",
            embedding=OpenAIEmbeddings(),
            persist_directory="chroma"
        )

def retrieve_documents():
    retriever = Chroma(
        collection_name="rag-chroma",
        persist_directory="../../chroma",
        embedding_function=OpenAIEmbeddings()
    ).as_retriever()

    return retriever


split_docs  = split_text(load_documents(scrape_urls))
store_to_vectordb(split_docs)
