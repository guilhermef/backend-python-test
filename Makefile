all: setup migrate-db create-fixtures

setup:
	@pip install -r requirements.txt

migrate-db:
	@python main.py initdb

create-fixtures:
	@python main.py fixtures

run:
	@FLASK_ENV=development python main.py run
