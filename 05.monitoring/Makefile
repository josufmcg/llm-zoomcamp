PREFIX=https://raw.githubusercontent.com/DataTalksClub/llm-zoomcamp/main

.PHONY: download-dependencies
download-dependencies:
	wget -O ingest.py ${PREFIX}/01-agentic-rag/code/ingest.py && \
		wget -O rag_helper.py ${PREFIX}/01-agentic-rag/code/rag_helper.py && \
		wget -O evaluation_utils.py ${PREFIX}/04-evaluation/code/evaluation_utils.py

.PHONY: network
network:
	docker network create monitoring

.PHONY: postgres
postgres:
	docker run -it \
		--name course-assistant-pg \
		--network monitoring \
		-e POSTGRES_USER=user \
		-e POSTGRES_PASSWORD=password \
		-e POSTGRES_DB=course_assistant \
		-p 5432:5432 \
		-v pgdata:/var/lib/postgresql/data \
		postgres:17

.PHONY: grafana
grafana:
	docker run \
		--name grafana \
		--network monitoring \
		-p 3000:3000 \
		-v grafana_data:/var/lib/grafana \
		grafana/grafana

.PHONY: init-db
init-db:
	uv run python db_init.py

.PHONY: generate-data
generate-data:
	uv run python generate_data.py

.PHONY: run
run:
	uv run python assistant.py

.PHONY: dashboard
dashboard:
	uv run streamlit run dashboard.py --server.port 8502

.PHONY: chat
chat:
	uv run streamlit run app.py
