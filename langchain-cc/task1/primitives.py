import json
import os
from langchain_openrouter import ChatOpenRouter
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.embeddings import DeterministicFakeEmbedding
from langchain_core.vectorstores import InMemoryVectorStore
from dotenv import load_dotenv

load_dotenv()


# chat Model
model = ChatOpenRouter(
    model="openai/gpt-oss-20b:free",
    temperature=0,
    api_key=os.environ["OPENROUTER_API_KEY"],
    base_url="https://openrouter.ai/api/v1"
)

# prompt
prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a precise assistant."),
    ("human", "{question}")
])

# parser
parser = StrOutputParser()

embeddings = DeterministicFakeEmbedding(size=128)

vector_store = InMemoryVectorStore.from_texts(
    [
        "LangChain is a framework for building LLM applications.",
        "LCEL stands for LangChain Expression Language.",
        "A retriever finds relevant documents.",
    ],
    embedding=embeddings,
)

# retriever

retriever = vector_store.as_retriever()

print("MODEL INPUT:", model.get_input_schema().model_json_schema())
print("MODEL OUTPUT:", model.get_output_schema().model_json_schema())

print("PROMPT INPUT:", prompt.get_input_schema().model_json_schema())
print("PROMPT OUTPUT:", prompt.get_output_schema().model_json_schema())

print("PARSER INPUT:", parser.get_input_schema().model_json_schema())
print("PARSER OUTPUT:", parser.get_output_schema().model_json_schema())

print("RETRIEVER INPUT:", retriever.get_input_schema().model_json_schema())
print("RETRIEVER OUTPUT:", retriever.get_output_schema().model_json_schema())