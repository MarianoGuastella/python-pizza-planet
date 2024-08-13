create:
	python -m venv venv && \
	source venv/Scripts/activate && \
	pip3 install -r requirements.txt

db:
	python manage.py db init && \
	python manage.py db migrate && \
	python manage.py db upgrade

run:
	python manage.py run

test:
	python manage.py test