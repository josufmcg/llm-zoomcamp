from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import ConsoleSpanExporter, SimpleSpanProcessor

from rag_helper import RAGBase

import sqlite3
from opentelemetry.sdk.trace.export import SpanExporter, SpanExportResult

# Q4
class SQLiteSpanExporter(SpanExporter):

    def __init__(self, db_path="traces.db"):
        self.conn = sqlite3.connect(db_path)
        self.conn.execute("""
            CREATE TABLE IF NOT EXISTS spans (
                name TEXT,
                start_time INTEGER,
                end_time INTEGER,
                input_tokens INTEGER,
                output_tokens INTEGER,
                cost REAL
            )
        """)
        self.conn.commit()

    def export(self, spans):
        for span in spans:
            attrs = dict(span.attributes or {})
            self.conn.execute(
                "INSERT INTO spans VALUES (?, ?, ?, ?, ?, ?)",
                (
                    span.name,
                    span.start_time,
                    span.end_time,
                    attrs.get("input_tokens"),
                    attrs.get("output_tokens"),
                    attrs.get("cost"),
                ),
            )
        self.conn.commit()
        return SpanExportResult.SUCCESS

    def shutdown(self):
        self.conn.close()

    def force_flush(self):
        return True

provider = TracerProvider()
provider.add_span_processor(
    # SimpleSpanProcessor(ConsoleSpanExporter())
    SimpleSpanProcessor(SQLiteSpanExporter("traces.db"))
)
trace.set_tracer_provider(provider)

tracer = trace.get_tracer("llm-zoomcamp")

# Q1: Implement a RAG class that traces the search and llm calls
class RAGTraced(RAGBase):
    def search(self, query, num_results=5):
        with tracer.start_as_current_span("rag.search") as span:
            span.set_attribute("query", query)
            span.set_attribute("num_results", num_results)
            return super().search(query, num_results=num_results)

    def llm(self, prompt):
        with tracer.start_as_current_span("rag.llm") as span:
            span.set_attribute("prompt_length", len(prompt))
            response = super().llm(prompt)
            usage = response.usage
            # Q2: Add telemetry attributes for input_tokens and output_tokens
            span.set_attribute("input_tokens", usage.input_tokens)
            span.set_attribute("output_tokens", usage.output_tokens)
            return response

    def rag(self, query):
        with tracer.start_as_current_span("rag.rag") as span:
            span.set_attribute("query", query)
            search_results = self.search(query)
            prompt = self.build_prompt(query, search_results)
            response = self.llm(prompt)
            return response.output_text


if __name__ == "__main__":
    with tracer.start_as_current_span("my_operation") as span:
        span.set_attribute("my_key", "my_value")
    