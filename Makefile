build:
	docker-compose up --build

up:
	docker-compose up

down:
	docker-compose down

up-detach:
	docker-compose up -d

migrate:
	docker compose run --no-deps --rm api python manage.py migrate

create-admin:
	docker compose run --no-deps --rm api python manage.py createadmin

test: up-detach
	docker compose run --no-deps --rm api python manage.py test
