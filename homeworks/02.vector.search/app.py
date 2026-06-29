import json
import numpy as np

from pathlib import Path
from embedder import Embedder
from gitsource import GithubRepositoryDataReader

from minsearch import VectorSearch, Index
from sqlitesearch import TextSearchIndex


# Q1. Embedding a query
embedder = Embedder()
v = embedder.encode("How does approximate nearest neighbor search work?")
print(f"Q1 - The first value is: {v[0]}")

# Loading the data from github
# reader = GithubRepositoryDataReader(
#     repo_owner="DataTalksClub",
#     repo_name="llm-zoomcamp",
#     commit_id="8c1834d",
#     allowed_extensions={"md"},
#     filename_filter=lambda path: "/lessons/" in path,
# )

documents_path = Path("documents.json")

# Writer
# documents = [file.parse() for file in reader.read()]
# documents_path.write_text(json.dumps(documents, indent=2))

# Reader
documents = json.loads(documents_path.read_text())


# Q2. Cosine similarity
document = next(filter(lambda doc: "02-vector-search/lessons/07-sqlitesearch-vector.md" in doc["filename"].lower(), documents))
v_doc = embedder.encode(document["content"])
print(f"Q2 - Cosine similarity: {v.dot(v_doc)}")

# Q3 Chunking and search by hand
from gitsource import chunk_documents
chunks = chunk_documents(documents, size=2000, step=1000)
encoded_chunks = [embedder.encode(chunk["content"]) for chunk in chunks]
X = np.array(encoded_chunks)


scores = X.dot(v)
idx = np.argmax(scores)

print(f"Q3 - Best matching chunk: {chunks[idx]['filename']}")

# Q4. Vector search with minsearch
vindex = VectorSearch(keyword_fields=['course'])
vindex.fit(
    vectors = X,
    payload = chunks
)
q4_vector = embedder.encode("What metric do we use to evaluate a search engine?")
results = vindex.search(q4_vector, num_results=5)
print(f"Q4 - Best matching chunk: {results[0]['filename']}")

# Q5. Text search vs vector search
q5_query = "How do I store vectors in PostgreSQL?"
tindex = Index(
    text_fields=['content'],
    keyword_fields=['filename']
)
tindex.fit(documents)
text_results = tindex.search(q5_query, num_results=5)
print(f"Q5 - Text search results: \n {[doc['filename'] for doc in text_results]}")

q5_vector = embedder.encode(q5_query)
vector_results = vindex.search(q5_vector, num_results=50)
unique_results = set()
for doc in vector_results:
    if doc['filename'] not in unique_results:
        unique_results.add(doc['filename'])
    if len(unique_results) >= 5:
        break
vector_results = list(unique_results)

print(f"Q5 - Vector search results: \n {[doc for doc in vector_results]}")
print(f"Q5 - Search differences: {list(set([doc for doc in vector_results]) - set([doc['filename'] for doc in text_results]))}")

# Q6. Hybrid search
q6_query = "How do I give the model access to tools?"
tindex = Index(
    text_fields=['content'],
    keyword_fields=['filename']
)
tindex.fit(documents)
text_results = tindex.search(q6_query, num_results=5)
print(f"Q6 - Text search results: \n {[doc['filename'] for doc in text_results]}")

q6_vector = embedder.encode(q6_query)
vector_search_results = vindex.search(q6_vector, num_results=50)
unique_results = set()
vector_results = []
for doc in vector_search_results:
    if doc['filename'] not in unique_results:
        unique_results.add(doc['filename'])
        vector_results.append(doc)
    if len(unique_results) >= 5:
        break

def rrf(result_lists, k=60, num_results=5):
    scores = {}
    docs = {}

    for results in result_lists:
        for rank, doc in enumerate(results):
            key = (doc["filename"],)
            scores[key] = scores.get(key, 0) + 1 / (k + rank)
            docs[key] = doc

    ranked = sorted(scores, key=scores.get, reverse=True)
    return [docs[key] for key in ranked[:num_results]]

results = rrf([vector_results, text_results])
print(f"Q6 - Hybrid search results: \n {[doc['filename'] for doc in results]}")
