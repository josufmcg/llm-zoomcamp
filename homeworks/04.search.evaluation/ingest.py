import requests
from minsearch import Index


def load_faq_data():
    docs_url = 'https://datatalks.club/faq/json/courses.json'
    response = requests.get(docs_url)
    courses_raw = response.json()

    documents = []
    url_prefix = 'https://datatalks.club/faq'

    for course in courses_raw:
        course_url = f'{url_prefix}{course["path"]}'
        course_response = requests.get(course_url)
        course_response.raise_for_status()
        course_data = course_response.json()

        documents.extend(course_data)

    return documents


def build_index(documents):
    if not documents:
        return Index(text_fields=['content'], keyword_fields=['filename'])

    sample_doc = documents[0]
    text_fields = []
    keyword_fields = []

    for field in ['content', 'question', 'section', 'answer']:
        if field in sample_doc:
            text_fields.append(field)

    for field in ['filename', 'course']:
        if field in sample_doc:
            keyword_fields.append(field)

    if not text_fields:
        text_fields = [field for field in sample_doc if isinstance(sample_doc[field], str)]

    if not keyword_fields:
        keyword_fields = [
            field for field in sample_doc
            if isinstance(sample_doc[field], str) and field not in text_fields
        ]

    index = Index(
        text_fields=text_fields,
        keyword_fields=keyword_fields,
    )
    index.fit(documents)
    return index
