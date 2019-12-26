all: setup migrate-db

setup:
	@pip install -r requirements.txt

migrate-db:
	@python main.py initdb

run:
	@python main.py
