from minsearch import Index

def build_index(documents):
    index = Index(
        text_fields=['content'],
        keyword_fields=['filename']
    )
    index.fit(documents)
    return index

def search(index, query, num_results=5):
    boost_dict = {'content': 1.0}

    return index.search(
        query,
        num_results=num_results,
        boost_dict=boost_dict,
    )