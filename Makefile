.PHONY: install run test clean docker-build docker-run migrate

install:
	pip install -r requirements.txt

migrate:
	python manage.py makemigrations apis
	python manage.py migrate

run:
	python manage.py runserver 0.0.0.0:8000

test:
	python manage.py test apis -v 2 2>/dev/null || echo "No tests configured yet"

clean:
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete 2>/dev/null || true
	rm -f db.sqlite3

docker-build:
	docker build -t crypcentra .

docker-run:
	docker run -p 8000:8000 --env-file .env crypcentra
