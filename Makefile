# Makefile

# OS specific commands and variables
ifeq ($(OS),Windows_NT)
    SET_ENV = set
else
    SET_ENV = export
endif


format:
	black main.py
	black mlbot/ routers/


docker-build:
	docker build -t mlbot-sandbox .
