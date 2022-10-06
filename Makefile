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

init-data:
	docker compose run --no-deps --rm api python manage.py loaddata core/fixtures/users.json core/fixtures/quizzes.json core/fixtures/questions.json core/fixtures/answers.json

test: up-detach
	docker compose run --no-deps --rm api python manage.py test
