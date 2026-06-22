from dotenv import load_dotenv
from gitsource import chunk_documents
from openai import OpenAI
from toyaikit.chat.runners import OpenAIResponsesRunner
from toyaikit.llm import OpenAIClient as ToyAIClient
from toyaikit.tools import Tools
from rag import RAG
from repository import get_documents
from search_engine import build_index, search as baseline_search

load_dotenv()
llm_client = OpenAI()

documents = get_documents()

# Q1 - How many lesson pages are in the dataset?
print(f"How many lesson pages are in the dataset? {len(documents)}")

# Q2 - What's the filename of the first result?
index = build_index(documents)
query = "How does the agentic loop keep calling the model until it stops?"
results = baseline_search(index, query, num_results=5)
print(f"Search results for query: '{query}'")
print(f"Filename of the first result: {results[0]['filename']}")

#print(f"Example result:\n {list(results[0].keys())}")
# Q3 - How many input (prompt) tokens did we send to the model for this request?
rag = RAG(index=index, llm_client=llm_client)
response = rag.rag(query)
print(f"Input tokens for this request: {response.usage.input_tokens}")

# Q4 - How many chunks do you get?
print(f"Documents before: {len(documents)}")
chunks = chunk_documents(documents, size=2000, step=1000)
print(f"How many chunks do you get? {len(chunks)}")

# Q5 - Measure rag with chunking
chunk_index = build_index(chunks)
rag_with_chunking = RAG(index=chunk_index, llm_client=llm_client)
response_with_chunking = rag_with_chunking.rag(query)
print(f"Input tokens for this request with chunking: {response_with_chunking.usage.input_tokens}")

# Q6 - How many times did the agent call search?
search_call_count = 0
def search(query: str, num_results: int = 5) -> list:
	"""Search the chunk index and return the most relevant chunks."""
	global search_call_count
	search_call_count += 1
	return baseline_search(chunk_index, query, num_results=num_results)


agent_instructions = """
You're a course teaching assistant. 
You're given a question from a course student and your task is to answer it.

If you want to look up the answer, explain why before making the call. Use as many 
keywords from the user question as possible when making first requests.

Make multiple searches. Try to expand your search by using new keywords based on the results you
get from the search.

At the end, make a clarifying question based on what you presented and ask if there are 
other areas that the user wants to explore.
""".strip()

tools = Tools()
tools.add_tool(search)

agent_runner = OpenAIResponsesRunner(
	llm_client=ToyAIClient(model="gpt-5.4-mini"),
	tools=tools,
	developer_prompt=agent_instructions,
)

agent_result = agent_runner.loop(prompt=query)

print(f"Agent answer: {agent_result.last_message}")
print(f"How many times did the agent call search? {search_call_count}")

