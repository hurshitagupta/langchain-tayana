from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter

def index_file(path:str, store)-> None:

    with open(path, 'r', encoding="utf-8") as file:
        text = file.read()

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=300,
        chunk_overlap=50
    )

    chunks = splitter.split_text(text)
    
    documents = [Document(page_content=chunk) for chunk in chunks]

    store.add_documents(documents)
