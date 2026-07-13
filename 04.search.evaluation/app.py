from ingest import load_faq_data

documents = load_faq_data()

documents_llm = []

for doc in documents:
    if doc["course"] == "llm-zoomcamp":
        documents_llm.append(doc)

len(documents_llm)
documents = documents_llm
doc = documents[0]
print(doc["id"])
print(doc["question"])
print(doc["answer"])


from pydantic import BaseModel

class Questions(BaseModel):
    questions: list[str]

data_gen_instructions = """
You emulate a student who's taking our course.
Formulate 5 questions this student might ask based on a FAQ record. The record
should contain the answer to the questions, and the questions should be complete and not too short.
If possible, use as fewer words as possible from the record.

The output should resemble how people ask questions
on the internet. Not too formal, not too short, not too long.
""".strip()

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
openai_client = OpenAI()

import json

user_prompt = json.dumps(doc)

messages = [
    {"role": "developer", "content": data_gen_instructions},
    {"role": "user", "content": user_prompt}
]

response = openai_client.responses.parse(
    model="gpt-5.4-mini",
    input=messages,
    text_format=Questions
)

result = response.output_parsed

print(result)