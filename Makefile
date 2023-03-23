all: makemigrations migrate run

run:
	python src/manage.py runserver

bot:
	python src/manage.py bot

build:
	docker build -t frogfrog243/bot-app:1 .

up:
	docker compose down
	docker compose up -d

test:
	echo "test"

migrate:
	python src/manage.py migrate $(if $m, api $m,)

makemigrations:
	python src/manage.py makemigrations
	sudo chown -R ${USER} src/app/migrations/

createsuperuser:
	python src/manage.py createsuperuser

collectstatic:
	python src/manage.py collectstatic --no-input

dev:
	python src/manage.py runserver localhost:8000

command:
	python src/manage.py ${c}

shell:
	python src/manage.py shell

debug:
	python src/manage.py debug

piplock:
	pipenv install
	sudo chown -R ${USER} Pipfile.lock

lint:
	isort .
	flake8 --config setup.cfg

check_lint:
	isort --check --diff .
	flake8 --config setup.cfg
