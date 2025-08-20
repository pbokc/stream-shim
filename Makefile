run:
	uvicorn app:app \
		--host $$(python -c "import config; print(config.BIND_HOST)") \
		--port $$(python -c "import config; print(config.BIND_PORT)") \
		--reload
