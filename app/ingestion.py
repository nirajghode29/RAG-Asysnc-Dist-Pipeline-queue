from dotenv import load_dotenv
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
#from langchain_community.document_loaders.parsers import LLMImageBlobParser
from langchain_openai import OpenAIEmbeddings
from langchain_qdrant import QdrantVectorStore
from pathlib import Path

load_dotenv()


pdf_path = Path(__file__).parent / "python.pdf"

loader = PyPDFLoader(
    file_path=pdf_path,
    extract_images=False,

)

docs = loader.load()

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size = 1000,
    chunk_overlap = 400
)

split_docs = text_splitter.split_documents(docs)


embedding_model = OpenAIEmbeddings(
    model = "text-embedding-3-large"
)


vector_store = QdrantVectorStore.from_documents(
    documents = split_docs,
    url = "http://localhost:6333",
    collection_name = "learning_vectors",
    embedding = embedding_model

)

print("Indexing of Documents Done........")
