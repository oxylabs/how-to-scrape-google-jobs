# Makefile for running the Google Jobs scraper


.PHONY: install
install:
	pip install poetry==1.8.2
	poetry install


.PHONY: scrape
scrape:
	@if [ -z "$(QUERY)" ]; then \
		echo 'Error: A query string for which to search Google Jobs is required. Use make scrape QUERY="<query>"'; \
		exit 1; \
	else \
		poetry run python -m google_jobs_scraper --query="$(QUERY)"; \
	fi
