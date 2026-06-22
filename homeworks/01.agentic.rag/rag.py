from rag_helper import RAGBase

class RAG(RAGBase):
    
    def search(self, query, num_results=5):
        boost_dict = {'content': 1.0}

        return self.index.search(
            query,
            num_results=num_results,
            boost_dict=boost_dict,
        )

    def build_context(self, search_results):
        lines = []

        for doc in search_results:
            lines.append('File: ' + doc['filename'])
            lines.append('Content: ' + doc['content'])
            lines.append('')

        return '\n'.join(lines).strip()

    def llm(self, prompt):
        input_messages = [
            {'role': 'developer', 'content': self.instructions},
            {'role': 'user', 'content': prompt}
        ]

        response = self.llm_client.responses.create(
            model=self.model,
            input=input_messages
        )

        return response