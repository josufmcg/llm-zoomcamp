KESTRA_SERVER=http://linuxsrv:8080

.PHONY: env-encode
env-encode:
	while IFS='=' read -r key value; do \
		echo "SECRET_$$key=$$(echo -n "$$value" | base64)"; \
	done < .env > .env_encoded
	echo SECRET_GCP_SERVICE_ACCOUNT=$$(cat ./keys/credentials.json | base64 -w 0) >> .env_encoded

.PHONY: import-flows
import-flows:
	curl -X POST -u 'admin@kestra.io:Admin1234!' $(KESTRA_SERVER)/api/v1/flows/import -F fileUpload=@flows/1_chat_without_rag.yaml
	curl -X POST -u 'admin@kestra.io:Admin1234!' $(KESTRA_SERVER)/api/v1/flows/import -F fileUpload=@flows/2_chat_with_rag.yaml
	curl -X POST -u 'admin@kestra.io:Admin1234!' $(KESTRA_SERVER)/api/v1/flows/import -F fileUpload=@flows/3_rag_with_websearch.yaml
	curl -X POST -u 'admin@kestra.io:Admin1234!' $(KESTRA_SERVER)/api/v1/flows/import -F fileUpload=@flows/4_simple_agent.yaml
	curl -X POST -u 'admin@kestra.io:Admin1234!' $(KESTRA_SERVER)/api/v1/flows/import -F fileUpload=@flows/5_web_research_agent.yaml
	curl -X POST -u 'admin@kestra.io:Admin1234!' $(KESTRA_SERVER)/api/v1/flows/import -F fileUpload=@flows/6_multi_agent_research.yaml