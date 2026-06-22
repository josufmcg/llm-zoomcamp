from dotenv import load_dotenv
from gitsource import chunk_documents
from openai import OpenAI
from rag import RAG
from repository import get_documents
from search_engine import build_index, search

load_dotenv()
llm_client = OpenAI()

documents = get_documents()

# Q1 - How many lesson pages are in the dataset?
print(f"How many lesson pages are in the dataset? {len(documents)}")

# Q2 - What's the filename of the first result?
index = build_index(documents)
query = "How does the agentic loop keep calling the model until it stops?"
results = search(index, query, num_results=5)
print(f"Search results for query: '{query}'")
print(f"Filename of the first result: {results[0]['filename']}")

#print(f"Example result:\n {list(results[0].keys())}")
# Q3 - How many input (prompt) tokens did we send to the model for this request?
rag = RAG(index=index, llm_client=llm_client)
# response = rag.rag(query)
# print(f"Input tokens for this request: {response.usage.input_tokens}")

# Q4 - How many chunks do you get?
print(f"Documents before: {len(documents)}")
chunks = chunk_documents(documents, size=2000, step=1000)
print(f"How many chunks do you get? {len(chunks)}")

# Q5 - Measure rag with chunking
rag_with_chunking = RAG(index=build_index(chunks), llm_client=llm_client)
response_with_chunking = rag_with_chunking.rag(query)
print(f"Input tokens for this request with chunking: {response_with_chunking.usage.input_tokens}")

# Q6 - How many times did the agent call search?

