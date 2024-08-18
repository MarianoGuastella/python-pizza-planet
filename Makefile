win-create:
	python -m venv venv && \
	call venv\\Scripts\\activate && \
	pip install -r requirements.txt

linux-create:
	python -m venv venv && \
	source venv/bin/activate && \
	pip install -r requirements.txt

win-source:
	source venv/Scripts/activate && \
	set FLASK_ENV=development

linux-source:
	source venv/bin/activate && \
	export FLASK_ENV=development 

db:
	python manage.py db init && \
	python manage.py db migrate && \
	python manage.py db upgrade

run:
	python manage.py run

test:
	python manage.py test

create-seed:
	python app/common/scripts/faker_seed.py

clean-seed:
	python app/common/scripts/clean_seed.py

format:
	black .

lint:
	ruff check .