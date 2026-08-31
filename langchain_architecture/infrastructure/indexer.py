from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
from config import Settings

def index_file(path:str, store, settings:Settings)-> None:

    with open(path, 'r', encoding="utf-8") as file:
        text = file.read()

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=settings.chunk_size,
        chunk_overlap=settings.chunk_overlap
    )

    chunks = splitter.split_text(text)
    
    documents = [Document(page_content=chunk) for chunk in chunks]

    store.add_documents(documents)
