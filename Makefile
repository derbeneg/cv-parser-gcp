.PHONY: up down

up:
	@PARSER_MODE=$(PARSER_MODE) docker compose up --build -d

down:
	@docker compose down